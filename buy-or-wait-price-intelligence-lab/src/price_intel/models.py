from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Mapping, Any


class Condition(StrEnum):
    UNKNOWN = "unknown"
    NEW = "new"
    REFURBISHED = "refurbished"
    USED = "used"
    OPEN_BOX = "open_box"


class ObservationTrust(StrEnum):
    """Trust boundary for price evidence.

    User-captured offers are private evidence until an explicit, audited
    corroboration policy promotes them. They are never global market history
    merely because their shape is valid.
    """

    TRUSTED_PROVIDER = "trusted_provider"
    USER_PRIVATE = "user_private"
    CORROBORATED = "corroborated"
    QUARANTINED = "quarantined"


class Urgency(StrEnum):
    IMMEDIATE = "immediate"
    NEEDED_SOON = "needed_soon"
    FLEXIBLE = "flexible"
    DISCRETIONARY = "discretionary"


class TimingRecommendation(StrEnum):
    BUY_NOW = "buy_now"
    HOLD_FOR_BETTER_PRICE = "hold_for_better_price"
    SET_PRICE_WATCH = "set_price_watch"
    BUY_USED_OR_REFURBISHED = "buy_used_or_refurbished"
    INSUFFICIENT_DATA = "insufficient_data"


class FinancialState(StrEnum):
    SAFE_NOW = "safe_now"
    SAFE_WITH_PLAN = "safe_with_plan"
    SAFE_LATER = "safe_later"
    NOT_AFFORDABLE = "not_affordable"


class FinancialCoverageState(StrEnum):
    FULL = "full"
    PARTIAL = "partial"
    STALE = "stale"
    UNKNOWN = "unknown"


class CombinedDecision(StrEnum):
    BUY_NOW = "buy_now"
    HOLD_FOR_PRICE = "hold_for_price"
    SET_PRICE_WATCH = "set_price_watch"
    CONSIDER_USED_OR_REFURBISHED = "consider_used_or_refurbished"
    FINANCIALLY_WAIT = "financially_wait"
    NOT_RECOMMENDED = "not_recommended"
    # Backwards-compatible name for the supplied prototype vocabulary.
    DO_NOT_BUY = "not_recommended"
    NEEDS_CONFIRMATION = "needs_confirmation"


@dataclass(frozen=True)
class ProductIdentity:
    title: str
    brand: str | None = None
    model: str | None = None
    gtin: str | None = None
    mpn: str | None = None
    asin: str | None = None
    variant: Mapping[str, str] = field(default_factory=dict)
    identity_confidence: Decimal = Decimal("1")
    identity_evidence: tuple[str, ...] = ()
    source_provenance: str | None = None

    def __post_init__(self) -> None:
        confidence = _decimal(self.identity_confidence, "identity_confidence")
        if confidence < 0 or confidence > 1:
            raise ValueError("identity_confidence must be within [0, 1]")
        object.__setattr__(self, "identity_confidence", confidence)


@dataclass(frozen=True)
class PurchaseIntent:
    product: ProductIdentity
    urgency: Urgency = Urgency.FLEXIBLE
    max_wait_days: int = 60
    accepted_conditions: frozenset[Condition] = frozenset({Condition.NEW})
    minimum_savings_dollars: Decimal = Decimal("25")
    minimum_savings_fraction: Decimal = Decimal("0.08")


@dataclass(frozen=True)
class PriceObservation:
    provider: str
    observed_at: datetime
    price: Decimal
    shipping: Decimal = Decimal("0")
    condition: Condition = Condition.NEW
    available: bool = True
    seller: str | None = None
    source_url: str | None = None
    product_match_confidence: Decimal = Decimal("1")
    deal_signal: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)
    currency: str = "USD"
    retailer: str | None = None
    captured: bool = False
    provenance: str | None = None
    freshness: str = "unknown"
    trust: ObservationTrust = ObservationTrust.TRUSTED_PROVIDER

    def __post_init__(self) -> None:
        price = _money(self.price, "price")
        shipping = _money(self.shipping, "shipping")
        confidence = _decimal(self.product_match_confidence, "product_match_confidence")
        if confidence < 0 or confidence > 1:
            raise ValueError("product_match_confidence must be within [0, 1]")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must include a timezone")
        if not isinstance(self.condition, Condition):
            raise ValueError("condition must be a supported Condition")
        if not isinstance(self.trust, ObservationTrust):
            try:
                trust = ObservationTrust(str(self.trust))
            except ValueError as exc:
                raise ValueError("trust must be a supported ObservationTrust") from exc
            object.__setattr__(self, "trust", trust)
        if self.captured and self.trust == ObservationTrust.TRUSTED_PROVIDER:
            object.__setattr__(self, "trust", ObservationTrust.USER_PRIVATE)
        currency = str(self.currency).strip().upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ValueError("currency must be a 3-letter ISO-style code")
        object.__setattr__(self, "price", price)
        object.__setattr__(self, "shipping", shipping)
        object.__setattr__(self, "product_match_confidence", confidence)
        object.__setattr__(self, "currency", currency)

    @property
    def landed_price(self) -> Decimal:
        return self.price + self.shipping


@dataclass(frozen=True)
class PriceMetrics:
    current_best_price: Decimal | None
    historical_low: Decimal | None
    historical_median: Decimal | None
    historical_p25: Decimal | None
    current_percentile: Decimal | None
    target_buy_price: Decimal | None
    expected_savings: Decimal | None
    estimated_wait_days: int | None
    history_count: int
    history_span_days: int
    deal_episode_count: int
    currency: str | None = None
    source_count: int = 0
    independent_source_count: int = 0
    coverage_state: str = "unknown"
    winsorized_target: Decimal | None = None


@dataclass(frozen=True)
class PriceDecision:
    recommendation: TimingRecommendation
    metrics: PriceMetrics
    confidence: Decimal
    reason_codes: tuple[str, ...]
    selected_offer: PriceObservation | None = None
    alternative_offer: PriceObservation | None = None
    evidence: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CombinedRecommendation:
    decision: CombinedDecision
    financial_state: FinancialState
    price_decision: PriceDecision
    reason_codes: tuple[str, ...]
    financial_result: "FinancialSafetyResult | None" = None


@dataclass(frozen=True)
class FinancialSafetyResult:
    """Typed seam for the authoritative financial-safety engine."""

    financial_state: FinancialState
    safe_amount_today: Decimal | None = None
    earliest_safe_full_payment_date: datetime | None = None
    minimum_balance: Decimal | None = None
    recommended_payment_method: str | None = None
    payment_plan: Mapping[str, Any] = field(default_factory=dict)
    financial_reason_codes: tuple[str, ...] = ()
    financial_data_as_of: datetime | None = None
    financial_coverage_state: FinancialCoverageState = FinancialCoverageState.UNKNOWN

    def __post_init__(self) -> None:
        for field_name in ("safe_amount_today", "minimum_balance"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _money(value, field_name))
        for field_name in ("earliest_safe_full_payment_date", "financial_data_as_of"):
            value = getattr(self, field_name)
            if value is not None and (value.tzinfo is None or value.utcoffset() is None):
                raise ValueError(f"{field_name} must include a timezone")
        if not isinstance(self.financial_state, FinancialState):
            raise ValueError("financial_state must be a FinancialState")
        if not isinstance(self.financial_coverage_state, FinancialCoverageState):
            raise ValueError("financial_coverage_state must be a FinancialCoverageState")
        if not isinstance(self.payment_plan, Mapping):
            raise ValueError("payment_plan must be a mapping")
        if any(not isinstance(code, str) for code in self.financial_reason_codes):
            raise ValueError("financial_reason_codes must contain strings")
        object.__setattr__(self, "financial_reason_codes", tuple(self.financial_reason_codes))


def _decimal(value: object, field_name: str) -> Decimal:
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"{field_name} must be a finite Decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{field_name} must be finite")
    return result


def _money(value: object, field_name: str) -> Decimal:
    result = _decimal(value, field_name)
    if result < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return result


def validate_non_negative_money(value: object, field_name: str) -> Decimal:
    """Validate a finite, non-negative monetary value at any domain boundary."""

    return _money(value, field_name)
