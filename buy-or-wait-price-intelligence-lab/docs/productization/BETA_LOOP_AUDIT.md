# Beta loop audit

- `src/finance_platform/connectors/plaid.py` owns Link, token exchange,
  accounts/balances, and incremental Transactions Sync.
- `src/finance_platform/ingestion.py` stores immutable raw payloads,
  normalizes transactions, and reconciles duplicate, pending→posted, and
  removed lifecycles into one canonical event.
- `src/finance_platform/canonical.py` rebuilds user-scoped state, recurring
  streams, pending obligations, provenance summaries, and freshness.
- `src/finance_platform/affordability.py` performs deterministic 90-day
  minimum-balance forecasting and payment-plan checks.
- `src/finance_platform/composition.py` keeps price intelligence and
  affordability separate, then composes one beta action.
- `src/finance_platform/api.py` exposes finance, connector, state, and
  `POST /v1/buy-or-wait` routes. `auth.py` selects development identity or
  production JWT validation by environment.
- `apps/mobile/App.tsx` remains the existing purchase UI shell; it now has a
  real-finance beta panel for connect/refresh, purchase entry, and composed
  result display. Its legacy fixture journey is preserved only for regression.

The backend loop is runnable without organizer data and has deterministic
tests. Live Plaid requires owner credentials and a running callback deployment.
Native Plaid Link/file-picker UX, Gmail, OCR, and background queues remain
later-sprint seams; the current mobile panel exposes the authenticated API
boundary and honest sync states.
