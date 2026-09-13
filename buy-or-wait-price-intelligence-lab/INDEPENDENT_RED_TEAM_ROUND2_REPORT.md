# Buy or Wait? Price Intelligence — Independent Red Team Round 2

## Review target

- Remediated archive: `buy-or-wait-price-intelligence-red-team-remediated.zip`
- Expected / verified SHA256: `4373c80a76aaa00b6923ea56b43343c4a9c84033a5a2b5b2bcbb04bebdcb83c0`
- Claimed remediation commit: `29b754bd54c16f307b4ed56d938cbc630b3d9107`
- Baseline Python suite from the archive: **71 passed**
- Independent Round 2 adversarial suite: **12 failed / 12 executed**
- ZIP integrity: PASS
- Secret-pattern scan: PASS
- Release hygiene: archive contains 38 cache artifacts (`*.pyc` / `.pytest_cache` entries)

## Verdict

**NOT READY FOR GITHUB PROMOTION AS A GREEN RELEASE CANDIDATE.**

The first remediation successfully closes the original 19 independent regressions, but the second independent sweep found 12 additional correctness/fail-closed gaps. These are primarily concentrated in four seams:

1. price-observation deduplication and currency handling;
2. connector response normalization;
3. financial as-of consistency;
4. watch API/domain validation.

The underlying architecture remains usable. This is another bounded remediation pass, not a redesign.

## Findings

### RT2-H01 — Deduplication collapses distinct currencies and reintroduces order dependence

**Severity:** HIGH

`PriceIntelligenceEngine._deduplicate()` does not include currency in its deduplication key. Two otherwise identical USD and EUR observations collapse to whichever row appears first. Reversing input order changes the selected decision currency.

**Observed:** USD-first => USD; EUR-first => EUR.

**Required fix:** Currency must be part of observation identity/deduplication. The same logical record in two different currencies is not a duplicate unless an explicit normalized-conversion identity says so.

---

### RT2-H02 — A stale duplicate can shadow a fresh duplicate based on input order

**Severity:** HIGH

Freshness is not represented in the deduplication policy and dedup occurs before current-offer freshness filtering. When stale and fresh versions share the current dedup key, stale-first can remove the fresh current offer.

**Observed:** stale-first => `INSUFFICIENT_DATA`; fresh-first => `SET_PRICE_WATCH` with a current price.

**Required fix:** Dedup must deterministically prefer the most trustworthy/fresh/current observation, or include state necessary to avoid collapsing materially different rows.

---

### RT2-M01 — Single-currency history falsely reports `MIXED_CURRENCY_IGNORED`

**Severity:** MEDIUM

The engine sets mixed-currency state using the number of observations rather than the number of distinct currencies.

**Observed:** three USD observations emit `MIXED_CURRENCY_IGNORED`.

**Required fix:** Use the distinct currency set, not list length.

---

### RT2-H03 — Equal mixed-currency counts can yield an arbitrary `BUY_NOW`

**Severity:** HIGH

When currencies tie in frequency, `_most_common` selects lexicographically. With no FX/home-currency context, an immediate purchase can become `BUY_NOW` in whichever currency wins the lexical tie.

**Required fix:** A cross-currency tie without explicit conversion/home-currency authority must fail closed or require confirmation; it must not become a buying recommendation because of alphabetical ordering.

---

### RT2-H04 — Quarantined observations can directly drive the core price engine

**Severity:** HIGH

The observation store excludes quarantined rows, but the provider-independent engine itself does not enforce the observation trust boundary. Passing quarantined observations directly to `evaluate()` can produce `BUY_NOW`.

**Required fix:** The deterministic core should reject/exclude `ObservationTrust.QUARANTINED`. Do not rely solely on every future integration remembering to pre-filter.

---

### RT2-H05 — Unknown provider availability values fail open as trusted/in-stock

**Severity:** HIGH

ShopSavvy normalization uses a deny-list for availability. An unexpected string such as `"banana"` is treated as available and, when the other fields are present, remains `TRUSTED_PROVIDER`.

**Required fix:** Use an explicit allow-list for known available/unavailable states. Unknown availability must be quarantined/unavailable.

---

### RT2-H06 — Malformed provider currency leaks a domain `ValueError`

**Severity:** HIGH

A provider row with currency `US1` reaches `PriceObservation`, whose validation raises `ValueError`. `_shop_savvy_offer_rows()` catches only `ConnectorNormalizationError`, so a malformed external row can escape the connector boundary.

**Required fix:** Validate currency inside connector normalization or wrap domain validation errors as connector normalization failures and drop/quarantine the row.

---

### RT2-H07 — Malformed product payload leaks `AttributeError`

**Severity:** HIGH

`ShopSavvyAdapter.resolve_product()` assumes the selected `product` is a mapping. A string/object of the wrong shape causes `.get()` to raise `AttributeError` instead of a connector-specific fail-closed error.

**Required fix:** Validate product, identifiers, and specifications shapes before dereferencing them; raise `ConnectorNormalizationError` or skip malformed candidates.

---

### RT2-H08 — Provider search discards all but the first candidate

**Severity:** HIGH

`ShopSavvyAdapter.resolve_product()` returns only `products[0]`. This bypasses the architecture's ambiguity/variant gate because downstream identity resolution cannot compare the other candidates.

**Required fix:** Normalize and return every valid candidate (within a deterministic bounded maximum) so `ProductIdentityResolver` can apply conflict/variant confirmation rules.

---

### RT2-H09 — Financial contradiction logic compares against wall-clock time instead of financial evidence time

**Severity:** HIGH

For `SAFE_NOW`, `earliest_safe_full_payment_date` is compared to `datetime.now()` rather than the authoritative financial evidence timestamp / evaluation time.

**Observed:** financial data as-of 2025-01-01 with earliest-safe-full-payment 2025-01-02 can produce `BUY_NOW` when replayed later, because the date is now in the wall-clock past.

**Required fix:** Financial consistency checks must use the financial/evaluation as-of boundary, never ambient wall clock. The same evidence must replay deterministically.

---

### RT2-M02 — Empty accepted watch conditions produce HTTP 500

**Severity:** MEDIUM

The API accepts `accepted_conditions: []`, then `WatchService.create()` raises an uncaught `ValueError`.

**Required fix:** Enforce at least one accepted condition at the Pydantic/API boundary and translate domain validation errors to 4xx responses.

---

### RT2-M03 — Non-finite watch target is not normalized at the domain boundary

**Severity:** MEDIUM

`Decimal('NaN')` reaches `target_price < 0`, causing `decimal.InvalidOperation` rather than a controlled validation error.

**Required fix:** Central finite/non-negative Decimal validation for watch money fields, independent of API/Pydantic validation.

## Deferred / known production gaps still present

These were already documented by the project and were not counted among the 12 new failures, but they still prevent calling this an internet-deployable end-user product:

- `FixtureAuthenticator` and legacy `X-User-Id` remain lab-only authentication.
- Real financial engine integration is not wired; `FixtureFinancialSafetyProvider` remains the RC provider.
- Live provider adapters are not wired into the intake/evaluation path and no live provider has been validated.
- Mobile “Scan barcode” and “Take photo” actions still send text-field values; native camera/barcode/image-picker/share/OCR flows are not wired.
- Persistence remains in-memory.
- Production scheduler/queue/notification runtime is not wired.
- Image malware/EXIF/retention controls and request/rate limits remain deployment follow-up.

## Release hygiene

The handoff archive contains `__pycache__`, `.pyc`, and `.pytest_cache` artifacts despite the packaging requirement to exclude caches. This is LOW severity but should be cleaned in the next package.

## Required promotion gate after remediation

Do not weaken the new tests. The next candidate must satisfy all of the following simultaneously:

- existing baseline suite: 71/71 PASS;
- Round 2 independent suite: 12/12 PASS;
- total suite: at least 83 PASS (plus any new remediation regressions);
- no skipped/xfail tests used to bypass findings;
- mobile typecheck PASS;
- Expo config validation PASS;
- dependency checks PASS;
- secret scan PASS;
- OpenAPI regenerated;
- cache artifacts excluded from the new handoff ZIP;
- a fresh clean local remediation commit;
- no GitHub push until a third independent verification confirms the package.
