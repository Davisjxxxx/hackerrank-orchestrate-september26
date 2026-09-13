# Real-world architecture

```text
Plaid / Gmail / CSV-OFX / documents / FX
        -> immutable raw ingestion + sync cursor
        -> normalizer + lifecycle resolver + provenance
        -> canonical events and evidence facts
        -> recurring stream detector
        -> canonical state service
        -> deterministic 90-day affordability service
        -> decision request/result API
```

Connectors are provider-neutral and expose `connect`, `disconnect`, `sync`,
`refresh`, and `health`. A connector never hands provider objects to the
decision engine. Sync diagnostics are persisted as `connector_sync_runs` and
cursors as `connector_cursors`; a queue adapter can replace the local inline
runner for production.

The current finance implementation is deterministic. It uses settled events
for recurrence, excludes pending credits from cash, reserves pending debits,
ignores cancelled/failed/unrealized records, treats explicit internal
transfers as neutral, and gives uncertain evidence a review state. All output
includes evidence counts and stream source IDs.

The existing price-intelligence service is intentionally separate. A future
composition layer can produce `good price + affordable`, `good price + wait
for cash`, or `bad price + affordable` without allowing the price signal to
override financial safety.
