from datetime import datetime, timedelta, timezone
from decimal import Decimal

from price_intel.engine import PriceIntelligenceEngine
from price_intel.models import (
    CombinedDecision,
    Condition,
    FinancialState,
    PriceObservation,
    ProductIdentity,
    PurchaseIntent,
    TimingRecommendation,
    Urgency,
)

NOW = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)
PRODUCT = ProductIdentity(title="Example OLED TV", brand="Example", model="X1", gtin="000111222333")


def obs(days_ago: int, price: str, condition=Condition.NEW, deal=False):
    return PriceObservation(
        provider="fixture",
        observed_at=NOW - timedelta(days=days_ago),
        price=Decimal(price),
        condition=condition,
        deal_signal=deal,
    )


def history(prices):
    return [obs((i + 1) * 10, str(p)) for i, p in enumerate(prices)]


def test_hold_when_current_price_is_high_and_deals_recur():
    observations = history([700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920])
    observations.append(obs(0, "920"))
    intent = PurchaseIntent(PRODUCT, urgency=Urgency.FLEXIBLE, max_wait_days=90)
    decision = PriceIntelligenceEngine().evaluate(intent, observations, now=NOW)
    assert decision.recommendation == TimingRecommendation.HOLD_FOR_BETTER_PRICE
    assert decision.metrics.expected_savings > 0


def test_buy_now_when_price_is_near_historical_low():
    observations = history([700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920])
    observations.append(obs(0, "705"))
    intent = PurchaseIntent(PRODUCT, urgency=Urgency.FLEXIBLE)
    decision = PriceIntelligenceEngine().evaluate(intent, observations, now=NOW)
    assert decision.recommendation == TimingRecommendation.BUY_NOW


def test_immediate_need_overrides_price_wait_signal():
    observations = history([700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920])
    observations.append(obs(0, "920"))
    intent = PurchaseIntent(PRODUCT, urgency=Urgency.IMMEDIATE)
    decision = PriceIntelligenceEngine().evaluate(intent, observations, now=NOW)
    assert decision.recommendation == TimingRecommendation.BUY_NOW
    assert "URGENCY_OVERRIDES_WAIT" in decision.reason_codes


def test_used_or_refurbished_option_is_condition_separated():
    observations = history([800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910])
    observations.extend([obs(0, "900", Condition.NEW), obs(0, "650", Condition.REFURBISHED)])
    intent = PurchaseIntent(
        PRODUCT,
        urgency=Urgency.FLEXIBLE,
        accepted_conditions=frozenset({Condition.NEW, Condition.REFURBISHED}),
    )
    decision = PriceIntelligenceEngine().evaluate(intent, observations, now=NOW)
    assert decision.recommendation == TimingRecommendation.BUY_USED_OR_REFURBISHED
    assert decision.alternative_offer.condition == Condition.REFURBISHED


def test_financial_safety_has_veto_authority():
    observations = history([700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920])
    observations.append(obs(0, "700"))
    engine = PriceIntelligenceEngine()
    price_decision = engine.evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    combined = engine.combine(FinancialState.NOT_AFFORDABLE, price_decision)
    assert combined.decision == CombinedDecision.DO_NOT_BUY
    assert "FINANCIAL_SAFETY_VETO" in combined.reason_codes


def test_sparse_history_returns_watch_for_nonurgent_item():
    observations = [obs(0, "500"), obs(10, "510"), obs(20, "490")]
    decision = PriceIntelligenceEngine().evaluate(PurchaseIntent(PRODUCT), observations, now=NOW)
    assert decision.recommendation == TimingRecommendation.SET_PRICE_WATCH
