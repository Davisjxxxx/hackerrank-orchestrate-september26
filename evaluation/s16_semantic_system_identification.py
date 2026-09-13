"""Sample-grounded system identification for the S16 recurrence gate.

This is evaluation tooling only.  The solved rows are authoritative behavioral
evidence here, but are never imported by ``code/main.py`` and never select a
request-specific branch.  Candidate models are whole deterministic policies
with stable names and provenance-preserving event sets.
"""
from __future__ import annotations

import csv
import json
import sys
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402
from recurrence_policy_experiment import ExperimentCanonicalizer  # noqa: E402
from s16_conservative_ambiguity_resolution import (  # noqa: E402
    compose_expense_candidate,
    suppress_literal_duplicate_projection,
)


PolicyFactory = Callable[[main.Request, main.Profile, main.WindowPolicy], list[main.CanonicalEvent]]


@dataclass(frozen=True)
class PolicySpec:
    name: str
    description: str
    complexity: int
    contract_compliant: bool
    factory: PolicyFactory


def stable(events: Iterable[main.CanonicalEvent]) -> list[main.CanonicalEvent]:
    return sorted(events, key=lambda event: ((event.settlement_date or event.event_date), event.event_id, event.provenance))


def suppress_salary(events: Iterable[main.CanonicalEvent]) -> list[main.CanonicalEvent]:
    return list(suppress_literal_duplicate_projection(list(events), {"salary"}))


def remove_salary_recurrence(events: Iterable[main.CanonicalEvent]) -> list[main.CanonicalEvent]:
    return [event for event in events if not (event.projected and event.category == "salary" and event.provenance == "recurrence:max_last_3")]


def remove_salary_continuation(events: Iterable[main.CanonicalEvent]) -> list[main.CanonicalEvent]:
    return [event for event in suppress_salary(events) if not (event.projected and event.provenance == "recurrence:confirmed_salary")]


def robust_cadence(events: Iterable[main.CanonicalEvent]) -> tuple[str, int]:
    """A bounded, evidence-based cadence rule used by one candidate model."""
    ordered = sorted(events, key=lambda event: event.event_date)
    gaps = [(right.event_date - left.event_date).days for left, right in zip(ordered, ordered[1:]) if (right.event_date - left.event_date).days > 0]
    if not gaps:
        return "none", 0
    median = int(statistics.median(gaps))
    if all(27 <= gap <= 32 for gap in gaps):
        return "month", 1
    supported = sum(abs(gap - median) <= 3 for gap in gaps)
    if median >= 5 and supported >= 2:
        return "gap", max(1, median)
    return "none", 0


def output_with_events(
    canonical: main.Canonicalizer,
    options: dict[str, list[main.PaymentOption]],
    request: main.Request,
    profile: main.Profile,
    policy: main.WindowPolicy,
    events: list[main.CanonicalEvent],
) -> tuple[dict[str, str], list[main.CanonicalEvent]]:
    planner = main.Planner(canonical, options, policy)
    original = canonical.for_request
    frozen = list(stable(events))
    canonical.for_request = lambda _r, _p, _policy, _events=frozen: list(_events)
    try:
        decision, used = planner.decide(request, profile)
    finally:
        canonical.for_request = original
    decision.explanation = main.make_explanation(decision, used)
    return main.serialize(decision), frozen


def fields(row: dict[str, str], expected: dict[str, str]) -> list[str]:
    return [column for column in main.OUTPUT_COLUMNS[1:] if row[column] != expected[column]]


def flow_path(canonical: main.Canonicalizer, request: main.Request, profile: main.Profile, events: list[main.CanonicalEvent], policy: main.WindowPolicy, payment: tuple[date, Decimal] | None = None) -> list[dict[str, object]]:
    flows = main.Simulator(canonical, policy).flows(request, profile, events)
    balance = profile.current_available_balance
    path: list[dict[str, object]] = []
    for offset in range(policy.upper_bound_offset() + 1):
        day = request.request_date + timedelta(days=offset)
        balance += flows.get(day, Decimal(0))
        payment_amount = Decimal(0)
        if payment is not None and day == payment[0]:
            payment_amount = payment[1]
            balance -= payment_amount
        path.append({"date": day.isoformat(), "balance": str(balance), "flow": str(flows.get(day, Decimal(0))), "payment": str(payment_amount)})
    return path


def first_incompatible_date(
    canonical: main.Canonicalizer,
    request: main.Request,
    profile: main.Profile,
    events: list[main.CanonicalEvent],
    expected: dict[str, str],
    policy: main.WindowPolicy,
) -> str | None:
    expected_date = expected["earliest_date_for_full_payment"]
    if expected_date:
        payment_date = date.fromisoformat(expected_date)
        path = flow_path(canonical, request, profile, events, policy, (payment_date, request.requested_amount))
        failing = [row["date"] for row in path if Decimal(str(row["balance"])) < profile.minimum_balance_to_keep]
        return failing[0] if failing else None
    path = flow_path(canonical, request, profile, events, policy)
    expected_implied = Decimal(expected["amount_safe_to_pay"]) + profile.minimum_balance_to_keep
    candidates = [row["date"] for row in path if Decimal(str(row["balance"])) <= expected_implied]
    return candidates[0] if candidates else None


def make_policies(
    canonical: main.Canonicalizer,
    args: tuple[object, ...],
) -> list[PolicySpec]:
    category = ExperimentCanonicalizer(*args, recurrence_policy="G_variable_category_fallback")
    description_family = ExperimentCanonicalizer(*args, recurrence_policy="C_description_family")
    structural = ExperimentCanonicalizer(*args, recurrence_policy="D_structural_cadence")
    sequence = ExperimentCanonicalizer(*args, recurrence_policy="H_sequence_phase_partition")
    active = ExperimentCanonicalizer(*args, recurrence_policy="I_phase_aware_active")
    exact = ExperimentCanonicalizer(*args, recurrence_policy="A_exact_normalized_description")

    def from_canon(source: main.Canonicalizer) -> PolicyFactory:
        return lambda request, profile, policy: list(source.for_request(request, profile, policy))

    def salary_variant(variant: str) -> PolicyFactory:
        def factory(request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
            base = canonical.for_request(request, profile, policy)
            if variant == "same_day":
                return suppress_salary(base)
            if variant == "anchor":
                return remove_salary_recurrence(base)
            return remove_salary_continuation(base)
        return factory

    def expense_variant(request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        base = canonical.for_request(request, profile, policy)
        alternative = category.for_request(request, profile, policy)
        return compose_expense_candidate(base, alternative)

    def robust_salary_variant(request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        original = main.cadence
        main.cadence = robust_cadence
        try:
            events = canonical.for_request(request, profile, policy)
        finally:
            main.cadence = original
        return suppress_salary(events)

    return [
        PolicySpec("P0_production", "Current production canonicalizer.", 1, True, from_canon(canonical)),
        PolicySpec("P1_exact_rebuilt", "Exact normalized-description streams using the experiment harness.", 2, True, from_canon(exact)),
        PolicySpec("P2_variable_category", "Category fallback only for variable categories.", 2, True, from_canon(category)),
        PolicySpec("P3_description_family", "Description family normalization.", 3, False, from_canon(description_family)),
        PolicySpec("P4_structural_phase", "Semantic bucket split by observed temporal phase.", 4, True, from_canon(structural)),
        PolicySpec("P5_sequence_phase", "Non-overlapping sequence extraction with phase partition.", 5, True, from_canon(sequence)),
        PolicySpec("P6_active_sequence", "Sequence partition plus stale-stream cutoff.", 6, True, from_canon(active)),
        PolicySpec("P7_salary_same_day", "Suppress only same-day explicit/projected salary collisions.", 2, True, salary_variant("same_day")),
        PolicySpec("P8_salary_anchor", "Remove historical salary recurrence when a future salary exists.", 2, False, salary_variant("anchor")),
        PolicySpec("P9_salary_explicit_only", "Suppress same-day salary duplicate and continuation from explicit salary.", 3, False, salary_variant("explicit_only")),
        PolicySpec("P10_expense_conservative", "Use existing category fallback as an expense-only supported alternative.", 3, True, expense_variant),
        PolicySpec("P11_robust_cadence_salary_collision", "Median-supported cadence with a bounded three-day outlier tolerance plus same-day salary collision suppression.", 4, True, robust_salary_variant),
    ]


def evaluate_policy(
    spec: PolicySpec,
    canonical: main.Canonicalizer,
    profiles: dict[str, main.Profile],
    requests: list[main.Request],
    options: dict[str, list[main.PaymentOption]],
    expected: dict[str, dict[str, str]],
    policy: main.WindowPolicy,
) -> dict[str, object]:
    rows: dict[str, dict[str, str]] = {}
    events_by_request: dict[str, list[main.CanonicalEvent]] = {}
    per_request: dict[str, dict[str, object]] = {}
    for request in requests:
        row, events = output_with_events(canonical, options, request, profiles[request.user_id], policy, spec.factory(request, profiles[request.user_id], policy))
        rows[request.request_id] = row
        events_by_request[request.request_id] = events
        diff = fields(row, expected[request.request_id])
        per_request[request.request_id] = {
            "fields": diff,
            "exact": not diff,
            "numeric": row["amount_safe_to_pay"] == expected[request.request_id]["amount_safe_to_pay"],
            "earliest_exact": row["earliest_date_for_full_payment"] == expected[request.request_id]["earliest_date_for_full_payment"],
            "status_method_exact": (row["affordability_status"], row["recommended_payment_method"]) == (expected[request.request_id]["affordability_status"], expected[request.request_id]["recommended_payment_method"]),
            "event_count": len(events),
        }
    return {
        "name": spec.name,
        "description": spec.description,
        "complexity": spec.complexity,
        "contract_compliant": spec.contract_compliant,
        "exact_rows": sum(item["exact"] for item in per_request.values()),
        "differing_fields": sum(len(item["fields"]) for item in per_request.values()),
        "numeric_mismatches": sum(not item["numeric"] for item in per_request.values()),
        "earliest_date_mismatches": sum(not item["earliest_exact"] for item in per_request.values()),
        "status_method_mismatches": sum(not item["status_method_exact"] for item in per_request.values()),
        "rows": rows,
        "events": {request_id: [event_signature(event) for event in events] for request_id, events in events_by_request.items()},
        "per_request": per_request,
    }


def event_signature(event: main.CanonicalEvent) -> dict[str, object]:
    return {
        "event_id": event.event_id,
        "source_event_id": event.source_event_id,
        "date": (event.settlement_date or event.event_date).isoformat(),
        "event_date": event.event_date.isoformat(),
        "category": event.category,
        "direction": event.direction,
        "amount": str(event.amount) if event.amount is not None else None,
        "currency": event.currency,
        "projected": event.projected,
        "status": event.status,
        "provenance": event.provenance,
    }


def implied_constraints(
    canonical: main.Canonicalizer,
    profiles: dict[str, main.Profile],
    requests: list[main.Request],
    expected: dict[str, dict[str, str]],
    baseline: dict[str, object],
    policy: main.WindowPolicy,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for request in requests:
        profile = profiles[request.user_id]
        row = baseline["rows"][request.request_id]
        # Event signatures are sufficient for the candidate matrix but not for
        # conversion; use the real canonical event list for the baseline path.
        events = canonical.for_request(request, profile, policy)
        path = flow_path(canonical, request, profile, events, policy)
        actual_min = min(path, key=lambda item: (Decimal(str(item["balance"])), item["date"]))
        target = expected[request.request_id]
        safe_delta = Decimal(row["amount_safe_to_pay"]) - Decimal(target["amount_safe_to_pay"])
        records.append({
            "request_id": request.request_id,
            "user_id": request.user_id,
            "request_date": request.request_date.isoformat(),
            "requested_amount": str(request.requested_amount),
            "current_available_balance": str(profile.current_available_balance),
            "minimum_balance_to_keep": str(profile.minimum_balance_to_keep),
            "expected_amount_safe_to_pay": target["amount_safe_to_pay"],
            "actual_amount_safe_to_pay": row["amount_safe_to_pay"],
            "safe_amount_delta_actual_minus_expected": str(safe_delta),
            "expected_earliest_full_payment": target["earliest_date_for_full_payment"],
            "actual_earliest_full_payment": row["earliest_date_for_full_payment"],
            "expected_status": target["affordability_status"],
            "actual_status": row["affordability_status"],
            "expected_method": target["recommended_payment_method"],
            "actual_method": row["recommended_payment_method"],
            "actual_minimum_balance": actual_min["balance"],
            "actual_minimum_date": actual_min["date"],
            "expected_implied_balance_constraint": str(Decimal(target["amount_safe_to_pay"]) + profile.minimum_balance_to_keep),
            "first_actual_incompatibility_date": first_incompatible_date(canonical, request, profile, events, target, policy),
            "binding_assumption": "expected safe amount plus reserve is treated as an implied trough only when the expected amount is not request-capped",
            "actual_future_flows_through_minimum": [item for item in path if item["date"] <= actual_min["date"]],
        })
    return records


def cross_validate(results: list[dict[str, object]], requests: list[main.Request]) -> list[dict[str, object]]:
    folds: list[dict[str, object]] = []
    request_ids = [request.request_id for request in requests]
    for held_out in request_ids:
        training = [result for result in results]
        ranked = sorted(training, key=lambda result: (
            sum(len(training_result["per_request"][rid]["fields"]) for rid in request_ids if rid != held_out for training_result in [result]),
            sum(not training_result["per_request"][rid]["numeric"] for rid in request_ids if rid != held_out for training_result in [result]),
            not result["contract_compliant"],
            result["complexity"],
            result["name"],
        ))
        selected = ranked[0]
        held = selected["per_request"][held_out]
        folds.append({
            "held_out": held_out,
            "selected_policy": selected["name"],
            "held_out_exact": held["exact"],
            "held_out_differing_fields": len(held["fields"]),
            "held_out_fields": held["fields"],
        })
    return folds


def build_report() -> dict[str, object]:
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    images = main.ImageEvidenceAdapter()
    adapter = main.FinancialEventAdapter(images)
    args = (adapter.canonical_rows(), main.MessageEvidenceAdapter().rows, main.ExchangeRateAdapter())
    canonical = main.Canonicalizer(*args)
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    specs = make_policies(canonical, args)
    results = [evaluate_policy(spec, canonical, profiles, requests, options, expected, policy) for spec in specs]
    baseline = next(result for result in results if result["name"] == "P0_production")
    constraints = implied_constraints(canonical, profiles, requests, expected, baseline, policy)
    matrix = []
    for result in results:
        matrix.append({
            "name": result["name"],
            "description": result["description"],
            "contract_compliant": result["contract_compliant"],
            "complexity": result["complexity"],
            "exact_rows": result["exact_rows"],
            "differing_fields": result["differing_fields"],
            "numeric_mismatches": result["numeric_mismatches"],
            "earliest_date_mismatches": result["earliest_date_mismatches"],
            "status_method_mismatches": result["status_method_mismatches"],
            "compatible_numeric_request_ids": [rid for rid, row in result["per_request"].items() if row["numeric"] and row["earliest_exact"]],
            "exact_request_ids": [rid for rid, row in result["per_request"].items() if row["exact"]],
        })
    return {
        "method": "global candidate-policy scoring using solved outputs as behavioral evidence; no expected value enters production",
        "policy_specs": matrix,
        "per_policy": results,
        "implied_constraints": constraints,
        "cross_validation": cross_validate(results, requests),
        "current_baseline": {"exact_rows": baseline["exact_rows"], "differing_fields": baseline["differing_fields"]},
    }


def write_reports(report: dict[str, object]) -> None:
    evaluation = ROOT / "evaluation"
    (evaluation / "s16_implied_cashflow_constraints.json").write_text(json.dumps(report["implied_constraints"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evaluation / "s16_candidate_semantics_matrix.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# S16 implied cash-flow constraints",
        "",
        "Solved outputs are used as behavioral evidence for this diagnostic only. They do not enter production runtime.",
        "",
    ]
    for item in report["implied_constraints"]:
        lines += [
            f"## `{item['request_id']}` / `{item['user_id']}`",
            "",
            f"- Request: `{item['requested_amount']}` on `{item['request_date']}`; opening balance `{item['current_available_balance']}`; reserve `{item['minimum_balance_to_keep']}`.",
            f"- Safe amount: expected `{item['expected_amount_safe_to_pay']}`, actual `{item['actual_amount_safe_to_pay']}`, actual-minus-expected `{item['safe_amount_delta_actual_minus_expected']}`.",
            f"- Earliest full payment: expected `{item['expected_earliest_full_payment'] or 'none'}`, actual `{item['actual_earliest_full_payment'] or 'none'}`.",
            f"- Status/method: expected `{item['expected_status']}/{item['expected_method']}`, actual `{item['actual_status']}/{item['actual_method']}`.",
            f"- Actual trough: `{item['actual_minimum_balance']}` on `{item['actual_minimum_date']}`; expected-implied reserve boundary `{item['expected_implied_balance_constraint']}`.",
            f"- First actual incompatibility under the expected full-payment constraint: `{item['first_actual_incompatibility_date'] or 'not observed in this bounded path'}`.",
            "",
        ]
    (evaluation / "s16_implied_cashflow_constraints.md").write_text("\n".join(lines), encoding="utf-8")

    matrix_lines = [
        "# S16 candidate semantics matrix",
        "",
        "This matrix evaluates whole deterministic policies. Candidate event sets retain event provenance. Solved values are used only for post-hoc compatibility scoring.",
        "",
        "| Policy | Exact | Differing fields | Numeric mismatches | Earliest mismatches | Status/method mismatches | Contract compliant |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in report["policy_specs"]:
        matrix_lines.append(f"| `{item['name']}` | {item['exact_rows']}/25 | {item['differing_fields']} | {item['numeric_mismatches']} | {item['earliest_date_mismatches']} | {item['status_method_mismatches']} | {item['contract_compliant']} |")
    matrix_lines += ["", "## Interpretation", "", "`P11_robust_cadence_salary_collision` is the current production policy. It is the same general behavior represented by `P0_production` after promotion, so the two rows have identical output scores. The pre-promotion production checkpoint was 3/25 with 67 differing fields; P11 reduced that to 53 without increasing exact rows. Candidate compatibility is reported per request in the JSON, including event signatures and exact/numeric-compatible request IDs.", ""]
    (evaluation / "s16_candidate_semantics_matrix.md").write_text("\n".join(matrix_lines), encoding="utf-8")

    cv_lines = [
        "# S16 policy cross-validation",
        "",
        "Leave-one-request-out selection uses the remaining solved rows to rank whole candidate policies by field error, numeric error, contract compliance, and complexity. The held-out row is never used to choose its policy. `P0_production` and `P11_robust_cadence_salary_collision` are output-equivalent after the general promotion; the selector therefore retains the simpler production label on ties.",
        "",
        "| Held out | Selected policy | Held-out exact | Held-out differing fields |",
        "|---|---|---|---:|",
    ]
    for fold in report["cross_validation"]:
        cv_lines.append(f"| `{fold['held_out']}` | `{fold['selected_policy']}` | {fold['held_out_exact']} | {fold['held_out_differing_fields']} |")
    selected = [fold["selected_policy"] for fold in report["cross_validation"]]
    cv_lines += ["", f"Selected-policy stability: `{len(set(selected))}` distinct output policy across 25 folds; counts: `{dict((name, selected.count(name)) for name in sorted(set(selected)))}`. The promoted P11 behavior is the equivalent current production implementation, not a request-specific exception.", "", "This is a finite policy-family validation, not proof that an untested policy is impossible. The promoted rule is eligible because it is contract-compliant, globally defined, and reduced the pre-pass full-set field error from 67 to 53 without request-specific behavior. S16 remains incomplete because exact rows remain 3/25.", ""]
    (evaluation / "s16_policy_cross_validation.md").write_text("\n".join(cv_lines), encoding="utf-8")


if __name__ == "__main__":
    data = build_report()
    write_reports(data)
    for item in data["policy_specs"]:
        print(item["name"], f"exact={item['exact_rows']}/25", f"fields={item['differing_fields']}", f"numeric={item['numeric_mismatches']}")
