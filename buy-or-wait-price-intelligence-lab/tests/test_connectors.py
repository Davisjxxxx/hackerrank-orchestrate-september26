from datetime import datetime, timezone
from decimal import Decimal

import pytest

from price_intel.connectors import ConnectorUnavailable, ShopSavvyAdapter, build_provider_adapters
from price_intel.intake import ProductIntakeMode, ProductIntakeRequest, normalize_intake
from price_intel.models import ProductIdentity


def test_unconfigured_provider_fails_closed_without_exposing_a_secret():
    adapter = ShopSavvyAdapter(api_key=None)
    with pytest.raises(ConnectorUnavailable, match="SHOPSAVVY_API_KEY"):
        adapter.resolve_product(normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.TEXT_SEARCH, query_text="camera")))


def test_shopsavvy_response_normalization_uses_decimal_and_condition(monkeypatch):
    adapter = ShopSavvyAdapter(api_key="test-only-not-a-real-key")
    monkeypatch.setattr(
        adapter,
        "_get",
        lambda path, params: {
            "product": {
                "name": "Example Camera",
                "brand": "Example",
                "model": "C1",
                "identifiers": {"upc": "036000291452", "asin": "B000000001"},
            }
        }
        if path == "products"
        else {
            "offers": [
                {
                    "retailer": "Example Store",
                    "condition": "refurbished",
                    "history": [{"price": "499.99", "shipping": "9.99", "timestamp": "2026-09-12T12:00:00Z"}],
                }
            ]
        },
    )
    product = adapter.resolve_product(normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.BARCODE, barcode="036000291452")))[0]
    assert product.asin == "B000000001"
    row = adapter.price_history(product, lookback_days=90)[0]
    assert row.price == Decimal("499.99")
    assert row.landed_price == Decimal("509.98")
    assert row.condition.value == "refurbished"
    assert row.provenance == "recorded_from_shopsavvy_response"


def test_provider_catalog_reports_configuration_without_network(monkeypatch):
    monkeypatch.delenv("SHOPSAVVY_API_KEY", raising=False)
    adapters = build_provider_adapters()
    statuses = {adapter.status.name: adapter.status for adapter in adapters}
    assert statuses["shopsavvy"].configured is False
    assert statuses["keepa"].credential_env == "KEEPA_API_KEY"
    assert statuses["ebay"].configured is False
