# Recurrence identity policy ablation

All policies use event_date on or before each request date for recurrence history; settlement_date remains the simulated cash date. Counts below are experiment-harness results, not a replacement for the production S16 gate. `Recurrence fixes` and `regressions` compare each candidate with Policy A, the exact-normalized-description baseline.

| Policy | Exact rows | Differing fields | Recurrence fixes | Regressions | False-merge proxy | False-split proxy |
|---|---:|---:|---:|---:|---:|---:|
| Production checkpoint (current) | 3/25 | 67 | n/a | n/a | n/a | n/a |
| A_exact_normalized_description | 2/25 | 73 | 0 | 0 | 0 | 74 |
| B_broad_category | 2/25 | 97 | 0 | 0 | 1 | 0 |
| C_description_family | 2/25 | 73 | 0 | 0 | 0 | 74 |
| D_structural_cadence | 2/25 | 84 | 0 | 0 | 1 | 1 |
| E_cadence_assisted | 2/25 | 97 | 0 | 0 | 1 | 0 |
| F_amount_supported | 2/25 | 87 | 0 | 0 | 1 | 0 |
| G_variable_category_fallback | 2/25 | 82 | 0 | 0 | 1 | 3 |
| H_sequence_phase_partition | 2/25 | 81 | 0 | 0 | 1 | 0 |
| I_phase_aware_active | 1/25 | 87 | 0 | 1 | 1 | 0 |

## Exact-row changes

- `A_exact_normalized_description` exact rows: request_12, request_16
- `B_broad_category` exact rows: request_12, request_16
- `C_description_family` exact rows: request_12, request_16
- `D_structural_cadence` exact rows: request_12, request_16
- `E_cadence_assisted` exact rows: request_12, request_16
- `F_amount_supported` exact rows: request_12, request_16
- `G_variable_category_fallback` exact rows: request_12, request_16
- `H_sequence_phase_partition` exact rows: request_12, request_16
- `I_phase_aware_active` exact rows: request_16

## Selection result

No candidate is promoted to production. The natural hybrid fallback (`G_variable_category_fallback`) reduces harness field mismatches relative to broad category projection but still produces no new exact sample rows and retains an anti-overmerge failure. The corrected phase-aware partition (`H_sequence_phase_partition`) also produces no new exact rows, increases harness field differences to 81, and regresses current exact `request_01`; the stale-stream variant (`I_phase_aware_active`) falls to 1/25. The supplied schema has no merchant/source/account/recurrence identifier that can resolve the remaining same-category, rotating-description cases without an unsupported alias. The production checkpoint therefore remains unchanged pending authoritative evidence.

