# Buy or Wait? Price Intelligence — Independent Red-Team Report

**Review target:** `b081c490df5222314b2c815dea12e41438207b99`  
**Archive SHA256 verified:** `48b5f5ea38ba4be3ca6ffc283929be72839397e94c82ff1f4dfb2580fb0cfd6c`  
**Archive integrity:** PASS — 68 entries, no path traversal, no symlinks  
**Existing suite:** 49/49 PASS  
**Independent adversarial suite:** 19/19 safety/correctness regressions FAIL against current RC  
**Recommendation:** **NO-GO for GitHub promotion as a release-ready build. Remediate and rerun.**

## Executive finding

The architecture is directionally strong, but the independent sweep found several trust-boundary and data-integrity defects not covered by the existing 49 tests. The most serious issue is that the public evaluation endpoint can treat a request as financially safe without an authoritative financial result. A client may omit financial data entirely or self-assert `safe_now`; stale/unknown coverage and even `safe_amount_today=0` do not stop the financial gate from passing.

A second critical issue is shared price-history poisoning: an untrusted user-captured price is written directly into the global canonical observation store and immediately changes recommendations for the product. In the reproduction, the same product changed from `hold_for_price` to `buy_now` after injecting a $1 captured price.

## Critical blockers

### RT-C01 — Financial safety is client-asserted and defaults fail-open

**Affected:** `src/price_intel/api/app.py:49-65, 179-205`; `src/price_intel/engine.py:239-260`

- `EvaluatePayload.financial_state` defaults to `SAFE_NOW`.
- `POST /v1/products/{product_id}/evaluate` accepts the financial result directly from the untrusted API caller.
- `financial_coverage_state`, `financial_data_as_of`, `safe_amount_today`, and the payment-plan contents are not used to validate the safety assertion.
- Empty `{}` evaluation returned HTTP 200 with `FINANCIAL_GATE_PASSED` and `financial_state=safe_now`.
- `safe_amount_today=0` plus `financial_coverage_state=stale` still returned a normal purchase timing recommendation with `FINANCIAL_GATE_PASSED`.

**Required remediation:** remove fail-open defaults; separate public purchase request from internal/authoritative financial result; require authenticated server-side financial-engine result or signed/internal service object; reject UNKNOWN/STALE coverage for `SAFE_NOW`; verify internally consistent amount/date/payment-plan semantics before composition.

### RT-C02 — Global first-party history is poisonable by untrusted captured prices

**Affected:** `src/price_intel/api/app.py:111-160`; `src/price_intel/observation_store.py`

- Barcode intake can append arbitrary user-observed price/timestamp/retailer data directly to the canonical global product history.
- There is no user/tenant/trust partition on observations.
- User-captured observations are treated with default match confidence 1 and participate in the price engine like provider observations.
- Reproduction: baseline decision `hold_for_price`; submit a $1 captured price for the exact GTIN; next evaluation becomes `buy_now`.

**Required remediation:** partition user-observed offers from trusted market history; assign trust/provenance class; require verification/corroboration before global promotion; never let one user mutate shared canonical market history; add anti-poisoning and tenant tests.

### RT-C03 — Financial decision records are unauthenticated and leak financial data

**Affected:** `src/price_intel/api/app.py:263-268`

- `GET /v1/decisions/{decision_id}` has no identity or authorization check.
- Stored response includes `safe_amount_today`, financial reason codes, financial state, and evidence.
- Reproduction: decision containing `safe_amount_today=123.45` and `PRIVATE_REASON` was retrievable with no authentication.

**Required remediation:** authenticated subject identity, decision ownership, authorization checks, opaque high-entropy IDs, tenant-scoped persistence, and privacy-safe response/log policies.

### RT-C04 — Authentication model is not production-safe

**Affected:** `src/price_intel/api/app.py:231-261`

`X-User-Id` is caller-controlled and defaults to `anonymous`. This means watch ownership is spoofable and all clients that omit the header share an identity. This was already documented as a production gap and remains a hard blocker for public deployment.

## High-severity correctness/integrity findings

### RT-H01 — Mixed-currency selection is order-dependent

**Affected:** `src/price_intel/engine.py:56-59, 367-373`

`_ordered_values()` removes duplicate currencies before `_most_common()` counts them. Therefore every remaining currency has count 1 and the first distinct currency wins.

Reproduction with identical observations reordered:

- USD-first: `BUY_NOW`, USD, 10 history points.
- EUR-first: `SET_PRICE_WATCH`, EUR, 2 history points.

Same evidence set, different order, different recommendation.

**Fix:** count currencies before de-duplication or explicitly partition by intended transaction currency. Add permutation invariance tests.

### RT-H02 — Unknown provider condition fails open as NEW

**Affected:** `src/price_intel/connectors/live.py:165-173`

Unknown or missing conditions map to `Condition.NEW`. A used/damaged/unknown listing can contaminate new-item pricing.

**Fix:** add `UNKNOWN` condition or reject/quarantine unknown mappings. Never default unknown to NEW.

### RT-H03 — Partial ShopSavvy offer data is aggressively fabricated

**Affected:** `src/price_intel/connectors/live.py:146-162`

An offer containing only `{"price":"10"}` becomes:

- observed now,
- NEW,
- available/in-stock,
- USD,
- free shipping.

This contradicts the documented fail-closed boundary.

**Fix:** require explicit fields needed for decision eligibility; represent missing condition/availability/currency/shipping as unknown; quarantine incomplete rows until policy allows them.

### RT-H04 — Negative shipping and non-finite money bypass domain invariants

**Affected:** `src/price_intel/models.py:80-101`; `src/price_intel/engine.py:49-55`; connector mapping

`PriceObservation` has no domain-level validation. Direct/provider construction accepts negative shipping and `Decimal('NaN')`.

Reproductions:

- price 10, shipping -100 -> landed price -90 and `buy_now`.
- NaN price -> `decimal.InvalidOperation` crash.

**Fix:** enforce finite non-negative price/shipping and valid confidence/currency at `PriceObservation` construction or a single mandatory factory. Do not rely only on Pydantic client validation.

### RT-H05 — Stale freshness flag is ignored by price engine

**Affected:** `src/price_intel/engine.py:49-73`; `EnginePolicy.stale_history_days` unused

A current timestamped observation explicitly marked `freshness="stale"` was selected as the current $1 offer and produced `buy_now`.

**Fix:** define freshness semantics once; exclude explicit stale/invalid freshness from current offers; remove or use the currently dead `stale_history_days` policy.

### RT-H06 — Amazon host spoofing permits false exact ASIN identity

**Affected:** `src/price_intel/intake.py:229-252`

`_extract_amazon_asin` only checks whether `"amazon."` occurs anywhere in the host. `https://notamazon.com/dp/B0CHX3TW6K` extracts the ASIN and resolves the fixture product exactly.

**Fix:** use parsed hostname and a strict supported Amazon-domain allowlist/registrable-domain check.

### RT-H07 — Same GTIN with contradictory variant data silently resolves EXACT

**Affected:** `src/price_intel/resolver.py:54-70, 111-122`

`_materially_different` returns immediately on equal GTINs and does not compare variant/model conflicts. Two candidates with the same GTIN but storage `128GB` vs `1TB` resolve to the first candidate instead of `NEEDS_CONFIRMATION`.

**Fix:** strong identifiers should normally unify identity, but contradictory price-relevant attributes from providers must create a conflict state and require reconciliation/confirmation rather than arbitrary first-candidate selection.

### RT-H08 — Canonical product ID fragments as metadata becomes richer

**Affected:** `src/price_intel/resolver.py:31-38`

The ID hashes all known identifiers and metadata. The same exact GTIN receives different canonical product IDs when ASIN/brand/model fields are later added. This fragments first-party price history across records representing the same SKU.

**Fix:** canonical ID should be based on a stable hierarchical primary identity key (for example normalized GTIN first; otherwise ASIN; otherwise brand+MPN/model+variant), while enrichment remains attributes, not identity-key churn.

### RT-H09 — Invalid watch product silently watches a different product

**Affected:** `src/price_intel/api/app.py:231-250`

If `product_id` is absent or invalid, the endpoint silently uses `next(iter(state.products))`. Reproduction requested `does-not-exist` and received a watch for the demo OLED TV.

**Fix:** 404/422 on invalid explicit product ID. Never substitute another product.

### RT-H10 — Watch refresh persists observations before eligibility/trust filtering

**Affected:** `src/price_intel/watch.py:176-209`

The service appends observations to first-party history before checking availability, accepted condition, source restrictions, retailer restrictions, or staleness.

Reproduction: an unavailable USED observation from disallowed source `evil` was rejected for the watch but still stored as first-party history.

**Fix:** canonical ingestion needs its own trust/validation policy; only eligible or explicitly quarantined observations should enter decision history.

### RT-H11 — Client-controlled naive `as_of` causes HTTP 500

**Affected:** `src/price_intel/api/app.py:65, 184`; engine timezone math

`as_of="2026-09-12T12:00:00"` is accepted by Pydantic but is timezone-naive and causes a 500 during aware/naive datetime subtraction.

**Fix:** reject timezone-naive externally supplied timestamps with 422; ideally do not expose arbitrary `as_of` in production purchase evaluation.

### RT-H12 — ShopSavvy barcode-only offer lookup sends GTIN as ASIN

**Affected:** `src/price_intel/connectors/live.py:66-73`

When a product has GTIN but no ASIN, `key=product.gtin` is still sent as `{"asin": key}`.

**Fix:** choose the correct provider parameter (`asin` vs `barcode`/GTIN) based on identifier type and test both paths.

### RT-H13 — eBay configuration status checks a nonexistent environment variable

**Affected:** `src/price_intel/connectors/live.py:121-129`

The eBay adapter uses credential string `EBAY_CLIENT_ID/EBAY_CLIENT_SECRET` and calls `os.getenv()` on that literal combined name. Setting both real env vars still reports `configured=False`.

**Fix:** provider status needs multi-credential requirements rather than one string env name.

### RT-H14 — Provider response parsing can crash instead of fail closed

**Affected:** `src/price_intel/connectors/live.py:41-43, 146-150`

- `{"products": []}` causes `IndexError`.
- offer with no price/current_price causes `decimal.InvalidOperation`.

**Fix:** schema validation + connector-specific normalization errors; malformed rows should be rejected/quarantined, not crash the service.

## Medium findings

### RT-M01 — Watch notifications are not idempotent

**Affected:** `src/price_intel/watch.py:210-221`

The same target-reached and max-wait events fire on every refresh. There is no persisted trigger state, dedupe key, or notification cooldown.

### RT-M02 — Deal recurrence estimate is optimistic

**Affected:** `src/price_intel/engine.py:287, 306-316`

Estimated wait uses `span_days / episodes`. For two separated deal episodes, the observed interval is closer to `span/(episodes-1)`. Current formula can understate expected wait and move a result from watch to hold.

### RT-M03 — Financial safety payload contents are not consistency-checked

Beyond C01, `safe_amount_today`, `minimum_balance`, payment plan, financial coverage and data timestamp are effectively evidence-only. Internal integration should validate state invariants even after authoritative service separation.

## Product/runtime gaps uncovered by code inspection

These are not necessarily defects in a lab skeleton, but they prevent describing the build as a deployable end-user app today.

1. **Live connectors are not wired into the API decision path.** `build_provider_adapters()` is used only by `/v1/connectors`; intake uses `FixtureProductResolver`, and evaluations use only the in-memory observation store. A ShopSavvy API key would not make live decisions work without integration.
2. **Barcode/camera/image-picker UI is not implemented.** `apps/mobile/App.tsx` does not import/use `expo-camera`, `expo-image-picker`, or `expo-linking`. The buttons send the text-field contents to API endpoints.
3. **Photo bytes/OCR/vision are not implemented.** The photo endpoint accepts an `image_ref`; live OCR/visual resolution is absent.
4. **Watches do not run in the deployed API.** Scheduler/notification abstractions exist, but there is no background runtime wiring in FastAPI.
5. **Persistence is process-local.** Restart loses products, observations, decisions, and watches.
6. **No live provider has been validated.** This is correctly documented and should remain explicit.

## Documentation mismatch

`SECURITY_PRIVACY_REVIEW.md` says "Watch and decision reads are user-scoped by repository key." Watch repository keys are user-scoped only by spoofable `X-User-Id`; decision reads have no user scope at all. The document also says provider/mixed-currency failures fail closed, which is contradicted by unknown-condition defaults and order-dependent currency selection.

Update security evidence only after controls exist in code.

## Independent regression evidence

A new 19-test independent suite was executed against the untouched RC. All 19 tests failed, each representing an expected safety/correctness invariant absent from the current implementation.

The suite covers:

- financial-gate fail-open/defaults;
- stale financial coverage;
- shared price-history poisoning;
- unauthenticated financial decision reads;
- Amazon-domain spoofing;
- invalid watch-product fallback;
- unknown condition handling;
- ShopSavvy GTIN parameter selection;
- negative/non-finite money;
- contradictory same-GTIN variants;
- mixed-currency order invariance;
- explicit freshness enforcement;
- timezone-naive `as_of` handling;
- watch ingestion trust filtering;
- notification idempotency;
- stable canonical product IDs;
- partial provider-response fail-closed behavior;
- eBay multi-secret configuration.

## Required remediation gate

Before GitHub promotion as a release candidate:

1. Fix RT-C01 through RT-C04.
2. Fix all RT-H01 through RT-H14 or explicitly remove/defer the affected feature from the release contract.
3. Add the independent tests to the repository as regression coverage.
4. Existing 49 tests must remain green.
5. New independent suite must be green.
6. Add tests proving test-order/permutation invariance for price observations.
7. Re-run secret/dependency/typecheck/OpenAPI gates.
8. Update SECURITY_PRIVACY_REVIEW.md and RELEASE_CANDIDATE.md to reflect only implemented controls.
9. Repackage and run a second independent red team before push.

**Target post-remediation baseline:** at least **68/68 Python tests PASS** (49 existing + 19 independent), plus mobile typecheck/config/audit.
