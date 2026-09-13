# Buy or Wait? repository reconciliation

## Decision

The canonical product shell is `buy-or-wait-price-intelligence-lab/`. It is
the more complete and current implementation: its source includes the
provider-independent price engine, deterministic intake and identity
resolution, trust-partitioned first-party observations, financial safety seam,
authenticated API, watches, connector catalog, mobile shell, and the
remediation/round-2 regression suites. It currently passes 87 Python tests.

`buy-or-wait-price-intelligence-red-team/` is retained as review provenance and
an independent red-team workspace, not as a second application. Its source is
an earlier 49-test snapshot and its archive is a review artifact. Its tests and
reports remain useful for attack-surface traceability; the canonical lab copy
already contains the later independent, round-2, and remediation-boundary
tests.

## Starting truth

- Repository: `/home/jd/hackerrank-buy-or-wait-integration`
- Branch: `product-integration`
- Starting HEAD: `74f44ecb3505aa15ffe16e832f795cce01d7eb09`
- Imported directories: both present and untracked at session start.
- Nested `.git` scan: no nested repository found.
- Separate finance worktree: not accessed or modified.

## Comparison

| Area | Lab | Red-team workspace | Disposition |
|---|---|---|---|
| Production source | Remediated current source | Earlier overlapping snapshot | Lab is canonical |
| Price engine | Currency, trust, freshness, condition controls | Earlier implementation | Reuse lab |
| Financial boundary | Server-side provider seam, fail-closed coverage | Earlier seam | Reuse lab |
| Persistence | In-memory canonical store, now plus SQLite port | Earlier in-memory version | Extend lab |
| API | FastAPI/OpenAPI and subject-scoped reads | Earlier API snapshot | Preserve one lab API |
| Mobile | Expo shell and validation evidence | Earlier shell | Retain only canonical lab shell |
| Adversarial evidence | 19 red-team, 12 round-2, 7 remediation tests | Original red-team snapshot/report | Retain reports; run lab tests |
| Demo data | Sanitized recorded provider fixture | Duplicate archive/fixture | Clearly label as non-live |

## Overlap and contradictions

The projects overlap in `src/price_intel`, `tests`, `apps/mobile`, `docs/openapi.json`,
the API/product specifications, connector guidance, and price policy. The
contradictions are versioned remediation differences, not two product
directions: the red-team snapshot contains the defects described by its first
report, while the lab contains the later fixes and broader tests. Maintaining
both as runnable APIs would make it unclear which trust and financial rules
govern a release.

## Reusable components

Reuse the lab's `models.py`, `intake.py`, `resolver.py`, `engine.py`,
`observation_store.py`, `watch.py`, `connectors/`, `financial.py`, `auth.py`,
and `api/app.py`. The integration lane adds `sqlite_store.py`,
`price_intelligence.py`, `financial_adapter.py`, and `governance.py` around
those stable ports. The red-team reports and tests are evidence, not runtime
dependencies.

## Stale or demo-only artifacts

The recorded ShopSavvy/catalog fixture, `DEMO_NOW`, and the Expo adapter-seam
buttons are deterministic demo/test material. They must remain labelled as
fixture-backed until live providers, native capture, and production identity
are separately validated. `.venv`, `node_modules`, `__pycache__`, and
`.pytest_cache` are local artifacts and are excluded from the checkpoint.
