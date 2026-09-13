# Plaid connector

`finance_platform.connectors.plaid.PlaidConnector` is a read-only,
Transactions/Accounts/Balances-oriented adapter. It supports Link-token
creation, public-token exchange, incremental `/transactions/sync`, refresh,
disconnect, and health semantics. Configure `PLAID_CLIENT_ID`, `PLAID_SECRET`,
and `PLAID_ENV=sandbox` locally. Access tokens must be encrypted before storage
and never sent to the frontend. Webhook verification is a deployment gate.

The flow is Link token → public-token exchange → encrypted Item persistence →
account balance sync → incremental Transactions Sync → raw ingestion →
canonical event reconciliation → recurring/state rebuild → composed purchase
decision. Plaid's pending-to-posted replacement is linked by
`pending_transaction_id`; removed transactions cancel their canonical effect
while preserving the immutable raw payload.

Run `./scripts/acceptance_plaid_sandbox.sh`. Without credentials it exits with
`PLAID CREDENTIALS REQUIRED` instead of pretending to use a live connection.
