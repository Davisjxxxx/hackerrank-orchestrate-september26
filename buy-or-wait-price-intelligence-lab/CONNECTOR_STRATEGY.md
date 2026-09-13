# Connector strategy and access report

Status at 2026-09-12: fixture-backed CI; no live credential was present or used. Keepa is optional Amazon-specific validation/backfill only.

## Implemented boundary

- `ProductResolutionConnector`, `CurrentOfferConnector`, `PriceHistoryConnector`, and `ProviderAdapter` are provider-independent protocols.
- `ShopSavvyAdapter` implements server-side product lookup, current offers, and history normalization. It uses `SHOPSAVVY_API_KEY` only from the server environment, maps condition and availability through explicit allow-lists, validates nested product/offer shapes, converts response amounts with `Decimal(str(value))`, and translates malformed external rows to connector normalization failures or quarantined observations.
- Product search preserves a bounded deterministic set of valid candidates so the identity resolver—not provider result ordering—enforces exact-identifier and variant ambiguity gates.
- `RecordedCatalogConnector` is the deterministic sanitized fixture lane.
- Keepa, eBay Browse, Best Buy, SerpApi, and Slickdeals are represented as explicit unconfigured provider adapters. They fail closed with a named credential requirement instead of scraping or inventing data.
- `InMemoryObservationStore` is the first-party history seam. It attaches canonical product/variant identity to each normalized observation, preserves landed cost, condition, currency, availability, provenance, and freshness, deduplicates repeated rows, and accepts both connector results and user-observed offers.

## Cost and dependency policy

No paid historical API is mandatory. The promotion gates and normal watch-refresh path operate from current authorized offers plus the growing first-party observation store. A provider is admitted only after measuring:

| Provider | Primary role | Cost unit to measure | Required decision-value question |
| --- | --- | --- | --- |
| ShopSavvy | authorized bootstrap/current/history accelerator | credits per lookup/offer/history day and refresh | Does incremental coverage change the recommendation enough to justify credits? |
| eBay Browse | current active listings and condition signals | request quota/partner economics | Does used/refurbished coverage improve the user's accepted-condition choice? |
| Best Buy | catalog/current/open-box | request quota and terms | Does electronics/open-box coverage improve landed-price alternatives? |
| SerpApi | broad current discovery | paid search | Does extra retailer breadth change a decision after caching? |
| Slickdeals | authorized deal signal | partner/token terms | Does a deal signal add an independent episode without scraping? |
| Keepa | optional Amazon validation/backfill | tokens per lookup/history/refresh | Is Amazon-specific validation worth the quota cost for this product or decision? |

Every authorized response is normalized and persisted once. Later evaluations and watch refreshes prefer canonical first-party observations, subject to freshness and coverage evidence. Cost, cacheability, licensing, and incremental value are recorded with the connector adapter before a provider can become a production dependency.

## Primary-source findings

- ShopSavvy documents bearer authentication, product lookup by barcode/ASIN/URL/model, offers, history, schedules, credits, and rate limits at <https://shopsavvy.com/data/documentation>. Its published data page currently lists paid plans and credit costs at <https://shopsavvy.com/data>.
- Keepa documents HTTPS JSON token-based access, Amazon history, product data, offers, deals, and tracking at <https://keepa.com/api-docs/>. Its token/quota economics make it optional Amazon-specific validation/backfill, not a required V1 historical source.
- eBay Browse documents GTIN search, active listing details, shipping, seller, condition, availability, and item resources at <https://developer.ebay.com/api-docs/buy/api-browse.html>. Its production requirements state that many Buy APIs are partner-oriented and require production access approval at <https://developer.ebay.com/api-docs/buy/buy-requirements.html>.
- Best Buy documents product catalog, near-real-time pricing/availability, stores, and open-box buying options at <https://developer.bestbuy.com/apis>.
- SerpApi documents a paid Google Shopping adapter at <https://serpapi.com/google-shopping-api>; use is deferred until discovery coverage justifies its cost and terms.
- Slickdeals remains an authorized partner/token lane only. No scraping is implemented.

## Reusable open-source references

- `shopsavvy/shopsavvy-mcp-server` is MIT-licensed and useful for request/identifier/monitoring patterns. No source was copied; the adapter was independently implemented. Reference: <https://github.com/shopsavvy/shopsavvy-mcp-server>.
- `aymanggv/barcode-price-comparison-app` was reviewed as a scan -> lookup -> compare flow reference. No code was copied and the repository was not used as a data-model dependency.
- Additional maintained patterns reviewed include `jez500/pricebuddy` and `bulletinmybeard/price-scout`; their self-hosted/provider isolation and alert concepts informed the port boundaries, with no code copied.

## Required before live production

Obtain the relevant credential and confirm access, rate limits, licensing/terms, caching rules, source attribution, and permitted commercial use. Record a sanitized response fixture and a failure/rate-limit fixture for each accepted adapter. Do not make ShopSavvy, Keepa, or any single provider a hard dependency.
