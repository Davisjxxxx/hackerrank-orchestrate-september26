# Final bounded recurrence policy search

Policies evaluated: **282**. Production code and dataset were not modified.

## Top 10

| Rank | Policy | Exact rows | Exact safe | Numeric mismatches | Absolute safe error | Status | Method | Plan | Earliest | Optimistic | Pessimistic |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `chronology=A0;debit_amount=median;credit_amount=median;consistent_intervals=2;fixed_tolerance=4;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 5203249.78 | 21/25 | 24/25 | 22/25 | 18/25 | 19 | 2 |
| 2 | `chronology=A0;debit_amount=max;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 6930596.72 | 21/25 | 24/25 | 22/25 | 18/25 | 19 | 2 |
| 3 | `chronology=A0;debit_amount=max;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(26, 33);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 6930596.72 | 21/25 | 24/25 | 22/25 | 18/25 | 19 | 2 |
| 4 | `chronology=A0;debit_amount=median;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 8068470.20 | 21/25 | 24/25 | 22/25 | 18/25 | 20 | 1 |
| 5 | `chronology=A0;debit_amount=median;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(26, 33);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 8068470.20 | 21/25 | 24/25 | 22/25 | 18/25 | 20 | 1 |
| 6 | `chronology=A1;debit_amount=median;credit_amount=median;consistent_intervals=2;fixed_tolerance=4;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 5203249.78 | 21/25 | 24/25 | 22/25 | 17/25 | 19 | 2 |
| 7 | `chronology=A2;debit_amount=median;credit_amount=median;consistent_intervals=2;fixed_tolerance=4;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 5203249.78 | 21/25 | 24/25 | 22/25 | 17/25 | 19 | 2 |
| 8 | `chronology=A1;debit_amount=max;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 6930596.72 | 21/25 | 24/25 | 22/25 | 17/25 | 19 | 2 |
| 9 | `chronology=A1;debit_amount=max;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(26, 33);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 6930596.72 | 21/25 | 24/25 | 22/25 | 17/25 | 19 | 2 |
| 10 | `chronology=A2;debit_amount=max;credit_amount=median;consistent_intervals=2;fixed_tolerance=3;monthly_range=(27, 32);shortfall=False;periods=2;period_estimator=latest;phase=latest` | 3/25 | 4/25 | 21 | 6930596.72 | 21/25 | 24/25 | 22/25 | 17/25 | 19 | 2 |

## Winner request-level changes

- `request_02`: R0 `18479330.16` -> candidate `18890252.09`; expected `17229139.2`; diagnostics `[]`
- `request_03`: R0 `1050071.39` -> candidate `1093118.58`; expected `873000`; diagnostics `[]`
- `request_04`: R0 `11584778.17` -> candidate `9444508.72`; expected `8401800`; diagnostics `[]`
- `request_05`: R0 `7006.21` -> candidate `7127.62`; expected `737`; diagnostics `[]`
- `request_07`: R0 `98080.53` -> candidate `99307.07`; expected `87170.56`; diagnostics `[]`
- `request_08`: R0 `383.59` -> candidate `330.99`; expected `284.57`; diagnostics `[]`
- `request_14`: R0 `613.64` -> candidate `565.92`; expected `597.74`; diagnostics `[]`
- `request_15`: R0 `225.66` -> candidate `228.91`; expected `83.05`; diagnostics `[]`
- `request_17`: R0 `248325.96` -> candidate `246396.8`; expected `243849.58`; diagnostics `[]`
- `request_18`: R0 `662.19` -> candidate `675.92`; expected `462`; diagnostics `[]`
- `request_19`: R0 `37555.87` -> candidate `34044.27`; expected `28820`; diagnostics `[]`
- `request_20`: R0 `14941.75` -> candidate `15109.36`; expected `5400`; diagnostics `[]`
- `request_22`: R0 `514.86` -> candidate `496.79`; expected `475.46`; diagnostics `[]`
- `request_23`: R0 `9303.91` -> candidate `10065.77`; expected `9152`; diagnostics `[]`
- `request_24`: R0 `12557.36` -> candidate `13607.92`; expected `13420`; diagnostics `[]`
- `request_25`: R0 `0` -> candidate `37170.78`; expected `1425000`; diagnostics `[]`
