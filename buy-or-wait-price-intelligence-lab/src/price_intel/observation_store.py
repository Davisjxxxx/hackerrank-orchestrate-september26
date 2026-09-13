from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Iterable, Protocol, Sequence

from .models import ObservationTrust, PriceObservation, ProductIdentity


@dataclass(frozen=True)
class CanonicalPriceObservation:
    """A first-party historical record with identity and variant context attached."""

    product_id: str
    product: ProductIdentity
    observation: PriceObservation
    ingested_at: datetime

    @property
    def landed_price(self) -> Decimal:
        return self.observation.landed_price

    @property
    def freshness(self) -> str:
        return self.observation.freshness


class ObservationStore(Protocol):
    def append(self, product_id: str, product: ProductIdentity, observations: Iterable[PriceObservation], *, ingested_at: datetime | None = None, user_id: str | None = None) -> Sequence[CanonicalPriceObservation]: ...

    def list(self, product_id: str, *, user_id: str | None = None) -> Sequence[CanonicalPriceObservation]: ...


class InMemoryObservationStore:
    """Deterministic persistence port for first-party history accumulation."""

    def __init__(self, *, freshness_window_days: int = 7):
        self.freshness_window_days = freshness_window_days
        self._records: dict[str, dict[tuple[object, ...], CanonicalPriceObservation]] = {}
        self._private_records: dict[tuple[str, str], dict[tuple[object, ...], CanonicalPriceObservation]] = {}

    def append(
        self,
        product_id: str,
        product: ProductIdentity,
        observations: Iterable[PriceObservation],
        *,
        ingested_at: datetime | None = None,
        user_id: str | None = None,
    ) -> Sequence[CanonicalPriceObservation]:
        ingested_at = _aware(ingested_at or datetime.now(timezone.utc))
        global_bucket = self._records.setdefault(product_id, {})
        stored: list[CanonicalPriceObservation] = []
        for observation in observations:
            normalized = self._with_freshness(observation, ingested_at)
            if normalized.trust == ObservationTrust.QUARANTINED:
                # Quarantine is evidence for audit/review, never decision history.
                continue
            if normalized.trust == ObservationTrust.USER_PRIVATE:
                if not user_id:
                    # An unauthenticated capture is deliberately non-persistent.
                    continue
                target_bucket = self._private_records.setdefault((user_id, product_id), {})
            else:
                target_bucket = global_bucket
            key = (
                product_id,
                normalized.provider,
                normalized.retailer or normalized.metadata.get("retailer", ""),
                _aware(normalized.observed_at).isoformat(),
                normalized.currency.upper(),
                normalized.landed_price,
                normalized.condition,
                normalized.source_url or "",
                normalized.trust,
            )
            record = CanonicalPriceObservation(product_id, product, normalized, ingested_at)
            target_bucket[key] = record
            stored.append(record)
        return tuple(stored)

    def list(self, product_id: str, *, user_id: str | None = None) -> Sequence[CanonicalPriceObservation]:
        records = list(self._records.get(product_id, {}).values())
        if user_id:
            records.extend(self._private_records.get((user_id, product_id), {}).values())
        return tuple(sorted(records, key=_record_key))

    def observations(self, product_id: str, *, user_id: str | None = None) -> tuple[PriceObservation, ...]:
        return tuple(record.observation for record in self.list(product_id, user_id=user_id))

    def _with_freshness(self, observation: PriceObservation, ingested_at: datetime) -> PriceObservation:
        if observation.freshness != "unknown":
            return observation
        age_days = max(0, (ingested_at - _aware(observation.observed_at)).days)
        freshness = "fresh" if age_days <= self.freshness_window_days else "stale"
        return PriceObservation(
            provider=observation.provider,
            observed_at=observation.observed_at,
            price=observation.price,
            shipping=observation.shipping,
            condition=observation.condition,
            available=observation.available,
            seller=observation.seller,
            source_url=observation.source_url,
            product_match_confidence=observation.product_match_confidence,
            deal_signal=observation.deal_signal,
            metadata=observation.metadata,
            currency=observation.currency,
            retailer=observation.retailer,
            captured=observation.captured,
            provenance=observation.provenance,
            freshness=freshness,
            trust=observation.trust,
        )


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _record_key(record: CanonicalPriceObservation) -> tuple[object, ...]:
    observation = record.observation
    return (
        _aware(observation.observed_at),
        observation.provider,
        observation.retailer or "",
        observation.currency,
        observation.landed_price,
        observation.condition.value,
        observation.source_url or "",
    )
