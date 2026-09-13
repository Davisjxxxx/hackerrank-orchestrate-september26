"""Independent adversarial regression suite for Buy or Wait? Price Intelligence RC.

These tests encode safety/correctness expectations discovered during external red-team review.
They are intentionally expected to FAIL against commit b081c490df5222314b2c815dea12e41438207b99.
"""
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import os

import pytest
from fastapi.testclient import TestClient

from price_intel.api.app import AppState, create_app
from price_intel.connectors.live import ShopSavvyAdapter, _condition, _shop_savvy_offer_rows, build_provider_adapters
from price_intel.demo import DEMO_NOW, DEMO_PRODUCT
from price_intel.engine import EnginePolicy, PriceIntelligenceEngine
from price_intel.intake import ProductIntakeMode, ProductIntakeRequest, normalize_intake, normalize_product_url
from price_intel.models import (
    Condition, FinancialCoverageState, FinancialSafetyResult, FinancialState,
    PriceObservation, ProductIdentity, PurchaseIntent
)
from price_intel.observation_store import InMemoryObservationStore
from price_intel.resolver import ProductIdentityResolver, IdentityResolutionState, canonical_product_id
from price_intel.watch import InMemoryWatchRepository, NoopNotificationGateway, WatchService


def _client():
    state = AppState()
    return state, TestClient(create_app(state), raise_server_exceptions=False)


def test_evaluate_must_not_default_financial_state_to_safe_now():
    _, api = _client()
    pid = canonical_product_id(DEMO_PRODUCT)
    response = api.post(f"/v1/products/{pid}/evaluate", json={})
    assert response.status_code in {400, 401, 403, 422, 503}, response.text


def test_untrusted_client_must_not_be_able_to_self_assert_safe_now():
    _, api = _client()
    pid = canonical_product_id(DEMO_PRODUCT)
    response = api.post(f"/v1/products/{pid}/evaluate", json={
        "financial_state": "safe_now",
        "safe_amount_today": "0",
        "financial_coverage_state": "stale",
        "as_of": DEMO_NOW.isoformat(),
    })
    body = response.json()
    assert body.get("combined_decision") not in {"buy_now", "hold_for_price", "set_price_watch", "consider_used_or_refurbished"}, body


def test_user_captured_price_must_not_poison_shared_canonical_history():
    _, api = _client()
    pid = canonical_product_id(DEMO_PRODUCT)
    before = api.post(f"/v1/products/{pid}/evaluate", json={"financial_state":"safe_now", "as_of":DEMO_NOW.isoformat()}).json()["combined_decision"]
    api.post("/v1/intake/barcode", json={
        "barcode": DEMO_PRODUCT.gtin,
        "observed_price": "1",
        "currency": "USD",
        "observed_at": DEMO_NOW.isoformat(),
        "retailer_hint": "untrusted-user",
    })
    after = api.post(f"/v1/products/{pid}/evaluate", json={"financial_state":"safe_now", "as_of":DEMO_NOW.isoformat()}).json()["combined_decision"]
    assert after == before, (before, after)


def test_decisions_containing_financial_data_must_not_be_publicly_readable():
    _, api = _client()
    pid = canonical_product_id(DEMO_PRODUCT)
    decision = api.post(f"/v1/products/{pid}/evaluate", json={
        "financial_state":"safe_now",
        "safe_amount_today":"123.45",
        "financial_reason_codes":["PRIVATE_REASON"],
        "as_of":DEMO_NOW.isoformat(),
    }).json()
    response = api.get(f"/v1/decisions/{decision['decision_id']}")
    assert response.status_code in {401,403,404}, response.text


def test_amazon_asin_extraction_requires_real_amazon_host():
    _, host, asin = normalize_product_url("https://notamazon.com/dp/B0CHX3TW6K")
    assert asin is None, (host, asin)


def test_invalid_watch_product_must_fail_instead_of_falling_back_to_first_product():
    _, api = _client()
    response = api.post("/v1/watches", headers={"X-User-Id":"u"}, json={
        "target_price":"10", "product_id":"does-not-exist", "max_wait_date":"2027-01-01"
    })
    assert response.status_code == 404, response.text


def test_unknown_provider_condition_must_not_default_to_new():
    assert _condition("damaged_return") != Condition.NEW


def test_shopsavvy_gtin_offer_lookup_must_use_barcode_not_asin_parameter():
    class Capture(ShopSavvyAdapter):
        def __init__(self):
            super().__init__("test")
            self.calls=[]
        def _get(self,path,params):
            self.calls.append((path,dict(params)))
            return {"offers":[]}
    adapter=Capture()
    adapter.current_offers(ProductIdentity("GTIN-only", gtin=DEMO_PRODUCT.gtin))
    _, params = adapter.calls[-1]
    assert params.get("barcode") == DEMO_PRODUCT.gtin and "asin" not in params, params


def test_price_observation_must_reject_negative_shipping_at_domain_boundary():
    with pytest.raises((TypeError, ValueError)):
        PriceObservation("provider", DEMO_NOW, Decimal("10"), shipping=Decimal("-100"))


def test_nonfinite_provider_money_must_fail_closed_before_engine_math():
    with pytest.raises((TypeError, ValueError)):
        PriceObservation("provider", DEMO_NOW, Decimal("NaN"))


def test_conflicting_variants_with_same_gtin_must_require_confirmation():
    intake=normalize_intake(ProductIntakeRequest(ProductIntakeMode.BARCODE, barcode=DEMO_PRODUCT.gtin))
    a=ProductIdentity("Phone 128",gtin=DEMO_PRODUCT.gtin,variant={"storage":"128GB"})
    b=ProductIdentity("Phone 1TB",gtin=DEMO_PRODUCT.gtin,variant={"storage":"1TB"})
    result=ProductIdentityResolver().resolve(intake,[a,b])
    assert result.state == IdentityResolutionState.NEEDS_CONFIRMATION, result


def test_currency_selection_must_be_order_independent_and_use_actual_counts():
    product=ProductIdentity("P")
    intent=PurchaseIntent(product)
    usd=[PriceObservation("s",DEMO_NOW-timedelta(days=i*5),Decimal("100")+i,currency="USD",source_url=f"u{i}") for i in range(10)]
    eur=[PriceObservation("e",DEMO_NOW-timedelta(days=i*5),Decimal("50")+i,currency="EUR",source_url=f"e{i}") for i in range(2)]
    engine=PriceIntelligenceEngine()
    a=engine.evaluate(intent, usd+eur, now=DEMO_NOW)
    b=engine.evaluate(intent, eur+usd, now=DEMO_NOW)
    assert (a.recommendation, a.metrics.currency, a.metrics.history_count) == (b.recommendation,b.metrics.currency,b.metrics.history_count)
    assert a.metrics.currency == "USD"


def test_explicit_stale_freshness_must_not_be_eligible_as_current_offer():
    p=ProductIdentity("P")
    obs=[PriceObservation("s",DEMO_NOW-timedelta(days=i*4),Decimal(100+i),source_url=str(i)) for i in range(10)]
    obs.append(PriceObservation("s",DEMO_NOW,Decimal("1"),freshness="stale",source_url="stale-current"))
    result=PriceIntelligenceEngine().evaluate(PurchaseIntent(p),obs,now=DEMO_NOW)
    assert result.selected_offer is None or result.selected_offer.freshness != "stale"


def test_naive_as_of_must_be_rejected_as_422_not_crash_500():
    _, api = _client()
    pid=canonical_product_id(DEMO_PRODUCT)
    response=api.post(f"/v1/products/{pid}/evaluate",json={"financial_state":"safe_now","as_of":"2026-09-12T12:00:00"})
    assert response.status_code == 422, response.text


def test_watch_must_not_persist_observations_it_rejects_for_source_condition_availability():
    store=InMemoryObservationStore()
    service=WatchService(InMemoryWatchRepository(), observation_store=store)
    product=ProductIdentity("P")
    watch=service.create(user_id="u",product_id="p",product_title="P",target_price=Decimal("100"),max_wait_date=date(2027,1,1),accepted_conditions=frozenset({Condition.NEW}),source_restrictions=frozenset({"trusted"}))
    poison=PriceObservation("evil",DEMO_NOW,Decimal("1"),condition=Condition.USED,available=False)
    service.evaluate(watch,[poison],now=DEMO_NOW,product=product)
    assert store.observations("p") == ()


def test_watch_notifications_need_idempotency_across_refreshes():
    notifier=NoopNotificationGateway(); service=WatchService(InMemoryWatchRepository(),notifier,approach_days=7)
    watch=service.create(user_id="u",product_id="p",product_title="P",target_price=Decimal("100"),max_wait_date=date(2026,9,15),accepted_conditions=frozenset({Condition.NEW}))
    obs=[PriceObservation("s",DEMO_NOW,Decimal("90"))]
    w1,e1=service.evaluate(watch,obs,now=DEMO_NOW)
    _,e2=service.evaluate(w1,obs,now=DEMO_NOW+timedelta(hours=1))
    assert not ({e.trigger for e in e1} & {e.trigger for e in e2}), (e1,e2)


def test_same_strong_identifier_must_produce_stable_canonical_id_as_metadata_enriches():
    x=DEMO_PRODUCT.gtin
    base=canonical_product_id(ProductIdentity("A",gtin=x))
    enriched=canonical_product_id(ProductIdentity("A",gtin=x,asin="B0CHX3TW6K",brand="Brand",model="M"))
    assert base == enriched, (base,enriched)


def test_shopsavvy_partial_offer_must_not_assume_new_in_stock_usd_free_shipping_now():
    row=_shop_savvy_offer_rows({"price":"10"},"shopsavvy")[0]
    assert not row.available or row.condition != Condition.NEW or row.currency == "UNKNOWN", row


def test_ebay_configuration_checks_real_two_environment_variables(monkeypatch):
    monkeypatch.setenv("EBAY_CLIENT_ID","x")
    monkeypatch.setenv("EBAY_CLIENT_SECRET","y")
    ebay=next(a for a in build_provider_adapters() if getattr(a,"name","")=="ebay")
    assert ebay.status.configured is True, ebay.status
