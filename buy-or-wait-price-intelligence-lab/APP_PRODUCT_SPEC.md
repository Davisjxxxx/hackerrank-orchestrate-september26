# Buy or Wait? — Deployable App Product Specification V0.2

## Product thesis

Buy or Wait? should become a mobile-first purchase decision application that answers two separate questions and then combines them:

1. **Can I safely afford this?**
2. **Is this a strategically good time and price to buy it?**

Financial safety has veto authority. A strong deal never makes an unsafe purchase safe.

## Primary user experience

The first screen should minimize friction and offer four primary intake paths:

1. **Scan barcode** — UPC/EAN/GTIN/ISBN/QR where appropriate.
2. **Take a photo** — identify a product, model label, shelf tag, or packaging in real time.
3. **Paste/share a product link** — retailer URL, marketplace listing, or shared link from another app.
4. **Search/type** — product name, brand/model, or manual description.

A fifth secondary path may support **upload image/screenshot**.

## Core flow

```text
Product Intake
  ├─ Barcode scan
  ├─ Camera photo
  ├─ Image/screenshot upload
  ├─ Product URL/share sheet
  ├─ Text search
  └─ Manual entry
        ↓
Deterministic Intake Normalization
        ↓
Product Identity Resolver
        ↓
Identity Confidence Gate
  ├─ exact/high confidence → continue
  └─ ambiguous → ask user to confirm variant
        ↓
CanonicalProduct
        ↓
Price Intelligence
  ├─ current multi-retailer offers
  ├─ historical price distributions
  ├─ historical deal episodes
  ├─ new/open-box/refurbished/used alternatives
  ├─ shipping / landed cost
  └─ timing / watch recommendation
        ↓
Financial Safety Engine
  ├─ available liquid cash
  ├─ pending and future obligations
  ├─ income / recurring cash flow
  ├─ minimum balance
  ├─ debt and payment obligations
  └─ supported installment options
        ↓
Combined Purchase Decision
  ├─ BUY NOW
  ├─ HOLD FOR PRICE
  ├─ SET PRICE WATCH
  ├─ CONSIDER USED / REFURBISHED
  ├─ FINANCIALLY WAIT
  └─ DO NOT BUY
```

## Identity hierarchy

Prefer identity evidence in this order:

1. valid GTIN/UPC/EAN/ISBN;
2. retailer-specific stable product ID such as ASIN;
3. manufacturer part number + brand;
4. exact brand + model + variant;
5. OCR-extracted model number from photo/label;
6. visual match candidates;
7. normalized title/search text.

A low-confidence visual or title match must not silently enter price history. Ask the user to confirm when materially different variants remain plausible.

## Price-relevant variant dimensions

At minimum preserve when applicable:

- storage/capacity;
- size/dimensions;
- generation/model year;
- color when it changes SKU/price materially;
- bundle contents;
- edition/configuration;
- region/carrier;
- condition;
- pack quantity.

## Capture-price behavior

When the user scans or photographs an item in-store, the app should allow the current observed shelf price to be captured or confirmed. The engine can then compare the exact in-store offer against online and historical alternatives.

Photo processing may extract:

- barcode;
- visible price;
- retailer/store clues;
- brand/model text;
- model number / MPN;
- capacity/size/variant text.

Extracted values are evidence, not trusted facts, until deterministic validation or user confirmation.

## Mobile architecture recommendation

### Client

A cross-platform mobile client is preferred for V1. A reasonable default is **React Native + Expo + TypeScript**, subject to Claude validating barcode/camera/share-extension requirements.

Client responsibilities:

- camera/barcode capture;
- image/screenshot upload;
- URL paste/share intake;
- user confirmation of product/variant;
- urgency and wait preference capture;
- display current/history/financial decision;
- watchlist management;
- push-notification registration.

### API/backend

Use a service boundary around the existing Python engine, with **FastAPI** as the provisional backend API so deterministic Python financial/price logic can be reused rather than rewritten in the mobile client.

Backend responsibilities:

- product resolution orchestration;
- connector fan-out and normalization;
- price-intelligence engine;
- financial-engine integration;
- watch persistence;
- scheduled refresh jobs;
- notification decisioning;
- source/provenance audit trail.

### Persistence

Production direction:

- PostgreSQL for users, canonical products, observations, decisions, watches, and connector provenance;
- queue/scheduler for watch refreshes;
- object storage for user-uploaded images only when necessary;
- encrypted secrets/credentials server-side only.

Do not require production infrastructure during the isolated lab phase. Design interfaces first and use local fixtures/in-memory persistence until promotion criteria justify infrastructure.

## Suggested API surface

```text
POST /v1/intake/barcode
POST /v1/intake/url
POST /v1/intake/photo
POST /v1/intake/search
POST /v1/products/{id}/evaluate
POST /v1/watches
GET  /v1/watches
DELETE /v1/watches/{id}
GET  /v1/products/{id}/prices
GET  /v1/products/{id}/history
GET  /v1/decisions/{id}
```

The API surface is provisional; Claude should validate and simplify it during execution.

## Minimal mobile screens

1. **Home / Capture** — scan, photo, paste link, search.
2. **Confirm Product** — exact product, variant, current observed price.
3. **Decision** — one primary recommendation plus concise rationale.
4. **Price Detail** — current offers, history, target price, expected savings.
5. **Financial Detail** — safe amount/date and obligations affecting the decision.
6. **Watch Setup** — target price, max wait, accepted conditions/sellers.
7. **Watchlist / Alerts** — watched products and trigger history.
8. **Settings / Connections** — financial connectors and preferences when supported.

## Decision-card requirement

The result must remain understandable in seconds. Example:

```text
HOLD — TARGET $749

You can safely afford this today, but $899 is high versus recent history.
Typical sale band: $699–$749
Estimated savings from waiting: ~$150
Deals recur about every 6–10 weeks.

[Watch at $749]   [Buy anyway]
```

Or:

```text
BUY NOW — GOOD PRICE

Current price: $499
Historical median: $549
Lowest observed in covered history: $449
Safe to pay today: $650
Expected savings from waiting: only ~$30–$50
```

## Safety and trust rules

- Financial safety veto cannot be overridden by deal quality.
- Available credit is not ordinary available cash.
- Unrealized investment value is not ordinary available cash.
- Product-match uncertainty must be surfaced.
- Do not compare mismatched variants.
- Do not mix new/used/refurbished/open-box histories.
- Do not expose financial credentials to the mobile client.
- Do not retain photos longer than necessary unless the user explicitly saves the item/watch.
- Every price/decision should retain source and freshness provenance.

## V1 vertical slice acceptance test

A user can:

1. scan a valid barcode in the mobile UI or simulator;
2. resolve it to one canonical product;
3. retrieve fixture or authorized current/history data;
4. evaluate price timing;
5. inject a fixture financial-state result;
6. receive one combined recommendation;
7. create a watch when the result says hold/watch;
8. replay the entire flow deterministically in automated tests.

The V1 slice must work without any live financial account connection. Live finance connectors remain a separate integration lane.
