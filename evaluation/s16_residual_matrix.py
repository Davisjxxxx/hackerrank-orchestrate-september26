"""Emit the locked S16 residual matrix and causal family clusters.

This is evaluation-only.  Expected sample rows are compared after the
production decision is built; they are never imported by the scoring runtime.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


FAMILIES = {
    "amount_safe_to_pay": "recurrence stream identity",
    "earliest_date_for_full_payment": "earliest-safe-date logic",
    "affordability_status": "payment-plan eligibility",
    "recommended_payment_method": "payment-plan eligibility",
    "payment_plan": "payment-plan eligibility",
    "spending_changes_needed": "spending-change eligibility",
    "decision_explanation": "serialization/explanation",
}


def build() -> tuple[list[dict[str, object]], dict[str, list[str]]]:
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    canonical = main.Canonicalizer(
        main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows(),
        main.read_csv("messages.csv"),
        main.ExchangeRateAdapter(),
    )
    planner = main.Planner(canonical, main.PaymentOptionAdapter().load(), policy)
    records: list[dict[str, object]] = []
    clusters: dict[str, list[str]] = defaultdict(list)
    for request in requests:
        profile = profiles[request.user_id]
        decision, events = planner.decide(request, profile)
        decision.explanation = main.make_explanation(decision, events)
        actual = main.serialize(decision)
        want = expected[request.request_id]
        differences = {
            field: {"expected": want[field], "actual": actual[field], "family": FAMILIES[field]}
            for field in main.OUTPUT_COLUMNS[1:]
            if actual[field] != want[field]
        }
        if not differences:
            continue
        flows = main.Simulator(canonical, policy).flows(request, profile, events)
        balance = profile.current_available_balance
        path = []
        for offset in range(policy.upper_bound_offset() + 1):
            day = request.request_date + main.timedelta(days=offset)
            balance += flows.get(day, Decimal(0))
            path.append((day, balance, flows.get(day, Decimal(0))))
        actual_min = min(path, key=lambda item: (item[1], item[0]))
        expected_safe = Decimal(want["amount_safe_to_pay"])
        actual_safe = Decimal(actual["amount_safe_to_pay"])
        expected_implied = expected_safe + profile.minimum_balance_to_keep
        source_events = []
        for event in events:
            day = event.settlement_date or event.event_date
            if day < request.request_date or day > actual_min[0] or not event.projected:
                continue
            converted = canonical.converted(event, profile)
            source_events.append({
                "event_id": event.event_id,
                "source_event_id": event.source_event_id,
                "date": day.isoformat(),
                "category": event.category,
                "description": event.description,
                "direction": event.direction,
                "amount_home": str(converted) if converted is not None else None,
                "provenance": event.provenance,
            })
        source_events.sort(key=lambda item: (item["date"], item["event_id"]))
        source_events = source_events[-8:]
        primary = next(iter(differences.values()))["family"]
        clusters[primary].append(request.request_id)
        records.append({
            "request_id": request.request_id,
            "user_id": request.user_id,
            "expected_output": {field: want[field] for field in main.OUTPUT_COLUMNS},
            "actual_output": actual,
            "differences": differences,
            "primary_family": primary,
            "upstream_or_downstream": {
                field: "upstream" if field == "amount_safe_to_pay" else "downstream"
                for field in differences
            },
            "first_behaviorally_incompatible_date": actual_min[0].isoformat(),
            "unexplained_net_cash_flow_delta_actual_minus_expected": str(actual_safe - expected_safe),
            "actual_limiting_balance": str(actual_min[1]),
            "actual_limiting_date": actual_min[0].isoformat(),
            "expected_implied_limiting_balance": str(expected_implied),
            "candidate_source_events": source_events,
            "candidate_source_note": "Candidate events are the current projected flows through the binding date; they identify causal leverage, not a solved-event lookup.",
        })
    return records, dict(sorted(clusters.items()))


def write() -> None:
    records, clusters = build()
    evaluation = ROOT / "evaluation"
    (evaluation / "s16_residual_53_matrix.json").write_text(
        json.dumps({"counts": {"rows": len(records), "fields": sum(len(r["differences"]) for r in records)}, "rows": records}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# S16 residual 53 matrix",
        "",
        "Production checkpoint: robust bounded cadence, settlement-date anchoring, salary same-date collision suppression, and `max(last_3_occurrences.amount)`. Expected values are post-hoc diagnostics only.",
        "",
        f"- Non-exact requests: `{len(records)}/25`",
        f"- Differing fields: `{sum(len(r['differences']) for r in records)}`",
        "",
        "| Request | Field | Expected | Actual | Primary family | Direction | First incompatible date | Net delta |",
        "|---|---|---|---|---|---|---|---:|",
    ]
    for record in records:
        for field, difference in record["differences"].items():
            lines.append(
                f"| `{record['request_id']}` | `{field}` | `{difference['expected']}` | `{difference['actual']}` | {difference['family']} | {record['upstream_or_downstream'][field]} | `{record['first_behaviorally_incompatible_date']}` | `{record['unexplained_net_cash_flow_delta_actual_minus_expected']}` |"
            )
    lines += ["", "## Causal notes", "", "- `amount_safe_to_pay` mismatches are upstream forecast-path mismatches.", "- Date, status, method, plan, spending-change, and explanation mismatches are downstream unless a fresh experiment proves an independent subsystem defect.", "- Candidate source events are evidence for diagnosis, not production identity rules.", ""]
    (evaluation / "s16_residual_53_matrix.md").write_text("\n".join(lines), encoding="utf-8")

    cluster_lines = [
        "# S16 residual family clusters",
        "",
        "Clusters are causal families, not request-specific policies. A request appears under its first differing field's primary family; downstream fields remain recorded in the matrix.",
        "",
        "| Cluster | Affected requests | Common evidence | Current behavior | Expected-implied behavior | Smallest general hypothesis |",
        "|---|---|---|---|---|---|",
    ]
    descriptions = {
        "recurrence stream identity": ("Rotating descriptions and sparse category histories; no source/account/merchant/stream ID.", "Exact-description streams project the current path.", "Choose one evidence-bounded economic stream partition from cadence, phase, chronology, and lifecycle evidence."),
        "earliest-safe-date logic": ("The first safe date moves with the forecast trough.", "Earliest date is calculated from the current canonical path.", "Keep date search downstream until the canonical cash-flow path is correct."),
        "payment-plan eligibility": ("Status/method/plan changes coincide with a different safe amount or trough.", "Planner ranks candidates against the current path.", "Repair upstream cash-flow construction before changing plan rules."),
        "spending-change eligibility": ("Expected edits target flexible recurring events at the binding trough.", "No edit is needed under the current path.", "Enumerate only trusted future flexible representatives after the baseline path is fixed."),
        "serialization/explanation": ("Numeric decision is exact for one row or follows a changed decision.", "Template family is deterministic but not always the sample wording.", "Tune templates only after numeric and plan state is exact."),
    }
    for family, request_ids in clusters.items():
        evidence, current, hypothesis = descriptions[family]
        cluster_lines.append(f"| **{family}** | {', '.join(f'`{x}`' for x in request_ids)} | {evidence} | {current} | Sample output implies a different {family.lower()} result. | {hypothesis} |")
    cluster_lines += ["", "## Cross-cluster conclusion", "", "The 21 numeric mismatches are concentrated in recurrence/lifecycle/evidence construction. The remaining 32 fields are largely downstream. The data supports both label-specific and chronology-supported rotating-category interpretations for the same trusted rows, so no request-specific selection is promoted.", ""]
    (evaluation / "s16_residual_family_clusters.md").write_text("\n".join(cluster_lines), encoding="utf-8")
    print(f"wrote {len(records)} residual rows and {sum(len(r['differences']) for r in records)} field mismatches")


if __name__ == "__main__":
    write()
