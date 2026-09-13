from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from collections import Counter
from typing import Iterable

from .models import (
    CombinedDecision,
    CombinedRecommendation,
    Condition,
    FinancialCoverageState,
    FinancialSafetyResult,
    FinancialState,
    ObservationTrust,
    PriceDecision,
    PriceMetrics,
    PriceObservation,
    PurchaseIntent,
    TimingRecommendation,
    Urgency,
)
from .statistics import empirical_percentile_rank, distinct_source_count, percentile, winsorize


@dataclass(frozen=True)
class EnginePolicy:
    lookback_days: int = 365
    current_offer_max_age_days: int = 3
    minimum_history_points: int = 10
    minimum_history_span_days: int = 30
    near_historical_low_fraction: Decimal = Decimal("0.03")
    deal_episode_gap_days: int = 4
    minimum_match_confidence: Decimal = Decimal("0.85")
    winsorization_lower_q: Decimal = Decimal("0.05")
    winsorization_upper_q: Decimal = Decimal("0.95")
    stale_history_days: int = 30


class PriceIntelligenceEngine:
    """Pure, provider-independent and Decimal-only price decision core."""

    def __init__(self, policy: EnginePolicy | None = None):
        self.policy = policy or EnginePolicy()

    def evaluate(
        self,
        intent: PurchaseIntent,
        observations: Iterable[PriceObservation],
        *,
        now: datetime | None = None,
    ) -> PriceDecision:
        now = now or datetime.now(timezone.utc)
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("now must include a timezone")
        eligible = self._deduplicate(
            o
            for o in observations
            if self._trust_eligible(o)
            and o.available
            and o.freshness != "invalid"
            and o.condition in intent.accepted_conditions
            and o.product_match_confidence >= self.policy.minimum_match_confidence
        )
        if not eligible:
            return self._insufficient("NO_ACCEPTABLE_OFFERS")

        currencies = [o.currency.upper() for o in eligible]
        currency_counts = Counter(currencies)
        distinct_currencies = frozenset(currency_counts)
        currency = self._dominant_currency(currency_counts)
        if len(distinct_currencies) > 1 and currency is None:
            return self._insufficient(
                "MIXED_CURRENCY_AMBIGUOUS",
                evidence={
                    "currencies": tuple(sorted(distinct_currencies)),
                    "currency_counts": dict(sorted(currency_counts.items())),
                    "mixed_currency_code": "MIXED_CURRENCY_AMBIGUOUS",
                },
            )
        currency_filtered = [o for o in eligible if o.currency.upper() == currency]
        mixed_currency_code = "MIXED_CURRENCY_IGNORED" if len(distinct_currencies) > 1 else None
        current = [
            o
            for o in currency_filtered
            if o.freshness not in {"stale", "invalid"}
            and 0 <= (now - self._aware(o.observed_at)).days <= self.policy.current_offer_max_age_days
        ]
        if not current:
            return self._insufficient("NO_FRESH_CURRENT_OFFER")

        # NEW is the anchor when present. Alternative conditions are compared
        # only after the anchor history has been evaluated.
        new_current = [o for o in current if o.condition == Condition.NEW]
        anchor_current = min(new_current or current, key=self._observation_sort_key)
        anchor_condition = anchor_current.condition
        history = [
            o
            for o in currency_filtered
            if o.condition == anchor_condition
            and 0 <= (now - self._aware(o.observed_at)).days <= self.policy.lookback_days
        ]
        prices = [o.landed_price for o in history]
        oldest = min((self._aware(o.observed_at) for o in history), default=now)
        span_days = max(0, (now - oldest).days)
        sources = {o.provider for o in history}
        independent_sources = distinct_source_count(
            [o.provider for o in history], [o.retailer for o in history]
        )
        base_evidence = {
            "currency": currency,
            "anchor_condition": anchor_condition.value,
            "current_observation": self._observation_evidence(anchor_current),
            "source_count": len(sources),
            "independent_source_count": independent_sources,
            "history_count": len(history),
            "history_span_days": span_days,
            "mixed_currency_code": mixed_currency_code,
        }

        if len(history) < self.policy.minimum_history_points or span_days < self.policy.minimum_history_span_days:
            metrics = self._metrics(
                anchor_current,
                prices,
                history_count=len(history),
                span_days=span_days,
                episodes=0,
                currency=currency,
                source_count=len(sources),
                independent_sources=independent_sources,
                coverage="sparse",
            )
            rec = TimingRecommendation.BUY_NOW if intent.urgency == Urgency.IMMEDIATE else TimingRecommendation.SET_PRICE_WATCH
            reasons = ["SPARSE_PRICE_HISTORY"]
            if mixed_currency_code:
                reasons.append(mixed_currency_code)
            reasons.append("URGENCY_OVERRIDES_WAIT" if rec == TimingRecommendation.BUY_NOW else "WATCH_UNTIL_HISTORY_IMPROVES")
            return PriceDecision(
                recommendation=rec,
                metrics=metrics,
                confidence=self._confidence(intent, history, span_days, 0, independent_sources),
                reason_codes=tuple(reasons),
                selected_offer=anchor_current,
                evidence=base_evidence,
            )

        hist_low = min(prices)
        median = percentile(prices, Decimal("0.5"))
        robust_prices = winsorize(
            prices,
            self.policy.winsorization_lower_q,
            self.policy.winsorization_upper_q,
        )
        robust_target = percentile(robust_prices, Decimal("0.25"))
        rank = empirical_percentile_rank(prices, anchor_current.landed_price)
        savings = max(Decimal("0"), anchor_current.landed_price - robust_target)
        episodes = self._count_deal_episodes(history, threshold=robust_target)
        estimated_wait = self._estimated_wait_days(history, threshold=robust_target)
        metrics = self._metrics(
            anchor_current,
            prices,
            history_count=len(history),
            span_days=span_days,
            episodes=episodes,
            currency=currency,
            source_count=len(sources),
            independent_sources=independent_sources,
            coverage="adequate",
            target=robust_target,
            expected_savings=savings,
            robust_target=robust_target,
            rank=rank,
            estimated_wait_days=estimated_wait,
        )
        base_evidence.update(
            {
                "historical_low": str(hist_low),
                "lowest_observed_price_in_covered_dataset": str(hist_low),
                "historical_low_claim_scope": "covered_dataset_only",
                "historical_median": str(median),
                "winsorized_target": str(robust_target),
                "target_buy_price": str(robust_target),
                "expected_savings": str(savings),
                "deal_episode_count": episodes,
                "estimated_wait_days": estimated_wait,
            }
        )

        alt = self._best_alternative(current, anchor_current)
        if alt is not None and intent.urgency != Urgency.IMMEDIATE:
            alt_savings = anchor_current.landed_price - alt.landed_price
            if self._material_savings(intent, anchor_current.landed_price, alt_savings):
                return PriceDecision(
                    TimingRecommendation.BUY_USED_OR_REFURBISHED,
                    metrics,
                    self._confidence(intent, history, span_days, episodes, independent_sources),
                    ("MATERIAL_ALT_CONDITION_SAVINGS",),
                    selected_offer=anchor_current,
                    alternative_offer=alt,
                    evidence=base_evidence,
                )

        near_low = anchor_current.landed_price <= hist_low * (Decimal("1") + self.policy.near_historical_low_fraction)
        attractive_quartile = anchor_current.landed_price <= robust_target or rank <= Decimal("25")
        if near_low or attractive_quartile:
            reasons = ["NEAR_HISTORICAL_LOW" if near_low else "LOW_PRICE_QUARTILE"]
            if mixed_currency_code:
                reasons.append(mixed_currency_code)
            return PriceDecision(
                TimingRecommendation.BUY_NOW,
                metrics,
                self._confidence(intent, history, span_days, episodes, independent_sources),
                tuple(reasons),
                selected_offer=anchor_current,
                evidence=base_evidence,
            )

        if intent.urgency == Urgency.IMMEDIATE:
            return PriceDecision(
                TimingRecommendation.BUY_NOW,
                metrics,
                Decimal("0.75"),
                ("URGENCY_OVERRIDES_WAIT", "PRICE_NOT_HISTORICALLY_ATTRACTIVE"),
                selected_offer=anchor_current,
                evidence=base_evidence,
            )

        material = self._material_savings(intent, anchor_current.landed_price, savings)
        wait_feasible = estimated_wait is not None and estimated_wait <= intent.max_wait_days
        if material and wait_feasible:
            return PriceDecision(
                TimingRecommendation.HOLD_FOR_BETTER_PRICE,
                metrics,
                self._confidence(intent, history, span_days, episodes, independent_sources),
                ("MATERIAL_EXPECTED_SAVINGS", "DEALS_RECUR_WITHIN_WAIT_WINDOW"),
                selected_offer=anchor_current,
                evidence=base_evidence,
            )
        if material:
            return PriceDecision(
                TimingRecommendation.SET_PRICE_WATCH,
                metrics,
                self._confidence(intent, history, span_days, episodes, independent_sources),
                ("MATERIAL_EXPECTED_SAVINGS", "WAIT_TIME_UNCERTAIN_OR_TOO_LONG"),
                selected_offer=anchor_current,
                evidence=base_evidence,
            )
        return PriceDecision(
            TimingRecommendation.BUY_NOW,
            metrics,
            self._confidence(intent, history, span_days, episodes, independent_sources),
            ("WAIT_SAVINGS_NOT_MATERIAL",),
            selected_offer=anchor_current,
            evidence=base_evidence,
        )

    def combine(
        self,
        financial_state: FinancialState | FinancialSafetyResult,
        price_decision: PriceDecision,
        *,
        as_of: datetime | None = None,
    ) -> CombinedRecommendation:
        result = financial_state if isinstance(financial_state, FinancialSafetyResult) else FinancialSafetyResult(financial_state)
        state = result.financial_state
        if state == FinancialState.NOT_AFFORDABLE:
            return CombinedRecommendation(CombinedDecision.NOT_RECOMMENDED, state, price_decision, ("FINANCIAL_SAFETY_VETO",), result)
        if state == FinancialState.SAFE_LATER:
            return CombinedRecommendation(CombinedDecision.FINANCIALLY_WAIT, state, price_decision, ("FINANCIAL_CAPACITY_AVAILABLE_LATER",), result)
        if state == FinancialState.SAFE_WITH_PLAN:
            return CombinedRecommendation(CombinedDecision.FINANCIALLY_WAIT, state, price_decision, ("SAFE_WITH_PLAN_REQUIRES_CONSERVATIVE_REVIEW",), result)

        if state == FinancialState.SAFE_NOW:
            if result.financial_coverage_state != FinancialCoverageState.FULL:
                return CombinedRecommendation(
                    CombinedDecision.NEEDS_CONFIRMATION,
                    state,
                    price_decision,
                    ("FINANCIAL_EVIDENCE_MISSING_OR_STALE",),
                    result,
                )
            if as_of is not None and result.financial_data_as_of is not None and result.financial_data_as_of > as_of:
                return CombinedRecommendation(
                    CombinedDecision.NEEDS_CONFIRMATION,
                    state,
                    price_decision,
                    ("FINANCIAL_DATA_FUTURE_DATED",),
                    result,
                )
            current_price = price_decision.metrics.current_best_price
            if result.safe_amount_today is not None and current_price is not None and result.safe_amount_today < current_price:
                return CombinedRecommendation(
                    CombinedDecision.NOT_RECOMMENDED,
                    FinancialState.NOT_AFFORDABLE,
                    price_decision,
                    ("FINANCIAL_DATA_CONTRADICTION", "FINANCIAL_SAFETY_VETO"),
                    result,
                )
            boundary = result.financial_data_as_of or as_of
            if boundary is not None and (boundary.tzinfo is None or boundary.utcoffset() is None):
                raise ValueError("financial evaluation time must include a timezone")
            if result.earliest_safe_full_payment_date is not None and (
                boundary is None or result.earliest_safe_full_payment_date > boundary
            ):
                return CombinedRecommendation(
                    CombinedDecision.FINANCIALLY_WAIT,
                    FinancialState.SAFE_LATER,
                    price_decision,
                    (
                        "FINANCIAL_DATA_CONTRADICTION",
                        "FINANCIAL_CAPACITY_AVAILABLE_LATER",
                        "FINANCIAL_EVIDENCE_TIME_MISSING" if boundary is None else "FINANCIAL_AS_OF_BOUNDARY",
                    ),
                    result,
                )

        mapping = {
            TimingRecommendation.BUY_NOW: CombinedDecision.BUY_NOW,
            TimingRecommendation.HOLD_FOR_BETTER_PRICE: CombinedDecision.HOLD_FOR_PRICE,
            TimingRecommendation.SET_PRICE_WATCH: CombinedDecision.SET_PRICE_WATCH,
            TimingRecommendation.BUY_USED_OR_REFURBISHED: CombinedDecision.CONSIDER_USED_OR_REFURBISHED,
            TimingRecommendation.INSUFFICIENT_DATA: CombinedDecision.SET_PRICE_WATCH,
        }
        return CombinedRecommendation(mapping[price_decision.recommendation], state, price_decision, ("FINANCIAL_GATE_PASSED",), result)

    def _metrics(
        self,
        anchor: PriceObservation,
        prices: list[Decimal],
        *,
        history_count: int,
        span_days: int,
        episodes: int,
        currency: str,
        source_count: int,
        independent_sources: int,
        coverage: str,
        target: Decimal | None = None,
        expected_savings: Decimal | None = None,
        robust_target: Decimal | None = None,
        rank: Decimal | None = None,
        estimated_wait_days: int | None = None,
    ) -> PriceMetrics:
        return PriceMetrics(
            current_best_price=anchor.landed_price,
            historical_low=min(prices) if prices else None,
            historical_median=percentile(prices, Decimal("0.5")) if prices else None,
            historical_p25=percentile(prices, Decimal("0.25")) if prices else None,
            current_percentile=rank if rank is not None else (empirical_percentile_rank(prices, anchor.landed_price) if prices else None),
            target_buy_price=target,
            expected_savings=expected_savings,
            estimated_wait_days=estimated_wait_days,
            history_count=history_count,
            history_span_days=span_days,
            deal_episode_count=episodes,
            currency=currency,
            source_count=source_count,
            independent_source_count=independent_sources,
            coverage_state=coverage,
            winsorized_target=robust_target,
        )

    def _material_savings(self, intent: PurchaseIntent, reference: Decimal, savings: Decimal) -> bool:
        required = max(intent.minimum_savings_dollars, reference * intent.minimum_savings_fraction)
        return savings >= required

    def _best_alternative(self, current: list[PriceObservation], anchor: PriceObservation) -> PriceObservation | None:
        alternatives = [o for o in current if o.condition != anchor.condition]
        return min(alternatives, key=self._observation_sort_key) if alternatives else None

    def _count_deal_episodes(self, history: list[PriceObservation], threshold: Decimal) -> int:
        return len(self._deal_episode_starts(history, threshold))

    def _estimated_wait_days(self, history: list[PriceObservation], threshold: Decimal) -> int | None:
        """Estimate recurrence from intervals between distinct deal episodes.

        A single episode has no recurrence evidence. For multiple episodes the
        observed span is divided by the number of intervals, not the number of
        episodes, so the estimate cannot be optimistic by one interval.
        """

        starts = self._deal_episode_starts(history, threshold)
        if len(starts) < 2:
            return None
        span_days = (starts[-1] - starts[0]).days
        return max(1, round(span_days / (len(starts) - 1)))

    def _deal_episode_starts(self, history: list[PriceObservation], threshold: Decimal) -> list[object]:
        deal_dates = sorted({self._aware(o.observed_at).date() for o in history if o.landed_price <= threshold or o.deal_signal})
        if not deal_dates:
            return []
        starts = [deal_dates[0]]
        previous = deal_dates[0]
        for date in deal_dates[1:]:
            if (date - previous).days > self.policy.deal_episode_gap_days:
                starts.append(date)
            previous = date
        return starts

    def _confidence(self, intent: PurchaseIntent, history: list[PriceObservation], span_days: int, episodes: int, sources: int) -> Decimal:
        identity = min(Decimal("1"), max(Decimal("0"), intent.product.identity_confidence))
        history_factor = min(Decimal("1"), Decimal(len(history)) / Decimal("30"))
        span_factor = min(Decimal("1"), Decimal(span_days) / Decimal("365"))
        source_factor = min(Decimal("1"), Decimal(max(sources, 1)) / Decimal("3"))
        episode_factor = min(Decimal("1"), Decimal(max(episodes, 1)) / Decimal("3"))
        score = identity * (Decimal("0.35") + history_factor * Decimal("0.25") + span_factor * Decimal("0.20") + source_factor * Decimal("0.10") + episode_factor * Decimal("0.10"))
        return score.quantize(Decimal("0.01"))

    def _deduplicate(self, observations: Iterable[PriceObservation]) -> list[PriceObservation]:
        selected: dict[tuple[object, ...], PriceObservation] = {}
        for observation in observations:
            key = (
                observation.provider,
                observation.retailer or observation.metadata.get("retailer", ""),
                self._aware(observation.observed_at).date(),
                observation.price,
                observation.shipping,
                observation.landed_price,
                observation.condition,
                observation.source_url or "",
                observation.currency.upper(),
            )
            current = selected.get(key)
            if current is None or self._observation_quality_key(observation) < self._observation_quality_key(current):
                selected[key] = observation
        return sorted(selected.values(), key=self._observation_sort_key)

    @staticmethod
    def _trust_eligible(observation: PriceObservation) -> bool:
        return observation.trust in {
            ObservationTrust.TRUSTED_PROVIDER,
            ObservationTrust.CORROBORATED,
            ObservationTrust.USER_PRIVATE,
        }

    @staticmethod
    def _observation_quality_key(observation: PriceObservation) -> tuple[object, ...]:
        trust_rank = {
            ObservationTrust.TRUSTED_PROVIDER: 0,
            ObservationTrust.CORROBORATED: 1,
            ObservationTrust.USER_PRIVATE: 2,
            ObservationTrust.QUARANTINED: 3,
        }
        freshness_rank = {"fresh": 0, "unknown": 1, "stale": 2, "invalid": 3}
        try:
            landed = observation.landed_price
            valid_money = not landed.is_finite() or landed < 0
        except (ArithmeticError, AttributeError, TypeError):
            valid_money = True
        timestamp_distance = datetime.max.replace(tzinfo=timezone.utc) - PriceIntelligenceEngine._aware(observation.observed_at)
        return (
            trust_rank.get(observation.trust, 4),
            1 if valid_money else 0,
            0 if observation.available else 1,
            freshness_rank.get(observation.freshness, 4),
            -observation.product_match_confidence,
            0 if observation.deal_signal else 1,
            timestamp_distance,
            observation.provenance or "",
            observation.seller or "",
            repr(sorted((str(key), str(value)) for key, value in observation.metadata.items())),
        )

    @staticmethod
    def _observation_evidence(observation: PriceObservation) -> dict[str, object]:
        return {
            "provider": observation.provider,
            "retailer": observation.retailer,
            "price": str(observation.price),
            "shipping": str(observation.shipping),
            "landed_price": str(observation.landed_price),
            "condition": observation.condition.value,
            "observed_at": observation.observed_at.isoformat(),
            "source_url": observation.source_url,
            "provenance": observation.provenance,
            "captured": observation.captured,
        }

    def _insufficient(self, code: str, *, evidence: dict[str, object] | None = None) -> PriceDecision:
        metrics = PriceMetrics(None, None, None, None, None, None, None, None, 0, 0, 0)
        return PriceDecision(TimingRecommendation.INSUFFICIENT_DATA, metrics, Decimal("0.10"), (code,), evidence=evidence or {})

    @staticmethod
    def _aware(value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("observation timestamps must include a timezone")
        return value

    @staticmethod
    def _most_common(values: list[str]) -> str:
        counts = Counter(values)
        return min(counts, key=lambda value: (-counts[value], value))

    @staticmethod
    def _dominant_currency(counts: Counter[str]) -> str | None:
        if not counts:
            return None
        highest = max(counts.values())
        winners = sorted(currency for currency, count in counts.items() if count == highest)
        return winners[0] if len(winners) == 1 else None

    @staticmethod
    def _observation_sort_key(observation: PriceObservation) -> tuple[object, ...]:
        return (
            observation.landed_price,
            observation.provider,
            observation.retailer or "",
            observation.source_url or "",
            observation.observed_at,
        )
