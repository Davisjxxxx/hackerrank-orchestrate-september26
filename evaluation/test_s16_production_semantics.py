"""Focused tests for the sample-grounded S16 production promotion."""
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "code"))

import main


def salary(event_id: str, when: date, *, projected: bool = False, status: str = "settled") -> main.CanonicalEvent:
    return main.CanonicalEvent(
        event_id,
        "synthetic",
        "income",
        "rotating payroll label",
        "salary",
        "credit",
        Decimal("100"),
        "USD",
        when,
        when,
        status,
        "fixed",
        None,
        projected=projected,
        provenance="structured",
    )


def test_robust_cadence_requires_repeated_median_support():
    rows = [
        salary("a", date(2026, 1, 1)),
        salary("b", date(2026, 1, 8)),
        salary("c", date(2026, 1, 28)),
        salary("d", date(2026, 2, 4)),
    ]
    assert main.cadence(rows) == ("gap", 7)


def test_confirmed_salary_same_date_is_counted_once_without_merging_dates():
    rows = [
        salary("jan", date(2026, 1, 15)),
        salary("feb", date(2026, 2, 15)),
        salary("mar", date(2026, 3, 15)),
        salary("confirmed", date(2026, 4, 15), status="scheduled"),
    ]
    canonical = main.Canonicalizer(rows, [], main.ExchangeRateAdapter())
    request = main.Request("synthetic", "synthetic", date(2026, 4, 1), "purchase", Decimal("10"), date(2026, 4, 30), False, "")
    profile = main.Profile("synthetic", "USD", Decimal("1000"), Decimal("100"), frozenset(), frozenset(), frozenset(), frozenset({"full_payment"}), None)
    events = canonical.for_request(request, profile, main.WindowPolicy.DAYS_0_THROUGH_89)
    same_day = [event for event in events if event.category == "salary" and (event.settlement_date or event.event_date) == date(2026, 4, 15)]
    assert len(same_day) == 1
    assert same_day[0].event_id == "confirmed"


def test_later_supported_salary_occurrence_remains_independent():
    rows = [
        salary("jan", date(2026, 1, 15)),
        salary("feb", date(2026, 2, 15)),
        salary("mar", date(2026, 3, 15)),
        salary("confirmed", date(2026, 4, 15), status="scheduled"),
    ]
    canonical = main.Canonicalizer(rows, [], main.ExchangeRateAdapter())
    request = main.Request("synthetic", "synthetic", date(2026, 4, 1), "purchase", Decimal("10"), date(2026, 6, 30), False, "")
    profile = main.Profile("synthetic", "USD", Decimal("1000"), Decimal("100"), frozenset(), frozenset(), frozenset(), frozenset({"full_payment"}), None)
    events = canonical.for_request(request, profile, main.WindowPolicy.DAYS_0_THROUGH_89)
    future_days = [(event.settlement_date or event.event_date) for event in events if event.category == "salary" and (event.settlement_date or event.event_date) >= date(2026, 4, 15)]
    assert future_days.count(date(2026, 4, 15)) == 1
    assert date(2026, 5, 15) in future_days
