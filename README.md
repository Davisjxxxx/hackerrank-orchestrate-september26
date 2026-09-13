# Buy or Wait? — real-world product branch

This branch turns the prototype into a provider-neutral financial decision
service. The product path is `buy-or-wait-price-intelligence-lab/`; the
historical HackerRank files at repository root are not imported by the
production finance package.

```bash
cd buy-or-wait-price-intelligence-lab
python -m pip install -e '.[dev]'
alembic upgrade head
PYTHONPATH=src uvicorn finance_platform.main:app --reload
```

The no-credential acceptance path is:

```bash
./scripts/demo_local_real_ingestion.sh
```

The API requires a user-scoped development identity (`X-User-Id`) locally or
`Authorization: Bearer user:<id>` in production-style requests. See
`docs/LOCAL_DEVELOPMENT.md` and `docs/architecture/REAL_WORLD_ARCHITECTURE.md`.

The service is read-only with respect to financial institutions. Credentials
for Plaid and Gmail are never committed; configure them only through the
environment variables described in `.env.example`.
