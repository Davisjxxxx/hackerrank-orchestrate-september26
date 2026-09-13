"""Evaluate the contract's financially-safer ambiguity tie-break for S16.

This module is deliberately evaluation-only.  It compares candidate future
cash-flow sets produced by existing history-supported recurrence policies; it
never reads solved output while constructing a candidate and never creates a
new event.  The solved rows are used only after planning to measure byte
compatibility.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402
from recurrence_policy_experiment import (  # noqa: E402
    ExperimentCanonicalizer,
    VARIABLE_CATEGORIES,
)
from s16_future_semantics_experiment import suppress_same_day_duplicate_projection  # noqa: E402


@dataclass(frozen=True)
class Candidate:
    name: str
    events: tuple[main.CanonicalEvent, ...]


def event_day(event: main.CanonicalEvent) -> date:
    return event.settlement_date or event.event_date


def event_sort_key(event: main.CanonicalEvent) -> tuple[str, str, str, str, str, str]:
    return (
        event_day(event).isoformat(),
        event.event_id,
        event.user_id,
        event.category,
        event.direction,
        event.currency,
    )


def stable_events(events: Iterable[main.CanonicalEvent]) -> tuple[main.CanonicalEvent, ...]:
    return tuple(sorted(events, key=event_sort_key))


def eligible(events: Iterable[main.CanonicalEvent]) -> tuple[main.CanonicalEvent, ...]:
    """Apply lifecycle exclusion before any ambiguity comparison."""
    return stable_events(
        event for event in events
        if event.status not in {"failed", "cancelled", "unrealized"}
        and event.direction != "non_cash"
    )


def suppress_literal_duplicate_projection(
    events: Iterable[main.CanonicalEvent],
    categories: set[str] | None = None,
) -> tuple[main.CanonicalEvent, ...]:
    """Keep explicit confirmed rows and remove only a same-day projection.

    The key includes economic fields, so this is not a general category merge
    and cannot turn the conservative rule into double counting.
    """
    return tuple(suppress_same_day_duplicate_projection(list(eligible(events)), categories))


def compose_expense_candidate(
    baseline: Iterable[main.CanonicalEvent],
    category_candidate: Iterable[main.CanonicalEvent],
) -> tuple[main.CanonicalEvent, ...]:
    """Replace only variable-category projected rows with a supported variant."""
    base = eligible(baseline)
    alternative = eligible(category_candidate)
    retained = [event for event in base if not (event.projected and event.category in VARIABLE_CATEGORIES)]
    replacement = [event for event in alternative if event.projected and event.category in VARIABLE_CATEGORIES]
    return stable_events([*retained, *replacement])


def candidate_sets(
    baseline: Iterable[main.CanonicalEvent],
    variable_category_candidate: Iterable[main.CanonicalEvent],
) -> dict[str, tuple[main.CanonicalEvent, ...]]:
    """Return only evidence-supported alternatives used in this pass."""
    base = stable_events(baseline)
    income = suppress_literal_duplicate_projection(base, {"salary"})
    expense = compose_expense_candidate(base, variable_category_candidate)
    both = suppress_literal_duplicate_projection(expense, {"salary"})
    return {
        "baseline": base,
        "income_conservative": income,
        "expense_conservative": expense,
        "both_conservative": both,
    }


def minimum_balance(
    canonical: main.Canonicalizer,
    request: main.Request,
    profile: main.Profile,
    events: Iterable[main.CanonicalEvent],
    policy: main.WindowPolicy,
) -> tuple[Decimal, date]:
    flows = main.Simulator(canonical, policy).flows(request, profile, list(events))
    balance = profile.current_available_balance
    path: list[tuple[Decimal, date]] = []
    for offset in range(policy.upper_bound_offset() + 1):
        day = request.request_date + timedelta(days=offset)
        balance += flows.get(day, Decimal(0))
        path.append((balance, day))
    return min(path, key=lambda item: (item[0], item[1]))


def choose_conservative(
    canonical: main.Canonicalizer,
    request: main.Request,
    profile: main.Profile,
    candidates: dict[str, tuple[main.CanonicalEvent, ...]],
    policy: main.WindowPolicy,
    allowed: tuple[str, ...],
) -> tuple[str, tuple[main.CanonicalEvent, ...], dict[str, dict[str, str]]]:
    """Choose the lowest supported forecast trough, with conservative ties.

    A future credit which occurs before the limiting date may leave the
    minimum balance unchanged, so a trough-only comparison would be
    optimistic for unresolved income identity.  In that tie case, prefer
    fewer credits, then more debits, then a stable name.  These are all
    properties of the supported candidate flows, not invented facts.
    """
    scores: dict[str, dict[str, str]] = {}
    for name in allowed:
        trough, day = minimum_balance(canonical, request, profile, candidates[name], policy)
        flows = main.Simulator(canonical, policy).flows(request, profile, list(candidates[name]))
        total_credit = sum((amount for amount in flows.values() if amount > 0), Decimal(0))
        total_debit = sum((-amount for amount in flows.values() if amount < 0), Decimal(0))
        scores[name] = {
            "minimum_balance": str(trough),
            "limiting_date": day.isoformat(),
            "total_credit": str(total_credit),
            "total_debit": str(total_debit),
        }
    selected = min(
        allowed,
        key=lambda name: (
            Decimal(scores[name]["minimum_balance"]),
            Decimal(scores[name]["total_credit"]),
            -Decimal(scores[name]["total_debit"]),
            name,
        ),
    )
    return selected, candidates[selected], scores


def run_with_events(
    planner: main.Planner,
    request: main.Request,
    profile: main.Profile,
    events: Iterable[main.CanonicalEvent],
) -> dict[str, str]:
    original = planner.canonicalizer.for_request
    frozen = list(stable_events(events))
    planner.canonicalizer.for_request = lambda _r, _p, _policy, _events=frozen: list(_events)
    try:
        decision, used = planner.decide(request, profile)
    finally:
        planner.canonicalizer.for_request = original
    decision.explanation = main.make_explanation(decision, used)
    return main.serialize(decision)


def event_signature(event: main.CanonicalEvent) -> tuple[str, str, str, str, str, str, bool, str]:
    return (
        event.event_id,
        event.category,
        event.direction,
        event_day(event).isoformat(),
        main.short_decimal(event.amount) if event.amount is not None else "",
        event.currency,
        event.projected,
        event.provenance,
    )


def build_context() -> tuple[main.Canonicalizer, ExperimentCanonicalizer, dict[str, main.Profile], list[main.Request], dict[str, list[main.PaymentOption]], main.WindowPolicy, dict[str, dict[str, str]]]:
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    images = main.ImageEvidenceAdapter()
    adapter = main.FinancialEventAdapter(images)
    args = (adapter.canonical_rows(), main.MessageEvidenceAdapter().rows, main.ExchangeRateAdapter())
    canonical = main.Canonicalizer(*args)
    category = ExperimentCanonicalizer(*args, recurrence_policy="G_variable_category_fallback")
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    return canonical, category, profiles, requests, options, policy, expected


def compare_policy(
    name: str,
    allowed: tuple[str, ...],
    canonical: main.Canonicalizer,
    category: ExperimentCanonicalizer,
    profiles: dict[str, main.Profile],
    requests: list[main.Request],
    options: dict[str, list[main.PaymentOption]],
    policy: main.WindowPolicy,
    expected: dict[str, dict[str, str]],
) -> dict[str, object]:
    rows: dict[str, dict[str, str]] = {}
    selections: dict[str, object] = {}
    planner = main.Planner(canonical, options, policy)
    for request in requests:
        profile = profiles[request.user_id]
        base = canonical.for_request(request, profile, policy)
        alternative = category.for_request(request, profile, policy)
        candidates = candidate_sets(base, alternative)
        selected, events, scores = choose_conservative(canonical, request, profile, candidates, policy, allowed)
        rows[request.request_id] = run_with_events(planner, request, profile, events)
        selections[request.request_id] = {
            "selected": selected,
            "scores": scores,
            "changed_from_baseline": [event_signature(event) for event in events if event_signature(event) not in {event_signature(item) for item in candidates["baseline"]}],
            "removed_from_baseline": [event_signature(event) for event in candidates["baseline"] if event_signature(event) not in {event_signature(item) for item in events}],
        }
    failures = {
        request_id: [field for field in main.OUTPUT_COLUMNS[1:] if row[field] != expected[request_id][field]]
        for request_id, row in rows.items()
    }
    failures = {request_id: fields for request_id, fields in failures.items() if fields}
    return {
        "name": name,
        "allowed": list(allowed),
        "exact_rows": len(requests) - len(failures),
        "differing_fields": sum(len(fields) for fields in failures.values()),
        "failures": failures,
        "rows": rows,
        "selections": selections,
    }


def report() -> dict[str, object]:
    canonical, category, profiles, requests, options, policy, expected = build_context()
    policies = [
        ("A_baseline", ("baseline",)),
        ("B_conservative_both", ("baseline", "income_conservative", "expense_conservative", "both_conservative")),
        ("C_conservative_income_only", ("baseline", "income_conservative")),
        ("D_conservative_expense_only", ("baseline", "expense_conservative")),
    ]
    results = [compare_policy(name, allowed, canonical, category, profiles, requests, options, policy, expected) for name, allowed in policies]
    baseline = results[0]
    for result in results[1:]:
        result["improved_requests"] = sorted(set(baseline["failures"]) - set(result["failures"]))
        result["regressed_requests"] = sorted(set(result["failures"]) - set(baseline["failures"]))
        result["amount_safe_to_pay_differences"] = sorted(
            request_id for request_id in result["rows"]
            if result["rows"][request_id]["amount_safe_to_pay"] != baseline["rows"][request_id]["amount_safe_to_pay"]
        )
        result["earliest_date_differences"] = sorted(
            request_id for request_id in result["rows"]
            if result["rows"][request_id]["earliest_date_for_full_payment"] != baseline["rows"][request_id]["earliest_date_for_full_payment"]
        )
    return {
        "rule": "Among supported candidate future-flow sets, select the deterministic candidate with the lowest 90-day minimum balance; lifecycle and duplicate exclusion remain higher precedence.",
        "candidate_sources": ["current exact-description recurrence", "existing variable-category fallback recurrence", "same-day explicit-vs-projected salary duplicate suppression"],
        "policies": results,
        "focus_requests": {request_id: {result["name"]: result["selections"][request_id] for result in results} for request_id in ("request_04", "request_10")},
    }


def write(report_data: dict[str, object]) -> None:
    evaluation = ROOT / "evaluation"
    (evaluation / "s16_conservative_ambiguity_resolution.json").write_text(json.dumps(report_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# S16 conservative ambiguity resolution",
        "",
        "Evaluation-only. Solved rows are used only to measure outputs after candidate construction; no expected value selects a candidate.",
        "",
        f"Rule: {report_data['rule']}",
        "",
        "## Policy comparison",
        "",
        "| Policy | Exact rows | Differing fields | Amount fields changed | Earliest-date fields changed | Improved | Regressed |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for result in report_data["policies"]:
        lines.append(
            f"| `{result['name']}` | {result['exact_rows']}/25 | {result['differing_fields']} | {len(result.get('amount_safe_to_pay_differences', []))} | {len(result.get('earliest_date_differences', []))} | {', '.join(result.get('improved_requests', [])) or 'none'} | {', '.join(result.get('regressed_requests', [])) or 'none'} |"
        )
    lines += [
        "",
        "## Supported candidate boundary",
        "",
        "- Baseline candidates are the current production exact-description recurrence streams.",
        "- Expense alternatives reuse the existing history-supported variable-category fallback experiment only for variable categories; they do not create events without a cadence-supported history.",
        "- Income alternatives suppress only a literal same-day explicit/projection salary collision; they do not collapse independent salary streams.",
        "- Cancelled, failed, unrealized, and non-cash records are excluded before comparison.",
        "- The resolver cannot synthesize or duplicate an event, and ties are broken by candidate name after the numeric trough.",
        "",
        "## User 04 / User 10",
        "",
        "User 04 dining and User 10 salary are the focus cases. Their per-policy candidate scores and changed event signatures are in `s16_conservative_ambiguity_resolution.json`; the evidence does not contain a source/account/stream identifier that distinguishes the competing supported streams.",
        "",
        "| Request | Policy | Selected candidate | Baseline trough | Selected trough | Candidate interpretation |",
        "|---|---|---|---:|---:|---|",
    ]
    for request_id in ("request_04", "request_10"):
        for policy_name, selection in report_data["focus_requests"][request_id].items():
            scores = selection["scores"]
            selected = selection["selected"]
            lines.append(
                f"| `{request_id}` | `{policy_name}` | `{selected}` | {scores['baseline']['minimum_balance']} | {scores[selected]['minimum_balance']} | supported alternatives only; changed flows={len(selection['changed_from_baseline']) + len(selection['removed_from_baseline'])} |"
            )
    lines += [
        "",
        "- User 04: the exact-description construction keeps separate dining labels; the variable-category construction merges the supported dining history. The category alternative has a higher trough for this request, so the conservative resolver retains the baseline. This is not evidence that either partition is the solved semantics.",
        "- User 10: the exact-description construction contains rotating salary labels and the variable-category alternative changes only expenses. The candidate set does not contain an authoritative payroll stream identifier, so the conservative resolver cannot justify collapsing independent income streams; the income-only candidate is the same forecast for this request because the explicit salary collision is not the unresolved identity conflict.",
        "- In both cases, the safer tie-break is applied only after evidence-supported candidates exist. It does not turn a category or label into a source identity and does not manufacture income or expenses.",
        "",
        "## Decision",
        "",
        "No production promotion is implied by this artifact. A candidate is eligible for promotion only if it is contract-supported and improves S16 without regressions or unsupported event synthesis.",
        "",
    ]
    (evaluation / "s16_conservative_ambiguity_resolution.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    data = report()
    write(data)
    for item in data["policies"]:
        print(item["name"], f"exact={item['exact_rows']}/25", f"fields={item['differing_fields']}", "improved=", item.get("improved_requests", []), "regressed=", item.get("regressed_requests", []))
