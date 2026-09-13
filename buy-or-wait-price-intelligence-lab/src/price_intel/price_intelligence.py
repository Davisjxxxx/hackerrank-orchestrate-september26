"""Machine-readable price intelligence boundary for product integration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from typing import Iterable, Sequence

from .engine import PriceIntelligenceEngine
from .models import Condition, PriceDecision, PriceObservation, ProductIdentity, PurchaseIntent, TimingRecommendation
from .observation_store import CanonicalPriceObservation, ObservationStore


@dataclass(frozen=True)
class PriceIntelligenceRecord:
    product_id: str
    current_best_price: Decimal | None
    current_offer_count: int
    historical_low: Decimal | None
    historical_high: Decimal | None
    historical_average: Decimal | None
    observation_count: int
    history_window_days: int
    price_percentile: Decimal | None
    price_trend: str
    used_best_price: Decimal | None
    refurbished_best_price: Decimal | None
    price_history_status: str
    price_signal: str
    confidence: Decimal
    provenance: tuple[str, ...]
    observation_ids: tuple[str, ...] = ()
    selected_offer: PriceObservation | None = None
    alternative_offer: PriceObservation | None = None

    def __post_init__(self) -> None:
        if self.price_history_status not in {"SUFFICIENT", "INSUFFICIENT", "UNAVAILABLE"}:
            raise ValueError("invalid price_history_status")
        if self.price_signal not in {"STRONG_BUY", "BUY", "NEUTRAL", "WAIT", "STRONG_WAIT", "UNKNOWN"}:
            raise ValueError("invalid price_signal")
        if not Decimal("0") <= self.confidence <= Decimal("1"):
            raise ValueError("confidence must be in [0, 1]")

    def to_dict(self) -> dict[str, object]:
        def money(value: Decimal | None) -> str | None:
            return str(value) if value is not None else None
        return {
            "product_id": self.product_id,
            "current_best_price": money(self.current_best_price),
            "current_offer_count": self.current_offer_count,
            "historical_low": money(self.historical_low),
            "historical_high": money(self.historical_high),
            "historical_average": money(self.historical_average),
            "observation_count": self.observation_count,
            "history_window_days": self.history_window_days,
            "price_percentile": money(self.price_percentile),
            "price_trend": self.price_trend,
            "used_best_price": money(self.used_best_price),
            "refurbished_best_price": money(self.refurbished_best_price),
            "price_history_status": self.price_history_status,
            "price_signal": self.price_signal,
            "confidence": str(self.confidence),
            "provenance": list(self.provenance),
            "observation_ids": list(self.observation_ids),
        }


class PriceIntelligenceService:
    """Resolves stored observations into a stable record without fabricating history."""

    def __init__(self, store: ObservationStore, engine: PriceIntelligenceEngine | None = None):
        self.store = store
        self.engine = engine or PriceIntelligenceEngine()

    def record_observation(self, product_id: str, product: ProductIdentity,
                           observation: PriceObservation, *, user_id: str | None = None,
                           ingested_at: datetime | None = None) -> CanonicalPriceObservation | None:
        append = getattr(self.store, "append", None)
        if append is None:
            raise TypeError("observation store must implement append")
        return next(iter(append(product_id, product, (observation,), user_id=user_id,
                                ingested_at=ingested_at)), None)

    def evaluate(self, product_id: str, product: ProductIdentity, intent: PurchaseIntent,
                 *, now: datetime | None = None, user_id: str | None = None) -> PriceIntelligenceRecord:
        now = now or datetime.now(timezone.utc)
        records = tuple(self.store.list(product_id, user_id=user_id))
        observations = tuple(record.observation for record in records)
        decision = self.engine.evaluate(intent, observations, now=now)
        history = [o for o in observations if o.condition == Condition.NEW and o.available and o.freshness != "invalid"]
        current = [o for o in observations if o.available and o.freshness not in {"stale", "invalid"}
                   and 0 <= (now - _aware(o.observed_at)).days <= self.engine.policy.current_offer_max_age_days]
        history_prices = [o.landed_price for o in history]
        high = max(history_prices) if history_prices else None
        average = sum(history_prices, Decimal("0")) / Decimal(len(history_prices)) if history_prices else None
        alternatives = [o for o in current if o.condition == Condition.USED]
        refurbs = [o for o in current if o.condition == Condition.REFURBISHED]
        status = "SUFFICIENT" if decision.metrics.coverage_state == "adequate" else (
            "UNAVAILABLE" if any(code in decision.reason_codes for code in {"NO_FRESH_CURRENT_OFFER", "NO_ACCEPTABLE_OFFERS"}) else "INSUFFICIENT"
        )
        signal = _signal(decision.recommendation, status)
        percentile = decision.metrics.current_percentile
        trend = _trend(decision.metrics.current_best_price, decision.metrics.historical_median)
        observation_ids = tuple(_observation_id(product_id, record.observation) for record in records)
        provenance = tuple(sorted({o.provenance or o.provider for o in observations}))
        return PriceIntelligenceRecord(
            product_id=product_id,
            current_best_price=decision.metrics.current_best_price,
            current_offer_count=len(current),
            historical_low=decision.metrics.historical_low,
            historical_high=high,
            historical_average=average,
            observation_count=len(history),
            history_window_days=decision.metrics.history_span_days,
            price_percentile=percentile,
            price_trend=trend,
            used_best_price=min((o.landed_price for o in alternatives), default=None),
            refurbished_best_price=min((o.landed_price for o in refurbs), default=None),
            price_history_status=status,
            price_signal=signal,
            confidence=decision.confidence,
            provenance=provenance,
            observation_ids=observation_ids,
            selected_offer=decision.selected_offer,
            alternative_offer=decision.alternative_offer,
        )


def _signal(recommendation: TimingRecommendation, status: str) -> str:
    if status == "UNAVAILABLE":
        return "UNKNOWN"
    return {
        TimingRecommendation.BUY_NOW: "STRONG_BUY",
        TimingRecommendation.HOLD_FOR_BETTER_PRICE: "STRONG_WAIT",
        TimingRecommendation.SET_PRICE_WATCH: "WAIT",
        TimingRecommendation.BUY_USED_OR_REFURBISHED: "BUY",
        TimingRecommendation.INSUFFICIENT_DATA: "UNKNOWN",
    }[recommendation]


def _trend(current: Decimal | None, median: Decimal | None) -> str:
    if current is None or median is None:
        return "unknown"
    if current < median * Decimal("0.97"):
        return "falling"
    if current > median * Decimal("1.03"):
        return "rising"
    return "stable"


def _observation_id(product_id: str, observation: PriceObservation) -> str:
    value = {
        "product_id": product_id, "provider": observation.provider,
        "retailer": observation.retailer, "source_url": observation.source_url,
        "observed_at": _aware(observation.observed_at).isoformat(),
        "condition": observation.condition.value, "price": str(observation.landed_price),
        "currency": observation.currency,
    }
    return "obs_" + hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:24]


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamps must include a timezone")
    return value
