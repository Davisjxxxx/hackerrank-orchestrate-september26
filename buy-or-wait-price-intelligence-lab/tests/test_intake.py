from decimal import Decimal

import pytest

from price_intel.intake import (
    ProductIntakeError,
    ProductIntakeMode,
    ProductIntakeRequest,
    normalize_intake,
)


def test_barcode_intake_validates_and_canonicalizes_gtin():
    result = normalize_intake(
        ProductIntakeRequest(
            mode=ProductIntakeMode.BARCODE,
            barcode="036000291452",
            observed_price=Decimal("4.99"),
            currency="usd",
        )
    )
    assert result.gtin == "036000291452"
    assert result.gtin14 == "00036000291452"
    assert result.currency == "USD"


def test_invalid_gtin_is_rejected_instead_of_guessed():
    with pytest.raises(ProductIntakeError, match="check digit"):
        normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.BARCODE, barcode="036000291453"))


def test_product_url_extracts_amazon_asin_without_needing_page_scraping():
    result = normalize_intake(
        ProductIntakeRequest(
            mode=ProductIntakeMode.PRODUCT_URL,
            product_url="https://www.amazon.com/example/dp/B0CHX3TW6K/",
        )
    )
    assert result.source_host == "amazon.com"
    assert result.asin == "B0CHX3TW6K"


def test_photo_intake_requires_durable_image_reference():
    with pytest.raises(ProductIntakeError, match="image_ref"):
        normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.CAMERA_PHOTO))


def test_text_search_is_normalized_but_not_silently_resolved_to_a_product():
    result = normalize_intake(
        ProductIntakeRequest(mode=ProductIntakeMode.TEXT_SEARCH, query_text="  Sony   WH-1000XM5  black ")
    )
    assert result.query_text == "Sony WH-1000XM5 black"
    assert result.gtin is None
    assert result.asin is None
