# Security and privacy review

## Controls in this release candidate

- Provider credentials are read only by server-side adapters and are never part of mobile configuration or API responses.
- URL intake requires absolute HTTP(S), rejects embedded credentials, invalid ports, control characters, and fragments are removed from the canonical provenance URL.
- OCR/image metadata is bounded and retained as inert evidence. No prompt, seller description, OCR text, or product URL can execute code or mutate financial state.
- Monetary fields are Decimal strings at the API boundary and are revalidated by the domain model. Financial composition consumes a server-side `FinancialSafetyProvider` seam; missing, stale, or contradictory SAFE_NOW evidence fails closed.
- Price observations carry trust classes. User captures are private to the authenticated fixture subject and cannot enter shared provider history without an explicit promotion policy.
- Images are represented by a durable reference rather than embedded bytes. Production retention must use short-lived object references and delete-after-resolution by default.
- Watch and decision reads are subject-scoped through the `Authenticator` dependency. The canonical lab credential is `Authorization: Bearer fixture:<subject>`; `X-User-Id` remains only a backward-compatible fixture header and is not a production identity mechanism.
- Notifications carry an opaque target reference and trigger/reason metadata, not financial balances or credentials.
- Provider outage, rate limiting, stale listings, out-of-stock or unknown-availability rows, mixed currencies, malformed nested payloads, and duplicate aggregation rows fail closed or degrade with explicit evidence. The engine independently excludes quarantined evidence even when called without the observation store.
- Financial evidence is structurally validated at the typed seam; SAFE_NOW contradictions use authoritative financial/evaluation time and future-dated evidence requires confirmation rather than a buy.

## Required production follow-up

- Replace the fixture authenticator with a production token-verification adapter and add tenant tests before exposing the service. The current in-memory fixture is not internet-deployable authentication.
- Encrypt persisted financial results and separate access logs from decision payloads; redact URLs, image references, and financial reason details from ordinary logs.
- Add malware/content scanning and EXIF stripping in the object-upload adapter.
- Add replay protection/expiry for image references, signed upload URLs, request size/rate limits, and SSRF controls before fetching third-party URLs.
- Confirm notification previews do not leak product/financial data on lock screens.
- Run secret scanning and dependency vulnerability/license scans in CI. This local scan must not print secret values.
