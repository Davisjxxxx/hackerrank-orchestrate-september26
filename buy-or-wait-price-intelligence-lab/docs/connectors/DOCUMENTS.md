# Documents and images

`POST /v1/documents` accepts PDF, PNG, and JPEG up to the configured limit.
Files are hashed and stored outside the public web root. PDFs use optional
local text extraction; image OCR and richer extraction remain behind the
`DocumentExtractor` seam. Low-confidence or missing extraction is
`needs_review`, never authoritative cash movement.
