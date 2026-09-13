"""Bounded R4/E1-E3 evaluation and request-level ledger report."""
from __future__ import annotations

import json
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT / "evaluation"))
import main  # noqa: E402
from r4_period_reconciled import EnvelopeEstimator, PeriodReconciledCanonicalizer  # noqa: E402


CORE = ["amount_safe_to_pay", "affordability_status", "recommended_payment_method", "payment_plan", "earliest_date_for_full_payment", "spending_changes_needed"]


def score(rows, expected):
    fields = main.OUTPUT_COLUMNS[1:]
    safe_deltas = [main.dec(a["amount_safe_to_pay"]) - main.dec(e["amount_safe_to_pay"]) for a, e in zip(rows, expected)]
    return {"core_exact": sum(all(a[f] == e[f] for f in CORE) for a, e in zip(rows, expected)), "full_exact": sum(all(a[f] == e[f] for f in fields) for a, e in zip(rows, expected)), "amount_exact": sum(a["amount_safe_to_pay"] == e["amount_safe_to_pay"] for a, e in zip(rows, expected)), "numeric_mismatches": sum(a["amount_safe_to_pay"] != e["amount_safe_to_pay"] for a, e in zip(rows, expected)), "safe_error": str(sum(abs(x) for x in safe_deltas)), "optimistic": sum(x > 0 for x in safe_deltas), "pessimistic": sum(x < 0 for x in safe_deltas), "max_abs": str(max((abs(x) for x in safe_deltas), default=Decimal(0))), "per_field": {f: sum(a[f] == e[f] for a, e in zip(rows, expected)) for f in fields}}


def run_candidate(estimator, profiles, requests, options, raw_events, messages, expected, window):
    canonical = PeriodReconciledCanonicalizer(raw_events, messages, main.ExchangeRateAdapter(), estimator)
    planner = main.Planner(canonical, options, window)
    rows = []
    ledgers = {}
    for request in requests:
        decision, events = planner.decide(request, profiles[request.user_id])
        decision.explanation = main.make_explanation(decision, events)
        row = main.serialize(decision)
        main.validate(row, request)
        rows.append(row)
        flows = planner.oracle.flows(request, profiles[request.user_id], events)
        _, balances, trough = planner.oracle.run(request, profiles[request.user_id], events, [(request.request_date, Decimal(0))])
        projected = [e for e in events if e.projected]
        ledgers[request.request_id] = {"r0_or_r4_trough": str(trough), "trough_date": min(balances, key=balances.get).isoformat(), "projected_count": len(projected), "diagnostics": canonical.envelope_diagnostics.get(request.request_id, {}), "projected": [{"event_id": e.event_id, "date": (e.settlement_date or e.event_date).isoformat(), "category": e.category, "direction": e.direction, "amount": str(e.amount), "provenance": e.provenance} for e in projected]}
    return rows, canonical, ledgers


def main_run():
    profiles = main.ProfileAdapter().load(); requests = main.RequestAdapter().load("sample_requests.csv"); options = main.PaymentOptionAdapter().load(); raw_events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows(); messages = main.read_csv("messages.csv"); expected = main.read_csv("sample_requests.csv"); window = main.WindowPolicy.DAYS_0_THROUGH_89
    r0_rows = main.execute(False, window)
    results = {"R0": score(r0_rows, expected)}; candidates = {}; all_ledgers = {}
    for estimator in EnvelopeEstimator:
        rows, canonical, ledgers = run_candidate(estimator, profiles, requests, options, raw_events, messages, expected, window)
        candidates[estimator.value] = score(rows, expected); all_ledgers[estimator.value] = ledgers
    comparison = results | candidates
    out = {"results": comparison, "ledgers": all_ledgers}
    tmp = Path("/tmp/buy_or_wait_reset"); tmp.mkdir(exist_ok=True)
    (tmp / "r4_period_reconciled.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    Path("evaluation/r4_period_reconciled_results.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# R4 period-reconciled R0", "", "R4 preserves R0 projected dates and planner semantics. Only inferred recurrence amounts are reconciled against eligible historical period envelopes.", "", "## Candidate comparison", "", "| Metric | R0 | R4-E1 | R4-E2 | R4-E3 |", "|---|---:|---:|---:|---:|"]
    for label, key in [("S16-CORE exact", "core_exact"), ("amount-safe exact", "amount_exact"), ("numeric mismatches", "numeric_mismatches"), ("absolute safe error", "safe_error"), ("earliest-date exact", "per_field"), ("status exact", "per_field"), ("method exact", "per_field"), ("plan exact", "per_field"), ("spending-change exact", "per_field")]:
        vals=[]
        for name in ["R0", EnvelopeEstimator.E1.value, EnvelopeEstimator.E2.value, EnvelopeEstimator.E3.value]:
            v=comparison[name][key]
            if key == "per_field": v=v[{"earliest-date exact":"earliest_date_for_full_payment","status exact":"affordability_status","method exact":"recommended_payment_method","plan exact":"payment_plan","spending-change exact":"spending_changes_needed"}[label]]
            if label in {"S16-CORE exact","amount-safe exact"} or label=="earliest-date exact" or label=="status exact" or label=="method exact" or label=="plan exact" or label=="spending-change exact": v=f"{v}/25"
            vals.append(str(v))
        lines.append(f"| {label} | " + " | ".join(vals) + " |")
    lines += ["", "## Direction and maximum residual", ""]
    for name in comparison: lines.append(f"- `{name}`: optimistic={comparison[name]['optimistic']}; pessimistic={comparison[name]['pessimistic']}; max absolute residual={comparison[name]['max_abs']}")
    lines += ["", "## Envelope evidence", ""]
    for estimator in EnvelopeEstimator:
        eligible = 0; dimensions_seen = 0; changed_buckets = 0; changed_requests = set()
        for rid, ledger in all_ledgers[estimator.value].items():
            for dim, diag in ledger["diagnostics"].items():
                dimensions_seen += 1
                if diag.get("state") != "PASS":
                    continue
                eligible += 1
                for bucket in diag.get("buckets", []):
                    if bucket["action"] != "none":
                        changed_buckets += 1; changed_requests.add(rid)
        lines.append(f"- `{estimator.value}`: eligible dimensions `{eligible}/{dimensions_seen}`; changed buckets `{changed_buckets}` across `{len(changed_requests)}/25` requests. Eligibility required supported cadence and at least two historical buckets.")
    lines += ["", "## Request-level comparison", "", "| Request | Expected safe | R0 safe | R4-E1 safe | R4-E2 safe | R4-E3 safe | R0 error | Best R4 error |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    r4_rows = {}
    for estimator in EnvelopeEstimator:
        rows, _, _ = run_candidate(estimator, profiles, requests, options, raw_events, messages, expected, window); r4_rows[estimator.value] = rows
    for i, exp in enumerate(expected):
        r0 = r0_rows[i]; r4vals=[r4_rows[e.value][i] for e in EnvelopeEstimator]; expv=main.dec(exp["amount_safe_to_pay"]); r0err=abs(main.dec(r0["amount_safe_to_pay"])-expv); best=min(abs(main.dec(row["amount_safe_to_pay"])-expv) for row in r4vals)
        lines.append(f"| `{exp['request_id']}` | {exp['amount_safe_to_pay']} | {r0['amount_safe_to_pay']} | {r4vals[0]['amount_safe_to_pay']} | {r4vals[1]['amount_safe_to_pay']} | {r4vals[2]['amount_safe_to_pay']} | {r0err} | {best} |")
    anchor_ids=["request_02","request_04","request_10","request_11","request_24","request_25"]
    lines += ["", "## Anchor requests", ""]
    for rid in anchor_ids:
        i=next(i for i,r in enumerate(expected) if r["request_id"]==rid); expv=main.dec(expected[i]["amount_safe_to_pay"]); lines += [f"### `{rid}`", "", f"- Expected safe: `{expected[i]['amount_safe_to_pay']}`; R0 safe: `{r0_rows[i]['amount_safe_to_pay']}`."]
        for estimator in EnvelopeEstimator:
            row=r4_rows[estimator.value][i]; led=all_ledgers[estimator.value][rid]; trough=led["r0_or_r4_trough"]; lines.append(f"- `{estimator.value}` safe `{row['amount_safe_to_pay']}`, trough `{trough}` on `{led['trough_date']}`, projected events `{led['projected_count']}`; R0 timing retained by construction.")
        lines.append(f"- Expected-implied trough: `{expv + profiles[requests[i].user_id].minimum_balance_to_keep}`.")
    lines += ["", "## Reconciliation actions", "", "The JSON report contains every changed request, dimension, cadence bucket, R0 amount, envelope, residual, action, dates, and historical-period count. The condensed action inventory follows:", ""]
    for estimator in EnvelopeEstimator:
        lines.append(f"### {estimator.value}")
        for rid, ledger in all_ledgers[estimator.value].items():
            actions=[]
            for dim, diag in ledger["diagnostics"].items():
                for bucket in diag.get("buckets", []):
                    if bucket["action"] != "none":
                        actions.append(f"{dim} bucket={bucket['bucket']} r0={bucket['r0_projected']} envelope={bucket['envelope']} residual={bucket['residual']} action={bucket['action']} periods={diag.get('historical_periods', '?')}")
            if actions:
                lines.append(f"- `{rid}`: " + "; ".join(actions))
    Path("evaluation/r4_period_reconciled_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    data=main_run()
    for name,result in data["results"].items(): print(name,result["core_exact"],result["amount_exact"],result["numeric_mismatches"],result["safe_error"])
