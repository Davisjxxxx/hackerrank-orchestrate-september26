# S16 future-cash-flow semantic experiment

Analysis only; no policy below is production behavior until separately promoted.

| Policy | Exact rows | Differing fields | Improved requests | Regressed requests | Verdict |
|---|---:|---:|---|---|---|
| `A_existing_behavior` | 3/25 | 53 | none | none | baseline |
| `B_confirmed_occurrence_suppression` | 3/25 | 53 | none | none | measure only; inspect arithmetic and stream semantics |
| `C_confirmed_anchor_authority` | 2/25 | 102 | none | request_16 | measure only; inspect arithmetic and stream semantics |
| `D_explicit_only_confirmation` | 2/25 | 59 | none | request_01 | measure only; inspect arithmetic and stream semantics |

## Definitions

- A: current production behavior.
- B: remove a historical salary projection only when a compatible explicit salary exists on the same settlement date.
- C: an explicit future salary is authoritative; remove all historical salary projections while retaining only explicit salary and any continuation explicitly generated from that anchor.
- D: count the explicit salary once, suppress its same-date historical duplicate, and do not let the explicit record alone generate continuation.

The experiment must be paired with the collision table and does not use request-specific rules.
