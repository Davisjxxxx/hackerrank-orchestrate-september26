# S16 semantic experiment ledger

This ledger records experiments against the canonical solved set. No solved
row, request identifier, or expected value is used by production code.

## Baseline

| Policy | Exact rows | Differing fields | Result |
|---|---:|---:|---|
| Existing production checkpoint | 3/25 | 67 | retained as starting point |

The baseline uses `WindowPolicy.DAYS_0_THROUGH_89`, Decimal arithmetic, and the locked `max(last_3_occurrences.amount)` estimator.

## Sample-grounded system-identification promotion

The final system-identification pass used solved rows only as behavioral
evidence for comparing whole, general policies. No request, user, event ID,
description alias, amount lookup, or expected value enters production code.

| Policy | General rule | Exact rows | Differing fields | Held-out validation | Verdict |
|---|---|---:|---:|---|---|
| Pre-pass production | Original fixed-gap eligibility plus exact-description streams | 3/25 | 67 | stable baseline | superseded |
| Robust cadence + salary collision | Admit a fixed-gap stream only when at least two intervals support the median within three days; suppress only projected salary rows on an explicit salary settlement date | 3/25 | 53 | selected equivalent policy in all 25 leave-one-request-out folds; 3 exact held-out rows | promoted minimal general change |

The promoted rule is evidence-bounded: it does not merge arbitrary categories,
invent a stream identity, or change the mandated variable amount estimator.
The exact-row count did not improve, so S16 remains open. The field reduction is
material but is not treated as a byte-exact acceptance result.

### Rejected same-day control

Dropping all projected recurrence on the request date was tested as a separate
same-day cash-flow semantic. It produced 3/25 exact rows and 56 differing
fields, with no new exact rows; it was not promoted. Explicit future events and
authoritative settlement semantics remain distinct from projected recurrence.

Suppressing every two-occurrence stream whose observed amounts differ was also
tested as a conservative anti-invention control. It produced 3/25 exact rows
and 61 differing fields, so it was rejected; the locked max-of-available
amount rule and cadence evidence remain the controlling recurrence inputs.

## Future salary collision policies

| Policy | Rule | Exact rows | Differing fields | Improved complete requests | Regressed complete requests | Verdict |
|---|---|---:|---:|---|---|---|
| A | Existing behavior: historical salary projections, explicit confirmed salary, and confirmed-salary continuation can coexist | 3/25 | 67 | n/a | n/a | baseline |
| B | Suppress a historical salary projection only when an explicit salary exists on the same settlement date | 3/25 | 74 | none at row level | none at row level | dates improve in request_02/request_07 but other fields regress |
| C | Treat explicit future salary as authoritative and remove all historical salary projections | 1/25 | 111 | none | request_12, request_16 | rejected |
| D | Count explicit salary once, suppress same-date duplicate, and remove continuation generated solely from the explicit record | 2/25 | 80 | none | request_01 | rejected |

Policy B corrected the baseline earliest date for request_02 (`2025-09-15`) and request_07 (`2024-10-23`), but it made request_07 no longer affordable under the unchanged variable-spend forecast and increased the overall mismatch count. It is not promotable by aggregate score or by the current target semantics.

## Stale-stream sensitivity

The existing phase-aware active-state experiment is retained as evidence:

| Policy | Exact rows | Differing fields |
|---|---:|---:|
| Phase-aware temporal partition | 2/25 | 81 |
| Phase-aware active/stale cutoff | 1/25 | 87 |

No cadence-relative stale cutoff produced a promotion candidate. The cutoff changes which obligations are projected without resolving the identity ambiguity in the underlying category histories.

## Future-expense audit

The collision audit found same-date explicit/projected collisions for salary only. Near-date non-salary records include outstanding balances, pending pharmacy charges, scheduled insurance, and pending authorizations; their categories and dates overlap but lifecycle/description/amount evidence does not authorize treating them as duplicates. No future-expense suppression policy was promoted.

## Root-cause conclusion

The remaining numeric differences are not explained by confirmed-salary collision alone. They are sensitive to whether rotating variable-category observations are one stream or multiple streams. The supplied schema has no merchant, account, provider, source-record, recurrence-marker, or stream-ID field. See `s16_blocker_evidence.md` for the authoritative conflict and exact arithmetic.

## Residual-family experiments in the 53-field checkpoint

| Candidate | S16 exact | Differing fields | Numeric mismatches | Date mismatches | Held-out performance | Contract compliant | Promoted |
|---|---:|---:|---:|---:|---|---|---|
| Current P11 checkpoint | 3/25 | 53 | 21 | 7 | Baseline | Yes | Yes |
| Per-category variable fallback combinations | 3/25 | 55–88 | 21 | 7–13 | No improvement in any of the eight category combinations | Yes | No |
| Variable-category stable-suffix stream | 3/25 | 80–83 | 21 | 7–13 | No improvement across suffix lengths 3–8 and gap tolerances 0–3 | Yes | No |

These were residual-family tests only. They preserved the required maximum-of-last-three amount estimator and did not use request IDs, user IDs, event IDs, exact solved amounts, or expected-output lookup in candidate construction.

## S16 cash-flow inversion pass

| Candidate | S16 exact | Differing fields | Numeric mismatches | Cross-validation | Promoted |
|---|---:|---:|---:|---|---|
| Bounded occurrence/stream/observed-amount flow edits, evaluation-only | 3/25 baseline | 53 baseline | 21 baseline | 22/22 residual requests had no exact explanation within the bounded evidence-supported search | No |
| Chronology-assigned latent streams with affirmative concurrency only, evaluation-only | 3/25 baseline family | 53 baseline family | 21 baseline family | Dataset-wide assignment produced 2,721 economic groups; no contract-compliant candidate output improvement over P11 | No |

The inversion used the exact signed correction `expected_safe - actual_safe` as the required path correction. Candidate edits were limited to removal of current projected occurrences or inferred streams and replacement by amounts observed in the same production stream. The nearest candidates frequently left residuals ranging from cents to millions, demonstrating that the remaining errors are not one uniform max-last-3 adjustment. Solved rows remain diagnostic constraints only.
