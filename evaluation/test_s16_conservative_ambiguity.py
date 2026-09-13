"""Metamorphic tests for the evaluation-only conservative S16 resolver."""
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "code"))
import main
import s16_conservative_ambiguity_resolution as resolver


def event(
    event_id: str,
    when: date,
    *,
    direction: str = "debit",
    category: str = "dining",
    amount: str = "10",
    projected: bool = False,
    status: str = "settled",
    description: str = "rotating label",
) -> main.CanonicalEvent:
    return main.CanonicalEvent(
        event_id,
        "synthetic",
        "income" if direction == "credit" else "expense",
        description,
        category,
        direction,
        Decimal(amount),
        "USD",
        when,
        when,
        status,
        "fixed",
        None,
        projected=projected,
        provenance="synthetic",
    )


def context() -> tuple[main.Canonicalizer, main.Request, main.Profile]:
    canonical = main.Canonicalizer([], [], main.ExchangeRateAdapter())
    request = main.Request("r", "synthetic", date(2026, 1, 1), "purchase", Decimal("10"), date(2026, 1, 30), False, "")
    profile = main.Profile("synthetic", "USD", Decimal("1000"), Decimal("100"), frozenset(), frozenset(), frozenset(), frozenset({"full_payment"}), None)
    return canonical, request, profile


def test_uncertain_income_does_not_select_more_future_income():
    canonical, request, profile = context()
    explicit = event("salary-explicit", date(2026, 1, 10), direction="credit", category="salary", amount="100")
    duplicate = event("salary-history@2026-01-10", date(2026, 1, 10), direction="credit", category="salary", amount="100", projected=True)
    candidates = {"baseline": (explicit, duplicate), "income_conservative": resolver.suppress_literal_duplicate_projection((explicit, duplicate), {"salary"})}
    selected, chosen, scores = resolver.choose_conservative(canonical, request, profile, candidates, main.WindowPolicy.DAYS_0_THROUGH_89, ("baseline", "income_conservative"))
    assert selected == "income_conservative"
    assert len([item for item in chosen if item.category == "salary"]) == 1
    assert Decimal(scores[selected]["minimum_balance"]) <= Decimal(scores["baseline"]["minimum_balance"])


def test_uncertain_expense_does_not_select_more_affordable_forecast():
    canonical, request, profile = context()
    base = event("dining-a", date(2026, 1, 10), amount="10", projected=True)
    supported_more_conservative = event("dining-b", date(2026, 1, 10), amount="25", projected=True)
    candidates = {"baseline": (base,), "expense_conservative": (supported_more_conservative,)}
    selected, _, scores = resolver.choose_conservative(canonical, request, profile, candidates, main.WindowPolicy.DAYS_0_THROUGH_89, ("baseline", "expense_conservative"))
    assert selected == "expense_conservative"
    assert Decimal(scores[selected]["minimum_balance"]) < Decimal(scores["baseline"]["minimum_balance"])


def test_literal_duplicate_exclusion_keeps_confirmed_salary_once():
    explicit = event("confirmed", date(2026, 1, 10), direction="credit", category="salary", projected=False)
    projected = event("confirmed@2026-01-10", date(2026, 1, 10), direction="credit", category="salary", projected=True)
    result = resolver.suppress_literal_duplicate_projection((projected, explicit), {"salary"})
    assert [item.event_id for item in result] == ["confirmed"]


def test_cancelled_and_failed_rows_cannot_become_supported_candidates():
    rows = [
        event("cancelled", date(2026, 1, 10), status="cancelled"),
        event("failed", date(2026, 1, 11), status="failed"),
        event("valid", date(2026, 1, 12)),
    ]
    assert [item.event_id for item in resolver.eligible(rows)] == ["valid"]


def test_amendment_wins_before_conservative_candidate_selection():
    old = event("old", date(2026, 1, 10), amount="20")
    amended = event("amended", date(2026, 1, 10), amount="5")
    # An explicit, already-canonical amendment is the only supported row for
    # the economic occurrence; the resolver must not add the superseded row.
    result = resolver.eligible((amended,))
    assert [item.event_id for item in result] == ["amended"]
    assert all(item.event_id != old.event_id for item in result)


def test_no_invention_only_existing_event_ids_survive():
    source = event("source", date(2026, 1, 10), amount="20")
    candidates = resolver.candidate_sets((source,), (source,))
    source_ids = {source.event_id}
    assert all(event.event_id in source_ids for rows in candidates.values() for event in rows)


def test_description_permutation_and_input_order_are_invariant():
    left = event("left", date(2026, 1, 10), description="Payroll A", direction="credit", category="salary")
    right = event("right", date(2026, 1, 17), description="Payroll B", direction="credit", category="salary")
    first = resolver.stable_events((left, right))
    second = resolver.stable_events((right, left))
    renamed = resolver.stable_events((event("left", date(2026, 1, 10), description="Payroll X", direction="credit", category="salary"), event("right", date(2026, 1, 17), description="Payroll Y", direction="credit", category="salary")))
    assert [item.event_id for item in first] == [item.event_id for item in second]
    assert [(item.event_id, item.event_date) for item in first] == [(item.event_id, item.event_date) for item in renamed]
