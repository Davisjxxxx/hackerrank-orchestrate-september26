# Provider fixture manifest

`providers/shopsavvy_product.json` is a sanitized, deterministic response-shape fixture. It contains no credential, customer data, or claim of a live lookup. Tests patch the adapter transport and verify product/offer normalization, Decimal money, shipping, condition, availability, and provenance.

Keepa, eBay, Best Buy, SerpApi, and Slickdeals have no live fixtures in this release because no authorized credential was available. Their adapters remain fail-closed and optional. A future fixture must document authorization basis, capture date, request cost, cacheability, licensing, and redacted response provenance.
