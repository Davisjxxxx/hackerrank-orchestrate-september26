from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal

from .models import Condition, PriceObservation, ProductIdentity


DEMO_NOW = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)
DEMO_PRODUCT = ProductIdentity(
    title="Example OLED TV 55-inch",
    brand="Example",
    model="OLED55-X1",
    gtin="036000291452",
    asin="B0CHX3TW6K",
    mpn="OLED55-X1",
    variant={"size": "55-inch", "generation": "2025", "pack_count": "1"},
    identity_evidence=("FIXTURE_GTIN",),
    source_provenance="recorded_fixture",
)


def demo_observations() -> tuple[PriceObservation, ...]:
    history = tuple(
        PriceObservation(
            provider="recorded_fixture",
            retailer="Example Store",
            observed_at=DEMO_NOW - timedelta(days=(index + 1) * 20),
            price=Decimal(str(price)),
            source_url="https://fixture.invalid/example-oled-tv",
            provenance="sanitized_fixture",
        )
        for index, price in enumerate((700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920))
    )
    return history + (
        PriceObservation(
            provider="recorded_fixture",
            retailer="Example Store",
            observed_at=DEMO_NOW,
            price=Decimal("899"),
            source_url="https://fixture.invalid/example-oled-tv",
            provenance="sanitized_fixture",
        ),
        PriceObservation(
            provider="recorded_fixture",
            retailer="Example Outlet",
            observed_at=DEMO_NOW,
            price=Decimal("699"),
            condition=Condition.REFURBISHED,
            source_url="https://fixture.invalid/example-oled-tv-refurb",
            provenance="sanitized_fixture",
        ),
    )
