# S16 policy cross-validation

Leave-one-request-out selection uses the remaining solved rows to rank whole candidate policies by field error, numeric error, contract compliance, and complexity. The held-out row is never used to choose its policy. `P0_production` and `P11_robust_cadence_salary_collision` are output-equivalent after the general promotion; the selector therefore retains the simpler production label on ties.

| Held out | Selected policy | Held-out exact | Held-out differing fields |
|---|---|---|---:|
| `request_01` | `P0_production` | True | 0 |
| `request_02` | `P0_production` | False | 1 |
| `request_03` | `P0_production` | False | 1 |
| `request_04` | `P0_production` | False | 2 |
| `request_05` | `P0_production` | False | 2 |
| `request_06` | `P0_production` | False | 5 |
| `request_07` | `P0_production` | False | 1 |
| `request_08` | `P0_production` | False | 1 |
| `request_09` | `P0_production` | False | 1 |
| `request_10` | `P0_production` | False | 3 |
| `request_11` | `P0_production` | False | 5 |
| `request_12` | `P0_production` | True | 0 |
| `request_13` | `P0_production` | False | 6 |
| `request_14` | `P0_production` | False | 2 |
| `request_15` | `P0_production` | False | 2 |
| `request_16` | `P0_production` | True | 0 |
| `request_17` | `P0_production` | False | 1 |
| `request_18` | `P0_production` | False | 4 |
| `request_19` | `P0_production` | False | 3 |
| `request_20` | `P0_production` | False | 2 |
| `request_21` | `P0_production` | False | 5 |
| `request_22` | `P0_production` | False | 2 |
| `request_23` | `P0_production` | False | 1 |
| `request_24` | `P0_production` | False | 2 |
| `request_25` | `P0_production` | False | 1 |

Selected-policy stability: `1` distinct output policy across 25 folds; counts: `{'P0_production': 25}`. The promoted P11 behavior is the equivalent current production implementation, not a request-specific exception.

This is a finite policy-family validation, not proof that an untested policy is impossible. The promoted rule is eligible because it is contract-compliant, globally defined, and reduced the pre-pass full-set field error from 67 to 53 without request-specific behavior. S16 remains incomplete because exact rows remain 3/25.
