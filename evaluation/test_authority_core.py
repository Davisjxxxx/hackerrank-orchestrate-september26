"""Focused authority-first controls; independent of solved output values."""
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "code"))
import main
from authority_core import AuthorityCanonicalizer, CandidatePolicy, ControlState


def event(event_id, when, description="Recurring bill", *, category="utilities", direction="debit", amount="10", projected=False):
    return main.CanonicalEvent(event_id, "u", "expense", description, category, direction, Decimal(amount), "EUR", when, when, "scheduled" if projected else "settled", "fixed", None, projected=projected, source_event_id=None, provenance="test")


def resolver(rows, policy=CandidatePolicy.R1, messages=None):
    return AuthorityCanonicalizer(rows, messages or [], main.ExchangeRateAdapter(), policy)


def profile():
    return main.Profile("u", "EUR", Decimal("1000"), Decimal("100"), frozenset(), frozenset(), frozenset(), frozenset({"full_payment"}), None)


def request():
    return main.Request("r", "u", date(2026, 4, 1), "purchase", Decimal("10"), date(2026, 5, 1), False, "")


def test_description_rename_does_not_disable_supported_track():
    rows = [event("a", date(2026, 1, 1)), event("b", date(2026, 2, 1)), event("c", date(2026, 3, 1))]
    renamed = [event("a", date(2026, 1, 1), "A"), event("b", date(2026, 2, 1), "B"), event("c", date(2026, 3, 1), "C")]
    left = resolver(rows, CandidatePolicy.R2).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    right = resolver(renamed, CandidatePolicy.R2).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert any(e.projected for e in left)
    assert any(e.projected for e in right)
    checked = resolver(rows)
    checked.for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert checked.control_results["ambiguous_source_identity"] == ControlState.UNRESOLVED


def test_duplicate_insertion_is_idempotent():
    rows = [event("a", date(2026, 1, 1)), event("b", date(2026, 2, 1)), event("c", date(2026, 3, 1))]
    one = resolver(rows).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    two = resolver(rows + [event("duplicate", date(2026, 2, 1))]).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert [(e.event_date, e.amount) for e in one] == [(e.event_date, e.amount) for e in two]


def test_explicit_future_event_suppresses_same_date_projection():
    rows = [event("a", date(2026, 1, 1)), event("b", date(2026, 2, 1)), event("c", date(2026, 3, 1)), event("future", date(2026, 4, 1), "Different label", projected=False)]
    got = resolver(rows).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert sum((e.settlement_date or e.event_date) == date(2026, 4, 1) for e in got) == 1


def test_row_order_does_not_change_resolved_cash_events():
    rows = [event("a", date(2026, 1, 1)), event("b", date(2026, 2, 1)), event("c", date(2026, 3, 1))]
    left = resolver(rows, CandidatePolicy.R2).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    right = resolver(list(reversed(rows)), CandidatePolicy.R2).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert [(e.event_date, e.direction, e.amount) for e in left] == [(e.event_date, e.direction, e.amount) for e in right]


def test_independent_supported_tracks_remain_distinct():
    rows = [event(f"a{i}", date(2026, i, 1), "A", amount="10") for i in (1, 2, 3)] + [event(f"b{i}", date(2026, i, 15), "B", amount="20") for i in (1, 2, 3)]
    got = resolver(rows).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    projected = [e for e in got if e.projected]
    assert {e.source_event_id for e in projected} == {"a3", "b3"}


def test_salary_is_counted_once_on_explicit_settlement_date():
    rows = [main.CanonicalEvent(f"s{i}", "u", "income", "Payroll", "salary", "credit", Decimal("100"), "EUR", date(2026, i, 15), date(2026, i, 15), "settled", "fixed", None) for i in (1, 2, 3)]
    rows.append(main.CanonicalEvent("confirmed", "u", "income", "Different payroll label", "salary", "credit", Decimal("100"), "EUR", date(2026, 4, 15), date(2026, 4, 15), "scheduled", "fixed", None))
    got = resolver(rows).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert sum((e.settlement_date or e.event_date) == date(2026, 4, 15) for e in got) == 1


def test_terminal_salary_is_conditional_to_message_evidence():
    rows = [main.CanonicalEvent(f"s{i}", "u", "income", "Payroll", "salary", "credit", Decimal("100"), "EUR", date(2026, i, 15), date(2026, i, 15), "settled", "fixed", None) for i in (1, 2, 3)]
    messages = [{"message_id": "m", "user_id": "u", "related_event_id": "", "source_type": "employer", "message_text": "Your employment has ended."}]
    got = resolver(rows, messages=messages).for_request(request(), profile(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert not any(e.projected and e.category == "salary" for e in got)
