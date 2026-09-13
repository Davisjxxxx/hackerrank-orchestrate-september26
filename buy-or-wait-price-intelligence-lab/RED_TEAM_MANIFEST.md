# Buy or Wait? Price Intelligence — Round 2 remediation red-team manifest

## Candidate identity

- Starting implementation commit: `29b754bd54c16f307b4ed56d938cbc630b3d9107`
- Final Round 2 remediation commit: `9645fda3aa18ab7fc4525291c1d03dc4c3782563`
- Branch: `main`
- Product implementation status: clean at the implementation commit
- Current packaging status: handoff metadata is maintained as a review overlay; implementation changes are committed locally before archive creation
- Original reviewed commit: `b081c490df5222314b2c815dea12e41438207b99`

## Verification results

- Python: `Python 3.13.0`
- Node: `v22.18.0`
- npm: `11.16.0`
- Expo package: `57.0.22`
- TypeScript package: `5.8.3`
- Original supplied suite: `49 passed`
- Independent red-team suite: `19 passed`
- Round 2 independent red-team suite: `12 passed`
- Additional remediation/regression tests: `7 passed`
- Total Python suite: `87 passed`
- TypeScript validation: PASS — `npm run typecheck`
- Expo validation: PASS — `npx expo config --json`
- Dependency tree: PASS — `npm ls --all --depth=2`
- Python dependency audit: PASS — `.venv/bin/python -m pip check`
- Node dependency audit: PASS — `npm audit --omit=dev --audit-level=high`, 0 vulnerabilities
- Secret scan: PASS — no credential-shaped values in source, docs, tests, or fixtures
- OpenAPI: regenerated at `docs/openapi.json`
- Round 2 cache hygiene: PASS — archive staging excludes `.git`, `.venv`, `node_modules`, Python/Expo/build caches, and OS metadata
- Final ZIP SHA256: supplied in the detached `.sha256` sidecar because embedding an archive's own digest is circular

## Exact verification commands

```bash
cd /home/jd/buy-or-wait-price-intelligence-lab
python -m pytest -q tests/test_independent_redteam.py
python -m pytest -q tests/test_independent_redteam_round2.py
python -m pytest -q
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
PYTHONPATH=src python scripts/generate_openapi.py
cd apps/mobile
npm run typecheck
npx expo config --json
npm ls --all --depth=2
npm audit --omit=dev --audit-level=high
```

## Architecture implemented

Product intake normalization -> identity resolver -> stable canonical product -> provider-independent connector protocols -> trust-partitioned canonical observations -> Decimal price policy -> server-side financial safety provider -> combined decision -> subject-scoped watch/decision service. The deterministic core remains independent of React Native, Expo, FastAPI, provider SDKs, camera/OCR, notification vendors, and database vendors.

## Connector adapters

- `ShopSavvyAdapter`: implemented, sanitized-fixture tested, server-side credential boundary.
- `RecordedCatalogConnector`: deterministic fixture connector.
- `UnconfiguredProviderAdapter`: explicit fail-closed seams for Keepa, eBay Browse, Best Buy, SerpApi Google Shopping, and Slickdeals.
- Keepa: optional Amazon-specific validation/backfill only; not required for V1, CI, promotion gates, or normal watch refreshes.
- First-party history: `InMemoryObservationStore`, with trusted/corroborated shared history and user-private capture partitions.

## Live and fixture validation

- Live providers actually validated: none; no live credentials were used.
- Fixture-only validation: ShopSavvy normalization/rate-limit/error behavior and recorded catalog observations.
- Credentials still needed for optional live validation: `SHOPSAVVY_API_KEY`, `KEEPA_API_KEY` (optional only), both `EBAY_CLIENT_ID` and `EBAY_CLIENT_SECRET`, `BESTBUY_API_KEY`, `SERPAPI_API_KEY`, and `SLICKDEALS_TOKEN`, all server-side.

## Independent findings disposition

- RT-C01: fixed — explicit server-side financial provider seam; missing state is 422; SAFE_NOW requires full coverage; contradictions fail closed.
- RT-C02: fixed — user captures are `USER_PRIVATE` and tenant-partitioned; they cannot poison shared provider history.
- RT-C03: fixed — decisions are owned by authenticated subjects; unauthenticated and cross-subject reads fail.
- RT-C04: remediated for the RC seam — fixture bearer authentication is available; legacy `X-User-Id` remains test-only and production token verification is still required.
- RT-H01 through RT-H14: fixed and green in `tests/test_independent_redteam.py`.
- RT2-H01 through RT2-H09: fixed and green in `tests/test_independent_redteam_round2.py`.
- RT2-M01: fixed previously through persisted trigger idempotency and remains green.
- RT2-M02/RT2-M03: fixed at API and domain boundaries with finite-money and supported-condition validation.
- Original RT-M02: safely dispositioned; recurrence requires two episodes and uses inter-episode intervals, while recurrence alone cannot produce `BUY_NOW`.
- Original RT-M03: safely dispositioned; typed financial payload invariants are validated, contradictions use authoritative as-of time, and unsafe/future/stale evidence cannot bypass the financial gate.

## Known production gaps and deferred features

- Replace `FixtureAuthenticator` with production token verification and remove legacy header compatibility.
- Replace the fixture financial provider with the authorized financial engine through `FinancialSafetyProvider`.
- Replace in-memory repositories with durable, encrypted, tenant-scoped persistence and transactional refresh/idempotency.
- Wire a production scheduler/queue and notification provider; the in-memory scheduler remains a port.
- Wire native barcode/camera/image-picker/share/OCR adapters and run device-bound permission/privacy tests; the mobile shell currently exposes adapter-seam actions only.
- Add image upload malware scanning, EXIF stripping, short-lived signed references, deletion-after-resolution, request limits, and SSRF defenses before fetching arbitrary URLs.
- Complete deployment-specific SBOM/license/vulnerability evidence and live provider terms validation.

## Archive digest note

The final ZIP digest is authoritative in the detached sidecar and final handoff report. A digest cannot be placed into a file inside the same ZIP without changing the digest itself.
