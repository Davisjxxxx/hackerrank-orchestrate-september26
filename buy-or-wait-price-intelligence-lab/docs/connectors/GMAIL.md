# Gmail connector

Gmail uses read-only OAuth scope and a separate untrusted-evidence classifier.
The connector is OAuth-ready and fail-closed without `GMAIL_CLIENT_ID` and
`GMAIL_CLIENT_SECRET`. Production sync should query narrow financial search
terms, store provider/thread metadata, sanitize body text, and link facts to
events only when evidence is direct. Email never supplies executable policy.
