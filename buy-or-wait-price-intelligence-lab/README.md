# Buy or Wait? — Price Intelligence & Purchase Decision App Lab

This is an **isolated prototype lane** for evolving Buy or Wait? from a financial affordability agent into a deployable purchase-decision application.

It remains separate from the active hackathon runtime so it can be iterated without destabilizing the scored S1–S19 build.

## Product vision

A user should eventually be able to:

- scan a barcode in a store;
- take a live photo of the item, label, or shelf tag;
- upload a screenshot/photo;
- paste or share a product link;
- search/type a product;

and receive one decision that combines:

> **Can I safely afford this?**

with:

> **Is this a strategically good time and price to buy it?**

Financial safety always has veto authority.

## Current lab capabilities

- canonical product identity model;
- deterministic product-intake normalization;
- GTIN-8/12/13/14 check-digit validation and canonical GTIN-14 representation;
- URL normalization and safe Amazon ASIN extraction;
- source-agnostic product-resolution connector protocol;
- current offers and first-party historical price observations with identity, variant, condition, provenance, freshness, shipping, and currency;
- condition-aware price comparison so new/used/refurbished/open-box are not mixed;
- deterministic historical percentile / median / quartile calculations;
- target-buy-price estimation;
- deal-frequency and estimated-wait heuristics;
- urgency-aware timing decisions;
- used/refurbished alternative recommendation;
- server-side financial-safety provider seam with fail-closed coverage checks;
- trust-partitioned first-party observations: provider history versus user-private captures;
- fixture-backed subject authentication and tenant-scoped watch/decision reads;
- connector capability catalog;
- initial regression tests.

Integration-lane additions:

- `price_intelligence.py` exposes a machine-readable price record;
- `sqlite_store.py` provides durable first-party history behind the observation port;
- `governance.py` implements synthesis, adversarial review, certification,
  committee selection, and the deterministic release veto;
- `financial_adapter.py` protects the finance-core convergence boundary;
- `POST /v1/products/{product_id}/governed-evaluate` exposes governance state
  in the existing API without accepting client-controlled finance arithmetic.

Current test baseline:

```text
71 passed (49 supplied, 19 independent red-team, 3 remediation-boundary)
```

The lab is now fixture-backed release-candidate work: FastAPI/OpenAPI, an Expo mobile shell, a first-party canonical observation store, decision-aware watches, optional provider adapters, financial-veto composition, and adversarial regression coverage. User-captured prices are private evidence and do not mutate shared provider history. Keepa is optional Amazon-specific validation/backfill only and is not required for CI, V1, or watch refreshes.

## Intended user decisions

- `BUY_NOW`
- `HOLD_FOR_PRICE`
- `SET_PRICE_WATCH`
- `CONSIDER_USED_OR_REFURBISHED`
- `FINANCIALLY_WAIT`
- `DO_NOT_BUY`

## Connector direction

### Aggregation accelerator

1. **Authorized current/bootstrap sources** — ShopSavvy, eBay Browse, Best Buy, and other sanctioned feeds are normalized once into first-party history; no provider is mandatory.

### Direct / validation sources

2. Keepa — optional Amazon-specific historical validation/backfill only; not required for V1, CI, or watch refreshes.
3. eBay Browse API — marketplace listings/conditions.
4. Best Buy APIs — current product/pricing/open-box.
5. SerpApi Google Shopping — broad current-price aggregation if justified.
6. Slickdeals authorized API/partner lane — deal signal.

### Deferred

- CamelCamelCamel automation without an official supported API;
- Brad's Deals without an authorized feed;
- Facebook Marketplace/local marketplace scraping without sanctioned access.

## Product/app architecture

See:

- `APP_PRODUCT_SPEC.md` — mobile-first UI, capture modes, API/backend, persistence, watch flow.
- `PRICE_INTELLIGENCE_SPEC.md` — deterministic price-intelligence and connector contract.
- `COMPETITIVE_LANDSCAPE.md` — current market/GitHub research.
- `CLAUDE_EXECUTION_PROMPT.md` — iterative execution/red-team prompt.

## Run tests

```bash
python -m pytest -q
```

The local API uses `Authorization: Bearer fixture:<subject>` as its fixture authentication seam. The legacy `X-User-Id` header exists only for compatibility with the supplied lab tests and is not production authentication. Native barcode/camera/image-picker/OCR capture, durable persistence, scheduler runtime, and live-provider evaluation remain explicitly deferred adapters.

Run the deterministic product stories with:

```bash
PYTHONPATH=src python scripts/run_governed_demos.py
```

The stories use sanitized fixtures and must not be described as live pricing.
The integration architecture and governance contract are documented in the
repository-level `docs/` directory.

## Promotion rule

Claude may iterate locally and prepare a release candidate, but it must **not push to GitHub** until reviewed and explicitly authorized.
