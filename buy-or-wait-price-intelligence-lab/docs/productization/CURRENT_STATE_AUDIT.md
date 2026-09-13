# Current-state audit

The finance checkout at `2465196` is a frozen HackerRank donor containing the
CSV-driven `code/main.py`, OCR/evaluation harnesses, and organizer contract.
The integration checkout at `eb55688` already contains the reusable product
price engine, FastAPI boundary, mobile shell, fixture authentication, SQLite
price history, governance checks, and finance-provider seam. It is the
canonical product destination for this branch.

## Reusable work

- `price_intel.engine`, `statistics`, `models`, and `observation_store` are
  pure Decimal product-price components.
- `governance.py` supplies a financial-veto composition boundary and
  adversarial checks.
- `financial_adapter.py` is a useful provider port, but the old fixture
  provider is not real financial persistence.
- `price_intel.api` is a compatibility/product-price API, not the new
  user-scoped finance API.

## Hackathon assumptions and gaps

The donor's `code/main.py`, root `dataset/`, `output.csv`, sample scoring,
image OCR cache, and `evaluation/` reports are competition artifacts. They are
not imported by `src/finance_platform`. The new runtime dependency gate scans
that package for organizer paths, sample IDs, and output references.

The integration product had no durable canonical financial schema, connector
sync ledger, real transaction-file ingestion, document storage, recurring
stream persistence, user-scoped finance decision API, production auth, or
PostgreSQL/Alembic boundary. Plaid/Gmail existed only as optional price
provider concepts; there was no bank/evidence ingestion pipeline.

## Intended source of truth

`finance_platform` owns users, preferences, raw evidence, canonical financial
events, recurring streams, FX rates, and affordability decisions. Provider
adapters can fetch evidence but cannot call the decision engine directly.
`price_intel` remains an independent price axis. A future composition service
can combine price timing with financial capacity, with financial safety veto.
