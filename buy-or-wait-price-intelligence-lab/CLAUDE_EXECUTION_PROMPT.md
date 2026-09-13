# Role

You are the **Lead Product Engineer, Mobile/App Architect, Connector Engineer, Adversarial Reviewer, and Prototype Executor** for the **Buy or Wait? Price Intelligence & Purchase Decision App** lane.

# Objective

Take the supplied `buy_or_wait_price_intelligence_lab` from its current tested prototype into a **deployable-app-ready release candidate** that can later be integrated with the main Buy or Wait? financial engine.

The product vision is no longer just a backend price analyzer.

A user should eventually be able to:

- scan a barcode in real time;
- take a photo of an item, packaging, model label, or shelf tag;
- upload a screenshot/photo;
- paste or share a product URL;
- type/search for a product;

and receive a combined decision answering:

1. **Can I safely afford this?**
2. **Is this a strategically good time and price to buy it?**
3. **What should I do now: buy, hold, watch, wait financially, buy another condition, or skip it?**

Work iteratively:

`inspect -> test -> challenge assumptions -> implement -> red-team -> retest -> document -> repeat`

Do **not push to GitHub** until the user explicitly authorizes the push after external review.

# Context

The main Buy or Wait? hackathon implementation is actively being built in a separate Codex session. Do not modify, reset, switch branches, or otherwise interfere with that active checkout.

Work only in the isolated Price Intelligence lab.

Recommended standalone path:

`~/buy-or-wait-price-intelligence-lab`

The supplied lab currently includes:

- deterministic price-intelligence models and engine;
- financial-safety composition seam;
- connector protocols and capability catalog;
- product-intake normalization for barcode, URL, photo/image, search, and manual inputs;
- GTIN validation and canonicalization;
- initial connector strategy;
- product/app specification;
- competitive-landscape research;
- regression tests.

The current supplied baseline should report:

`12 passed`

Treat this as the expected baseline, not as proof that the architecture is complete.

The product must preserve one absolute rule:

> **Financial safety has veto authority. A bargain never makes an unsafe purchase safe.**

# Instructions

## Instruction 1 — Isolate and establish the baseline

Do not modify the active hackathon checkout.

Create or use an isolated working copy of this lab.

Read in full:

- `README.md`
- `PRICE_INTELLIGENCE_SPEC.md`
- `APP_PRODUCT_SPEC.md`
- `COMPETITIVE_LANDSCAPE.md`
- all Python source and tests.

Run:

```bash
python -m pytest -q
```

Confirm the expected baseline or document any difference.

Before implementing, inventory:

- package structure;
- existing decision semantics;
- intake modes;
- connector protocols;
- missing modules;
- tests;
- dependencies;
- environment assumptions.

Do not push anything.

---

## Instruction 2 — Preserve the domain boundary

Keep the system separated into these domains:

```text
Mobile / Web Client
        ↓
Product Intake API
        ↓
Product Identity Resolver
        ↓
Canonical Product
        ↓
Price / Deal Connector Layer
        ↓
Canonical Price Observations
        ↓
Price Intelligence Engine
        ↓
Financial Safety Interface
        ↓
Combined Purchase Decision
        ↓
Watch / Alert Service
```

The deterministic decision engine must not depend directly on:

- React Native;
- Expo;
- FastAPI;
- database libraries;
- provider-specific API response structures;
- camera SDKs;
- OCR vendors;
- notification vendors.

All such technology belongs behind adapters or service boundaries.

---

## Instruction 3 — Build the Product Intake & Identity layer

Treat product intake as a first-class subsystem.

Supported modes:

1. barcode scan;
2. live camera photo;
3. uploaded image/screenshot;
4. pasted/shared product URL;
5. text search;
6. manual entry.

The existing deterministic intake normalization should be reviewed and hardened.

### Barcode requirements

Support and validate:

- GTIN-8;
- UPC-A / GTIN-12;
- EAN-13;
- GTIN-14;
- ISBN where it can be represented through supported barcode standards;
- QR only when it contains a product URL or supported identifier.

Never accept an invalid check digit and silently continue.

### Product identity hierarchy

Prioritize:

1. valid GTIN/UPC/EAN/ISBN;
2. source-specific stable ID such as ASIN;
3. MPN + brand;
4. exact brand + model + variant tuple;
5. OCR-extracted model/MPN/label evidence;
6. visual-search candidates;
7. normalized title as low-confidence fallback.

### Variant safety

Never silently merge products that differ materially in:

- storage/capacity;
- generation/model year;
- screen/physical size;
- pack count;
- bundle contents;
- edition/configuration;
- carrier/region;
- condition;
- any other price-relevant SKU attribute.

Implement an identity-confidence model with explicit evidence/rationale.

When multiple materially different candidates remain plausible, return a `NEEDS_CONFIRMATION` state and require a user selection rather than guessing.

Add deterministic fixtures and tests.

---

## Instruction 4 — Design the deployable app surface

The target is a simple, mobile-first application.

Evaluate **React Native + Expo + TypeScript** as the provisional cross-platform client unless a concrete blocker makes Flutter or native development materially better.

Do not rewrite the Python decision engine in JavaScript merely to build the UI.

Evaluate a thin **FastAPI** service boundary around the Python domain engine.

Create an app architecture decision record covering:

- mobile framework;
- barcode/camera library;
- image upload flow;
- share-sheet/deep-link flow;
- API boundary;
- local versus server processing;
- push notification approach;
- authentication direction;
- persistence direction;
- deployment target;
- privacy implications.

Do not overbuild infrastructure yet.

Implement the smallest viable vertical-slice UI or app skeleton that proves the boundaries.

The home experience should expose:

- **Scan barcode**
- **Take photo**
- **Paste/share link**
- **Search/type item**

and route all of them through the same canonical intake/identity pipeline.

---

## Instruction 5 — Build the API contract before coupling the UI

Define and test a stable application/API contract.

A provisional surface may include:

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

Change or simplify this if implementation evidence supports a better contract.

Use typed request/response models.

The client must never receive provider credentials.

---

## Instruction 6 — Capture the in-store observed price

A barcode/photo scan may occur while the user is physically looking at an item.

Support an optional current observed offer containing:

- observed price;
- currency;
- retailer/store hint;
- capture time;
- source mode;
- photo/OCR provenance when applicable.

For camera/photo flows, evaluate OCR/vision extraction of:

- visible shelf price;
- barcode;
- brand/model text;
- MPN/model number;
- size/capacity/variant;
- retailer clues.

Treat extracted values as evidence until deterministically validated or confirmed by the user.

The app should make correction easy.

---

## Instruction 7 — Red-team the price decision policy

Challenge at least these scenarios and add tests where materially relevant:

1. current price is the lowest observation in the covered dataset (do not call it an all-time market low without sufficient external coverage);
2. current price is historically expensive;
3. history is sparse;
4. one anomalous low distorts the distribution;
5. one long sale produces many repeated observations;
6. multiple deal episodes occur close together;
7. exact GTIN match versus fuzzy title match;
8. wrong capacity/storage variant;
9. wrong generation/model year;
10. single item versus multipack;
11. standalone product versus bundle;
12. new versus open-box versus refurbished versus used;
13. shipping makes the nominal low offer more expensive;
14. tax information is unavailable;
15. coupon/member-only price;
16. stale listing;
17. out-of-stock listing;
18. marketplace seller risk;
19. immediate need;
20. discretionary item;
21. user's savings threshold is not met;
22. likely deal occurs after maximum wait date;
23. multiple currencies;
24. duplicate offers from aggregators;
25. provider outage;
26. provider rate limit;
27. invalid barcode;
28. photo produces multiple plausible products;
29. URL points to a marketplace listing rather than canonical product page;
30. current store price is manually corrected by user;
31. exceptional deal but financial state is `NOT_AFFORDABLE`;
32. temporary deal but financial state is `SAFE_LATER`;
33. financially safe installment plan but weak liquidity;
34. price source disagrees with the captured shelf price;
35. history contains discontinued/replacement-model contamination.

Do not weaken financial safety because of a rare deal.

---

## Instruction 8 — Replace fragile price heuristics where evidence supports it

The current p25 target is a prototype, not a sacred rule.

Evaluate deterministic alternatives such as:

- winsorized distributions;
- rolling 30/90/365-day medians;
- recency weighting;
- sale-episode clustering;
- recurring deal bands;
- retailer/channel-specific history;
- distinct-source consensus;
- minimum coverage requirements;
- seasonal evidence only when enough history exists.

Do not claim predictive accuracy unsupported by evidence.

The lowest observed price in the covered dataset is context, not automatically the target price or an all-time market claim.

Document the final deterministic policy precisely.

---

## Instruction 9 — Evaluate ShopSavvy as an optional authorized bootstrap connector

Current research indicates ShopSavvy is both a major competitor and a potentially useful data-plane accelerator.

Its documented capabilities include:

- product lookup by barcode;
- ASIN lookup;
- URL lookup;
- model/product search;
- current offers across retailers;
- historical price data;
- deal discovery;
- scheduled monitoring.

Credential:

`SHOPSAVVY_API_KEY`

Research and validate the current official API documentation, access model, pricing/credits, rate limits, data license, and production-use terms before depending on it.

If access is practical, build a **ShopSavvy adapter** behind the canonical connector interfaces.

Use recorded/sanitized fixtures for tests.

The core engine must remain provider-independent.

Do not let a competitor API become a hard architectural dependency.

---

## Instruction 10 — Preserve and validate direct-source connector lanes

Continue evaluating these official/authorized sources:

### Keepa (optional Amazon validation/backfill)

Keepa is not a required V1 connector, preferred historical source, promotion-gate dependency, CI dependency, or normal watch-refresh dependency. Use it only when Amazon-specific validation/backfill has measured incremental decision value greater than its token/quota cost.

Credential:

`KEEPA_API_KEY`

Validate:

- ASIN/product lookup;
- price history;
- deals;
- offer history/current offers;
- token/rate cost;
- data licensing.

### eBay Browse API

Credential:

`EBAY_CLIENT_ID`
`EBAY_CLIENT_SECRET`

Validate:

- GTIN/product/category/keyword lookup;
- active listings;
- condition;
- shipping/landed cost;
- seller/listing provenance;
- image search if useful.

Do not make limited-release sold-history APIs a V1 requirement.

### Best Buy APIs

Credential:

`BESTBUY_API_KEY`

Validate product/pricing/open-box capabilities and actual current production availability.

### SerpApi Google Shopping

Credential:

`SERPAPI_API_KEY`

Use only if broad current-price discovery materially improves coverage enough to justify cost and dependency.

### Slickdeals

Credential if authorized:

`SLICKDEALS_TOKEN`

Use as an authorized deal/community signal lane, not through unsanctioned scraping.

### Deferred

Do not build direct automated scraping of:

- CamelCamelCamel;
- Brad's Deals;
- Facebook Marketplace;
- other local marketplaces

unless an explicit sanctioned API/feed/partner method is confirmed.

---

## Instruction 11 — Use existing open-source work intelligently

Inspect, but do not blindly copy, relevant public repositories.

### `shopsavvy/shopsavvy-mcp-server`

Use as a reference for:

- ShopSavvy API request patterns;
- identifier support;
- current/history calls;
- scheduled monitoring;
- API error/rate-limit handling.

Confirm its current license before reusing code. Preserve attribution/license obligations if any code is incorporated.

### `aymanggv/barcode-price-comparison-app`

Use only as a UI/flow reference for:

`scan -> identify -> retrieve -> compare -> display`

Do not inherit its data model as the architecture for this product.

Independently search GitHub for stronger maintained barcode/camera/product-resolution/watchlist examples and document anything worth borrowing.

---

## Instruction 12 — Build the watch service as a decision-aware subsystem

A generic price alert is not enough.

Persist a watch with:

- canonical product identity;
- target price;
- maximum wait date;
- accepted conditions;
- retailer/source restrictions;
- last checked time;
- best observed price;
- originating decision;
- urgency;
- notification endpoint reference;
- source freshness/provenance.

A watch should alert when:

- target price is reached;
- a materially better accepted-condition alternative appears;
- a deal is sufficiently attractive under the same deterministic policy;
- the max-wait window is approaching and the recommendation should be reevaluated.

Do not automatically buy anything in this phase.

---

## Instruction 13 — Preserve financial safety as an external deterministic authority

Do not reimplement the full hackathon financial engine here.

Define a clean integration contract that can consume a future result equivalent to:

```text
financial_state
safe_amount_today
earliest_safe_full_payment_date
minimum_balance
recommended_payment_method
payment_plan
financial_reason_codes
financial_data_as_of
financial_confidence_or_coverage_state
```

The combined decision layer must handle at least:

- `SAFE_NOW`
- `SAFE_WITH_PLAN`
- `SAFE_LATER`
- `NOT_AFFORDABLE`

Rules:

- `NOT_AFFORDABLE` always vetoes buying;
- `SAFE_LATER` cannot become `BUY_NOW` because of a discount;
- available credit is not equivalent to liquid cash;
- unrealized investments are not ordinary available cash;
- `SAFE_WITH_PLAN` must be treated conservatively until integration semantics are fully established.

Add tests proving price intelligence cannot bypass the financial result.

---

## Instruction 14 — Add confidence, evidence, and provenance

Every product and price recommendation should preserve enough evidence to explain:

- what product was identified;
- why it is believed to be that exact variant;
- current observed/captured price;
- best external current price;
- historical reference distribution;
- data freshness;
- source coverage;
- accepted condition;
- target buy price;
- estimated savings;
- reason for buy/hold/watch;
- financial-veto reason when applicable.

Price recommendation confidence should consider:

- identifier strength;
- number of independent sources;
- history count;
- history span;
- freshness;
- condition consistency;
- retailer/source quality;
- agreement across sources;
- distinct deal episodes.

Never let a model's self-reported confidence directly determine financial safety.

---

## Instruction 15 — Privacy and security review

Red-team the deployable app for:

- image retention;
- EXIF/location leakage;
- financial-account secrecy;
- API-key exposure;
- malicious URLs;
- OCR/vision prompt injection;
- unsafe marketplace links;
- untrusted seller descriptions;
- replayed/stale prices;
- user-account separation;
- notification leakage;
- logging of financial data;
- secrets committed to Git.

Default toward minimum retention.

Do not put provider credentials in the mobile app.

Do not allow image/OCR/text content to execute instructions or mutate trusted financial state.

---

## Instruction 16 — Implement a minimal end-to-end vertical slice

Before expanding UI polish, prove this automated flow:

1. create a barcode intake request;
2. validate/canonicalize the barcode;
3. resolve fixture or authorized provider product identity;
4. obtain current/historical fixture or authorized provider price observations;
5. run price intelligence;
6. supply a fixture financial decision;
7. generate the combined recommendation;
8. render it through the provisional API/client contract;
9. create a watch for hold/watch outcomes;
10. replay deterministically in tests.

Then add corresponding URL intake.

Then add photo/image intake using a mocked or authorized vision adapter.

Do not make live provider availability a prerequisite for deterministic CI.

---

## Instruction 17 — Phased promotion sequence

Use this promotion sequence and do not skip gates.

### P0 — Baseline integrity

- existing tests pass;
- source inventory complete;
- no active-hackathon repo mutation.

### P1 — Intake & identity hardening

- barcode/url/photo/search contracts;
- invalid barcode rejection;
- exact-versus-ambiguous identity states;
- variant safety tests.

### P2 — Price-policy hardening

- adversarial policy suite;
- robust historical/deal-band rule;
- condition separation;
- landed-cost logic;
- confidence/provenance.

### P3 — Connector contract & market-data strategy

- ShopSavvy validated/prototyped if practical;
- direct-source lanes validated;
- recorded fixtures;
- graceful degradation and rate-limit behavior.

### P4 — App/API architecture

- architecture decision record;
- typed API contract;
- mobile skeleton;
- barcode capture route;
- URL/share route;
- photo/image route seam.

### P5 — Watch service

- persisted watch model;
- scheduler abstraction;
- deterministic trigger logic;
- notification adapter abstraction.

### P6 — Financial integration seam

- typed financial-result contract;
- safety-veto tests;
- `SAFE_WITH_PLAN` handling documented;
- no finance logic duplicated unnecessarily.

### P7 — End-to-end vertical slice

- scan/input -> identity -> price data -> timing -> financial gate -> decision -> watch;
- deterministic fixture replay;
- API/client integration test.

### P8 — Security/privacy/adversarial gate

- malformed URLs;
- malicious text/image evidence;
- cross-user isolation design;
- secret scanning;
- stale data;
- connector failures;
- confidence-gate bypass attempts.

### P9 — Release candidate

- all tests green;
- product/app/spec docs synchronized;
- no secrets;
- no provider credentials committed;
- integration plan for main Buy or Wait? repo;
- Git diff reviewed;
- **STOP BEFORE PUSHING TO GITHUB.**

---

## Instruction 18 — Iterate autonomously

Within this isolated lab, do not stop for routine implementation decisions.

When a test fails:

1. diagnose the underlying defect;
2. fix the implementation or invalid test assumption;
3. rerun the narrow test;
4. rerun the complete suite;
5. continue if green.

Do not ask permission to create normal source/test/docs files.

Do not push to GitHub.

STOP only when:

- external credentials or partner access are actually required for the next live-provider step;
- a provider's legal/access terms make the proposed integration inappropriate;
- architecture requires changing the active hackathon repository;
- a product/financial-safety requirement is genuinely contradictory;
- destructive action would affect unrelated user work.

If a live credential is unavailable, continue everything possible with recorded fixtures and adapter contracts.

---

## Instruction 19 — Required final evidence

Before declaring P9 ready, produce:

- complete pytest result;
- coverage or equivalent test inventory;
- intake/identity test report;
- price-policy adversarial report;
- connector capability/access report;
- provider fixture manifest;
- app architecture decision record;
- API contract/OpenAPI output if FastAPI is selected;
- mobile vertical-slice evidence;
- watch-service test report;
- financial-veto integration report;
- security/privacy review;
- dependency/license review;
- competitive differentiation update;
- Git status/diff summary;
- exact remaining blockers;
- recommended integration plan into the main Buy or Wait? repository.

# Notes

- **Do not push to GitHub.** The user wants review before push.
- Do not touch the active `/home/jd/hackerrank-orchestrate-september26` checkout.
- Preserve financial safety veto authority.
- Do not hardcode products, retailers, sample answers, or provider response fixtures into production decision logic.
- Do not use binary floating-point for financial or price-decision arithmetic.
- Do not silently resolve ambiguous products.
- Do not mix conditions in price histories.
- Prefer official APIs/feeds over scraping.
- Treat ShopSavvy as both a competitor and an optional V1 data provider, not as the product's decision engine.
- The strategic differentiation is the **combined purchasing decision**, not barcode scanning alone.

At the end, report:

1. highest completed promotion stage;
2. PASS/FAIL for each stage;
3. total tests and failures;
4. major architecture changes;
5. live connectors actually validated;
6. exact credentials/access still needed;
7. security/privacy blockers;
8. current Git status;
9. files changed;
10. recommendation: `READY FOR REVIEW BEFORE GITHUB PUSH` or `NOT READY — <specific blockers>`.
