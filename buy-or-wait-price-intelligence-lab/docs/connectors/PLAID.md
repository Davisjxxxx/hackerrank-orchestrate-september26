# Plaid connector

`finance_platform.connectors.plaid.PlaidConnector` is a read-only,
Transactions/Accounts/Balances-oriented adapter. It supports Link-token
creation, public-token exchange, incremental `/transactions/sync`, refresh,
disconnect, and health semantics. Configure `PLAID_CLIENT_ID`, `PLAID_SECRET`,
and `PLAID_ENV=sandbox` locally. Access tokens must be encrypted before storage
and never sent to the frontend. Webhook verification is a deployment gate.
