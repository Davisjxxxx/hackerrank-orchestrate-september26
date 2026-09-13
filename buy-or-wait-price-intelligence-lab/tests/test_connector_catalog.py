from price_intel.connectors.catalog import CONNECTOR_CATALOG


def test_no_provider_is_mandatory_and_keepa_is_optional_backfill():
    assert all(candidate.mandatory_for_v1 is False for candidate in CONNECTOR_CATALOG)
    keepa = next(candidate for candidate in CONNECTOR_CATALOG if candidate.name == "Keepa")
    assert keepa.historical_role == "optional_amazon_backfill"
    assert "not required" in keepa.notes.lower()
