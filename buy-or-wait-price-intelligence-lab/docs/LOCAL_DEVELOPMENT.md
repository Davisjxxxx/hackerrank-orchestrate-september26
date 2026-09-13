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
