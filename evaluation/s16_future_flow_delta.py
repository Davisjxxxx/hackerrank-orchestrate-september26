"""Produce S16 future-flow arithmetic and collision evidence.

This is evaluation tooling only.  It compares the current deterministic
implementation with the participant-facing solved rows; no expected value is
used by production code.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


def output_for(planner: main.Planner, canonical: main.Canonicalizer, request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> tuple[dict[str, str], list[main.CanonicalEvent]]:
    decision, events = planner.decide(request, profile)
    decision.explanation = main.make_explanation(decision, events)
    return main.serialize(decision), list(events)


def flow_rows(canonical: main.Canonicalizer, profile: main.Profile, request: main.Request, events: list[main.CanonicalEvent], policy: main.WindowPolicy) -> list[dict[str, object]]:
    end = request.request_date + timedelta(days=policy.upper_bound_offset())
    rows: list[dict[str, object]] = []
    for event in events:
        day = event.settlement_date or event.event_date
        if not request.request_date <= day <= end:
            continue
        amount = canonical.converted(event, profile)
        if amount is None:
            continue
        signed = amount if event.direction == "credit" else -amount
        rows.append({
            "date": day.isoformat(),
            "event_id": event.event_id,
            "source_event_id": event.source_event_id,
            "event_type": event.event_type,
            "category": event.category,
            "description": event.description,
            "direction": event.direction,
            "amount": str(event.amount) if event.amount is not None else None,
            "converted_amount": str(amount),
            "signed_flow": str(signed),
            "currency": event.currency,
            "status": event.status,
            "projected": event.projected,
            "provenance": event.provenance,
        })
    return sorted(rows, key=lambda row: (row["date"], row["event_id"]))


def minimum_balance(profile: main.Profile, request: main.Request, flows: list[dict[str, object]], policy: main.WindowPolicy) -> dict[str, object]:
    by_day: dict[str, Decimal] = defaultdict(Decimal)
    for row in flows:
        by_day[str(row["date"])] += Decimal(str(row["signed_flow"]))
    balance = profile.current_available_balance
    path: list[dict[str, str]] = []
    for offset in range(policy.upper_bound_offset() + 1):
        day = request.request_date + timedelta(days=offset)
        balance += by_day.get(day.isoformat(), Decimal(0))
        path.append({"date": day.isoformat(), "balance": str(balance), "flow": str(by_day.get(day.isoformat(), Decimal(0)))})
    limiting = min(path, key=lambda row: (Decimal(row["balance"]), row["date"]))
    return {"date": limiting["date"], "balance": limiting["balance"], "flow": limiting["flow"], "path": path}


def candidate_explanations(delta: Decimal, flows: list[dict[str, object]]) -> list[dict[str, object]]:
    target = abs(delta)
    candidates: list[tuple[Decimal, list[dict[str, object]]]] = []
    for row in flows:
        candidates.append((abs(abs(Decimal(str(row["converted_amount"]))) - target), [row]))
    for left, right in combinations(flows, 2):
        candidates.append((abs(abs(Decimal(str(left["converted_amount"]))) + abs(Decimal(str(right["converted_amount"]))) - target), [left, right]))
    candidates.sort(key=lambda item: (item[0], [(x["date"], x["event_id"]) for x in item[1]]))
    return [{"absolute_error": str(error), "flows": [{"date": x["date"], "event_id": x["event_id"], "amount": x["converted_amount"], "category": x["category"], "provenance": x["provenance"]} for x in rows]} for error, rows in candidates[:5]]


def collision_rows(request: main.Request, events: list[main.CanonicalEvent]) -> list[dict[str, object]]:
    explicit = [event for event in events if not event.projected]
    projected = [event for event in events if event.projected]
    rows: list[dict[str, object]] = []
    for left in explicit:
        left_day = left.settlement_date or left.event_date
        for right in projected:
            right_day = right.settlement_date or right.event_date
            if (left.event_type, left.category, left.direction, left.currency, left.flexibility, left_day) != (right.event_type, right.category, right.direction, right.currency, right.flexibility, right_day):
                continue
            rows.append({
                "explicit_event_id": left.event_id,
                "explicit_date": left_day.isoformat(),
                "explicit_amount": str(left.amount) if left.amount is not None else None,
                "explicit_description": left.description,
                "projected_event_id": right.event_id,
                "projected_date": right_day.isoformat(),
                "projected_amount": str(right.amount) if right.amount is not None else None,
                "projected_description": right.description,
                "projected_provenance": right.provenance,
                "both_counted": True,
                "economic_family": f"{left.event_type}/{left.category}/{left.direction}/{left.currency}/{left.flexibility}",
            })
    return sorted(rows, key=lambda row: (row["explicit_date"], row["explicit_event_id"], row["projected_event_id"]))


def main_run() -> dict[str, object]:
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    raw = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    canonical = main.Canonicalizer(raw, main.read_csv("messages.csv"), main.ExchangeRateAdapter())
    planner = main.Planner(canonical, options, policy)
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    records: list[dict[str, object]] = []
    collisions: list[dict[str, object]] = []
    for request in requests:
        actual, events = output_for(planner, canonical, request, profiles[request.user_id], policy)
        fields = [field for field in main.OUTPUT_COLUMNS[1:] if actual[field] != expected[request.request_id][field]]
        if not fields:
            continue
        flows = flow_rows(canonical, profiles[request.user_id], request, events, policy)
        minimum = minimum_balance(profiles[request.user_id], request, flows, policy)
        expected_safe = Decimal(expected[request.request_id]["amount_safe_to_pay"])
        actual_safe = Decimal(actual["amount_safe_to_pay"])
        record = {
            "request_id": request.request_id,
            "user_id": request.user_id,
            "request_date": request.request_date.isoformat(),
            "expected": expected[request.request_id],
            "actual": actual,
            "differing_fields": fields,
            "safe_amount_delta_actual_minus_expected": str(actual_safe - expected_safe),
            "current_minimum_balance": minimum,
            "expected_implied_limiting_balance": str(expected_safe + profiles[request.user_id].minimum_balance_to_keep),
            "flows_through_current_limiting_date": [row for row in flows if row["date"] <= minimum["date"]],
            "all_future_flows": flows,
            "ranked_arithmetic_explanations": candidate_explanations(actual_safe - expected_safe, flows),
        }
        records.append(record)
        collisions.extend({"request_id": request.request_id, **row} for row in collision_rows(request, events))
    return {"policy": policy.value, "non_exact_records": records, "collisions": collisions, "counts": {"non_exact_requests": len(records), "differing_fields": sum(len(row["differing_fields"]) for row in records)}}


def write_reports(report: dict[str, object]) -> None:
    evaluation = ROOT / "evaluation"
    (evaluation / "s16_future_flow_delta.json").write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    lines = ["# S16 future-flow delta and collision audit", "", "This is a read-only diagnostic of the current production path. Expected solved-row values are used only for arithmetic attribution, never by production code.", "", f"- Non-exact requests: `{report['counts']['non_exact_requests']}/25`", f"- Differing fields: `{report['counts']['differing_fields']}`", ""]
    for record in report["non_exact_records"]:
        lines += [f"## `{record['request_id']}` / `{record['user_id']}`", "", f"- Safe amount: expected `{record['expected']['amount_safe_to_pay']}`, actual `{record['actual']['amount_safe_to_pay']}`, actual-minus-expected `{record['safe_amount_delta_actual_minus_expected']}`.", f"- Earliest full payment: expected `{record['expected']['earliest_date_for_full_payment'] or 'none'}`, actual `{record['actual']['earliest_date_for_full_payment'] or 'none'}`.", f"- Current limiting balance: `{record['current_minimum_balance']['balance']}` on `{record['current_minimum_balance']['date']}` with flow `{record['current_minimum_balance']['flow']}`.", f"- Expected implied limiting balance at the same minimum reserve: `{record['expected_implied_limiting_balance']}`.", "- Ranked one/two-flow arithmetic candidates:"]
        for candidate in record["ranked_arithmetic_explanations"][:3]:
            desc = ", ".join(f"{flow['event_id']} ({flow['amount']} {flow['category']})" for flow in candidate["flows"])
            lines.append(f"  - error `{candidate['absolute_error']}`: {desc}")
        lines += ["- Cash flows through the current limiting date:", "", "| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |", "|---|---:|---|---|---|---|"]
        for flow in record["flows_through_current_limiting_date"]:
            lines.append(f"| {flow['date']} | {flow['signed_flow']} | `{flow['event_id']}` | {flow['category']} / {flow['description']} | {'projected' if flow['projected'] else 'explicit'} | `{flow['provenance']}` |")
        lines.append("")
    lines += ["## Explicit-future versus projected collisions", "", "These rows share user, direction, event type, category, currency, flexibility, and settlement date. Description differences do not prevent the audit.", "", "| Request | Explicit | Date | Explicit amount/description | Projected | Projected amount/description | Both counted |", "|---|---|---|---|---|---|---|"]
    for row in report["collisions"]:
        lines.append(f"| {row['request_id']} | `{row['explicit_event_id']}` | {row['explicit_date']} | {row['explicit_amount']} / {row['explicit_description']} | `{row['projected_event_id']}` | {row['projected_amount']} / {row['projected_description']} | {row['both_counted']} |")
    (evaluation / "s16_future_flow_delta.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_reports(main_run())
