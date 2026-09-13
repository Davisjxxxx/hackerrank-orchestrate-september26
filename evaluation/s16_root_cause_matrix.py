#!/usr/bin/env python3
"""Emit request-level S16 cash-flow attribution for the current production path."""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


def stream_groups(events: list[main.CanonicalEvent]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str], list[main.CanonicalEvent]] = defaultdict(list)
    for event in events:
        grouped[(event.event_type, event.category, event.flexibility, event.description)].append(event)
    result = []
    for key, members in sorted(grouped.items()):
        kind, step = main.cadence(members)
        if kind == "none":
            continue
        ordered = sorted(members, key=lambda event: event.event_date)
        result.append({
            "stream_id": "|".join(key),
            "event_type": key[0],
            "category": key[1],
            "flexibility": key[2],
            "description": key[3],
            "member_event_ids": [event.event_id for event in ordered],
            "member_dates": [event.event_date.isoformat() for event in ordered],
            "recurrence_type": kind,
            "cadence_days": step,
            "projected_amount": main.short_decimal(max(event.amount for event in ordered[-3:] if event.amount is not None)),
        })
    return result


def build() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    images = main.ImageEvidenceAdapter()
    adapter = main.FinancialEventAdapter(images)
    args = (adapter.canonical_rows(), main.MessageEvidenceAdapter().rows, main.ExchangeRateAdapter())
    canonicalizer = main.Canonicalizer(*args)
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    options = main.PaymentOptionAdapter().load()
    planner = main.Planner(canonicalizer, options, main.WindowPolicy.DAYS_0_THROUGH_89)
    matrix: list[dict[str, object]] = []
    attribution: list[dict[str, object]] = []
    for request in requests:
        profile = profiles[request.user_id]
        decision, events = planner.decide(request, profile)
        decision.explanation = main.make_explanation(decision, events)
        actual = main.serialize(decision)
        target = expected[request.request_id]
        differences = {column: {"expected": target[column], "actual": actual[column]} for column in main.OUTPUT_COLUMNS if target[column] != actual[column]}
        if not differences:
            continue
        rows = canonicalizer.message_adjustments(request.user_id, canonicalizer.by_user.get(request.user_id, []), request.request_date)
        history = [event for event in rows if event.amount is not None and event.event_date <= request.request_date and event.status not in {"failed", "cancelled", "unrealized"} and event.direction != "non_cash"]
        flows = main.Simulator(canonicalizer, main.WindowPolicy.DAYS_0_THROUGH_89).flows(request, profile, events)
        balance = profile.current_available_balance
        balances: list[dict[str, str]] = []
        for offset in range(main.WindowPolicy.DAYS_0_THROUGH_89.upper_bound_offset() + 1):
            day = request.request_date + timedelta(days=offset)
            balance += flows.get(day, 0)
            balances.append({"date": day.isoformat(), "balance": main.short_decimal(balance), "flow": main.short_decimal(flows.get(day, main.Decimal(0)))})
        min_point = min(balances, key=lambda item: item["balance"])
        common = {
            "request_id": request.request_id,
            "user_id": request.user_id,
            "request_date": request.request_date.isoformat(),
            "opening_balance": main.short_decimal(profile.current_available_balance),
            "minimum_balance_to_keep": main.short_decimal(profile.minimum_balance_to_keep),
            "expected_output": target,
            "actual_output": actual,
            "differences": differences,
            "historical_streams": stream_groups(history),
            "projected_events": [
                {"event_id": event.event_id, "source_event_id": event.source_event_id, "date": (event.settlement_date or event.event_date).isoformat(), "amount": main.short_decimal(event.amount or 0), "currency": event.currency, "category": event.category, "description": event.description, "provenance": event.provenance}
                for event in events if event.projected
            ],
            "minimum_forecast_balance": min_point,
            "planner_result": {"status": decision.status, "method": decision.method, "payment_plan": actual["payment_plan"], "earliest": actual["earliest_date_for_full_payment"], "changes": actual["spending_changes_needed"]},
        }
        matrix.append(common)
        attribution.append({**common, "cash_flows_and_balances": balances, "classification_by_field": {field: classify(field) for field in differences}})
    return matrix, attribution


def classify(field: str) -> str:
    return {
        "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
        "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate",
        "affordability_status": "safe-payment eligibility derived from the forecast predicate",
        "recommended_payment_method": "planner candidate eligibility/ranking downstream of forecast",
        "payment_plan": "plan construction downstream of status/earliest date",
        "spending_changes_needed": "spending-change enumeration/provenance or forecast binding trough",
        "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
    }[field]


def write() -> None:
    matrix, attribution = build()
    evaluation = ROOT / "evaluation"
    (evaluation / "s16_root_cause_matrix.json").write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evaluation / "s16_cashflow_attribution.json").write_text(json.dumps(attribution, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# S16 root-cause matrix", "", "This report traces the current production checkpoint. It does not use expected values as production inputs and does not assign every field difference to recurrence.", ""]
    for item in matrix:
        lines += [f"## `{item['request_id']}` / `{item['user_id']}`", "", f"- Request date: `{item['request_date']}`; opening balance: `{item['opening_balance']}`; minimum: `{item['minimum_balance_to_keep']}`", f"- Minimum forecast balance: `{item['minimum_forecast_balance']['balance']}` on `{item['minimum_forecast_balance']['date']}` with flow `{item['minimum_forecast_balance']['flow']}`", f"- Planner result: `{item['planner_result']}`", "- Expected output:", "```json", json.dumps(item["expected_output"], indent=2, sort_keys=True), "```", "- Actual output:", "```json", json.dumps(item["actual_output"], indent=2, sort_keys=True), "```", "- Differing fields and classification:", "```json", json.dumps({field: {**values, "classification": classify(field)} for field, values in item["differences"].items()}, indent=2, sort_keys=True), "```", "- Historical inferred streams:", "```json", json.dumps(item["historical_streams"], indent=2, sort_keys=True), "```", "- Projected future events:", "```json", json.dumps(item["projected_events"], indent=2, sort_keys=True), "```", ""]
    (evaluation / "s16_root_cause_matrix.md").write_text("\n".join(lines), encoding="utf-8")
    lines = ["# S16 cash-flow attribution", "", "Current production path only. Each section lists every non-zero canonical future cash flow and resulting daily balance. The phase-aware policy remains experimental and is not silently substituted.", ""]
    for item in attribution:
        lines += [f"## `{item['request_id']}` / `{item['user_id']}`", "", f"- Opening/minimum: `{item['opening_balance']}` / `{item['minimum_balance_to_keep']}`", f"- Expected safe amount: `{item['expected_output']['amount_safe_to_pay']}`; actual: `{item['actual_output']['amount_safe_to_pay']}`", f"- Expected earliest: `{item['expected_output']['earliest_date_for_full_payment']}`; actual: `{item['actual_output']['earliest_date_for_full_payment']}`", "- Classified differences:", "```json", json.dumps(item["classification_by_field"], indent=2, sort_keys=True), "```", "- Future flow and balance path:", "```text", "\n".join(f"{row['date']} flow={row['flow']} balance={row['balance']}" for row in item["cash_flows_and_balances"] if row["flow"] != "0"), "```", "- Projected event attribution:", "```json", json.dumps(item["projected_events"], indent=2, sort_keys=True), "```", ""]
    (evaluation / "s16_cashflow_attribution.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote root-cause matrix and cash-flow attribution for {len(matrix)} mismatching requests")


if __name__ == "__main__":
    write()
