from datetime import datetime, timedelta, timezone
from decimal import Decimal

from price_intel.engine import PriceIntelligenceEngine
from price_intel.models import Condition, PriceObservation, ProductIdentity, PurchaseIntent, TimingRecommendation, Urgency


NOW = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)
PRODUCT = ProductIdentity("Example Camera", brand="Example", model="C1", gtin="036000291452")


def offer(days_ago: int, price: str, *, provider="fixture", retailer=None, condition=Condition.NEW, shipping="0", available=True, currency="USD", deal=False, url=None):
    return PriceObservation(
        provider=provider,
        retailer=retailer,
        observed_at=NOW - timedelta(days=days_ago),
        price=Decimal(price),
        shipping=Decimal(shipping),
        condition=condition,
        available=available,
        currency=currency,
        deal_signal=deal,
        source_url=url,
    )


def long_history(values, step=20):
    return [offer((index + 1) * step, str(value)) for index, value in enumerate(values)]


def test_shipping_can_reverse_the_nominal_low():
    observations = long_history([100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155])
    observations.append(offer(0, "90", retailer="cheap", shipping="30"))
    observations.append(offer(0, "100", retailer="fair", shipping="0"))
    decision = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    assert decision.metrics.current_best_price == Decimal("100")
    assert decision.selected_offer is not None and decision.selected_offer.retailer == "fair"


def test_condition_history_is_never_mixed():
    observations = long_history([800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910])
    observations.extend([offer(0, "900", condition=Condition.NEW), offer(0, "500", condition=Condition.USED)])
    decision = PriceIntelligenceEngine().evaluate(
        PurchaseIntent(PRODUCT, accepted_conditions=frozenset({Condition.NEW, Condition.USED})), observations, now=NOW
    )
    assert decision.metrics.historical_low == Decimal("800")
    assert decision.selected_offer is not None and decision.selected_offer.condition == Condition.NEW


def test_out_of_stock_and_stale_listing_cannot_be_current():
    observations = [offer(0, "50", available=False), offer(8, "40")]
    decision = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    assert decision.recommendation == TimingRecommendation.INSUFFICIENT_DATA
    assert decision.reason_codes == ("NO_FRESH_CURRENT_OFFER",)


def test_duplicate_aggregator_rows_do_not_create_fake_deal_episodes():
    observations = long_history([800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020])
    observations.append(offer(2, "700", provider="aggregator", retailer="Store"))
    observations.append(offer(0, "900"))
    once = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    twice = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations + [observations[-2]], now=NOW)
    assert twice.metrics.deal_episode_count == once.metrics.deal_episode_count


def test_separate_deal_episodes_are_counted_by_date_gap():
    observations = long_history([800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020])
    observations.extend([offer(120, "700", deal=True), offer(80, "700", deal=True), offer(0, "900")])
    decision = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    assert decision.metrics.deal_episode_count >= 2


def test_recurrence_estimate_uses_inter_episode_intervals_and_needs_two_episodes():
    engine = PriceIntelligenceEngine()
    two_episodes = [offer(120, "700", deal=True), offer(118, "700", deal=True), offer(40, "700", deal=True)]
    one_episode = [offer(2, "700", deal=True), offer(0, "700", deal=True)]
    assert engine._estimated_wait_days(two_episodes, threshold=Decimal("700")) == 80
    assert engine._estimated_wait_days(one_episode, threshold=Decimal("700")) is None


def test_mixed_currency_is_never_compared_as_one_distribution():
    observations = long_history([900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900])
    observations.append(offer(0, "900", currency="USD"))
    observations.append(offer(0, "100", currency="EUR"))
    decision = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    assert decision.metrics.currency == "USD"
    assert "MIXED_CURRENCY_IGNORED" in decision.reason_codes


def test_urgent_purchase_can_buy_with_sparse_history_but_says_why():
    decision = PriceIntelligenceEngine().evaluate(
        PurchaseIntent(PRODUCT, urgency=Urgency.IMMEDIATE),
        [offer(0, "900"), offer(10, "920")],
        now=NOW,
    )
    assert decision.recommendation == TimingRecommendation.BUY_NOW
    assert "URGENCY_OVERRIDES_WAIT" in decision.reason_codes
