# Beta acceptance flow

This is the intended end-to-end, read-only user loop:

```text
CONNECT → SYNC → CANONICALIZE → FORECAST → PRICE ANALYSIS
        → AFFORDABILITY → COMPOSE → DISPLAY
```

## Local, no-credential path

Run `./scripts/demo_local_real_ingestion.sh` to create synthetic local data,
import a statement, detect recurring salary/rent/utilities, reserve a pending
debit, exclude a pending credit, and evaluate a purchase. The fixture is new
developer test data and is not organizer data.

## Connected-account path

The mobile/API flow is:

1. Authenticate the beta user and create a Plaid Link token.
2. Complete Plaid Link in Sandbox and exchange the public token.
3. Refresh the connection. The server stores account balances, the incremental
   cursor, immutable raw payloads, and canonical events.
4. Repeated sync is idempotent; pending→posted uses Plaid's lifecycle link and
   removed transactions cancel the canonical effect without deleting raw data.
5. `GET /v1/state` exposes only user-scoped state, freshness, pending
   obligations, and recurring-stream summaries.
6. Submit the contemplated purchase to `POST /v1/buy-or-wait`. Price evidence
   and financial capacity are evaluated independently and composed into one
   recommendation.

Live Sandbox execution requires the credentials listed in
`docs/NEXT_EXTERNAL_CREDENTIALS.md`. Without them, the acceptance script fails
clearly and the local import path remains the supported beta demonstration.
