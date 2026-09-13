"""Metamorphic checks for the bounded phase-aware recurrence experiment."""
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "code"))
import main
import recurrence_policy_experiment as experiment


def event(event_id: str, when: date, description: str = "rotating label", *, category: str = "groceries", event_type: str = "expense", direction: str = "debit", status: str = "settled") -> main.CanonicalEvent:
    return main.CanonicalEvent(event_id, "synthetic", event_type, description, category, direction, Decimal("10"), "USD", when, when, status, "fixed", None)


def test_description_rotation_does_not_split_temporal_sequence():
    rows = [event("a", date(2026, 1, 1), "Neighbourhood grocer"), event("b", date(2026, 1, 8), "Bulk pantry shop"), event("c", date(2026, 1, 15), "Grocery delivery")]
    clusters = experiment.sequence_clusters(rows)
    assert [[item.event_id for item in cluster] for cluster in clusters] == [["a", "b", "c"]]


def test_category_collision_keeps_independent_phases_separate():
    rows = [event(str(i), date(2026, 1, 1) + main.timedelta(days=7 * i), "stream A") for i in range(3)]
    rows += [event(str(i + 3), date(2026, 1, 4) + main.timedelta(days=7 * i), "stream B") for i in range(3)]
    clusters = experiment.sequence_clusters(rows)
    assert {frozenset(item.event_id for item in cluster) for cluster in clusters} == {frozenset({"0", "1", "2"}), frozenset({"3", "4", "5"})}


def test_isolated_same_category_outlier_is_not_absorbed():
    rows = [event(str(i), date(2026, 1, 1) + main.timedelta(days=7 * i)) for i in range(3)]
    rows.append(event("outlier", date(2026, 1, 3)))
    clusters = experiment.sequence_clusters(rows)
    assert any({item.event_id for item in cluster} == {"0", "1", "2"} for cluster in clusters)
    assert all("outlier" not in {item.event_id for item in cluster} for cluster in clusters)


def test_input_order_does_not_change_sequence_membership():
    rows = [event(str(i), date(2026, 1, 1) + main.timedelta(days=7 * i)) for i in range(3)]
    forward = {frozenset(item.event_id for item in cluster) for cluster in experiment.sequence_clusters(rows)}
    reversed_rows = list(reversed(rows))
    backward = {frozenset(item.event_id for item in cluster) for cluster in experiment.sequence_clusters(reversed_rows)}
    assert forward == backward


def test_cancelled_row_cannot_create_or_extend_recurrence():
    rows = [event("a", date(2026, 1, 1)), event("b", date(2026, 1, 8)), event("cancelled", date(2026, 1, 15), status="cancelled")]
    valid = [item for item in rows if item.status not in {"failed", "cancelled", "unrealized"}]
    assert experiment.sequence_clusters(valid) == []


def test_stale_phase_is_not_projected_by_active_policy():
    rows = [event("a", date(2026, 1, 1)), event("b", date(2026, 1, 8)), event("c", date(2026, 1, 15))]
    canonical = experiment.ExperimentCanonicalizer(rows, [], main.ExchangeRateAdapter(), recurrence_policy="I_phase_aware_active")
    profile = main.Profile("synthetic", "USD", Decimal("1000"), Decimal("100"), frozenset(), frozenset(), frozenset(), frozenset({"full_payment"}), None)
    request = main.Request("synthetic-request", "synthetic", date(2026, 3, 15), "purchase", Decimal("10"), date(2026, 3, 20), False, "")
    assert not any(item.projected for item in canonical.for_request(request, profile, main.WindowPolicy.DAYS_0_THROUGH_89))


def test_multiple_monthly_income_phases_remain_independent():
    rows = []
    for i, month in enumerate((1, 2, 3)):
        rows.append(event(f"a{i}", date(2026, month, 15), "primary", category="salary", event_type="income", direction="credit"))
        rows.append(event(f"b{i}", date(2026, month, 20), "secondary", category="salary", event_type="income", direction="credit"))
    clusters = experiment.sequence_clusters(rows)
    assert {frozenset(item.event_id for item in cluster) for cluster in clusters} == {frozenset({"a0", "a1", "a2"}), frozenset({"b0", "b1", "b2"})}


def test_rotating_description_biweekly_sequence_is_preserved():
    rows = [event("a", date(2026, 1, 1), "Coffee shop", category="dining"), event("b", date(2026, 1, 15), "Takeaway order", category="dining"), event("c", date(2026, 1, 29), "Family dinner", category="dining")]
    clusters = experiment.sequence_clusters(rows)
    assert len(clusters) == 1
    assert {item.event_id for item in clusters[0]} == {"a", "b", "c"}
