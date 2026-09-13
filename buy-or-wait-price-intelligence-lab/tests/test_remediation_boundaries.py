from datetime import timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from price_intel.api.app import AppState, create_app
from price_intel.demo import DEMO_NOW, DEMO_PRODUCT
from price_intel.models import Condition, FinancialCoverageState, FinancialSafetyResult, FinancialState, ObservationTrust, PriceObservation
from price_intel.observation_store import InMemoryObservationStore
from price_intel.resolver import canonical_product_id


def test_private_capture_is_visible_only_to_its_subject_and_never_global():
    store = InMemoryObservationStore()
    private = PriceObservation("capture", DEMO_NOW, Decimal("1"), condition=Condition.NEW, captured=True, trust=ObservationTrust.USER_PRIVATE)
    provider = PriceObservation("provider", DEMO_NOW, Decimal("90"), condition=Condition.NEW)
    store.append("p", DEMO_PRODUCT, [private, provider], ingested_at=DEMO_NOW, user_id="alice")
    assert [row.provider for row in store.observations("p")] == ["provider"]
    assert {row.provider for row in store.observations("p", user_id="alice")} == {"capture", "provider"}
    assert [row.provider for row in store.observations("p", user_id="bob")] == ["provider"]


def test_fixture_bearer_subject_owns_decision_reads():
    state = AppState()
    api = TestClient(create_app(state))
    product_id = canonical_product_id(DEMO_PRODUCT)
    headers = {"Authorization": "Bearer fixture:alice"}
    response = api.post(
        f"/v1/products/{product_id}/evaluate",
        headers=headers,
        json={"financial_state": "not_affordable", "as_of": DEMO_NOW.isoformat()},
    )
    decision_id = response.json()["decision_id"]
    assert api.get(f"/v1/decisions/{decision_id}").status_code == 401
    assert api.get(f"/v1/decisions/{decision_id}", headers={"Authorization": "Bearer fixture:bob"}).status_code == 404
    assert api.get(f"/v1/decisions/{decision_id}", headers=headers).status_code == 200


def test_safe_now_with_non_full_coverage_cannot_buy():
    from price_intel.engine import PriceIntelligenceEngine
    from price_intel.models import PriceDecision, PriceMetrics, TimingRecommendation

    price = PriceDecision(
        TimingRecommendation.BUY_NOW,
        PriceMetrics(Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("100"), Decimal("10"), Decimal("0"), None, 1, 1, 0),
        Decimal("0.5"),
        ("TEST",),
    )
    result = FinancialSafetyResult(FinancialState.SAFE_NOW, financial_coverage_state=FinancialCoverageState.STALE)
    assert PriceIntelligenceEngine().combine(result, price).decision.value == "needs_confirmation"


def test_watch_api_rejects_nonfinite_target_price_as_422():
    state = AppState()
    api = TestClient(create_app(state), raise_server_exceptions=False)
    product_id = canonical_product_id(DEMO_PRODUCT)
    for value in ("NaN", "Infinity", "-Infinity"):
        response = api.post(
            "/v1/watches",
            headers={"Authorization": "Bearer fixture:alice"},
            json={
                "product_id": product_id,
                "target_price": value,
                "max_wait_date": "2027-01-01",
                "accepted_conditions": ["new"],
            },
        )
        assert response.status_code == 422, (value, response.text)


def test_watch_domain_rejects_unknown_condition():
    from datetime import date

    from price_intel.watch import WatchService

    with pytest.raises(ValueError):
        WatchService().create(
            user_id="alice",
            product_id="p",
            product_title="P",
            target_price=Decimal("10"),
            max_wait_date=date(2027, 1, 1),
            accepted_conditions=frozenset({Condition.UNKNOWN}),
        )


def test_future_dated_financial_payload_requires_confirmation_at_evaluation_time():
    from price_intel.engine import PriceIntelligenceEngine
    from price_intel.models import PriceDecision, PriceMetrics, TimingRecommendation

    price = PriceDecision(
        TimingRecommendation.BUY_NOW,
        PriceMetrics(Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("0"), None, 1, 1, 0),
        Decimal("0.5"),
        ("TEST",),
    )
    result = FinancialSafetyResult(
        FinancialState.SAFE_NOW,
        safe_amount_today=Decimal("100"),
        financial_coverage_state=FinancialCoverageState.FULL,
        financial_data_as_of=DEMO_NOW + timedelta(days=1),
    )
    assert PriceIntelligenceEngine().combine(result, price, as_of=DEMO_NOW).decision.value == "needs_confirmation"
