"""Compare confirmed-future salary semantics without changing production."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


def suppress_same_day_duplicate_projection(events: list[main.CanonicalEvent], categories: set[str] | None = None) -> list[main.CanonicalEvent]:
    """Apply the audited same-day collision rule for experiments only."""
    explicit_keys = {
        (event.user_id, event.event_type, event.category, event.direction, event.currency, event.flexibility, event.settlement_date or event.event_date)
        for event in events
        if not event.projected and (categories is None or event.category in categories)
    }
    result = []
    for event in events:
        key = (event.user_id, event.event_type, event.category, event.direction, event.currency, event.flexibility, event.settlement_date or event.event_date)
        if event.projected and (categories is None or event.category in categories) and key in explicit_keys:
            continue
        result.append(event)
    return sorted(result, key=lambda event: ((event.settlement_date or event.event_date), event.event_id))


def filtered_events(canonical: main.Canonicalizer, request: main.Request, profile: main.Profile, policy: main.WindowPolicy, mode: str) -> list[main.CanonicalEvent]:
    events = canonical.for_request(request, profile, policy)
    if mode == "B_confirmed_occurrence_suppression" or mode == "D_explicit_only_confirmation":
        events = suppress_same_day_duplicate_projection(events, {"salary"})
    if mode == "C_confirmed_anchor_authority":
        events = [event for event in events if not (event.projected and event.category == "salary" and event.provenance == "recurrence:max_last_3")]
    if mode == "D_explicit_only_confirmation":
        events = [event for event in events if not (event.projected and event.provenance == "recurrence:confirmed_salary")]
    return sorted(events, key=lambda event: ((event.settlement_date or event.event_date), event.event_id))


def run_policy(mode: str, canonical: main.Canonicalizer, profiles: dict[str, main.Profile], requests: list[main.Request], options: dict[str, list[main.PaymentOption]], policy: main.WindowPolicy, expected: dict[str, dict[str, str]]) -> dict[str, object]:
    planner = main.Planner(canonical, options, policy)
    failures: dict[str, list[str]] = {}
    rows: dict[str, dict[str, str]] = {}
    for request in requests:
        events = filtered_events(canonical, request, profiles[request.user_id], policy, mode)
        decision = planner.decide_with_events(request, profiles[request.user_id], events) if hasattr(planner, "decide_with_events") else None
        if decision is None:
            # The experiment is deliberately isolated from production: clone
            # only the planner call sites that consume the event list.
            safe = planner.safe_amount(request, profiles[request.user_id], events)
            earliest = planner.earliest_full(request, profiles[request.user_id], events)
            candidates: list[main.Decision] = []
            if "full_payment" in profiles[request.user_id].methods and planner.oracle.run(request, profiles[request.user_id], events, [(request.request_date, request.requested_amount)])[0]:
                candidates.append(main.Decision(request, profiles[request.user_id], safe, "affordable_now", "full_payment", [(request.request_date, request.requested_amount, main.short_decimal(request.requested_amount))], earliest or request.request_date, (), total_paid=request.requested_amount))
            if "full_payment" in profiles[request.user_id].methods and earliest is not None and request.request_date < earliest <= request.desired_completion_date:
                candidates.append(main.Decision(request, profiles[request.user_id], safe, "affordable_later", "wait", [(earliest, request.requested_amount, main.short_decimal(request.requested_amount))], earliest, (), total_paid=request.requested_amount))
            # For the policy measurement, preserve the production planner's
            # complete candidate logic by temporarily supplying this event set.
            original = planner.canonicalizer.for_request
            planner.canonicalizer.for_request = lambda _r, _p, _policy, _events=events: list(_events)
            decision, _ = planner.decide(request, profiles[request.user_id])
            planner.canonicalizer.for_request = original
        decision.explanation = main.make_explanation(decision, events)
        row = main.serialize(decision)
        rows[request.request_id] = row
        fields = [field for field in main.OUTPUT_COLUMNS[1:] if row[field] != expected[request.request_id][field]]
        if fields:
            failures[request.request_id] = fields
    return {"mode": mode, "exact_rows": len(requests) - len(failures), "differing_fields": sum(len(fields) for fields in failures.values()), "failures": failures, "rows": rows}


def main_run() -> dict[str, object]:
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    raw = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    canonical = main.Canonicalizer(raw, main.read_csv("messages.csv"), main.ExchangeRateAdapter())
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    policies = ["A_existing_behavior", "B_confirmed_occurrence_suppression", "C_confirmed_anchor_authority", "D_explicit_only_confirmation"]
    reports = [run_policy(mode, canonical, profiles, requests, options, policy, expected) for mode in policies]
    baseline = reports[0]
    for report in reports[1:]:
        report["improved_requests"] = sorted(set(baseline["failures"]) - set(report["failures"]))
        report["regressed_requests"] = sorted(set(report["failures"]) - set(baseline["failures"]))
    return {"policies": reports}


def write(report: dict[str, object]) -> None:
    (ROOT / "evaluation" / "s16_future_semantics_experiment.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# S16 future-cash-flow semantic experiment", "", "Analysis only; no policy below is production behavior until separately promoted.", "", "| Policy | Exact rows | Differing fields | Improved requests | Regressed requests | Verdict |", "|---|---:|---:|---|---|---|"]
    for report_item in report["policies"]:
        improved = ", ".join(report_item.get("improved_requests", [])) or "none"
        regressed = ", ".join(report_item.get("regressed_requests", [])) or "none"
        verdict = "baseline" if report_item["mode"].startswith("A_") else "measure only; inspect arithmetic and stream semantics"
        lines.append(f"| `{report_item['mode']}` | {report_item['exact_rows']}/25 | {report_item['differing_fields']} | {improved} | {regressed} | {verdict} |")
    lines += ["", "## Definitions", "", "- A: current production behavior.", "- B: remove a historical salary projection only when a compatible explicit salary exists on the same settlement date.", "- C: an explicit future salary is authoritative; remove all historical salary projections while retaining only explicit salary and any continuation explicitly generated from that anchor.", "- D: count the explicit salary once, suppress its same-date historical duplicate, and do not let the explicit record alone generate continuation.", "", "The experiment must be paired with the collision table and does not use request-specific rules.", ""]
    (ROOT / "evaluation" / "s16_future_semantics_experiment.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write(main_run())
