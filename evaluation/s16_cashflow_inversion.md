# S16 cash-flow inversion

Evaluation-only inversion of the 22 non-exact solved rows. Expected outputs are constraints, never runtime inputs.

- Differing fields: `53`

| Request | Expected safe | Actual safe | Delta actual-expected | Expected trough constraint | Actual trough | First target-level date | Delta interval | Direction |
|---|---:|---:|---:|---|---|---|---|---|
| `request_02` | 17229139.2 | 18479330.16 | 1250190.96 | exact `46387539.2` | `47637730.16` on `2025-08-13` | `not reached` | `2025-08-05..2025-09-15` | extra debit or missing credit (production too optimistic) |
| `request_03` | 873000 | 1050071.39 | 177071.39 | exact `3541700` | `3718771.39` on `2019-09-14` | `not reached` | `2019-09-03..2019-11-15` | extra debit or missing credit (production too optimistic) |
| `request_04` | 8401800 | 11584778.17 | 3182978.17 | exact `39088400` | `42271378.17` on `2024-06-13` | `not reached` | `2024-06-04..2024-06-15` | extra debit or missing credit (production too optimistic) |
| `request_05` | 737 | 7006.21 | 6269.21 | exact `13837` | `20106.21` on `2026-02-02` | `not reached` | `2025-11-06..2026-02-02` | extra debit or missing credit (production too optimistic) |
| `request_06` | 603.3 | 620.4 | 17.1 | exact `1403.3` | `1430.32` on `2026-01-13` | `not reached` | `2026-01-03..2026-01-15` | extra debit or missing credit (production too optimistic) |
| `request_07` | 87170.56 | 98080.53 | 10909.97 | exact `180170.56` | `191080.53` on `2024-09-20` | `not reached` | `2024-09-05..2024-10-23` | extra debit or missing credit (production too optimistic) |
| `request_08` | 284.57 | 383.59 | 99.02 | exact `1084.57` | `1183.59` on `2025-02-12` | `not reached` | `2025-02-07..2025-04-15` | extra debit or missing credit (production too optimistic) |
| `request_09` | 166.61 | 166.61 | 0.00 | lower_bound `766.61` | `2051.84` on `2026-07-19` | `not reached` | `2026-07-04..2026-07-19` | timing displacement or downstream-only |
| `request_10` | 12700 | 266700 | 254000 | exact `238100` | `725801.48` on `2024-12-07` | `not reached` | `2024-12-06..2024-12-07` | extra debit or missing credit (production too optimistic) |
| `request_11` | 12510645 | 13110000 | 599355 | exact `46651245` | `48809337.19` on `2025-05-14` | `not reached` | `2025-05-03..2025-07-15` | extra debit or missing credit (production too optimistic) |
| `request_13` | 433.4 | 941.6 | 508.2 | exact `1733.4` | `2538.37` on `2024-03-14` | `not reached` | `2024-03-07..2024-05-15` | extra debit or missing credit (production too optimistic) |
| `request_14` | 597.74 | 613.64 | 15.90 | exact `2797.74` | `2813.64` on `2025-08-14` | `not reached` | `2025-08-04..2025-08-14` | extra debit or missing credit (production too optimistic) |
| `request_15` | 83.05 | 225.66 | 142.61 | exact `1283.05` | `1425.66` on `2026-01-13` | `not reached` | `2026-01-06..2026-01-13` | extra debit or missing credit (production too optimistic) |
| `request_17` | 243849.58 | 248325.96 | 4476.38 | exact `409949.58` | `414425.96` on `2026-03-13` | `not reached` | `2026-03-01..2026-03-15` | extra debit or missing credit (production too optimistic) |
| `request_18` | 462 | 662.19 | 200.19 | exact `1862` | `2062.19` on `2026-07-11` | `not reached` | `2026-07-07..2026-09-15` | extra debit or missing credit (production too optimistic) |
| `request_19` | 28820 | 37555.87 | 8735.87 | exact `121620` | `130355.87` on `2024-09-14` | `not reached` | `2024-09-04..2024-09-15` | extra debit or missing credit (production too optimistic) |
| `request_20` | 5400 | 14941.75 | 9541.75 | exact `69900` | `79441.75` on `2026-02-13` | `not reached` | `2026-02-07..2026-02-13` | extra debit or missing credit (production too optimistic) |
| `request_21` | 1543.35 | 1574.4 | 31.05 | exact `3343.35` | `3445.70` on `2026-04-12` | `not reached` | `2026-04-03..2026-04-15` | extra debit or missing credit (production too optimistic) |
| `request_22` | 475.46 | 514.86 | 39.40 | exact `975.46` | `1014.86` on `2024-12-14` | `not reached` | `2024-12-05..2025-01-15` | extra debit or missing credit (production too optimistic) |
| `request_23` | 9152 | 9303.91 | 151.91 | exact `36152` | `36303.91` on `2025-05-14` | `not reached` | `2025-05-07..2025-07-15` | extra debit or missing credit (production too optimistic) |
| `request_24` | 13420 | 12557.36 | -862.64 | exact `64420` | `63557.36` on `2026-01-13` | `2026-01-13` | `2026-01-04..2026-01-13` | missing debit or extra credit (production too pessimistic) |
| `request_25` | 1425000 | 0 | -1425000 | exact `24804100` | `22772958.09` on `2024-03-14` | `2024-03-09` | `2024-03-06..2024-03-14` | missing debit or extra credit (production too pessimistic) |

## Interpretation

For uncapped expected safe amounts, expected safe plus the protected minimum is an exact implied trough. Positive actual-minus-expected means the production path leaves too much safe cash and needs an extra debit or missing credit; negative means it leaves too little and needs a missing debit or extra credit. A capped expected safe amount would provide only a lower bound; no request-specific production branch is derived from this table.
