# External credentials still required

The no-credential CSV/OFX/QFX and local SQLite workflow is available now.

- Plaid: obtain client ID and secret, choose Sandbox/Development/Production,
  register the HTTPS redirect/webhook domain, configure encrypted token
  storage, and complete webhook verification.
- Google: create an OAuth client ID and secret, register an HTTPS redirect URI,
  request the read-only Gmail scope, and configure refresh-token storage.
- Production: provide a managed PostgreSQL URL, secret-manager key for token
  encryption, object storage/malware scanner, OIDC identity provider, and job
  queue/worker.

No credentials are present in this branch.
