"""Second independent adversarial sweep for remediated Buy or Wait RC.

These tests intentionally target seams not covered by the first independent suite.
They encode fail-closed, deterministic, and domain-boundary expectations.
"""
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from price_intel.api.app import AppState, create_app
from price_intel.connectors.base import ConnectorNormalizationError
from price_intel.connectors.live import ShopSavvyAdapter, _shop_savvy_offer_rows
from price_intel.demo import DEMO_NOW, DEMO_PRODUCT
from price_intel.engine import PriceIntelligenceEngine
from price_intel.models import (
    CombinedDecision,
    Condition,
    FinancialCoverageState,
    FinancialSafetyResult,
    FinancialState,
    ObservationTrust,
    PriceDecision,
    PriceMetrics,
    PriceObservation,
    ProductIdentity,
    PurchaseIntent,
    TimingRecommendation,
    Urgency,
)
from price_intel.resolver import canonical_product_id
from price_intel.watch import InMemoryWatchRepository, WatchService


def obs(*, currency="USD", freshness="unknown", trust=ObservationTrust.TRUSTED_PROVIDER,
        provider="p", retailer="r", url="https://store/item", price="100", days=0):
    return PriceObservation(
        provider=provider,
        retailer=retailer,
        observed_at=DEMO_NOW - timedelta(days=days),
        price=Decimal(price),
        condition=Condition.NEW,
        source_url=url,
        currency=currency,
        freshness=freshness,
        trust=trust,
    )


def test_deduplication_must_not_collapse_distinct_currencies_or_depend_on_input_order():
    engine = PriceIntelligenceEngine()
    intent = PurchaseIntent(ProductIdentity("P"))
    usd = obs(currency="USD")
    eur = obs(currency="EUR")
    a = engine.evaluate(intent, [usd, eur], now=DEMO_NOW)
    b = engine.evaluate(intent, [eur, usd], now=DEMO_NOW)
    assert (a.recommendation, a.metrics.currency) == (b.recommendation, b.metrics.currency), (a, b)


def test_deduplication_must_not_let_stale_row_shadow_fresh_row_by_order():
    engine = PriceIntelligenceEngine()
    intent = PurchaseIntent(ProductIdentity("P"))
    stale = obs(freshness="stale")
    fresh = obs(freshness="fresh")
    a = engine.evaluate(intent, [stale, fresh], now=DEMO_NOW)
    b = engine.evaluate(intent, [fresh, stale], now=DEMO_NOW)
    assert (a.recommendation, a.metrics.current_best_price) == (b.recommendation, b.metrics.current_best_price), (a, b)


def test_single_currency_history_must_not_claim_mixed_currency_was_ignored():
    engine = PriceIntelligenceEngine()
    observations = [obs(url=f"u{i}", days=i * 5, price=str(100 + i)) for i in range(3)]
    decision = engine.evaluate(PurchaseIntent(ProductIdentity("P")), observations, now=DEMO_NOW)
    assert "MIXED_CURRENCY_IGNORED" not in decision.reason_codes
    assert decision.evidence.get("mixed_currency_code") is None


def test_equal_currency_counts_without_fx_context_must_not_buy_now_arbitrarily():
    engine = PriceIntelligenceEngine()
    observations = [
        obs(currency="USD", url="u1", price="100"),
        obs(currency="USD", url="u2", price="105", days=1),
        obs(currency="EUR", url="e1", price="50"),
        obs(currency="EUR", url="e2", price="55", days=1),
    ]
    decision = engine.evaluate(
        PurchaseIntent(ProductIdentity("P"), urgency=Urgency.IMMEDIATE),
        observations,
        now=DEMO_NOW,
    )
    assert decision.recommendation != TimingRecommendation.BUY_NOW, decision


def test_quarantined_observations_must_never_drive_engine_decisions_even_if_called_directly():
    engine = PriceIntelligenceEngine()
    observations = [
        obs(trust=ObservationTrust.QUARANTINED, url=f"q{i}", days=i * 4, price=str(100 + i))
        for i in range(12)
    ]
    decision = engine.evaluate(PurchaseIntent(ProductIdentity("P")), observations, now=DEMO_NOW)
    assert decision.recommendation == TimingRecommendation.INSUFFICIENT_DATA, decision


def test_unknown_provider_availability_value_must_fail_closed_not_become_trusted_in_stock():
    rows = _shop_savvy_offer_rows({
        "price": "10",
        "shipping": "0",
        "currency": "USD",
        "condition": "new",
        "availability": "banana",
        "timestamp": DEMO_NOW.isoformat(),
        "url": "https://shop/item",
    }, "shopsavvy")
    assert rows
    row = rows[0]
    assert (not row.available) or row.trust == ObservationTrust.QUARANTINED, row


def test_malformed_provider_currency_must_be_quarantined_or_dropped_not_escape_as_valueerror():
    try:
        rows = _shop_savvy_offer_rows({
            "price": "10",
            "shipping": "0",
            "currency": "US1",
            "condition": "new",
            "availability": "in_stock",
            "timestamp": DEMO_NOW.isoformat(),
        }, "shopsavvy")
    except Exception as exc:
        pytest.fail(f"provider normalization leaked {type(exc).__name__}: {exc}")
    assert not rows or all(r.trust == ObservationTrust.QUARANTINED or not r.available for r in rows)


def test_malformed_product_payload_must_raise_connector_normalization_error_not_attributeerror():
    class Bad(ShopSavvyAdapter):
        def __init__(self):
            super().__init__("x")
        def _get(self, path, params):
            return {"product": "not-an-object"}
    with pytest.raises(ConnectorNormalizationError):
        Bad().resolve_product(__import__('price_intel.intake', fromlist=['NormalizedProductInput']).NormalizedProductInput(mode=__import__('price_intel.intake', fromlist=['ProductIntakeMode']).ProductIntakeMode.TEXT_SEARCH, query_text="phone"))


def test_provider_product_search_must_preserve_multiple_candidates_for_ambiguity_gate():
    class Many(ShopSavvyAdapter):
        def __init__(self):
            super().__init__("x")
        def _get(self, path, params):
            return {"products": [
                {"name": "Phone 128GB", "brand": "B", "model": "M", "identifiers": {"gtin": "036000291452"}, "specifications": {"storage": "128GB"}},
                {"name": "Phone 1TB", "brand": "B", "model": "M", "identifiers": {"gtin": "012345678905"}, "specifications": {"storage": "1TB"}},
            ]}
    from price_intel.intake import NormalizedProductInput, ProductIntakeMode
    candidates = Many().resolve_product(NormalizedProductInput(mode=ProductIntakeMode.TEXT_SEARCH, query_text="Phone"))
    assert len(candidates) == 2, candidates


def test_financial_earliest_date_consistency_must_use_financial_as_of_not_wall_clock_now():
    metrics = PriceMetrics(Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("10"), Decimal("0"), None, 10, 100, 2)
    price = PriceDecision(TimingRecommendation.BUY_NOW, metrics, Decimal("0.8"), ("TEST",))
    financial = FinancialSafetyResult(
        financial_state=FinancialState.SAFE_NOW,
        safe_amount_today=Decimal("100"),
        earliest_safe_full_payment_date=datetime(2025, 1, 2, tzinfo=timezone.utc),
        financial_data_as_of=datetime(2025, 1, 1, tzinfo=timezone.utc),
        financial_coverage_state=FinancialCoverageState.FULL,
    )
    combined = PriceIntelligenceEngine().combine(financial, price)
    assert combined.decision == CombinedDecision.FINANCIALLY_WAIT, combined


def test_watch_api_empty_accepted_conditions_must_be_422_not_internal_500():
    state = AppState()
    api = TestClient(create_app(state), raise_server_exceptions=False)
    pid = canonical_product_id(DEMO_PRODUCT)
    response = api.post(
        "/v1/watches",
        headers={"Authorization": "Bearer fixture:alice"},
        json={"product_id": pid, "target_price": "10", "max_wait_date": "2027-01-01", "accepted_conditions": []},
    )
    assert response.status_code == 422, response.text


def test_watch_service_target_price_must_be_finite_at_domain_boundary():
    service = WatchService(InMemoryWatchRepository())
    with pytest.raises(ValueError):
        service.create(
            user_id="u",
            product_id="p",
            product_title="P",
            target_price=Decimal("NaN"),
            max_wait_date=date(2027, 1, 1),
            accepted_conditions=frozenset({Condition.NEW}),
        )
