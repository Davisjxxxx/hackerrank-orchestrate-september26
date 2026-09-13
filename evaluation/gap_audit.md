# Buy or Wait? contract gap audit

Audit baseline: R0 production benchmark on the 25 solved requests. No files
under `dataset/` were modified.

## 2. Required inputs

| Input | Result | Evidence |
|---|---|---|
| `requests.csv` | PARTIAL | `RequestAdapter.load()` (`code/main.py:135-137`) parses all request rows and the planner uses dates, amount, partial flag, and deadline. `request_type` and free-form `request_text` are retained but have no organizer-defined arithmetic effect. |
| `sample_requests.csv` | FIXED | Only `--samples`/`--score-samples` use it (`code/main.py:818-832`); normal target execution loads `requests.csv` and does not use solved outputs as labels. |
| `financial_profiles.csv` | PRESENT | `ProfileAdapter.load()` (`code/main.py:127-132`) loads balance, minimum, permissions, methods, installment limit, and priorities. |
| `financial_events.csv` | PRESENT | `FinancialEventAdapter.canonical_rows()` (`code/main.py:255-267`) normalizes and feeds every request ledger. |
| `exchange_rates.csv` | FIXED | `ExchangeRateAdapter.convert()` (`code/main.py:160-165`) requires the exact settlement-date and directed currency-pair row. |
| `request_payment_options.csv` | PRESENT | `PaymentOptionAdapter` and planner/validator (`code/main.py:140-147`, `652-662`, `767-773`) use supplied schedules. |
| `messages.csv` | PARTIAL | `MessageEvidenceAdapter` and `Canonicalizer.message_adjustments()` (`code/main.py:270-277`, `381-424`) use applicable, pre-request payroll evidence. Non-payroll text is not treated as an instruction and structured event state remains authoritative. |
| `images.csv` + image files | FIXED | Blank event amounts are joined by `related_event_id` and extracted in `FinancialEventAdapter`/`ImageEvidenceAdapter` (`code/main.py:168-267`). |
| `dataset/output.csv` | PRESENT AS TEMPLATE | Inventory only; predictions are written to root `output.csv` (`code/main.py:807-814`). |

## 3. Output contract

FIXED. `serialize()` and `validate()` (`code/main.py:696-796`) enforce the
column order, amount bounds, allowed domains, status/method consistency,
chronological plans, exact partial-payment arithmetic, exact supplied
installment schedules, accepted methods, deadline, and flexible-only spending
changes. The root target run was regenerated with 250 rows.

## 4. Financial logic

PRESENT for current supported cash-state rules: pending debits remain,
pending credits and non-cash/unrealized rows are excluded, failed/cancelled
rows are excluded, settlement dates drive cash timing, and recurring rows are
forecast by `Canonicalizer.for_request()` (`code/main.py:434-497`).

FIXED: blank amounts no longer become zero. The three previously unresolved
image-backed amounts are now grounded as event_3051 `1995.00`, event_3231
`8528`, and event_6033 `79679.26`. An unresolved future debit blocks a safe plan
rather than silently disappearing (`code/main.py:506-513`, `529-540`).

REMAINING PARTIAL GAP: recurrence is still description-grouped and uses the
existing bounded cadence plus `max(last_3)` estimator. This is the known source
of the 21 solved numeric residuals; it was not replaced during this input and
contract gap pass.

## 5. Conflict resolution

PARTIAL. Status filtering and linked-row deduplication are implemented, and
pre-request message timing is enforced. A fully explicit generic precedence
engine for every possible newer-source/amendment conflict is not present. The
current dataset has no missing message/image links, no linkage cycles, and the
status/lifecycle records are handled by the existing canonical filter.

## 6. Ranking and eligibility

PRESENT. Planner candidate generation and `rank_key()` (`code/main.py:648-669`)
enforce accepted methods, supplied installment options, partial-payment
requirements, full-payment deadlines, user preferences, no-change preference,
total paid, start date, payment count, and option-ID tie-breaking.

## 7. Untrusted content

PRESENT. Messages are parsed only for grounded financial facts; no message or
OCR text is executed. OCR failures produce unknown evidence, not zero. Future
messages are excluded from earlier request decisions (`code/main.py:381-388`).

## 8. Packaging and operations

FIXED LOCALLY: README documents the terminal entry point and reference-only
sample modes. The final package must be refreshed from this tree because the
pre-existing `code.zip` contained an older source hash. Determinism is standard
library/Decimal based with zero model calls. `AGENTS.md` logging is append-only
in root `log.txt`, and organizer-only files are not imported by the scored
runtime.

## Silent plausible-but-wrong risks

1. The remaining description-grouped recurrence can over- or under-project
   obligations despite valid arithmetic.
2. Unlinked, non-payroll messages are retained as advisory context but do not
   independently amend structured events without a grounded event linkage.
3. A fresh environment without the packaged OCR cache and OCR dependency will
   leave a blank image amount unresolved; the safe behavior is conservative
   blocking, but packaging must include the cache for replay equivalence.
4. The 21 solved numeric mismatches remain unresolved; the current output is
   contract-valid, not solved-sample exact.
