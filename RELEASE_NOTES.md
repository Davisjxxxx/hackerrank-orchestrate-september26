# Release notes — HackerRank Orchestrate September 2026 submission

This branch is the packaged release for the HackerRank Orchestrate 24-hour hackathon (September 2026).

## Scored HackerRank solution

The scored challenge is the finance-decision problem defined by `problem_statement.md`.

- Runtime entry point: `python3 code/main.py`
- Reads inputs from `dataset/`
- Writes `output.csv` at the repository root (250 predictions, one per row in `dataset/requests.csv`, exact required schema)
- Frozen R0 SHA256 (`code/main.py`): `7a92094d5999aa9355efc3a07785b4e289aae9a28711a405bc2efd89fd58d1c4`
- Deterministic final `output.csv` SHA256: `580233223fbf85dbd502bbc42143b390e335f1833b0a8dfc052af7af174b4a1d`
- Token/cost report: `evaluation/usage_report.md` — the scored runtime is fully local and makes zero model calls
- Deterministic three-run replay documented in `evaluation/replay_evidence.md`

Only stdlib is required for the scored run. `ImageEvidenceAdapter` optionally uses local PaddleOCR to extract text from packaged image evidence and caches results in `evaluation/ocr_cache.json`; the pre-populated cache is shipped in `code.zip` so a clean-room replay reproduces `output.csv` byte-for-byte without PaddleOCR installed.

Known sample non-exactness is accepted per the forensic audit recorded in `evaluation/s16_semantic_experiment_ledger.md`. R0 is frozen — do not tune against solved rows.

## Supplementary product demo

The `buy-or-wait-price-intelligence-lab/` subtree is a supplementary demonstration of the end-user surface. It is **not** the scored HackerRank artifact.

- Path: `buy-or-wait-price-intelligence-lab/`
- Backend: FastAPI service in `src/price_intel/` with fixture-backed price intelligence, product-identity resolver, adversarial reviewer, certification gate, decision committee, and deterministic finance-safety veto (`src/price_intel/governance.py`).
- Mobile app: Expo + React Native + TypeScript at `apps/mobile/` with barcode / photo / URL / search intake, user-confirmation gate for ambiguous identity, governed evaluation call, decision screen (recommendation, product, price intelligence, financial safety, explanation, governance badges), inline loading and error states, and a fixture-mode banner.
- Deterministic finance veto: a strong price signal cannot override an unsafe finance state. Covered by `tests/test_api.py::test_governed_finance_veto_beats_strong_price_signal` and the confirmed-search variant.
- Baseline test count: **130 backend tests pass**; frontend `npm run typecheck` clean; Expo config validates with `npx expo config --type public`.

The product demo is fixture-backed. Prices come from `src/price_intel/demo.py` and `fixtures/providers/*.json`. Financial safety inputs are demo posture selections. No live retailer feed and no connected financial account are used.

## Mobile app launcher icon

The phone launcher / home-screen icon is packaged in the app assets:

- `buy-or-wait-price-intelligence-lab/apps/mobile/assets/icon.png` (SHA256 `a29facd010896a262e0f19823eb3ff8e5a283573347302a93a473532090fe8a5`, 1254 x 1254)
- `buy-or-wait-price-intelligence-lab/apps/mobile/assets/adaptive-icon.png` (same file for Android adaptive-icon foreground)

Expo is configured to use these files as `icon`, iOS `icon`, Android `icon`, Android `adaptiveIcon.foregroundImage`, and web `favicon` in `apps/mobile/app.json` with a preserved dark `#0d1726` background.

## Submission artifacts

The three files uploaded to HackerRank live in `/home/jd/hackerrank-final-submission/`:

- `code.zip` — full runnable submission including `code/`, `dataset/`, `evaluation/usage_report.md`, the mobile app subtree, the icon assets, and this release notes file.
- `output.csv` — final deterministic finance predictions.
- `chat_transcript.txt` — development log from `log.txt`.

`SUBMISSION_MANIFEST.md` in the same directory records each artifact's SHA256 for the user's reference.
