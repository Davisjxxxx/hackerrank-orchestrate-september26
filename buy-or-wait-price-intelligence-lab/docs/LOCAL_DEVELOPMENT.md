# Local development

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
alembic upgrade head
PYTHONPATH=src uvicorn finance_platform.main:app --reload
```

Use SQLite locally by leaving `FINANCE_DATABASE_URL` unset. For PostgreSQL,
set it to a `postgresql+psycopg://...` URL and run the Alembic migration.
Create a development user through `POST /v1/users?user_id=...`, set a profile,
then preview and commit a CSV/OFX/QFX import. No organizer dataset is needed.

`./scripts/demo_local_real_ingestion.sh` runs the full no-credential path with
new synthetic rows. The production server must use a real authentication
provider instead of the development `X-User-Id` compatibility header.

## Beta purchase loop

1. Create a user and profile, or connect the app to an authenticated user.
2. Use Plaid Link and exchange its public token, or import a CSV/OFX/QFX file.
3. Refresh the connection and inspect `/v1/state`, `/v1/accounts`, and
   `/v1/connections`.
4. Post a purchase to `/v1/buy-or-wait`. Price observations supplied in
   `price_context.historical_prices` are explicit user/provider evidence; no
   market price is invented.

The endpoint returns `financial_freshness` (`current`, `stale`, or
`incomplete`) and lowers confidence when a successful sync is missing or old.
Production mode requires a validated OIDC/JWT bearer token and
`FINANCE_JWT_PUBLIC_KEY`; the development identity provider is unavailable
when `ENVIRONMENT=production`.
