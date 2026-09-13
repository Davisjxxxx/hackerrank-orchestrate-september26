# S16 candidate semantics matrix

This matrix evaluates whole deterministic policies. Candidate event sets retain event provenance. Solved values are used only for post-hoc compatibility scoring.

| Policy | Exact | Differing fields | Numeric mismatches | Earliest mismatches | Status/method mismatches | Contract compliant |
|---|---:|---:|---:|---:|---:|---|
| `P0_production` | 3/25 | 53 | 21 | 7 | 4 | True |
| `P1_exact_rebuilt` | 2/25 | 73 | 22 | 11 | 6 | True |
| `P2_variable_category` | 2/25 | 82 | 22 | 13 | 10 | True |
| `P3_description_family` | 2/25 | 73 | 22 | 11 | 6 | False |
| `P4_structural_phase` | 2/25 | 84 | 23 | 13 | 10 | True |
| `P5_sequence_phase` | 2/25 | 81 | 22 | 13 | 9 | True |
| `P6_active_sequence` | 1/25 | 87 | 23 | 14 | 10 | True |
| `P7_salary_same_day` | 3/25 | 53 | 21 | 7 | 4 | True |
| `P8_salary_anchor` | 2/25 | 102 | 22 | 15 | 14 | False |
| `P9_salary_explicit_only` | 2/25 | 59 | 22 | 8 | 5 | False |
| `P10_expense_conservative` | 3/25 | 88 | 21 | 13 | 12 | True |
| `P11_robust_cadence_salary_collision` | 3/25 | 53 | 21 | 7 | 4 | True |

## Interpretation

`P11_robust_cadence_salary_collision` is the current production policy. It is the same general behavior represented by `P0_production` after promotion, so the two rows have identical output scores. The pre-promotion production checkpoint was 3/25 with 67 differing fields; P11 reduced that to 53 without increasing exact rows. Candidate compatibility is reported per request in the JSON, including event signatures and exact/numeric-compatible request IDs.
