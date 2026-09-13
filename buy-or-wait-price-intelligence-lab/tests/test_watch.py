from datetime import date, datetime, timezone
from decimal import Decimal

from price_intel.models import Condition, PriceObservation, ProductIdentity, TimingRecommendation
from price_intel.watch import InMemoryWatchRepository, InMemoryWatchScheduler, NoopNotificationGateway, WatchService, WatchTrigger


NOW = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)


def test_watch_persists_decision_context_and_triggers_target():
    notifier = NoopNotificationGateway()
    service = WatchService(InMemoryWatchRepository(), notifier)
    watch = service.create(
        user_id="user-a",
        product_id="prod-1",
        product_title="Example Camera",
        target_price=Decimal("700"),
        max_wait_date=date(2026, 10, 1),
        accepted_conditions=frozenset({Condition.NEW}),
        retailer_restrictions=frozenset({"Store A"}),
        source_restrictions=frozenset({"fixture"}),
        original_decision="hold_for_price",
        notification_target_ref="device-ref-1",
    )
    updated, events = service.evaluate(
        watch,
        [
            PriceObservation("fixture", datetime(2026, 9, 12, tzinfo=timezone.utc), Decimal("699"), retailer="Store A")
        ],
        now=datetime(2026, 9, 12, tzinfo=timezone.utc),
    )
    assert updated.best_observed_price == Decimal("699")
    assert WatchTrigger.TARGET_REACHED in {event.trigger for event in events}
    assert notifier.events == list(events)


def test_watch_conditions_and_users_are_isolated():
    repository = InMemoryWatchRepository()
    service = WatchService(repository)
    a = service.create(user_id="a", product_id="p", product_title="A", target_price=Decimal("1"), max_wait_date=date(2027, 1, 1), accepted_conditions=frozenset({Condition.NEW}))
    b = service.create(user_id="b", product_id="p", product_title="B", target_price=Decimal("1"), max_wait_date=date(2027, 1, 1), accepted_conditions=frozenset({Condition.NEW}))
    assert [watch.id for watch in repository.list("a")] == [a.id]
    assert repository.get("a", b.id) is None
    assert service.repository.delete("a", b.id) is False


def test_watch_max_wait_approaching_is_a_decision_reevaluation_trigger():
    notifier = NoopNotificationGateway()
    service = WatchService(notifier=notifier, approach_days=7)
    watch = service.create(user_id="a", product_id="p", product_title="A", target_price=Decimal("1"), max_wait_date=date(2026, 9, 15), accepted_conditions=frozenset({Condition.NEW}))
    _, events = service.evaluate(watch, [], now=datetime(2026, 9, 12, tzinfo=timezone.utc))
    assert any(event.trigger == WatchTrigger.MAX_WAIT_APPROACHING for event in events)


def test_scheduler_only_refreshes_due_watches_and_never_purchases():
    service = WatchService()
    scheduler = InMemoryWatchScheduler()
    watch = service.create(user_id="u", product_id="p", product_title="A", target_price=Decimal("10"), max_wait_date=date(2027, 1, 1), accepted_conditions=frozenset({Condition.NEW}))
    scheduler.schedule(watch)
    events = scheduler.run_due(
        service,
        lambda current: [PriceObservation("fixture", NOW, Decimal("9"), condition=Condition.NEW)],
        now=NOW,
        products={"p": ProductIdentity("A")},
    )
    assert any(event.trigger == WatchTrigger.TARGET_REACHED for event in events)
    assert scheduler.due(now=NOW) == ()
    assert not any(event.trigger.value == "purchase_executed" for event in events)
