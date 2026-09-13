"""Evaluate the bounded authority-first R1-R3 candidates without production edits."""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402
from authority_core import AuthorityCanonicalizer, CandidatePolicy  # noqa: E402


def score(rows: list[dict[str, str]], expected: list[dict[str, str]]) -> dict[str, object]:
    fields = main.OUTPUT_COLUMNS[1:]
    core_fields = ["amount_safe_to_pay", "affordability_status", "recommended_payment_method", "payment_plan", "earliest_date_for_full_payment", "spending_changes_needed"]
    exact_rows = sum(all(a[f] == e[f] for f in fields) for a, e in zip(rows, expected))
    core_exact_rows = sum(all(a[f] == e[f] for f in core_fields) for a, e in zip(rows, expected))
    per = {f: sum(a[f] == e[f] for a, e in zip(rows, expected)) for f in fields}
    safe_error = sum(abs(main.dec(a["amount_safe_to_pay"]) - main.dec(e["amount_safe_to_pay"])) for a, e in zip(rows, expected))
    numeric = sum(a["amount_safe_to_pay"] != e["amount_safe_to_pay"] for a, e in zip(rows, expected))
    signed = [main.dec(a["amount_safe_to_pay"]) - main.dec(e["amount_safe_to_pay"]) for a, e in zip(rows, expected) if a["amount_safe_to_pay"] != e["amount_safe_to_pay"]]
    return {"exact_rows": exact_rows, "core_exact_rows": core_exact_rows, "differing_fields": sum(a[f] != e[f] for a, e in zip(rows, expected) for f in fields), "numeric_mismatches": numeric, "safe_absolute_error": str(safe_error), "optimistic_numeric": sum(x > 0 for x in signed), "pessimistic_numeric": sum(x < 0 for x in signed), "per_field_exact": per, "rows": rows}


def evaluate(policy: CandidatePolicy, profiles, requests, options, raw_events, messages, fx, window):
    canonical = AuthorityCanonicalizer(raw_events, messages, fx, policy)
    planner = main.Planner(canonical, options, window)
    rows = []
    for request in requests:
        decision, events = planner.decide(request, profiles[request.user_id])
        decision.explanation = main.make_explanation(decision, events)
        row = main.serialize(decision)
        main.validate(row, request)
        rows.append(row)
    return rows, canonical


def main_run() -> dict[str, object]:
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    raw_events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    messages = main.read_csv("messages.csv")
    expected = main.read_csv("sample_requests.csv")
    window = main.WindowPolicy.DAYS_0_THROUGH_89
    baseline = main.execute(False, window)
    results = {"R0_current_production": score(baseline, expected)}
    diagnostics = {}
    for policy in CandidatePolicy:
        rows, canonical = evaluate(policy, profiles, requests, options, raw_events, messages, main.ExchangeRateAdapter(), window)
        result = score(rows, expected)
        result.pop("rows")
        results[policy.value] = result
        diagnostics[policy.value] = {r.request_id: [{"event_id": e.event_id, "date": (e.settlement_date or e.event_date).isoformat(), "direction": e.direction, "category": e.category, "amount": str(e.amount), "provenance": e.provenance} for e in canonical.for_request(r, profiles[r.user_id], window) if e.projected] for r in requests}
    out = {"results": results, "diagnostics": diagnostics}
    tmp = Path("/tmp/buy_or_wait_reset")
    tmp.mkdir(exist_ok=True)
    (tmp / "authority_candidate_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Bounded authority-first recurrence candidates", "", "Evaluation-only. R0 is the unchanged production benchmark; R1-R3 use the parallel resolver.", "", "| Metric | R0 | R1 | R2 | R3 |", "|---|---:|---:|---:|---:|"]
    metric_map = [("S16-CORE exact rows", "core_exact_rows"), ("amount_safe exact", "per_field_exact"), ("numeric mismatches", "numeric_mismatches"), ("absolute safe error", "safe_absolute_error"), ("earliest-date exact", "per_field_exact"), ("status exact", "per_field_exact"), ("method exact", "per_field_exact"), ("plan exact", "per_field_exact"), ("spending-change exact", "per_field_exact"), ("S16-FULL-BYTE", "exact_rows")]
    for label, key in metric_map:
        vals = []
        for name in ["R0_current_production", CandidatePolicy.R1.value, CandidatePolicy.R2.value, CandidatePolicy.R3.value]:
            v = results[name][key]
            if isinstance(v, dict):
                field = {"amount_safe exact": "amount_safe_to_pay", "earliest-date exact": "earliest_date_for_full_payment", "status exact": "affordability_status", "method exact": "recommended_payment_method", "plan exact": "payment_plan", "spending-change exact": "spending_changes_needed"}[label]
                v = f"{v[field]}/25"
            elif key in {"exact_rows", "core_exact_rows"}: v = f"{v}/25"
            vals.append(str(v))
        lines.append(f"| {label} | " + " | ".join(vals) + " |")
    lines += ["", "## Error direction", ""]
    for name in results:
        lines.append(f"- `{name}`: optimistic numeric={results[name]['optimistic_numeric']}; pessimistic numeric={results[name]['pessimistic_numeric']}; largest absolute error={max((abs(main.dec(a['amount_safe_to_pay']) - main.dec(e['amount_safe_to_pay'])) for a, e in zip((baseline if name == 'R0_current_production' else []), expected)), default=Decimal(0)) if name == 'R0_current_production' else 'see JSON'}")
    (tmp / "authority_candidate_comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    data = main_run()
    for name, result in data["results"].items():
        print(name, result["exact_rows"], result["differing_fields"], result["numeric_mismatches"], result["safe_absolute_error"])
