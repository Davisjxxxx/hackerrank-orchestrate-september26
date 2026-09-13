"""Focused deterministic checks for the Buy or Wait? contract.

The tests use only participant-facing data and small synthetic records.  They
are deliberately independent of the solved output values so they also protect
the implementation when the target request set changes.
"""
from datetime import date
from decimal import Decimal
from pathlib import Path
import csv
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "code"))
import main


def _fixture():
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    canonical = main.Canonicalizer(events, main.read_csv("messages.csv"), main.ExchangeRateAdapter())
    return profiles, requests, canonical


def test_observed_domains_and_inventory_are_clean():
    inventory = main.DatasetInventory().build()
    cross = inventory["cross_file"]
    assert cross["direction_exact_domain"]
    assert cross["non_cash"]["supported_semantics"]
    assert cross["linked_event_id"]["cycle_count"] == 0
    assert cross["linkage"]["requests_without_options"] == []
    assert cross["linkage"]["events_without_profiles"] == []
    assert cross["linkage"]["messages_to_missing_events"] == []
    assert cross["linkage"]["images_to_missing_events"] == []


def test_profile_priorities_are_loaded_and_protect_change_selection():
    profiles = main.ProfileAdapter().load()
    assert profiles["user_01"].priorities == frozenset({"education", "debt_repayment"})


def test_decimal_fx_and_month_end_clamp():
    assert main.dec("1,234.50") == Decimal("1234.50")
    assert main.add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)
    assert main.add_months(date(2023, 1, 31), 1) == date(2023, 2, 28)
    fx = main.ExchangeRateAdapter()
    assert fx.convert(Decimal("10"), "USD", "EUR", date(2024, 1, 15)) > 0


def test_non_cash_does_not_enter_flows_and_pending_credit_does_not_increase_cash():
    profiles, requests, canonical = _fixture()
    assert any(event.direction == "non_cash" for event in canonical.events)
    request = next(x for x in requests if x.request_id == "request_22")
    profile = profiles[request.user_id]
    events = canonical.for_request(request, profile, main.WindowPolicy.DAYS_0_THROUGH_89)
    simulator = main.Simulator(canonical, main.WindowPolicy.DAYS_0_THROUGH_89)
    flows = simulator.flows(request, profile, events)
    assert all(event.direction != "non_cash" for event in events)
    assert all(event.status != "pending" or event.direction != "credit" for event in events)
    assert all(isinstance(value, Decimal) for value in flows.values())


def test_terminal_payroll_does_not_project_prior_salary_stream():
    profiles, requests, canonical = _fixture()
    request = next(x for x in requests if x.request_id == "request_05")
    events = canonical.for_request(request, profiles[request.user_id], main.WindowPolicy.DAYS_0_THROUGH_89)
    assert not any(event.projected and event.category == "salary" for event in events)


def test_unresolved_amounts_are_not_serialized_as_zero():
    events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    image_events = [event for event in events if event.provenance.startswith("ocr:")]
    assert image_events
    assert all(event.amount is not None for event in image_events)
    by_id = {event.event_id: event.amount for event in image_events}
    assert by_id["event_3051"] == Decimal("1995.00")
    assert by_id["event_3231"] == Decimal("8528")
    assert by_id["event_6033"] == Decimal("79679.26")
    assert main.dec_or_none("") is None


def test_unresolved_future_debit_blocks_safe_plans_without_becoming_zero():
    profiles, requests, canonical = _fixture()
    request = next(x for x in requests if x.request_id == "request_01")
    profile = profiles[request.user_id]
    unknown = main.CanonicalEvent(
        "unknown-future-debit", request.user_id, "expense", "unresolved bill", "rent", "debit",
        None, profile.home_currency, request.request_date + main.timedelta(days=3),
        request.request_date + main.timedelta(days=3), "scheduled", "fixed", None,
    )
    events = canonical.for_request(request, profile, main.WindowPolicy.DAYS_0_THROUGH_89) + [unknown]
    planner = main.Planner(canonical, main.PaymentOptionAdapter().load(), main.WindowPolicy.DAYS_0_THROUGH_89)
    assert planner.safe_amount(request, profile, events) == Decimal(0)
    assert planner.oracle.run(request, profile, events, [(request.request_date, request.requested_amount)])[0] is False


def test_oracle_and_production_differential_on_all_solved_requests():
    profiles, requests, canonical = _fixture()
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    oracle = main.Simulator(canonical, policy)
    production = main.ProductionSimulator(canonical, policy)
    for request in requests:
        profile = profiles[request.user_id]
        events = canonical.for_request(request, profile, policy)
        payments = [(request.request_date, Decimal(0))]
        assert oracle.run(request, profile, events, payments) == production.run(request, profile, events, payments)


def test_safe_amount_is_closed_form_and_bounded():
    profiles, requests, canonical = _fixture()
    policy = main.WindowPolicy.DAYS_0_THROUGH_89
    planner = main.Planner(canonical, main.PaymentOptionAdapter().load(), policy)
    for request in requests:
        profile = profiles[request.user_id]
        events = canonical.for_request(request, profile, policy)
        safe = planner.safe_amount(request, profile, events)
        assert Decimal(0) <= safe <= request.requested_amount
        decision, _ = planner.decide(request, profile)
        assert decision.amount_safe == safe


def test_installments_echo_supplied_option_schedule():
    profiles, requests, canonical = _fixture()
    options = main.PaymentOptionAdapter().load()
    for request in requests:
        for option in options.get(request.request_id, []):
            schedule = main.Planner.installment_schedule(option) if option.payment_frequency_days else []
            if schedule:
                assert len(schedule) == option.number_of_payments
                assert schedule[0][0] == option.first_payment_date
                assert schedule[0][2] == option.payment_amount_text
                assert all(schedule[i][0] - schedule[i - 1][0] == main.timedelta(days=option.payment_frequency_days) for i in range(1, len(schedule)))


def test_output_schema_and_plan_bounds():
    rows = main.execute(False, main.WindowPolicy.DAYS_0_THROUGH_89)
    assert len(rows) == 25
    assert all(list(row) == main.OUTPUT_COLUMNS for row in rows)
    for row in rows:
        assert row["spending_changes_needed"] == "none" or len(row["spending_changes_needed"].split("|")) <= 3
        assert row["recommended_payment_method"] == "not_recommended" or row["payment_plan"] != "none"
