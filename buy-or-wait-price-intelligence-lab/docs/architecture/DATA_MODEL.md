# Data model

Alembic migration `0001_real_world_finance` creates:

`users`, `financial_profiles`, `source_connections`, `source_accounts`,
`connector_sync_runs`, `connector_cursors`, `raw_ingestion_records`,
`financial_events`, `evidence_messages`, `evidence_documents`,
`evidence_images`, `evidence_facts`, `event_evidence_links`,
`recurring_streams`, `recurring_stream_occurrences`, `decision_requests`,
`decision_results`, `decision_evidence`, `payment_options`, and
`exchange_rates`.

Raw records are append-only and uniquely keyed by provider, connection,
external ID, and payload hash. Canonical events preserve provider/external IDs,
lifecycle status, amount/currency, account, confidence, and recurrence
eligibility. Derived streams preserve supporting event IDs and reason text.

Production target is PostgreSQL through SQLAlchemy 2.x. SQLite is used for
isolated local acceptance tests through the same ORM metadata.
