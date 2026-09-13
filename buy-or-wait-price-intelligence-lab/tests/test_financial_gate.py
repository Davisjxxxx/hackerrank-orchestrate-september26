from datetime import datetime, timezone
from decimal import Decimal

from price_intel.engine import PriceIntelligenceEngine
from price_intel.models import CombinedDecision, FinancialCoverageState, FinancialSafetyResult, FinancialState, ProductIdentity, PriceDecision, PriceMetrics, TimingRecommendation


PRODUCT = ProductIdentity("Example", gtin="036000291452")


def price_decision(recommendation=TimingRecommendation.BUY_NOW):
    metrics = PriceMetrics(Decimal("100"), Decimal("80"), Decimal("90"), Decimal("85"), Decimal("10"), Decimal("85"), Decimal("15"), 10, 12, 2, 2)
    return PriceDecision(recommendation, metrics, Decimal("0.8"), ("TEST_PRICE_SIGNAL",))


def test_safe_later_vetoes_a_great_price():
    result = FinancialSafetyResult(
        financial_state=FinancialState.SAFE_LATER,
        safe_amount_today=Decimal("0"),
        earliest_safe_full_payment_date=datetime(2026, 10, 1, tzinfo=timezone.utc),
        minimum_balance=Decimal("500"),
        recommended_payment_method="cash_after_payday",
        financial_reason_codes=("PENDING_OBLIGATION",),
        financial_coverage_state=FinancialCoverageState.FULL,
    )
    combined = PriceIntelligenceEngine().combine(result, price_decision())
    assert combined.decision == CombinedDecision.FINANCIALLY_WAIT
    assert "FINANCIAL_CAPACITY_AVAILABLE_LATER" in combined.reason_codes


def test_safe_with_plan_remains_conservative_and_does_not_buy_now():
    combined = PriceIntelligenceEngine().combine(
        FinancialSafetyResult(financial_state=FinancialState.SAFE_WITH_PLAN, payment_plan={"installments": 4}),
        price_decision(),
    )
    assert combined.decision == CombinedDecision.FINANCIALLY_WAIT
    assert "SAFE_WITH_PLAN_REQUIRES_CONSERVATIVE_REVIEW" in combined.reason_codes


def test_not_affordable_is_not_recommended_even_when_price_is_low():
    combined = PriceIntelligenceEngine().combine(FinancialState.NOT_AFFORDABLE, price_decision())
    assert combined.decision == CombinedDecision.NOT_RECOMMENDED
    assert combined.decision == CombinedDecision.DO_NOT_BUY
    assert "FINANCIAL_SAFETY_VETO" in combined.reason_codes
