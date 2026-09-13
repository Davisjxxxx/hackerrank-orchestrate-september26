# CSV, OFX, and QFX imports

`POST /v1/imports/transactions/preview` parses without committing. The commit
route detects CSV/OFX/QFX, normalizes dates and signed/debit-credit amounts,
assigns a file-import source connection, stores a raw payload hash, and creates
canonical events idempotently. Each imported row keeps its external ID and
source connection. Real banks differ, so unrecognized columns require a future
mapping UI rather than silent coercion.
