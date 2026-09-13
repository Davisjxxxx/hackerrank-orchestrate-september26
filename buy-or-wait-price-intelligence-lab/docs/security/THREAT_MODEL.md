# Threat model

Bank access tokens, account balances, transaction history, email/document
evidence, user preferences, and decision explanations are sensitive.

- User IDs are required at the finance API boundary and every read is scoped
  by user ID; production must replace the development identity adapter with an
  OIDC/session verifier.
- Raw payloads are immutable and should be encrypted using managed database or
  object-storage encryption. Plaid tokens are encrypted with Fernet before
  persistence when `FINANCE_TOKEN_ENCRYPTION_KEY` is configured.
- Bank access is read-only. No connector exposes money movement operations.
- Uploads enforce MIME, extension, and size checks, use content hashes, and
  store outside the public web root. Extraction is review-only when confidence
  is low.
- Email, OCR, and document contents are data, never executable instructions.
- Logs must contain IDs and counts, not tokens, account numbers, raw bodies, or
  full provider payloads. Add structured audit logging and rate limiting at
  deployment.

Before production launch add a secret manager, TLS, CSRF protection for browser
sessions, verified webhook signatures, malware scanning, object retention and
deletion policies, SSRF-safe outbound clients, and a formal OIDC provider.
