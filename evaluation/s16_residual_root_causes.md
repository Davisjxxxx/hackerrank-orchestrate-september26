# S16 residual root causes after sample-grounded promotion

The sample-grounded system-identification pass promoted one global,
contract-compatible change. The current production checkpoint is `3/25`
exact with `53` differing fields, down from the pre-pass `67`. Solved values
were used only to rank whole candidate policies; they do not enter production
runtime.

## Policy result

| Policy | Exact | Differing fields | Result |
|---|---:|---:|---|
| Pre-pass production | 3/25 | 67 | starting checkpoint |
| Robust cadence + salary collision | 3/25 | 53 | current production |
| Conservative income only | 3/25 | 74 | rejected; no improvement and regressions |
| Conservative expense only | 3/25 | 77 | rejected; no improvement and regressions |
| Conservative income + expense | 3/25 | 87 | rejected; no improvement and regressions |

## Remaining mismatch classification

All 22 non-exact rows have an upstream future-cash-flow mismatch or a field
derived from one. The numeric rows are classified as follows:

- `request_02`, `request_06`, `request_07`, `request_08`, `request_13`,
  `request_14`, `request_15`, `request_17`, `request_21`, and `request_25`:
  explicit-future versus projected recurrence collision is present in the
  current flow audit, including confirmed salary collisions. Suppression was
  tested and did not improve S16.
- `request_03`, `request_04`, `request_05`, `request_10`, `request_11`,
  `request_18`, `request_19`, `request_20`, `request_22`, `request_23`,
  `request_24`, and `request_25`: recurrence identity / stream partition is
  unresolved from the authoritative fields. Description, category, cadence,
  and amount evidence support more than one partition for at least part of
  the forecast.
- Earliest-date, affordability, payment-plan, and explanation differences
  are downstream effects of the same cash-flow construction differences,
  not independent safety-predicate changes.

The supplied evidence still does not establish a general source/account/
merchant/stream identity that distinguishes every remaining competing
partition. The safer-interpretation rule can choose a lower supported forecast
trough, but it cannot identify which unsupported stream identity is true.
Applying it to the supplied alternatives produced no improved request and
introduced regressions. This is a residual investigation boundary, not yet a
formal blocker under the sample-grounded stopping standard.

## Non-numeric residuals

`request_09` differs only in serialized explanation. Numeric financial state
is otherwise exact for that row; explanation tuning is downstream and was not
promoted while numeric S16 remains unresolved.

## Evidence boundary

No expected output, request-specific rule, user-specific rule, description
alias, amount policy change, or invented future event was used. The minimal
unblock remains an authoritative recurrence/source identity rule or additional
source/account/merchant data. This pass therefore freezes the production
engine and preserves the blocker rather than introducing a non-contractual
partition.
