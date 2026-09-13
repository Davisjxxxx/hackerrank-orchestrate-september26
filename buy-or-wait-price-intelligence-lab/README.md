# Buy or Wait? — production-shaped finance service

Buy or Wait? combines a user's actual cash-flow capacity with an optional
product-price signal. Financial safety remains the veto: the price engine may
say a deal is good, but it cannot make an unsafe purchase safe.

## Architecture

`finance_platform` is independent of the legacy fixture-backed price package.
Connectors first preserve immutable raw payloads, then normalize to canonical
events. The canonical state service resolves lifecycle and evidence semantics;
the recurring detector produces confidence- and provenance-bearing streams;
the deterministic affordability service performs all forecast arithmetic.

The existing `price_intel` package remains a separate product-price lane. The
`BuyOrWaitService` composes it with financial capacity without allowing price
data to bypass the minimum-balance safety check.

## Local start

```bash
python -m pip install -e '.[dev]'
alembic upgrade head
PYTHONPATH=src uvicorn finance_platform.main:app --reload
```

Use `X-User-Id: demo-user` only in development, or use
`Authorization: Bearer user:demo-user`. Production authentication must replace
the development identity adapter before deployment.

Run the credential-free workflow:

```bash
./scripts/demo_local_real_ingestion.sh
```

Run tests and the organizer-runtime dependency gate:

```bash
python -m pytest -q
PYTHONPATH=src python scripts/check_no_hackathon_runtime_dependencies.py
```

## API examples

Create a local user:

```bash
curl -X POST 'http://localhost:8000/v1/users?user_id=demo-user'
curl -X PUT http://localhost:8000/v1/profile -H 'X-User-Id: demo-user' \
  -H 'Content-Type: application/json' \
  -d '{"home_currency":"USD","current_available_cash":"3000","minimum_balance_to_keep":"1000","payment_methods":["full_payment","wait","partial_payment"]}'
```

Import a CSV statement with `POST /v1/imports/transactions` and preview it
first with `/preview`. Submit an affordability request to `POST /v1/decisions`:

```json
{"amount":"1000","currency":"USD","description":"Laptop","category":"electronics","allows_partial_payment":true}
```

Useful read routes are `GET /v1/state`, `GET /v1/decisions/{id}`,
`GET /v1/connectors`, `GET /v1/connections`, and `GET /v1/accounts`. Documents
are uploaded to `POST /v1/documents`.

The combined beta endpoint is `POST /v1/buy-or-wait`:

```json
{"product_name":"55-inch OLED TV","merchant":"Example Retailer","price":"899.99","currency":"USD","category":"electronics","allows_partial_payment":true,"price_context":{"historical_prices":["999.99","949.99","899.99"]}}
```

It returns separate price and financial verdicts, confidence values, the
financial-state freshness/as-of timestamp, the safe amount, and one composed
action such as `BUY_NOW`, `WAIT_FOR_PRICE`, `WAIT_FOR_CASH_FLOW`,
`USE_PAYMENT_PLAN`, or `DO_NOT_BUY`.

## Data and security

PostgreSQL is the production database target; SQLite is supported for local
tests. Alembic owns the schema migration. Raw provider records are immutable,
canonical events retain source IDs, and user-scoped queries prevent cross-user
reads. Pending credits are not spendable; pending debits are reserved. One-time
credits do not recur, and uncertain document/email facts remain review-only.

Plaid is read-only and Sandbox-ready. Gmail requests read-only OAuth scope.
Uploaded files are size/type checked and stored outside the public web root.
Provider tokens require `FINANCE_TOKEN_ENCRYPTION_KEY` and are never returned
by API responses. See `docs/security/THREAT_MODEL.md`.

For the beta acceptance boundary, run `./scripts/acceptance_plaid_sandbox.sh`.
Without Plaid credentials it exits with `PLAID CREDENTIALS REQUIRED`; the
deterministic local CSV path remains fully usable.
