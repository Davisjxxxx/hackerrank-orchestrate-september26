# Price Intelligence V0.2 Specification

## Objective

Add a second decision axis to Buy or Wait? and expose it through a deployable mobile-first product:

1. **Financial safety:** can the user safely buy it?
2. **Market timing:** is the current price strategically attractive?

The market-timing layer MUST NOT override financial safety.

The target experience is: scan a barcode, take/upload a photo, paste/share a product link, or search manually; resolve the exact product; compare current/historical pricing; combine that with financial safety; return a clear buy/hold/watch decision.

## Product intake boundary

Supported intake modes:

- barcode;
- camera photo;
- image/screenshot upload;
- product URL/share sheet;
- text search;
- manual entry.

Deterministic intake normalization occurs before product resolution. `src/price_intel/intake.py` is the initial source-agnostic seam.

For barcode mode:

- validate GTIN check digit;
- support GTIN-8, UPC-A/GTIN-12, EAN-13, GTIN-14;
- preserve the source barcode and canonical GTIN-14 form;
- reject invalid codes rather than guessing.

For URLs:

- require absolute HTTPS/HTTP URLs;
- preserve host/source provenance;
- deterministically extract stable source identifiers when safe, such as an Amazon ASIN;
- do not scrape unsupported sites merely because a URL was supplied.

For photo/image modes:

- preserve a durable image reference;
- treat OCR/vision outputs as candidate evidence;
- barcode/model/price evidence must be validated before use;
- require user confirmation when identity remains materially ambiguous.

## Core flow

```text
Product Intake
  -> Deterministic Intake Normalization
  -> Product Identity Resolution
  -> Identity Confidence Gate
  -> Current Offer Connectors
  -> Historical Price / Deal Connectors
  -> Observation Normalization
  -> Condition-Specific History
  -> Deterministic Price Metrics
  -> Timing Recommendation
  -> Financial Safety Gate
  -> Final Purchase Recommendation
  -> Optional Watch Persistence / Alerting
```

## Product identity

Strong identifiers in descending order:

1. GTIN / UPC / EAN / ISBN
2. ASIN where Amazon-specific
3. manufacturer part number + brand
4. exact brand + model + variant tuple
5. OCR-extracted model number / label evidence
6. visual candidate match with user confirmation
7. fuzzy title only as a low-confidence fallback

Variant keys must preserve meaningful differences such as size, storage, generation, color when price-relevant, bundle status, pack quantity, condition, region/carrier, and model year.

## Non-negotiable comparison rule

Do not mix new, used, refurbished, and open-box observations into one historical distribution.

Alternative-condition savings may be compared only after the main-condition price evaluation is complete.

## Initial metrics

- current best landed price;
- lowest observed price in the covered first-party dataset (not an all-time market low unless coverage supports that claim);
- historical median;
- 25th percentile or a more robust replacement selected through testing;
- empirical current-price percentile;
- target buy price;
- expected savings versus target;
- deal episode count;
- estimated wait between deal episodes;
- history coverage count and span;
- confidence;
- source freshness and independent-source count.

## Initial decision policy

- `BUY_NOW`: current price is in a historically attractive band, expected savings from waiting are immaterial, or urgency is immediate.
- `HOLD_FOR_BETTER_PRICE`: expected savings are material and recurring deal evidence suggests a likely opportunity inside the user's wait window.
- `SET_PRICE_WATCH`: waiting may save materially but timing is uncertain, history is sparse, or the target should be monitored.
- `BUY_USED_OR_REFURBISHED`: the user accepts the condition and a materially cheaper valid alternative is available.
- `INSUFFICIENT_DATA`: no acceptable current offer, product identity is unresolved, or no usable observation set exists.

## Safety composition

Financial state has veto authority:

- `NOT_AFFORDABLE` -> `DO_NOT_BUY`
- `SAFE_LATER` -> `FINANCIALLY_WAIT`
- otherwise price-intelligence recommendation may influence timing.

`SAFE_WITH_PLAN` must be evaluated conservatively during integration; do not automatically treat financed affordability as equal to liquid `SAFE_NOW`.

## Connector strategy

### Authorized bootstrap/current-source candidates

ShopSavvy is an optional bootstrap/current-offer/history accelerator because its documented API supports product lookup by barcode/ASIN/URL/model, multi-retailer current pricing, price history, deal discovery, and scheduled monitoring. Its output must be persisted as canonical first-party observations so the product becomes less dependent on paid history over time.

Credential:

`SHOPSAVVY_API_KEY`

Do not embed ShopSavvy-specific semantics in the decision engine. Treat it as one adapter behind canonical protocols so direct-source connectors can replace, validate, or supplement it.

### Direct / validation connectors

- Keepa — optional Amazon-specific historical validation/backfill only. It is not required for V1, CI, promotion gates, or normal watch refreshes because its token/quota economics are not a mandatory product dependency.
- eBay Browse API — current marketplace listings and conditions.
- Best Buy APIs — current catalog/prices/open-box where available.
- SerpApi Google Shopping — broad current-price aggregation if justified.
- Slickdeals partner/API lane — historical/editorial/community deal signal where authorized.

### Deferred

- CamelCamelCamel direct automation;
- Brad's Deals without an authorized feed;
- Facebook Marketplace or other local-market scraping without sanctioned access.

## V1 connector acceptance requirements

Every live connector must have:

- official/authorized access basis documented;
- credentials isolated in environment variables;
- deterministic response-normalization fixture;
- timeout/retry/rate-limit behavior;
- product-match confidence;
- timestamp and currency normalization;
- condition normalization;
- shipping/landed-cost handling;
- cache policy;
- provenance;
- failure isolation so one connector cannot break the decision engine.

Every authorized response and user-observed offer should be persisted in a first-party canonical observation store with product identity, exact variant, condition, source, timestamp, currency, item/shipping/landed price, availability, provenance, and freshness. Future watches use that growing history first and only call paid history providers when the measured incremental value justifies the cost.

## Watch service

The hold/watch mode should persist:

- canonical product identity;
- target price;
- maximum wait date;
- accepted conditions;
- retailer/source restrictions;
- last checked time;
- best observed price;
- alert reason;
- originating decision ID;
- notification endpoint/device token reference.

A scheduler refreshes only eligible sources and emits an alert when the target is crossed or a materially better valid alternative appears.

## Deployable app boundary

The price-intelligence package remains pure decision/domain logic. A mobile/API layer wraps it rather than embedding camera, HTTP framework, database, or notification code in the engine.

See `APP_PRODUCT_SPEC.md` for the app architecture and V1 end-to-end acceptance slice.
