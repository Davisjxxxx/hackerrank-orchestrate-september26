#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

if [[ -z "${PLAID_CLIENT_ID:-}" || -z "${PLAID_SECRET:-}" ]]; then
  echo "PLAID CREDENTIALS REQUIRED" >&2
  exit 2
fi

echo "Starting Plaid Sandbox acceptance boundary."
echo "A running API, authenticated beta user, and FINANCE_TOKEN_ENCRYPTION_KEY are required."
echo "PLAID_ENV=${PLAID_ENV:-sandbox}; secrets are intentionally not printed."
PYTHONPATH=src python3 - <<'PY'
from finance_platform.connectors.plaid import PlaidConnector
connector = PlaidConnector()
print({"provider": connector.provider, "environment": connector.environment, "health": connector.health().__dict__})
PY
