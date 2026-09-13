"""Metamorphic tests for the S16 future-flow collision experiment."""
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "code"))
import main
from s16_future_semantics_experiment import suppress_same_day_duplicate_projection


def event(event_id: str, when: date, description: str, *, category: str = "salary", event_type: str = "income", direction: str = "credit", projected: bool = False, provenance: str = "structured", status: str = "settled") -> main.CanonicalEvent:
    return main.CanonicalEvent(event_id, "synthetic", event_type, description, category, direction, Decimal("100"), "USD", when, when, status, "fixed", None, projected=projected, source_event_id="source" if projected else None, provenance=provenance)


def test_confirmed_salary_duplicate_suppression_is_description_invariant():
    explicit = event("confirmed", date(2026, 4, 15), "confirmed payroll", status="scheduled")
    projected = event("historical@2026-04-15", date(2026, 4, 15), "rotating payroll label", projected=True, provenance="recurrence:max_last_3", status="scheduled")
    kept = suppress_same_day_duplicate_projection([projected, explicit], {"salary"})
    assert [row.event_id for row in kept] == ["confirmed"]
    renamed = suppress_same_day_duplicate_projection([projected, event("confirmed", date(2026, 4, 15), "different employer wording", status="scheduled")], {"salary"})
    assert [row.event_id for row in renamed] == ["confirmed"]


def test_independent_salary_streams_remain_distinct():
    rows = [event("primary", date(2026, 4, 15), "primary payroll", status="scheduled"), event("secondary", date(2026, 4, 20), "secondary payroll", status="scheduled")]
    kept = suppress_same_day_duplicate_projection(rows, {"salary"})
    assert {row.event_id for row in kept} == {"primary", "secondary"}


def test_future_expense_collision_rule_does_not_merge_opposite_direction_or_category():
    explicit = event("debit-confirmed", date(2026, 4, 15), "scheduled bill", category="utilities", event_type="expense", direction="debit", status="scheduled")
    projected_same = event("debit-projected", date(2026, 4, 15), "rotating bill", category="utilities", event_type="expense", direction="debit", projected=True, provenance="recurrence:max_last_3", status="scheduled")
    refund = event("refund", date(2026, 4, 15), "refund", category="utilities", event_type="refund", direction="credit", status="scheduled")
    kept = suppress_same_day_duplicate_projection([refund, projected_same, explicit])
    assert [row.event_id for row in kept] == ["debit-confirmed", "refund"]


def test_collision_selection_is_input_order_invariant():
    rows = [event("projected", date(2026, 4, 15), "future label", projected=True, provenance="recurrence:max_last_3", status="scheduled"), event("explicit", date(2026, 4, 15), "confirmed label", status="scheduled")]
    forward = [(row.event_id, row.provenance) for row in suppress_same_day_duplicate_projection(rows, {"salary"})]
    reverse = [(row.event_id, row.provenance) for row in suppress_same_day_duplicate_projection(list(reversed(rows)), {"salary"})]
    assert forward == reverse == [("explicit", "structured")]


def test_cancelled_future_representation_is_not_retained_or_resurrected():
    cancelled = event("cancelled", date(2026, 4, 15), "cancelled payroll", status="cancelled")
    projected = event("projected", date(2026, 4, 15), "projected payroll", projected=True, provenance="recurrence:max_last_3", status="scheduled")
    # The collision helper only consumes explicit accepted events.  A caller
    # must apply status/lifecycle filtering before invoking it.
    valid = [row for row in [cancelled, projected] if row.status not in {"failed", "cancelled", "unrealized"}]
    assert [row.event_id for row in suppress_same_day_duplicate_projection(valid, {"salary"})] == ["projected"]
