from datetime import datetime, timedelta, timezone
from decimal import Decimal

from price_intel.models import Condition, PriceObservation, ProductIdentity
from price_intel.observation_store import InMemoryObservationStore
from price_intel.watch import WatchService


NOW = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)
PRODUCT = ProductIdentity("Example Camera", brand="Example", model="C1", gtin="036000291452", variant={"storage": "128GB"})


def test_first_party_store_persists_identity_variant_landed_price_and_freshness():
    store = InMemoryObservationStore(freshness_window_days=7)
    observation = PriceObservation(
        provider="authorized-fixture",
        retailer="Store A",
        observed_at=NOW,
        price=Decimal("90"),
        shipping=Decimal("10"),
        condition=Condition.NEW,
        currency="USD",
        provenance="connector-response-1",
    )
    records = store.append("prod-1", PRODUCT, [observation], ingested_at=NOW)
    record = records[0]
    assert record.product.variant["storage"] == "128GB"
    assert record.landed_price == Decimal("100")
    assert record.observation.freshness == "fresh"
    assert record.observation.provenance == "connector-response-1"


def test_store_deduplicates_same_connector_observation_but_keeps_new_days():
    store = InMemoryObservationStore()
    row = PriceObservation("fixture", NOW, Decimal("10"), retailer="A")
    store.append("p", PRODUCT, [row, row], ingested_at=NOW)
    store.append("p", PRODUCT, [PriceObservation("fixture", NOW - timedelta(days=1), Decimal("10"), retailer="A")], ingested_at=NOW)
    assert len(store.list("p")) == 2


def test_watch_refresh_adds_connector_observations_to_first_party_history():
    store = InMemoryObservationStore()
    service = WatchService(observation_store=store)
    watch = service.create(
        user_id="u",
        product_id="p",
        product_title=PRODUCT.title,
        target_price=Decimal("10"),
        max_wait_date=NOW.date(),
        accepted_conditions=frozenset({Condition.NEW}),
    )
    service.evaluate(
        watch,
        [PriceObservation("authorized", NOW, Decimal("9"), retailer="A")],
        now=NOW,
        product=PRODUCT,
    )
    assert len(store.list("p")) == 1
