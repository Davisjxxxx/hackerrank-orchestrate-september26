# S16 conservative ambiguity resolution

Evaluation-only. Solved rows are used only to measure outputs after candidate construction; no expected value selects a candidate.

Rule: Among supported candidate future-flow sets, select the deterministic candidate with the lowest 90-day minimum balance; lifecycle and duplicate exclusion remain higher precedence.

## Policy comparison

| Policy | Exact rows | Differing fields | Amount fields changed | Earliest-date fields changed | Improved | Regressed |
|---|---:|---:|---:|---:|---|---|
| `A_baseline` | 3/25 | 67 | 0 | 0 | none | none |
| `B_conservative_both` | 3/25 | 87 | 17 | 8 | none | none |
| `C_conservative_income_only` | 3/25 | 74 | 0 | 4 | none | none |
| `D_conservative_expense_only` | 3/25 | 77 | 17 | 5 | none | none |

## Supported candidate boundary

- Baseline candidates are the current production exact-description recurrence streams.
- Expense alternatives reuse the existing history-supported variable-category fallback experiment only for variable categories; they do not create events without a cadence-supported history.
- Income alternatives suppress only a literal same-day explicit/projection salary collision; they do not collapse independent salary streams.
- Cancelled, failed, unrealized, and non-cash records are excluded before comparison.
- The resolver cannot synthesize or duplicate an event, and ties are broken by candidate name after the numeric trough.

## User 04 / User 10

User 04 dining and User 10 salary are the focus cases. Their per-policy candidate scores and changed event signatures are in `s16_conservative_ambiguity_resolution.json`; the evidence does not contain a source/account/stream identifier that distinguishes the competing supported streams.

| Request | Policy | Selected candidate | Baseline trough | Selected trough | Candidate interpretation |
|---|---|---|---:|---:|---|
| `request_04` | `A_baseline` | `baseline` | 39780384.61 | 39780384.61 | supported alternatives only; changed flows=0 |
| `request_04` | `B_conservative_both` | `baseline` | 39780384.61 | 39780384.61 | supported alternatives only; changed flows=0 |
| `request_04` | `C_conservative_income_only` | `baseline` | 39780384.61 | 39780384.61 | supported alternatives only; changed flows=0 |
| `request_04` | `D_conservative_expense_only` | `baseline` | 39780384.61 | 39780384.61 | supported alternatives only; changed flows=0 |
| `request_10` | `A_baseline` | `baseline` | 288949.82 | 288949.82 | supported alternatives only; changed flows=0 |
| `request_10` | `B_conservative_both` | `both_conservative` | 288949.82 | 196257.92 | supported alternatives only; changed flows=51 |
| `request_10` | `C_conservative_income_only` | `baseline` | 288949.82 | 288949.82 | supported alternatives only; changed flows=0 |
| `request_10` | `D_conservative_expense_only` | `expense_conservative` | 288949.82 | 196257.92 | supported alternatives only; changed flows=51 |

- User 04: the exact-description construction keeps separate dining labels; the variable-category construction merges the supported dining history. The category alternative has a higher trough for this request, so the conservative resolver retains the baseline. This is not evidence that either partition is the solved semantics.
- User 10: the exact-description construction contains rotating salary labels and the variable-category alternative changes only expenses. The candidate set does not contain an authoritative payroll stream identifier, so the conservative resolver cannot justify collapsing independent income streams; the income-only candidate is the same forecast for this request because the explicit salary collision is not the unresolved identity conflict.
- In both cases, the safer tie-break is applied only after evidence-supported candidates exist. It does not turn a category or label into a source identity and does not manufacture income or expenses.

## Decision

No production promotion is implied by this artifact. A candidate is eligible for promotion only if it is contract-supported and improves S16 without regressions or unsupported event synthesis.
