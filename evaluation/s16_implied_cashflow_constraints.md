# S16 implied cash-flow constraints

Solved outputs are used as behavioral evidence for this diagnostic only. They do not enter production runtime.

## `request_01` / `user_01`

- Request: `25256` on `2024-03-03`; opening balance `58481.1`; reserve `18000`.
- Safe amount: expected `25256`, actual `25256`, actual-minus-expected `0`.
- Earliest full payment: expected `2024-03-03`, actual `2024-03-03`.
- Status/method: expected `affordable_now/full_payment`, actual `affordable_now/full_payment`.
- Actual trough: `45494.32` on `2024-04-14`; expected-implied reserve boundary `43256`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_02` / `user_02`

- Request: `46018000` on `2025-08-05`; opening balance `60383889.2`; reserve `29158400`.
- Safe amount: expected `17229139.2`, actual `18479330.16`, actual-minus-expected `1250190.96`.
- Earliest full payment: expected `2025-09-15`, actual `2025-09-15`.
- Status/method: expected `affordable_with_plan/installments`, actual `affordable_with_plan/installments`.
- Actual trough: `47637730.16` on `2025-08-13`; expected-implied reserve boundary `46387539.2`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_03` / `user_03`

- Request: `5491000` on `2019-09-03`; opening balance `5810300`; reserve `2668700`.
- Safe amount: expected `873000`, actual `1050071.39`, actual-minus-expected `177071.39`.
- Earliest full payment: expected `2019-11-15`, actual `2019-11-15`.
- Status/method: expected `affordable_later/wait`, actual `affordable_later/wait`.
- Actual trough: `3718771.39` on `2019-09-14`; expected-implied reserve boundary `3541700`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_04` / `user_04`

- Request: `12693000` on `2024-06-04`; opening balance `52206950`; reserve `30686600`.
- Safe amount: expected `8401800`, actual `11584778.17`, actual-minus-expected `3182978.17`.
- Earliest full payment: expected `2024-06-15`, actual `2024-06-15`.
- Status/method: expected `affordable_later/wait`, actual `affordable_later/wait`.
- Actual trough: `42271378.17` on `2024-06-13`; expected-implied reserve boundary `39088400`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_05` / `user_05`

- Request: `15488` on `2025-11-06`; opening balance `46475.1`; reserve `13100`.
- Safe amount: expected `737`, actual `7006.21`, actual-minus-expected `6269.21`.
- Earliest full payment: expected `none`, actual `none`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `20106.21` on `2026-02-02`; expected-implied reserve boundary `13837`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_06` / `user_06`

- Request: `620.4` on `2026-01-03`; opening balance `1942.4`; reserve `800`.
- Safe amount: expected `603.3`, actual `620.4`, actual-minus-expected `17.1`.
- Earliest full payment: expected `2026-01-15`, actual `2026-01-03`.
- Status/method: expected `affordable_with_plan/full_payment`, actual `affordable_now/full_payment`.
- Actual trough: `1430.32` on `2026-01-13`; expected-implied reserve boundary `1403.3`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_07` / `user_07`

- Request: `197400` on `2024-09-05`; opening balance `218945.56`; reserve `93000`.
- Safe amount: expected `87170.56`, actual `98080.53`, actual-minus-expected `10909.97`.
- Earliest full payment: expected `2024-10-23`, actual `2024-10-23`.
- Status/method: expected `affordable_with_plan/installments`, actual `affordable_with_plan/installments`.
- Actual trough: `191080.53` on `2024-09-20`; expected-implied reserve boundary `180170.56`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_08` / `user_08`

- Request: `996.6` on `2025-02-07`; opening balance `1536.57`; reserve `800`.
- Safe amount: expected `284.57`, actual `383.59`, actual-minus-expected `99.02`.
- Earliest full payment: expected `2025-04-15`, actual `2025-04-15`.
- Status/method: expected `affordable_later/wait`, actual `affordable_later/wait`.
- Actual trough: `1183.59` on `2025-02-12`; expected-implied reserve boundary `1084.57`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_09` / `user_09`

- Request: `166.61` on `2026-07-04`; opening balance `2231.1`; reserve `600`.
- Safe amount: expected `166.61`, actual `166.61`, actual-minus-expected `0.00`.
- Earliest full payment: expected `2026-07-04`, actual `2026-07-04`.
- Status/method: expected `affordable_now/full_payment`, actual `affordable_now/full_payment`.
- Actual trough: `2051.84` on `2026-07-19`; expected-implied reserve boundary `766.61`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_10` / `user_10`

- Request: `266700` on `2024-12-06`; opening balance `750155`; reserve `225400`.
- Safe amount: expected `12700`, actual `266700`, actual-minus-expected `254000`.
- Earliest full payment: expected `none`, actual `2024-12-06`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `725801.48` on `2024-12-07`; expected-implied reserve boundary `238100`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_11` / `user_11`

- Request: `13110000` on `2025-05-03`; opening balance `63531795`; reserve `34140600`.
- Safe amount: expected `12510645`, actual `13110000`, actual-minus-expected `599355`.
- Earliest full payment: expected `2025-07-15`, actual `2025-05-03`.
- Status/method: expected `affordable_with_plan/full_payment`, actual `affordable_now/full_payment`.
- Actual trough: `48809337.19` on `2025-05-14`; expected-implied reserve boundary `46651245`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_12` / `user_12`

- Request: `65164` on `2026-04-05`; opening balance `193089.89`; reserve `43200`.
- Safe amount: expected `65164`, actual `65164`, actual-minus-expected `0`.
- Earliest full payment: expected `2026-04-05`, actual `2026-04-05`.
- Status/method: expected `affordable_with_plan/installments`, actual `affordable_with_plan/installments`.
- Actual trough: `183546.53` on `2026-04-11`; expected-implied reserve boundary `108364`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_13` / `user_13`

- Request: `941.6` on `2024-03-07`; opening balance `2789.52`; reserve `1300`.
- Safe amount: expected `433.4`, actual `941.6`, actual-minus-expected `508.2`.
- Earliest full payment: expected `2024-05-15`, actual `2024-03-07`.
- Status/method: expected `affordable_later/wait`, actual `affordable_now/full_payment`.
- Actual trough: `2538.37` on `2024-03-14`; expected-implied reserve boundary `1733.4`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_14` / `user_14`

- Request: `5414.2` on `2025-08-04`; opening balance `3931.74`; reserve `2200`.
- Safe amount: expected `597.74`, actual `613.64`, actual-minus-expected `15.90`.
- Earliest full payment: expected `none`, actual `none`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `2813.64` on `2025-08-14`; expected-implied reserve boundary `2797.74`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_15` / `user_15`

- Request: `3685` on `2026-01-06`; opening balance `1770.05`; reserve `1200`.
- Safe amount: expected `83.05`, actual `225.66`, actual-minus-expected `142.61`.
- Earliest full payment: expected `none`, actual `none`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `1425.66` on `2026-01-13`; expected-implied reserve boundary `1283.05`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_16` / `user_16`

- Request: `122500` on `2023-08-12`; opening balance `362370`; reserve `122400`.
- Safe amount: expected `122500`, actual `122500`, actual-minus-expected `0`.
- Earliest full payment: expected `2023-08-12`, actual `2023-08-12`.
- Status/method: expected `affordable_now/full_payment`, actual `affordable_now/full_payment`.
- Actual trough: `284780.16` on `2023-09-13`; expected-implied reserve boundary `244900`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_17` / `user_17`

- Request: `274600` on `2026-03-01`; opening balance `550379.58`; reserve `166100`.
- Safe amount: expected `243849.58`, actual `248325.96`, actual-minus-expected `4476.38`.
- Earliest full payment: expected `2026-03-15`, actual `2026-03-15`.
- Status/method: expected `affordable_with_plan/installments`, actual `affordable_with_plan/installments`.
- Actual trough: `414425.96` on `2026-03-13`; expected-implied reserve boundary `409949.58`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_18` / `user_18`

- Request: `3246.1` on `2026-07-07`; opening balance `2486`; reserve `1400`.
- Safe amount: expected `462`, actual `662.19`, actual-minus-expected `200.19`.
- Earliest full payment: expected `2026-09-15`, actual `2026-08-15`.
- Status/method: expected `affordable_later/wait`, actual `affordable_later/wait`.
- Actual trough: `2062.19` on `2026-07-11`; expected-implied reserve boundary `1862`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_19` / `user_19`

- Request: `39660` on `2024-09-04`; opening balance `199545`; reserve `92800`.
- Safe amount: expected `28820`, actual `37555.87`, actual-minus-expected `8735.87`.
- Earliest full payment: expected `2024-09-15`, actual `2024-09-15`.
- Status/method: expected `affordable_with_plan/partial_payment`, actual `affordable_with_plan/partial_payment`.
- Actual trough: `130355.87` on `2024-09-14`; expected-implied reserve boundary `121620`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_20` / `user_20`

- Request: `303700` on `2026-02-07`; opening balance `102609.05`; reserve `64500`.
- Safe amount: expected `5400`, actual `14941.75`, actual-minus-expected `9541.75`.
- Earliest full payment: expected `none`, actual `none`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `79441.75` on `2026-02-13`; expected-implied reserve boundary `69900`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_21` / `user_21`

- Request: `1574.4` on `2026-04-03`; opening balance `3911.35`; reserve `1800`.
- Safe amount: expected `1543.35`, actual `1574.4`, actual-minus-expected `31.05`.
- Earliest full payment: expected `2026-04-15`, actual `2026-04-03`.
- Status/method: expected `affordable_with_plan/full_payment`, actual `affordable_now/full_payment`.
- Actual trough: `3445.70` on `2026-04-12`; expected-implied reserve boundary `3343.35`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_22` / `user_22`

- Request: `731.5` on `2024-12-05`; opening balance `1132.46`; reserve `500`.
- Safe amount: expected `475.46`, actual `514.86`, actual-minus-expected `39.40`.
- Earliest full payment: expected `2025-01-15`, actual `2024-12-15`.
- Status/method: expected `affordable_with_plan/installments`, actual `affordable_with_plan/installments`.
- Actual trough: `1014.86` on `2024-12-14`; expected-implied reserve boundary `975.46`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_23` / `user_23`

- Request: `38016` on `2025-05-07`; opening balance `51957.9`; reserve `27000`.
- Safe amount: expected `9152`, actual `9303.91`, actual-minus-expected `151.91`.
- Earliest full payment: expected `2025-07-15`, actual `2025-07-15`.
- Status/method: expected `affordable_later/wait`, actual `affordable_later/wait`.
- Actual trough: `36303.91` on `2025-05-14`; expected-implied reserve boundary `36152`.
- First actual incompatibility under the expected full-payment constraint: `not observed in this bounded path`.

## `request_24` / `user_24`

- Request: `109600` on `2026-01-04`; opening balance `85045`; reserve `51000`.
- Safe amount: expected `13420`, actual `12557.36`, actual-minus-expected `-862.64`.
- Earliest full payment: expected `none`, actual `none`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `63557.36` on `2026-01-13`; expected-implied reserve boundary `64420`.
- First actual incompatibility under the expected full-payment constraint: `2026-01-13`.

## `request_25` / `user_25`

- Request: `60496000` on `2024-03-06`; opening balance `32063050`; reserve `23379100`.
- Safe amount: expected `1425000`, actual `0`, actual-minus-expected `-1425000`.
- Earliest full payment: expected `none`, actual `none`.
- Status/method: expected `not_affordable/not_recommended`, actual `not_affordable/not_recommended`.
- Actual trough: `22772958.09` on `2024-03-14`; expected-implied reserve boundary `24804100`.
- First actual incompatibility under the expected full-payment constraint: `2024-03-09`.
