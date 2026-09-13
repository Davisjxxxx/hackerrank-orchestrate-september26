"""Run the bounded semantic recurrence experiment against solved samples."""
from __future__ import annotations

import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT / "evaluation"))
import main  # noqa: E402
from semantic_recurrence_policy import SemanticRecurrencePolicy, resolve_users  # noqa: E402


FIELDS = main.OUTPUT_COLUMNS[1:]
CORE = ["amount_safe_to_pay", "affordability_status", "recommended_payment_method", "payment_plan", "earliest_date_for_full_payment"]


def metrics(actual: list[dict[str, str]], expected: list[dict[str, str]]) -> dict[str, object]:
    signed = [main.dec(a["amount_safe_to_pay"]) - main.dec(e["amount_safe_to_pay"]) for a, e in zip(actual, expected)]
    return {
        "exact_rows": sum(all(a[f] == e[f] for f in FIELDS) for a, e in zip(actual, expected)),
        "exact_safe_amounts": sum(a["amount_safe_to_pay"] == e["amount_safe_to_pay"] for a, e in zip(actual, expected)),
        "numeric_mismatches": sum(x != 0 for x in signed),
        "absolute_safe_error": str(sum(abs(x) for x in signed)),
        "optimistic": sum(x > 0 for x in signed), "pessimistic": sum(x < 0 for x in signed),
        "status_exact": sum(a["affordability_status"] == e["affordability_status"] for a, e in zip(actual, expected)),
        "method_exact": sum(a["recommended_payment_method"] == e["recommended_payment_method"] for a, e in zip(actual, expected)),
        "plan_exact": sum(a["payment_plan"] == e["payment_plan"] for a, e in zip(actual, expected)),
        "earliest_exact": sum(a["earliest_date_for_full_payment"] == e["earliest_date_for_full_payment"] for a, e in zip(actual, expected)),
        "per_field": {f: sum(a[f] == e[f] for a, e in zip(actual, expected)) for f in FIELDS},
    }


def run(policy: SemanticRecurrencePolicy, profiles, requests, options, window) -> tuple[list[dict[str, str]], dict[str, object]]:
    planner = main.Planner(policy, options, window)
    rows = []
    for request in requests:
        decision, events = planner.decide(request, profiles[request.user_id])
        decision.explanation = main.make_explanation(decision, events)
        row = main.serialize(decision)
        main.validate(row, request, profiles[request.user_id], options, decision, events)
        rows.append(row)
    return rows, policy.diagnostics


def main_run() -> dict[str, object]:
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    expected = main.read_csv("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    messages = main.read_csv("messages.csv")
    images = main.read_csv("images.csv")
    raw_event_rows = main.read_csv("financial_events.csv")
    linked_by_id = {r["event_id"]: r["linked_event_id"] for r in raw_event_rows if r.get("linked_event_id")}
    window = main.WindowPolicy.DAYS_0_THROUGH_89
    users = sorted({r.user_id for r in requests})

    semantic, usage = resolve_users(users, events, messages, images, linked_by_id)
    policy = SemanticRecurrencePolicy(events, messages, images, main.ExchangeRateAdapter(), semantic)
    actual, diagnostics = run(policy, profiles, requests, options, window)
    baseline = main.execute(False, window)
    result = {"R0": metrics(baseline, expected), "semantic_candidate": metrics(actual, expected), "usage": usage, "diagnostics": diagnostics}

    changed = []
    for actual_row, r0, want in zip(actual, baseline, expected):
        if actual_row["amount_safe_to_pay"] != r0["amount_safe_to_pay"] or actual_row["earliest_date_for_full_payment"] != r0["earliest_date_for_full_payment"]:
            changed.append({"request_id": actual_row["request_id"], "r0_safe": r0["amount_safe_to_pay"], "semantic_safe": actual_row["amount_safe_to_pay"], "expected_safe": want["amount_safe_to_pay"], "r0_earliest": r0["earliest_date_for_full_payment"], "semantic_earliest": actual_row["earliest_date_for_full_payment"], "expected_earliest": want["earliest_date_for_full_payment"], "diagnostic": diagnostics.get(actual_row["request_id"], {})})
    result["changed_requests"] = changed
    out = Path("/tmp/buy_or_wait_reset")
    out.mkdir(exist_ok=True)
    (out / "semantic_recurrence_results.json").write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")

    lines = ["# Semantic recurrence experiment", "", "Evaluation-only. The model saw evidence packets only; solved outputs were loaded after resolution.", "", "## Model execution", "", "```json", json.dumps(usage, indent=2, sort_keys=True), "```", "", "## Metrics", "", "| Metric | R0 | Semantic candidate |", "|---|---:|---:|"]
    for label, key in [("Exact rows", "exact_rows"), ("Exact safe amounts", "exact_safe_amounts"), ("Numeric mismatches", "numeric_mismatches"), ("Absolute safe error", "absolute_safe_error"), ("Status exact", "status_exact"), ("Method exact", "method_exact"), ("Plan exact", "plan_exact"), ("Earliest-date exact", "earliest_exact")]:
        lines.append(f"| {label} | {result['R0'][key]}/25 | {result['semantic_candidate'][key]}/25 |" if key not in {"absolute_safe_error"} else f"| {label} | {result['R0'][key]} | {result['semantic_candidate'][key]} |")
    lines += ["", "## Changed requests", ""]
    for item in changed:
        lines.append(f"- `{item['request_id']}`: R0 safe {item['r0_safe']}; semantic {item['semantic_safe']}; expected {item['expected_safe']}; semantic projected streams={item['diagnostic'].get('verified_streams', 0)}; rejected={item['diagnostic'].get('rejected_streams', [])}")
    (out / "semantic_recurrence_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"R0": result["R0"], "semantic_candidate": result["semantic_candidate"], "usage": usage}, sort_keys=True))
    return result


if __name__ == "__main__":
    main_run()
