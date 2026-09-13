# S16 semantic blocker evidence

## Minimal conflict

The locked contract requires future occurrences to be supported by observed
cadence and requires each variable stream to use
`max(last_3_occurrences.amount)`. It does not supply a recurrence identity
field. The actual dataset contains histories for which two different stream
partitions are both supported by the same trusted structured rows.

### User 04 dining history

The observed rows include a continuous 14-day dining sequence with rotating
descriptions:

| Evidence | Dates | Description pattern |
|---|---|---|
| category sequence | 2024-04-01, 04-15, 04-29, 05-13, 05-27 | rotating dining labels |
| exact-label sequence 1 | 2024-01-08, 01-22 | `Takeaway order` |
| exact-label sequence 2 | 2024-04-15, 05-13 | `Bakery and snacks` |

Two deterministic interpretations are therefore both consistent with the
authoritative input:

1. one variable dining stream at a 14-day cadence, with the latest three
   category occurrences determining the projected amount; or
2. multiple label-specific streams, with the two-row label histories eligible
   under the contract's fewer-than-three rule and each projected separately.

The resulting request-04 safe amounts are different even though both use
Decimal arithmetic, observed dates, observed amounts, and the mandated
maximum estimator:

| Construction | `amount_safe_to_pay` |
|---|---:|
| Current exact-description construction | 9,093,784.61 |
| Variable-category construction | 9,567,344.90 |
| Supplied solved row | 8,401,800 |

No field in the participant-facing data selects between the first two
constructions, and the supplied solved value does not identify which future
cash-flow set produced it. Description is evidence, but the inventory shows
that it is not a stable source/merchant/stream identifier.

### User 03 arithmetic corroboration

For request_03, the exact-description construction gives `720,303.21`, while
the variable-category construction gives `872,452.60`; the solved value is
`873,000`. The difference is caused by a different set of projected dining
and grocery flows before the binding trough, not by a salary collision.

### User 10 salary ambiguity

User 10 has weekly salary credits whose descriptions rotate among delivery
platform, app, task-marketplace, and driver-platform labels. The data has no
source/account/provider identifier. Treating those records as one recurring
income stream and treating them as independent streams are both compatible
with the observed columns and produce different future income. A resolver
cannot silently choose one without inventing source identity.

## Status after sample-grounded system identification

The earlier blocker conclusion was too strong because the contract permits
solved rows to establish an otherwise ambiguous general semantic policy. A
bounded robust-cadence rule plus same-day salary collision handling was tested
against all 25 rows, generalized under leave-one-request-out validation, and
promoted without request-specific behavior. It reduced the current mismatch
from 67 to 53 fields, but did not produce a new byte-exact row.

The following evidence therefore describes the *remaining* ambiguity after
that promotion; it is not a claim that no sample-grounded improvement exists.

## Why a 25/25 result remains unresolved

- The contract forbids inventing event or stream identity.
- The dataset does not contain a field that distinguishes the competing
  recurrence partitions.
- Exact-description and cadence/category constructions both satisfy the
  deterministic recurrence and amount rules for different subsets of the same
  rows.
- Confirmed-salary collision suppression was tested independently and did not
  resolve the numeric mismatches; it changed 67 differing fields to 74.
- Existing temporal-partition and stale-cutoff experiments likewise did not
  resolve the conflict.

Choosing a stream partition separately for a request based on the solved output
would be expected-output lookup, which is prohibited. The promoted rule is a
single global policy selected from cross-sample evidence. The remaining
alternatives would require an additional global rule or an authoritative stream
identity field; choosing one separately by request, category label, or exact
amount would silently merge or split materially different obligations.

This is not yet a proven irreconcilable blocker under the stricter
sample-grounded standard. It is the current residual evidence boundary: the
promoted global policy is partial, and further work must either identify a
globally generalizable rule from the remaining constraints or document two
indistinguishable general policies before declaring S16 blocked.

## Residual-family closure in this run

The complete 53-field matrix and cluster report are in
`s16_residual_53_matrix.{md,json}` and `s16_residual_family_clusters.md`.
The remaining numeric fields were tested with two further global hypotheses:

1. replace the current variable-category projections independently for dining,
   groceries, and transport in every one of the eight category combinations;
2. replace variable-category projections with a longest stable chronological
   suffix, over suffix lengths 3–8 and gap tolerances 0–3.

Neither candidate produced a new exact row or changed the count of numeric
mismatches. Both are contract-shaped alternatives, but each creates more field
differences than the current 53-field candidate. This closes those residual
families without promoting a request-specific choice.

The remaining ambiguity is still observable in trusted rows. For example,
user_04 dining supports a 14-day rotating-category sequence and also supports
separate label histories; user_10 salary rows support independent payout labels
and a single rotating payout stream. No participant-facing source/account/
merchant/stream identifier resolves those partitions. The current candidate is
therefore retained as the best evidence-bounded production state, with S16
remaining partial rather than being declared byte-exact.
