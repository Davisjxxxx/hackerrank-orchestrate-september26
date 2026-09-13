# S16 best-candidate checkpoint

## Current production candidate

- Bounded fixed-gap cadence: a gap stream is eligible when its median is at least five days and at least two observed intervals are within three days of that median; monthly streams require all observed gaps to be 27–32 days.
- Recurrence identity is built from observed economic fields plus description, with description contributing evidence rather than a category-wide absolute merge.
- Variable recurring amount is `max(last_3_occurrences.amount)`, falling back to the maximum available amount when fewer than three observations exist.
- Settlement date anchors projected cash timing and explicit future events suppress only a same-economic-date projected salary duplicate.
- Confirmed salary is counted once on its authoritative date; unsupported pending credits, failed/cancelled rows, and non-cash investment values do not improve cash.

## Gate evidence

- S16: `3/25` exact rows, `53` differing fields.
- Exact rows: `request_01`, `request_12`, and `request_16`.
- Evaluation suite: `32 passed`.
- Oracle/production differential: `PASS`.
- Deterministic replay: `PASS` for three target generations.
- `git diff --check`: `PASS` at checkpoint creation.
- Current production file: `code/main.py`.

## Fingerprint

The current candidate is the dirty worktree state at HEAD `250cb88` (parent production baseline `74f44ecb3505aa15ffe16e832f795cce01d7eb09`).

Current file hashes:

```text
code/main.py 7a92094d5999aa9355efc3a07785b4e289aae9a28711a405bc2efd89fd58d1c4
output.csv 580233223fbf85dbd502bbc42143b390e335f1833b0a8dfc052af7af174b4a1d
evaluation/golden_report.md 7b3030e2f2ea4c57a27c66e7f7ad9c169de9569adcd2c0ed9c03bd9ceba286be
git diff --check PASS
```

Recompute the fingerprint after any intentional production change with:

```text
sha256sum code/main.py output.csv evaluation/golden_report.md
git diff --check
```

This checkpoint preserves unrelated dirty files and does not authorize a push or interaction with the product-integration worktree.
