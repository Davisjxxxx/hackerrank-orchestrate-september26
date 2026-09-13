# S16 expected path constraints

Expected path constraints are reconstructed from safe amount, reserve, and earliest-date semantics. They are post-hoc diagnostics, not production labels.

| Request | Exact/lower-bound trough | Actual trough | First actual target-level date | Expected earliest | First violation paying expected date |
|---|---|---|---|---|---|
| `request_02` | exact `46387539.2` | `47637730.16` on `2025-08-13` | `not reached` | `2025-09-15` | `none` |
| `request_03` | exact `3541700` | `3718771.39` on `2019-09-14` | `not reached` | `2019-11-15` | `none` |
| `request_04` | exact `39088400` | `42271378.17` on `2024-06-13` | `not reached` | `2024-06-15` | `none` |
| `request_05` | exact `13837` | `20106.21` on `2026-02-02` | `not reached` | `none` | `none` |
| `request_06` | exact `1403.3` | `1430.32` on `2026-01-13` | `not reached` | `2026-01-15` | `none` |
| `request_07` | exact `180170.56` | `191080.53` on `2024-09-20` | `not reached` | `2024-10-23` | `none` |
| `request_08` | exact `1084.57` | `1183.59` on `2025-02-12` | `not reached` | `2025-04-15` | `none` |
| `request_09` | lower_bound `766.61` | `2051.84` on `2026-07-19` | `not reached` | `2026-07-04` | `none` |
| `request_10` | exact `238100` | `725801.48` on `2024-12-07` | `not reached` | `none` | `none` |
| `request_11` | exact `46651245` | `48809337.19` on `2025-05-14` | `not reached` | `2025-07-15` | `none` |
| `request_13` | exact `1733.4` | `2538.37` on `2024-03-14` | `not reached` | `2024-05-15` | `none` |
| `request_14` | exact `2797.74` | `2813.64` on `2025-08-14` | `not reached` | `none` | `none` |
| `request_15` | exact `1283.05` | `1425.66` on `2026-01-13` | `not reached` | `none` | `none` |
| `request_17` | exact `409949.58` | `414425.96` on `2026-03-13` | `not reached` | `2026-03-15` | `none` |
| `request_18` | exact `1862` | `2062.19` on `2026-07-11` | `not reached` | `2026-09-15` | `none` |
| `request_19` | exact `121620` | `130355.87` on `2024-09-14` | `not reached` | `2024-09-15` | `none` |
| `request_20` | exact `69900` | `79441.75` on `2026-02-13` | `not reached` | `none` | `none` |
| `request_21` | exact `3343.35` | `3445.70` on `2026-04-12` | `not reached` | `2026-04-15` | `none` |
| `request_22` | exact `975.46` | `1014.86` on `2024-12-14` | `not reached` | `2025-01-15` | `none` |
| `request_23` | exact `36152` | `36303.91` on `2025-05-14` | `not reached` | `2025-07-15` | `none` |
| `request_24` | exact `64420` | `63557.36` on `2026-01-13` | `2026-01-13` | `none` | `none` |
| `request_25` | exact `24804100` | `22772958.09` on `2024-03-14` | `2024-03-09` | `none` | `none` |

## First incompatible events

- `request_02` never reaches its expected implied level on the current path; the actual trough is `2025-08-13`.
- `request_03` never reaches its expected implied level on the current path; the actual trough is `2019-09-14`.
- `request_04` never reaches its expected implied level on the current path; the actual trough is `2024-06-13`.
- `request_05` never reaches its expected implied level on the current path; the actual trough is `2026-02-02`.
- `request_06` never reaches its expected implied level on the current path; the actual trough is `2026-01-13`.
- `request_07` never reaches its expected implied level on the current path; the actual trough is `2024-09-20`.
- `request_08` never reaches its expected implied level on the current path; the actual trough is `2025-02-12`.
- `request_09` never reaches its expected implied level on the current path; the actual trough is `2026-07-19`.
- `request_10` never reaches its expected implied level on the current path; the actual trough is `2024-12-07`.
- `request_11` never reaches its expected implied level on the current path; the actual trough is `2025-05-14`.
- `request_13` never reaches its expected implied level on the current path; the actual trough is `2024-03-14`.
- `request_14` never reaches its expected implied level on the current path; the actual trough is `2025-08-14`.
- `request_15` never reaches its expected implied level on the current path; the actual trough is `2026-01-13`.
- `request_17` never reaches its expected implied level on the current path; the actual trough is `2026-03-13`.
- `request_18` never reaches its expected implied level on the current path; the actual trough is `2026-07-11`.
- `request_19` never reaches its expected implied level on the current path; the actual trough is `2024-09-14`.
- `request_20` never reaches its expected implied level on the current path; the actual trough is `2026-02-13`.
- `request_21` never reaches its expected implied level on the current path; the actual trough is `2026-04-12`.
- `request_22` never reaches its expected implied level on the current path; the actual trough is `2024-12-14`.
- `request_23` never reaches its expected implied level on the current path; the actual trough is `2025-05-14`.
- `request_24` first reaches the expected implied level on `2026-01-13` with net flow `-1916.16`; candidate events: event_2082@2026-01-13.
- `request_25` first reaches the expected implied level on `2024-03-09` with net flow `-1675144.82`; candidate events: event_2204@2024-03-09, event_2218@2024-03-09.

A payment-date violation is evidence that the current path cannot support the expected full-payment date, but it does not identify whether the cause is a missing occurrence, an extra occurrence, or timing without a stream assignment. Those alternatives are enumerated separately in the minimal-flow artifact.
