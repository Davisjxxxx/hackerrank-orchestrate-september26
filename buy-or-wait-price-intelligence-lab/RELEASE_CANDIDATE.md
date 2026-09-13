# Release candidate 0.2.1 evidence

Date: 2026-09-12

## Promotion result

| Gate | Result | Evidence |
| --- | --- | --- |
| P0 baseline integrity | PASS | Supplied baseline was 12 passed; protected hackathon path was not edited. |
| P1 intake and identity | PASS | GTIN-8/12/13/14, ISBN, URL, photo, search, exact-identifier priority, variant ambiguity tests. |
| P2 price policy | PASS | Decimal landed cost, condition separation, winsorized target, quality-aware/currency-aware deduplication, explicit mixed-currency ambiguity, recurrence safeguards, stale/sparse adversarial tests. |
| P3 connectors | PASS | Provider protocols, ShopSavvy server adapter, recorded fixture lane, fail-closed optional provider adapters, first-party observation store. Keepa is optional backfill only. |
| P4 app/API | PASS | FastAPI routes and generated OpenAPI; Expo SDK 57/TypeScript shell with four intake actions. |
| P5 watches | PASS | In-memory persistence port, scheduler port, target/better-deal/good-deal/max-wait triggers, notification port, user scoping. |
| P6 financial integration | PASS | Typed `FinancialSafetyResult`; server-side seam, as-of anchored contradiction checks, future-dated payload confirmation, NOT_AFFORDABLE veto, SAFE_LATER and conservative SAFE_WITH_PLAN regressions. |
| P7 vertical slice | PASS | Barcode -> identity -> first-party fixture history -> price decision -> financial result -> deterministic API decision -> watch creation; URL/photo replay tests. |
| P8 security/adversarial | PASS WITH FOLLOW-UP | Round 1 and Round 2 independent suites, provider fail-closed normalization, engine trust enforcement, watch-domain validation, malformed/malicious/stale/rate-limit/isolation checks, secret scan, and mobile audit. Production token verification, EXIF/upload hardening, and durable tenant persistence remain integration work. |
| P9 release candidate | PASS FOR THIRD INDEPENDENT RED TEAM | 87 Python tests: 49 supplied, 19 Round 1 independent, 12 Round 2 independent, and 7 remediation regressions. Mobile typecheck/config/audit, pip check, OpenAPI regeneration, secret scan, and cache-free archive verification pass. Local Git only; no push. |

## Architecture

`apps/mobile` is an Expo + React Native + TypeScript shell. `src/price_intel/api` is a thin FastAPI boundary. Domain logic remains provider/framework-independent: intake -> resolver -> canonical product -> connector protocols -> canonical first-party observations -> Decimal price policy -> financial safety composition -> decision-aware watch service.

## Provider truth boundary

No live provider credential was available or used. ShopSavvy response mapping and rate-limit behavior were tested with sanitized/monkeypatched fixtures only. Keepa is not required for V1, CI, promotion gates, or normal watch refreshes; it is optional Amazon-specific validation/backfill only. eBay production access is partner-gated per its published requirements. All provider credentials still needed for live validation remain server-side environment/secret-manager inputs.

The system reports a lowest observed price in the covered dataset, not an all-time market low, unless future authorized coverage justifies that claim. Connector/user observations accumulate in the first-party store and are reused by future evaluations and watch refreshes.

## Remaining integration blockers

- Replace the fixture authenticator and legacy `X-User-Id` compatibility path with production token verification before multi-user exposure.
- Replace the fixture financial provider with the authorized financial engine through the same server-side interface; public request fields are not a production financial authority.
- Replace process-local product/observation/decision/watch repositories with durable tenant-scoped persistence and transactional/idempotent refreshes.
- Run a device/simulator build to verify camera permissions, barcode capture, share-sheet delivery, image upload/delete, and real API reachability.
- Obtain authorized provider credentials/terms and record sanitized live fixtures only if incremental decision value justifies cost.
- Add production PostgreSQL/object storage/queue adapters and encrypted financial/notification handling.
- Run deployment-specific SBOM/license/vulnerability scans and a native store build.

Recommendation: **READY FOR THIRD INDEPENDENT RED TEAM**.
