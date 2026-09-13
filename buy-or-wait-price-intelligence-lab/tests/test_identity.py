from decimal import Decimal

import pytest

from price_intel.intake import ProductIntakeError, ProductIntakeMode, ProductIntakeRequest, normalize_intake
from price_intel.models import ProductIdentity
from price_intel.resolver import IdentityResolutionState, ProductIdentityResolver


def test_isbn10_is_validated_and_canonicalized_to_isbn13_gtin():
    result = normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.BARCODE, barcode="0-306-40615-2"))
    assert result.gtin == "9780306406157"
    assert result.gtin14 == "09780306406157"


def test_invalid_isbn10_is_rejected():
    with pytest.raises(ProductIntakeError, match="ISBN"):
        normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.BARCODE, barcode="0306406153"))


def test_url_credentials_and_control_characters_are_rejected():
    for value in ("https://user:pass@example.com/item", "https://example.com/item\nnext"):
        with pytest.raises(ProductIntakeError):
            normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.PRODUCT_URL, product_url=value))


def test_exact_gtin_wins_over_title_and_preserves_variant():
    intake = normalize_intake(
        ProductIntakeRequest(mode=ProductIntakeMode.BARCODE, barcode="036000291452", observed_price=Decimal("4.99"))
    )
    small = ProductIdentity("Example Pack", brand="Example", model="X", gtin="036000291452", variant={"pack_count": "1"})
    multipack = ProductIdentity("Example Pack", brand="Example", model="X", gtin="00036000291469", variant={"pack_count": "12"})
    result = ProductIdentityResolver().resolve(intake, [multipack, small])
    assert result.state == IdentityResolutionState.EXACT
    assert result.product is not None
    assert result.product.gtin == "036000291452"
    assert "EXACT_GTIN" in result.product.identity_evidence


def test_exact_gtin_is_not_blocked_by_weaker_fuzzy_candidate():
    intake = normalize_intake(ProductIntakeRequest(mode=ProductIntakeMode.BARCODE, barcode="036000291452"))
    exact = ProductIdentity("Example Pack", brand="Example", model="X", gtin="036000291452", variant={"pack_count": "1"})
    fuzzy = ProductIdentity("Example Pack", brand="Example", model="X", gtin="00036000291469", variant={"pack_count": "12"})
    result = ProductIdentityResolver().resolve(intake, [exact, fuzzy])
    assert result.state == IdentityResolutionState.EXACT
    assert result.product and result.product.gtin == "036000291452"


def test_fuzzy_title_with_materially_different_variants_requires_confirmation():
    intake = normalize_intake(
        ProductIntakeRequest(mode=ProductIntakeMode.TEXT_SEARCH, query_text="Example Phone")
    )
    result = ProductIdentityResolver().resolve(
        intake,
        [
            ProductIdentity("Example Phone 128GB", brand="Example", model="P1", variant={"storage": "128GB"}),
            ProductIdentity("Example Phone 256GB", brand="Example", model="P1", variant={"storage": "256GB"}),
        ],
    )
    assert result.state == IdentityResolutionState.NEEDS_CONFIRMATION
    assert result.product is None
