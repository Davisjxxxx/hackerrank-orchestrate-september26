from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from enum import StrEnum
from typing import Callable, Iterable, Protocol, Sequence
from uuid import uuid4

from .models import Condition, ObservationTrust, PriceObservation, ProductIdentity, TimingRecommendation, Urgency, validate_non_negative_money
from .observation_store import ObservationStore


class WatchTrigger(StrEnum):
    TARGET_REACHED = "target_reached"
    MATERIALLY_BETTER_OFFER = "materially_better_offer"
    UNUSUALLY_GOOD_DEAL = "unusually_good_deal"
    MAX_WAIT_APPROACHING = "max_wait_approaching"


@dataclass(frozen=True)
class PriceWatch:
    id: str
    user_id: str
    product_id: str
    product_title: str
    target_price: Decimal
    max_wait_date: date
    accepted_conditions: frozenset[Condition]
    retailer_restrictions: frozenset[str] = frozenset()
    source_restrictions: frozenset[str] = frozenset()
    last_checked_at: datetime | None = None
    best_observed_price: Decimal | None = None
    original_decision: str = "set_price_watch"
    urgency: Urgency = Urgency.FLEXIBLE
    notification_target_ref: str | None = None
    source_freshness: str = "unknown"
    source_provenance: tuple[str, ...] = ()
    triggered_triggers: frozenset[WatchTrigger] = frozenset()


@dataclass(frozen=True)
class WatchEvent:
    watch_id: str
    trigger: WatchTrigger
    observed_price: Decimal | None
    reason_codes: tuple[str, ...]
    created_at: datetime


class WatchRepository(Protocol):
    def save(self, watch: PriceWatch) -> PriceWatch: ...

    def get(self, user_id: str, watch_id: str) -> PriceWatch | None: ...

    def list(self, user_id: str) -> Sequence[PriceWatch]: ...

    def delete(self, user_id: str, watch_id: str) -> bool: ...


class InMemoryWatchRepository:
    def __init__(self):
        self._watches: dict[tuple[str, str], PriceWatch] = {}

    def save(self, watch: PriceWatch) -> PriceWatch:
        self._watches[(watch.user_id, watch.id)] = watch
        return watch

    def get(self, user_id: str, watch_id: str) -> PriceWatch | None:
        return self._watches.get((user_id, watch_id))

    def list(self, user_id: str) -> Sequence[PriceWatch]:
        return tuple(watch for (owner, _), watch in self._watches.items() if owner == user_id)

    def delete(self, user_id: str, watch_id: str) -> bool:
        return self._watches.pop((user_id, watch_id), None) is not None


class NotificationGateway(Protocol):
    def notify(self, event: WatchEvent, target_ref: str | None) -> None: ...


class WatchScheduler(Protocol):
    def schedule(self, watch: PriceWatch) -> None: ...

    def unschedule(self, watch_id: str) -> None: ...

    def due(self, *, now: datetime) -> Sequence[PriceWatch]: ...


class InMemoryWatchScheduler:
    """Scheduler port for tests; production can replace it with a queue/cron adapter."""

    def __init__(self, *, refresh_interval: timedelta = timedelta(hours=6)):
        self.refresh_interval = refresh_interval
        self._watches: dict[str, PriceWatch] = {}

    def schedule(self, watch: PriceWatch) -> None:
        self._watches[watch.id] = watch

    def unschedule(self, watch_id: str) -> None:
        self._watches.pop(watch_id, None)

    def due(self, *, now: datetime) -> Sequence[PriceWatch]:
        result = []
        for watch in self._watches.values():
            if watch.last_checked_at is None or _aware(now) - _aware(watch.last_checked_at) >= self.refresh_interval:
                result.append(watch)
        return tuple(result)

    def run_due(
        self,
        service: "WatchService",
        refresh: Callable[[PriceWatch], Iterable[PriceObservation]],
        *,
        now: datetime,
        products: dict[str, ProductIdentity],
    ) -> tuple[WatchEvent, ...]:
        events: list[WatchEvent] = []
        for watch in self.due(now=now):
            updated, emitted = service.evaluate(watch, refresh(watch), now=now, product=products.get(watch.product_id))
            self._watches[updated.id] = updated
            events.extend(emitted)
        return tuple(events)


class NoopNotificationGateway:
    def __init__(self):
        self.events: list[WatchEvent] = []

    def notify(self, event: WatchEvent, target_ref: str | None) -> None:
        self.events.append(event)


class WatchService:
    def __init__(self, repository: WatchRepository | None = None, notifier: NotificationGateway | None = None, *, approach_days: int = 7, observation_store: ObservationStore | None = None):
        self.repository = repository or InMemoryWatchRepository()
        self.notifier = notifier or NoopNotificationGateway()
        self.approach_days = approach_days
        self.observation_store = observation_store

    def create(
        self,
        *,
        user_id: str,
        product_id: str,
        product_title: str,
        target_price: Decimal,
        max_wait_date: date,
        accepted_conditions: frozenset[Condition],
        retailer_restrictions: frozenset[str] = frozenset(),
        source_restrictions: frozenset[str] = frozenset(),
        original_decision: str = "set_price_watch",
        urgency: Urgency = Urgency.FLEXIBLE,
        notification_target_ref: str | None = None,
    ) -> PriceWatch:
        target_price = validate_non_negative_money(target_price, "target_price")
        if not product_id:
            raise ValueError("product_id is required")
        if not accepted_conditions:
            raise ValueError("at least one accepted condition is required")
        if any(
            not isinstance(condition, Condition) or condition == Condition.UNKNOWN
            for condition in accepted_conditions
        ):
            raise ValueError("accepted_conditions must contain supported purchasable conditions")
        watch = PriceWatch(
            id=f"watch_{uuid4().hex[:16]}",
            user_id=user_id,
            product_id=product_id,
            product_title=product_title,
            target_price=target_price,
            max_wait_date=max_wait_date,
            accepted_conditions=accepted_conditions,
            retailer_restrictions=retailer_restrictions,
            source_restrictions=source_restrictions,
            original_decision=original_decision,
            urgency=urgency,
            notification_target_ref=notification_target_ref,
        )
        return self.repository.save(watch)

    def evaluate(
        self,
        watch: PriceWatch,
        observations: Iterable[PriceObservation],
        *,
        now: datetime | None = None,
        price_recommendation: TimingRecommendation | None = None,
        product: ProductIdentity | None = None,
    ) -> tuple[PriceWatch, tuple[WatchEvent, ...]]:
        now = now or datetime.now(timezone.utc)
        observations = tuple(observations)
        eligible = [
            observation
            for observation in observations
            if observation.available
            and observation.trust in {ObservationTrust.TRUSTED_PROVIDER, ObservationTrust.CORROBORATED, ObservationTrust.USER_PRIVATE}
            and observation.condition in watch.accepted_conditions
            and (not watch.retailer_restrictions or (observation.retailer in watch.retailer_restrictions))
            and (not watch.source_restrictions or observation.provider in watch.source_restrictions)
            and 0 <= (now - _aware(observation.observed_at)).days <= 3
            and observation.freshness not in {"stale", "invalid"}
        ]
        if self.observation_store is not None and product is not None:
            # Only observations that passed the watch's trust/condition/source
            # policy enter first-party history. Rejected provider rows are not
            # allowed to poison future decisions.
            self.observation_store.append(watch.product_id, product, eligible, ingested_at=now, user_id=watch.user_id)
        best = min((observation.landed_price for observation in eligible), default=None)
        updated = replace(
            watch,
            last_checked_at=now,
            best_observed_price=min(
                [value for value in (watch.best_observed_price, best) if value is not None],
                default=None,
            ),
            source_freshness="fresh" if eligible else "stale_or_unavailable",
            source_provenance=tuple(sorted({observation.provenance or observation.provider for observation in eligible})),
        )
        self.repository.save(updated)
        events: list[WatchEvent] = []
        already = watch.triggered_triggers
        if best is not None and best <= watch.target_price and WatchTrigger.TARGET_REACHED not in already:
            events.append(self._event(watch, WatchTrigger.TARGET_REACHED, best, "WATCH_TARGET_REACHED", now))
        if best is not None and watch.best_observed_price is not None and best < watch.best_observed_price * Decimal("0.95") and WatchTrigger.MATERIALLY_BETTER_OFFER not in already:
            events.append(self._event(watch, WatchTrigger.MATERIALLY_BETTER_OFFER, best, "MATERIALLY_BETTER_ACCEPTED_OFFER", now))
        if price_recommendation in {TimingRecommendation.BUY_NOW, TimingRecommendation.BUY_USED_OR_REFURBISHED} and best is not None and WatchTrigger.UNUSUALLY_GOOD_DEAL not in already:
            events.append(self._event(watch, WatchTrigger.UNUSUALLY_GOOD_DEAL, best, "POLICY_IDENTIFIES_GOOD_DEAL", now))
        days_left = (watch.max_wait_date - now.date()).days
        if 0 <= days_left <= self.approach_days and WatchTrigger.MAX_WAIT_APPROACHING not in already:
            events.append(self._event(watch, WatchTrigger.MAX_WAIT_APPROACHING, best, "MAX_WAIT_DATE_APPROACHING", now))
        updated = replace(updated, triggered_triggers=frozenset(set(already).union(event.trigger for event in events)))
        self.repository.save(updated)
        for event in events:
            self.notifier.notify(event, watch.notification_target_ref)
        return updated, tuple(events)

    @staticmethod
    def _event(watch: PriceWatch, trigger: WatchTrigger, price: Decimal | None, reason: str, now: datetime) -> WatchEvent:
        return WatchEvent(watch.id, trigger, price, (reason,), now)


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
