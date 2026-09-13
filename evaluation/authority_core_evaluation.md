# Authority-first candidate evaluation

R0 is the unchanged production benchmark. R1-R3 were run through the
parallel resolver and the existing typed planner. Solved outputs were used
only for evaluation, never by the resolver.

| Metric | R0 | R1 | R2 | R3 |
|---|---:|---:|---:|---:|
| S16-CORE exact rows | 4/25 | 4/25 | 2/25 | 3/25 |
| amount_safe exact | 4/25 | 4/25 | 2/25 | 3/25 |
| numeric mismatches | 21 | 21 | 23 | 22 |
| absolute safe error | 6,930,596.72 | 6,965,227.45 | 4,489,782.06 | 6,397,305.41 |
| earliest-date exact | 18/25 | 14/25 | 11/25 | 15/25 |
| status exact | 21/25 | 20/25 | 13/25 | 18/25 |
| method exact | 24/25 | 23/25 | 15/25 | 20/25 |
| plan exact | 22/25 | 20/25 | 15/25 | 18/25 |
| spending-change exact | 22/25 | 22/25 | 23/25 | 22/25 |
| S16-FULL-BYTE | 3/25 | 3/25 | 1/25 | 2/25 |

Error direction for safe amounts: R0 `19 optimistic / 2 pessimistic`; R1
`20 / 1`; R2 `10 / 13`; R3 `15 / 7`. R2 materially lowers aggregate absolute
error but does not improve organizer-aligned exactness and causes decision
field regressions, so it is not promoted.

The largest R0 absolute safe residuals are request_04 `3,182,978.17`,
request_02 `1,250,190.96`, request_25 `1,425,000.00` pessimistic,
request_11 `599,355.00`, and request_10 `254,000.00`. The two inverse-direction
anchors remain request_24 (`862.64` pessimistic) and request_25 (`1,425,000`
pessimistic); this confirms that a one-direction recurrence fix is unsafe.
