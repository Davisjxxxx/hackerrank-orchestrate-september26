# S16 future-flow delta and collision audit

This is a read-only diagnostic of the current production path. Expected solved-row values are used only for arithmetic attribution, never by production code.

- Non-exact requests: `22/25`
- Differing fields: `53`

## `request_02` / `user_02`

- Safe amount: expected `17229139.2`, actual `18479330.16`, actual-minus-expected `1250190.96`.
- Earliest full payment: expected `2025-09-15`, actual `2025-09-15`.
- Current limiting balance: `47637730.16` on `2025-08-13` with flow `-369550`.
- Expected implied limiting balance at the same minimum reserve: `46387539.2`.
- Ranked one/two-flow arithmetic candidates:
  - error `79156.48`: event_174@2025-08-12 (1329347.44 transport)
  - error `79156.48`: event_174@2025-08-26 (1329347.44 transport)
  - error `79156.48`: event_174@2025-09-09 (1329347.44 transport)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2025-08-07 | -2141849.94 | `event_138@2025-08-07` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2025-08-08 | -1132400 | `event_139@2025-08-08` | insurance / Household insurance | projected | `recurrence:max_last_3` |
| 2025-08-08 | -1651100 | `event_185` | shopping / Pending merchant debit | explicit | `structured` |
| 2025-08-09 | -3040000 | `event_140@2025-08-09` | education / Course tuition | projected | `recurrence:max_last_3` |
| 2025-08-11 | -1641668.72 | `event_141@2025-08-11` | healthcare / Clinic payment | projected | `recurrence:max_last_3` |
| 2025-08-12 | -1440242.94 | `event_168@2025-08-12` | transport / Ride-hailing trip | projected | `recurrence:max_last_3` |
| 2025-08-12 | -1329347.44 | `event_174@2025-08-12` | transport / Commuter pass | projected | `recurrence:max_last_3` |
| 2025-08-13 | -369550 | `event_143@2025-08-13` | cloud_storage / Shared storage plan | projected | `recurrence:max_last_3` |

## `request_03` / `user_03`

- Safe amount: expected `873000`, actual `1050071.39`, actual-minus-expected `177071.39`.
- Earliest full payment: expected `2019-11-15`, actual `2019-11-15`.
- Current limiting balance: `3718771.39` on `2019-09-14` with flow `-201295.29`.
- Expected implied limiting balance at the same minimum reserve: `3541700`.
- Ranked one/two-flow arithmetic candidates:
  - error `3323.90`: event_216@2019-09-14 (180395.29 shopping)
  - error `3323.90`: event_216@2019-10-14 (180395.29 shopping)
  - error `3323.90`: event_216@2019-11-14 (180395.29 shopping)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2019-09-04 | -1140000 | `event_212@2019-09-04` | rent / Landlord standing order | projected | `recurrence:max_last_3` |
| 2019-09-07 | -95000 | `event_254` | healthcare / Pending pharmacy card charge | explicit | `structured` |
| 2019-09-08 | -303042.45 | `event_213@2019-09-08` | utilities / Water and power payment | projected | `recurrence:max_last_3` |
| 2019-09-08 | -234390.87 | `event_219@2019-09-08` | groceries / Bulk pantry shop | projected | `recurrence:max_last_3` |
| 2019-09-11 | -117800 | `event_215@2019-09-11` | streaming / Video streaming plan | projected | `recurrence:max_last_3` |
| 2019-09-14 | -20900 | `event_214@2019-09-14` | cloud_storage / Shared storage plan | projected | `recurrence:max_last_3` |
| 2019-09-14 | -180395.29 | `event_216@2019-09-14` | shopping / Clothing and household items | projected | `recurrence:max_last_3` |

## `request_04` / `user_04`

- Safe amount: expected `8401800`, actual `11584778.17`, actual-minus-expected `3182978.17`.
- Earliest full payment: expected `2024-06-15`, actual `2024-06-15`.
- Current limiting balance: `42271378.17` on `2024-06-13` with flow `-3429476.1`.
- Expected implied limiting balance at the same minimum reserve: `39088400`.
- Ranked one/two-flow arithmetic candidates:
  - error `63941.83`: event_357 (1704300 education), event_290@2024-06-13 (1542620 entertainment)
  - error `63941.83`: event_357 (1704300 education), event_290@2024-07-13 (1542620 entertainment)
  - error `63941.83`: event_357 (1704300 education), event_290@2024-08-13 (1542620 entertainment)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-06-05 | -2033868.83 | `event_286@2024-06-05` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2024-06-09 | -1027900 | `event_289@2024-06-09` | gym / Gym membership | projected | `recurrence:max_last_3` |
| 2024-06-09 | -1030376.9 | `event_341@2024-06-09` | transport / Ride-hailing trip | projected | `recurrence:max_last_3` |
| 2024-06-10 | -332500 | `event_287@2024-06-10` | music_subscription / Music service subscription | projected | `recurrence:max_last_3` |
| 2024-06-11 | -1704300 | `event_357` | education / Scheduled school fee | explicit | `structured` |
| 2024-06-12 | -377150 | `event_288@2024-06-12` | delivery_membership / Food delivery membership | projected | `recurrence:max_last_3` |
| 2024-06-13 | -1542620 | `event_290@2024-06-13` | entertainment / Local event tickets | projected | `recurrence:max_last_3` |
| 2024-06-13 | -1886856.1 | `event_355@2024-06-13` | dining / Bakery and snacks | projected | `recurrence:max_last_3` |

## `request_05` / `user_05`

- Safe amount: expected `737`, actual `7006.21`, actual-minus-expected `6269.21`.
- Earliest full payment: expected `none`, actual `none`.
- Current limiting balance: `20106.21` on `2026-02-02` with flow `-4972`.
- Expected implied limiting balance at the same minimum reserve: `13837`.
- Ranked one/two-flow arithmetic candidates:
  - error `329.21`: event_393@2025-11-11 (968 debt_repayment), event_398@2025-12-02 (4972 rent)
  - error `329.21`: event_393@2025-11-11 (968 debt_repayment), event_398@2026-01-02 (4972 rent)
  - error `329.21`: event_393@2025-11-11 (968 debt_repayment), event_398@2026-02-02 (4972 rent)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2025-11-06 | -750.89 | `event_392@2025-11-06` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2025-11-10 | -722.37 | `event_394@2025-11-10` | healthcare / Therapy appointment | projected | `recurrence:max_last_3` |
| 2025-11-11 | -968 | `event_393@2025-11-11` | debt_repayment / Vehicle loan payment | projected | `recurrence:max_last_3` |
| 2025-11-12 | -113.3 | `event_396@2025-11-12` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2025-11-12 | -422.67 | `event_397@2025-11-12` | shopping / Personal shopping | projected | `recurrence:max_last_3` |
| 2025-11-13 | -840.4 | `event_395@2025-11-13` | family_support / Dependent care payment | projected | `recurrence:max_last_3` |
| 2025-12-02 | -4972 | `event_398@2025-12-02` | rent / Apartment rent transfer | projected | `recurrence:max_last_3` |
| 2025-12-06 | -750.89 | `event_392@2025-12-06` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2025-12-10 | -722.37 | `event_394@2025-12-10` | healthcare / Therapy appointment | projected | `recurrence:max_last_3` |
| 2025-12-11 | -968 | `event_393@2025-12-11` | debt_repayment / Vehicle loan payment | projected | `recurrence:max_last_3` |
| 2025-12-12 | -113.3 | `event_396@2025-12-12` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2025-12-12 | -422.67 | `event_397@2025-12-12` | shopping / Personal shopping | projected | `recurrence:max_last_3` |
| 2025-12-13 | -840.4 | `event_395@2025-12-13` | family_support / Dependent care payment | projected | `recurrence:max_last_3` |
| 2026-01-02 | -4972 | `event_398@2026-01-02` | rent / Apartment rent transfer | projected | `recurrence:max_last_3` |
| 2026-01-06 | -750.89 | `event_392@2026-01-06` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2026-01-10 | -722.37 | `event_394@2026-01-10` | healthcare / Therapy appointment | projected | `recurrence:max_last_3` |
| 2026-01-11 | -968 | `event_393@2026-01-11` | debt_repayment / Vehicle loan payment | projected | `recurrence:max_last_3` |
| 2026-01-12 | -113.3 | `event_396@2026-01-12` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2026-01-12 | -422.67 | `event_397@2026-01-12` | shopping / Personal shopping | projected | `recurrence:max_last_3` |
| 2026-01-13 | -840.4 | `event_395@2026-01-13` | family_support / Dependent care payment | projected | `recurrence:max_last_3` |
| 2026-02-02 | -4972 | `event_398@2026-02-02` | rent / Apartment rent transfer | projected | `recurrence:max_last_3` |

## `request_06` / `user_06`

- Safe amount: expected `603.3`, actual `620.4`, actual-minus-expected `17.1`.
- Earliest full payment: expected `2026-01-15`, actual `2026-01-03`.
- Current limiting balance: `1430.32` on `2026-01-13` with flow `-44.88`.
- Expected implied limiting balance at the same minimum reserve: `1403.3`.
- Ranked one/two-flow arithmetic candidates:
  - error `1.9`: event_476@2026-01-10 (19 streaming)
  - error `1.9`: event_476@2026-02-10 (19 streaming)
  - error `1.9`: event_476@2026-03-10 (19 streaming)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-01-03 | -254.1 | `event_472@2026-01-03` | rent / Monthly rent | projected | `recurrence:max_last_3` |
| 2026-01-07 | -58.98 | `event_473@2026-01-07` | utilities / Water and power payment | projected | `recurrence:max_last_3` |
| 2026-01-07 | -51.55 | `event_489@2026-01-07` | groceries / Fresh food shop | projected | `recurrence:max_last_3` |
| 2026-01-08 | -26 | `event_474@2026-01-08` | insurance / Vehicle insurance premium | projected | `recurrence:max_last_3` |
| 2026-01-10 | -19 | `event_476@2026-01-10` | streaming / Family streaming plan | projected | `recurrence:max_last_3` |
| 2026-01-11 | -57.57 | `event_552@2026-01-11` | dining / Neighbourhood restaurant | projected | `recurrence:max_last_3` |
| 2026-01-13 | -5 | `event_475@2026-01-13` | cloud_storage / Shared storage plan | projected | `recurrence:max_last_3` |
| 2026-01-13 | -39.88 | `event_477@2026-01-13` | shopping / Household shopping | projected | `recurrence:max_last_3` |

## `request_07` / `user_07`

- Safe amount: expected `87170.56`, actual `98080.53`, actual-minus-expected `10909.97`.
- Earliest full payment: expected `2024-10-23`, actual `2024-10-23`.
- Current limiting balance: `191080.53` on `2024-09-20` with flow `-3822.62`.
- Expected implied limiting balance at the same minimum reserve: `180170.56`.
- Ranked one/two-flow arithmetic candidates:
  - error `300.06`: event_580@2024-09-08 (7387.41 utilities), event_604@2024-09-20 (3822.62 transport)
  - error `300.06`: event_580@2024-09-08 (7387.41 utilities), event_604@2024-10-11 (3822.62 transport)
  - error `300.06`: event_580@2024-09-08 (7387.41 utilities), event_604@2024-11-01 (3822.62 transport)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-09-08 | -7387.41 | `event_580@2024-09-08` | utilities / Electricity bill | projected | `recurrence:max_last_3` |
| 2024-09-13 | -15650 | `event_581@2024-09-13` | debt_repayment / Personal loan payment | projected | `recurrence:max_last_3` |
| 2024-09-13 | -1005 | `event_582@2024-09-13` | music_subscription / Music subscription | projected | `recurrence:max_last_3` |
| 2024-09-20 | -3822.62 | `event_604@2024-09-20` | transport / Rail pass | projected | `recurrence:max_last_3` |

## `request_08` / `user_08`

- Safe amount: expected `284.57`, actual `383.59`, actual-minus-expected `99.02`.
- Earliest full payment: expected `2025-04-15`, actual `2025-04-15`.
- Current limiting balance: `1183.59` on `2025-02-12` with flow `-24`.
- Expected implied limiting balance at the same minimum reserve: `1084.57`.
- Ranked one/two-flow arithmetic candidates:
  - error `0.67`: event_649@2025-02-12 (24 delivery_membership), event_661@2025-02-18 (74.35 groceries)
  - error `0.67`: event_649@2025-02-12 (24 delivery_membership), event_661@2025-03-04 (74.35 groceries)
  - error `0.67`: event_649@2025-02-12 (24 delivery_membership), event_661@2025-03-18 (74.35 groceries)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2025-02-07 | -89 | `event_646@2025-02-07` | education / School fee payment | projected | `recurrence:max_last_3` |
| 2025-02-10 | -177 | `event_647@2025-02-10` | debt_repayment / Personal loan payment | projected | `recurrence:max_last_3` |
| 2025-02-10 | -14 | `event_648@2025-02-10` | music_subscription / Music subscription | projected | `recurrence:max_last_3` |
| 2025-02-10 | -48.98 | `event_708@2025-02-10` | dining / Neighbourhood restaurant | projected | `recurrence:max_last_3` |
| 2025-02-12 | -24 | `event_649@2025-02-12` | delivery_membership / Grocery delivery membership | projected | `recurrence:max_last_3` |

## `request_09` / `user_09`

- Safe amount: expected `166.61`, actual `166.61`, actual-minus-expected `0.00`.
- Earliest full payment: expected `2026-07-04`, actual `2026-07-04`.
- Current limiting balance: `2051.84` on `2026-07-19` with flow `-54.9`.
- Expected implied limiting balance at the same minimum reserve: `766.61`.
- Ranked one/two-flow arithmetic candidates:
  - error `5.00`: event_749@2026-07-12 (5 cloud_storage)
  - error `5.00`: event_749@2026-08-12 (5 cloud_storage)
  - error `5.00`: event_749@2026-09-12 (5 cloud_storage)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-07-06 | -71.04 | `event_748@2026-07-06` | utilities / Water and power payment | projected | `recurrence:max_last_3` |
| 2026-07-09 | -20 | `event_750@2026-07-09` | streaming / Video streaming plan | projected | `recurrence:max_last_3` |
| 2026-07-12 | -5 | `event_749@2026-07-12` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2026-07-12 | -28.32 | `event_751@2026-07-12` | shopping / Household shopping | projected | `recurrence:max_last_3` |
| 2026-07-19 | -54.9 | `event_760@2026-07-19` | groceries / Local market purchase | projected | `recurrence:max_last_3` |

## `request_10` / `user_10`

- Safe amount: expected `12700`, actual `266700`, actual-minus-expected `254000`.
- Earliest full payment: expected `none`, actual `2024-12-06`.
- Current limiting balance: `725801.48` on `2024-12-07` with flow `-17771.13`.
- Expected implied limiting balance at the same minimum reserve: `238100`.
- Ranked one/two-flow arithmetic candidates:
  - error `88665.46`: event_832@2024-12-10 (82667.27 salary), event_832@2024-12-25 (82667.27 salary)
  - error `88665.46`: event_832@2024-12-10 (82667.27 salary), event_832@2025-01-09 (82667.27 salary)
  - error `88665.46`: event_832@2024-12-10 (82667.27 salary), event_832@2025-01-24 (82667.27 salary)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-12-06 | -6582.39 | `event_883@2024-12-06` | transport / Local taxi | projected | `recurrence:max_last_3` |
| 2024-12-07 | -17771.13 | `event_834@2024-12-07` | utilities / Electricity and water bill | projected | `recurrence:max_last_3` |

## `request_11` / `user_11`

- Safe amount: expected `12510645`, actual `13110000`, actual-minus-expected `599355`.
- Earliest full payment: expected `2025-07-15`, actual `2025-05-03`.
- Current limiting balance: `48809337.19` on `2025-05-14` with flow `-168150`.
- Expected implied limiting balance at the same minimum reserve: `46651245`.
- Ranked one/two-flow arithmetic candidates:
  - error `263055`: event_949@2025-05-14 (168150 cloud_storage), event_949@2025-06-14 (168150 cloud_storage)
  - error `263055`: event_949@2025-05-14 (168150 cloud_storage), event_949@2025-07-14 (168150 cloud_storage)
  - error `263055`: event_949@2025-06-14 (168150 cloud_storage), event_949@2025-07-14 (168150 cloud_storage)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2025-05-05 | -2954500 | `event_943@2025-05-05` | housing / Home association fee | projected | `recurrence:max_last_3` |
| 2025-05-05 | -1212904.33 | `event_972@2025-05-05` | transport / Metro and bus fares | projected | `recurrence:max_last_3` |
| 2025-05-08 | -2796165.18 | `event_944@2025-05-08` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2025-05-09 | -1881000 | `event_945@2025-05-09` | insurance / Vehicle insurance premium | projected | `recurrence:max_last_3` |
| 2025-05-10 | -2544100 | `event_946@2025-05-10` | education / Child education fee | projected | `recurrence:max_last_3` |
| 2025-05-12 | -3165638.3 | `event_947@2025-05-12` | healthcare / Regular medicine purchase | projected | `recurrence:max_last_3` |
| 2025-05-14 | -168150 | `event_949@2025-05-14` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |

## `request_13` / `user_13`

- Safe amount: expected `433.4`, actual `941.6`, actual-minus-expected `508.2`.
- Earliest full payment: expected `2024-05-15`, actual `2024-03-07`.
- Current limiting balance: `2538.37` on `2024-03-14` with flow `-37.9`.
- Expected implied limiting balance at the same minimum reserve: `1733.4`.
- Ranked one/two-flow arithmetic candidates:
  - error `114.4`: event_1094@2024-04-02 (622.6 rent)
  - error `114.4`: event_1094@2024-05-02 (622.6 rent)
  - error `114.4`: event_1094@2024-06-02 (622.6 rent)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-03-10 | -61 | `event_1092@2024-03-10` | gym / Community fitness plan | projected | `recurrence:max_last_3` |
| 2024-03-11 | -29 | `event_1090@2024-03-11` | music_subscription / Music subscription | projected | `recurrence:max_last_3` |
| 2024-03-12 | -102.25 | `event_1114@2024-03-12` | groceries / Local market purchase | projected | `recurrence:max_last_3` |
| 2024-03-13 | -21 | `event_1091@2024-03-13` | delivery_membership / Delivery service plan | projected | `recurrence:max_last_3` |
| 2024-03-14 | -37.9 | `event_1093@2024-03-14` | entertainment / Local event tickets | projected | `recurrence:max_last_3` |

## `request_14` / `user_14`

- Safe amount: expected `597.74`, actual `613.64`, actual-minus-expected `15.90`.
- Earliest full payment: expected `none`, actual `none`.
- Current limiting balance: `2813.64` on `2025-08-14` with flow `-226`.
- Expected implied limiting balance at the same minimum reserve: `2797.74`.
- Ranked one/two-flow arithmetic candidates:
  - error `1.90`: event_1198@2025-08-13 (14 cloud_storage)
  - error `1.90`: event_1198@2025-09-13 (14 cloud_storage)
  - error `1.90`: event_1198@2025-10-13 (14 cloud_storage)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2025-08-07 | -153.69 | `event_1194@2025-08-07` | utilities / Energy provider bill | projected | `recurrence:max_last_3` |
| 2025-08-10 | -138.85 | `event_1225@2025-08-10` | groceries / Weekly produce market | projected | `recurrence:max_last_3` |
| 2025-08-11 | -95.17 | `event_1196@2025-08-11` | healthcare / Family healthcare expense | projected | `recurrence:max_last_3` |
| 2025-08-12 | -350 | `event_1195@2025-08-12` | debt_repayment / Credit card repayment | projected | `recurrence:max_last_3` |
| 2025-08-13 | -14 | `event_1198@2025-08-13` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2025-08-13 | -140.39 | `event_1199@2025-08-13` | shopping / Online retail purchases | projected | `recurrence:max_last_3` |
| 2025-08-14 | -226 | `event_1197@2025-08-14` | family_support / Family support payment | projected | `recurrence:max_last_3` |

## `request_15` / `user_15`

- Safe amount: expected `83.05`, actual `225.66`, actual-minus-expected `142.61`.
- Earliest full payment: expected `none`, actual `none`.
- Current limiting balance: `1425.66` on `2026-01-13` with flow `-95`.
- Expected implied limiting balance at the same minimum reserve: `1283.05`.
- Ranked one/two-flow arithmetic candidates:
  - error `1.91`: event_1269@2026-01-13 (84 debt_repayment), event_1296@2026-02-03 (56.7 groceries)
  - error `1.91`: event_1269@2026-01-13 (84 debt_repayment), event_1296@2026-03-17 (56.7 groceries)
  - error `1.91`: event_1296@2026-02-03 (56.7 groceries), event_1269@2026-02-13 (84 debt_repayment)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-01-08 | -90.39 | `event_1267@2026-01-08` | utilities / Energy provider bill | projected | `recurrence:max_last_3` |
| 2026-01-10 | -159 | `event_1268@2026-01-10` | education / School fee payment | projected | `recurrence:max_last_3` |
| 2026-01-13 | -84 | `event_1269@2026-01-13` | debt_repayment / Credit card repayment | projected | `recurrence:max_last_3` |
| 2026-01-13 | -11 | `event_1270@2026-01-13` | music_subscription / Music subscription | projected | `recurrence:max_last_3` |

## `request_17` / `user_17`

- Safe amount: expected `243849.58`, actual `248325.96`, actual-minus-expected `4476.38`.
- Earliest full payment: expected `2026-03-15`, actual `2026-03-15`.
- Current limiting balance: `414425.96` on `2026-03-13` with flow `-1675`.
- Expected implied limiting balance at the same minimum reserve: `409949.58`.
- Ranked one/two-flow arithmetic candidates:
  - error `366.38`: event_1476@2026-03-11 (2055 music_subscription), event_1476@2026-04-11 (2055 music_subscription)
  - error `366.38`: event_1476@2026-03-11 (2055 music_subscription), event_1476@2026-05-11 (2055 music_subscription)
  - error `366.38`: event_1476@2026-04-11 (2055 music_subscription), event_1476@2026-05-11 (2055 music_subscription)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-03-01 | -11433.33 | `event_1499@2026-03-01` | groceries / Local market purchase | projected | `recurrence:max_last_3` |
| 2026-03-02 | -49600 | `event_1472@2026-03-02` | rent / Apartment rent transfer | projected | `recurrence:max_last_3` |
| 2026-03-06 | -10246.53 | `event_1473@2026-03-06` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2026-03-08 | -13660 | `event_1474@2026-03-08` | education / Course tuition | projected | `recurrence:max_last_3` |
| 2026-03-09 | -5650.43 | `event_1526@2026-03-09` | transport / Metro and bus fares | projected | `recurrence:max_last_3` |
| 2026-03-11 | -30200 | `event_1475@2026-03-11` | debt_repayment / Credit card repayment | projected | `recurrence:max_last_3` |
| 2026-03-11 | -2055 | `event_1476@2026-03-11` | music_subscription / Music subscription | projected | `recurrence:max_last_3` |
| 2026-03-11 | -11433.33 | `event_1499@2026-03-11` | groceries / Local market purchase | projected | `recurrence:max_last_3` |
| 2026-03-13 | -1675 | `event_1477@2026-03-13` | delivery_membership / Food delivery membership | projected | `recurrence:max_last_3` |

## `request_18` / `user_18`

- Safe amount: expected `462`, actual `662.19`, actual-minus-expected `200.19`.
- Earliest full payment: expected `2026-09-15`, actual `2026-08-15`.
- Current limiting balance: `2062.19` on `2026-07-11` with flow `-162.41`.
- Expected implied limiting balance at the same minimum reserve: `1862`.
- Ranked one/two-flow arithmetic candidates:
  - error `6.79`: event_1573@2026-07-07 (125.4 utilities), event_1574@2026-07-08 (68 insurance)
  - error `6.79`: event_1573@2026-07-07 (125.4 utilities), event_1576@2026-07-10 (68 streaming)
  - error `6.79`: event_1573@2026-07-07 (125.4 utilities), event_1574@2026-08-08 (68 insurance)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-07-07 | -125.4 | `event_1573@2026-07-07` | utilities / Energy provider bill | projected | `recurrence:max_last_3` |
| 2026-07-08 | -68 | `event_1574@2026-07-08` | insurance / Household insurance | projected | `recurrence:max_last_3` |
| 2026-07-10 | -68 | `event_1576@2026-07-10` | streaming / Family streaming plan | projected | `recurrence:max_last_3` |
| 2026-07-11 | -162.41 | `event_1575@2026-07-11` | healthcare / Clinic payment | projected | `recurrence:max_last_3` |

## `request_19` / `user_19`

- Safe amount: expected `28820`, actual `37555.87`, actual-minus-expected `8735.87`.
- Earliest full payment: expected `2024-09-15`, actual `2024-09-15`.
- Current limiting balance: `130355.87` on `2024-09-14` with flow `-6464.58`.
- Expected implied limiting balance at the same minimum reserve: `121620`.
- Ranked one/two-flow arithmetic candidates:
  - error `14.65`: event_1667@2024-09-17 (4871.72 groceries), event_1690@2024-09-25 (3849.5 transport)
  - error `14.65`: event_1667@2024-09-17 (4871.72 groceries), event_1690@2024-10-25 (3849.5 transport)
  - error `14.65`: event_1667@2024-09-17 (4871.72 groceries), event_1690@2024-11-25 (3849.5 transport)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-09-04 | -36100 | `event_1655@2024-09-04` | rent / Residential rent payment | projected | `recurrence:max_last_3` |
| 2024-09-08 | -6129.19 | `event_1656@2024-09-08` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2024-09-12 | -8645.36 | `event_1658@2024-09-12` | healthcare / Clinic payment | projected | `recurrence:max_last_3` |
| 2024-09-13 | -11850 | `event_1657@2024-09-13` | debt_repayment / Loan repayment | projected | `recurrence:max_last_3` |
| 2024-09-14 | -395 | `event_1660@2024-09-14` | cloud_storage / Online backup subscription | projected | `recurrence:max_last_3` |
| 2024-09-14 | -6069.58 | `event_1661@2024-09-14` | shopping / Clothing and household items | projected | `recurrence:max_last_3` |

## `request_20` / `user_20`

- Safe amount: expected `5400`, actual `14941.75`, actual-minus-expected `9541.75`.
- Earliest full payment: expected `none`, actual `none`.
- Current limiting balance: `79441.75` on `2026-02-13` with flow `-2115.92`.
- Expected implied limiting balance at the same minimum reserve: `69900`.
- Ranked one/two-flow arithmetic candidates:
  - error `20.30`: event_1737@2026-02-07 (8740 education), event_1786 (822.05 utilities)
  - error `20.30`: event_1786 (822.05 utilities), event_1737@2026-03-07 (8740 education)
  - error `20.30`: event_1786 (822.05 utilities), event_1737@2026-04-07 (8740 education)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-02-07 | -8740 | `event_1737@2026-02-07` | education / School fee payment | projected | `recurrence:max_last_3` |
| 2026-02-08 | -4470 | `event_1787` | shopping / Pending online order charge | explicit | `structured` |
| 2026-02-09 | -6654.33 | `event_1738@2026-02-09` | healthcare / Family healthcare expense | projected | `recurrence:max_last_3` |
| 2026-02-09 | -822.05 | `event_1786` | utilities / Outstanding telecom bill | explicit | `ocr:image_05:grounded` |
| 2026-02-11 | -365 | `event_1740@2026-02-11` | cloud_storage / Shared storage plan | projected | `recurrence:max_last_3` |
| 2026-02-13 | -2115.92 | `event_1739@2026-02-13` | entertainment / Cinema and events | projected | `recurrence:max_last_3` |

## `request_21` / `user_21`

- Safe amount: expected `1543.35`, actual `1574.4`, actual-minus-expected `31.05`.
- Earliest full payment: expected `2026-04-15`, actual `2026-04-03`.
- Current limiting balance: `3445.70` on `2026-04-12` with flow `-137.38`.
- Expected implied limiting balance at the same minimum reserve: `3343.35`.
- Ranked one/two-flow arithmetic candidates:
  - error `9.05`: event_1815@2026-04-12 (11 cloud_storage), event_1815@2026-05-12 (11 cloud_storage)
  - error `9.05`: event_1815@2026-04-12 (11 cloud_storage), event_1815@2026-06-12 (11 cloud_storage)
  - error `9.05`: event_1815@2026-05-12 (11 cloud_storage), event_1815@2026-06-12 (11 cloud_storage)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-04-05 | -53 | `event_1857` | transport / Pending fuel authorization | explicit | `structured` |
| 2026-04-06 | -124.08 | `event_1814@2026-04-06` | utilities / Municipal utilities | projected | `recurrence:max_last_3` |
| 2026-04-06 | -104.19 | `event_1831@2026-04-06` | groceries / Weekly produce market | projected | `recurrence:max_last_3` |
| 2026-04-09 | -47 | `event_1816@2026-04-09` | streaming / Streaming subscription | projected | `recurrence:max_last_3` |
| 2026-04-12 | -11 | `event_1815@2026-04-12` | cloud_storage / Online backup subscription | projected | `recurrence:max_last_3` |
| 2026-04-12 | -126.38 | `event_1817@2026-04-12` | shopping / Monthly shopping spend | projected | `recurrence:max_last_3` |

## `request_22` / `user_22`

- Safe amount: expected `475.46`, actual `514.86`, actual-minus-expected `39.40`.
- Earliest full payment: expected `2025-01-15`, actual `2024-12-15`.
- Current limiting balance: `1014.86` on `2024-12-14` with flow `-5`.
- Expected implied limiting balance at the same minimum reserve: `975.46`.
- Ranked one/two-flow arithmetic candidates:
  - error `0.89`: event_1892@2024-12-11 (17 gym), event_1893@2024-12-15 (23.29 entertainment)
  - error `0.89`: event_1892@2024-12-11 (17 gym), event_1893@2025-01-15 (23.29 entertainment)
  - error `0.89`: event_1892@2024-12-11 (17 gym), event_1893@2025-02-15 (23.29 entertainment)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-12-05 | -15.08 | `event_1943@2024-12-05` | transport / Ride-hailing trip | projected | `recurrence:max_last_3` |
| 2024-12-07 | -31.52 | `event_1889@2024-12-07` | utilities / Electricity and water bill | projected | `recurrence:max_last_3` |
| 2024-12-08 | -43 | `event_1961` | shopping / Pending merchant debit | explicit | `structured` |
| 2024-12-11 | -17 | `event_1892@2024-12-11` | gym / Gym membership | projected | `recurrence:max_last_3` |
| 2024-12-12 | -6 | `event_1890@2024-12-12` | music_subscription / Music service subscription | projected | `recurrence:max_last_3` |
| 2024-12-14 | -5 | `event_1891@2024-12-14` | delivery_membership / Food delivery membership | projected | `recurrence:max_last_3` |

## `request_23` / `user_23`

- Safe amount: expected `9152`, actual `9303.91`, actual-minus-expected `151.91`.
- Earliest full payment: expected `2025-07-15`, actual `2025-07-15`.
- Current limiting balance: `36303.91` on `2025-05-14` with flow `-3893.21`.
- Expected implied limiting balance at the same minimum reserve: `36152`.
- Ranked one/two-flow arithmetic candidates:
  - error `143.99`: event_2000@2025-05-14 (295.9 cloud_storage)
  - error `143.99`: event_2000@2025-06-14 (295.9 cloud_storage)
  - error `143.99`: event_2000@2025-07-14 (295.9 cloud_storage)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2025-05-08 | -2915.67 | `event_1996@2025-05-08` | utilities / Electricity bill | projected | `recurrence:max_last_3` |
| 2025-05-11 | -1553.2 | `event_2042` | healthcare / Pending pharmacy card charge | explicit | `structured` |
| 2025-05-12 | -1439.91 | `event_1998@2025-05-12` | healthcare / Clinic payment | projected | `recurrence:max_last_3` |
| 2025-05-13 | -5852 | `event_1997@2025-05-13` | debt_repayment / Education loan instalment | projected | `recurrence:max_last_3` |
| 2025-05-14 | -295.9 | `event_2000@2025-05-14` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2025-05-14 | -1389.39 | `event_2001@2025-05-14` | shopping / Personal shopping | projected | `recurrence:max_last_3` |
| 2025-05-14 | -2207.92 | `event_2021@2025-05-14` | groceries / Supermarket basket | projected | `recurrence:max_last_3` |

## `request_24` / `user_24`

- Safe amount: expected `13420`, actual `12557.36`, actual-minus-expected `-862.64`.
- Earliest full payment: expected `none`, actual `none`.
- Current limiting balance: `63557.36` on `2026-01-13` with flow `-1916.16`.
- Expected implied limiting balance at the same minimum reserve: `64420`.
- Ranked one/two-flow arithmetic candidates:
  - error `152.64`: event_2079@2026-01-11 (355 cloud_storage), event_2079@2026-02-11 (355 cloud_storage)
  - error `152.64`: event_2079@2026-01-11 (355 cloud_storage), event_2079@2026-03-11 (355 cloud_storage)
  - error `152.64`: event_2079@2026-02-11 (355 cloud_storage), event_2079@2026-03-11 (355 cloud_storage)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2026-01-05 | -3490.5 | `event_2077@2026-01-05` | utilities / Household utility payment | projected | `recurrence:max_last_3` |
| 2026-01-06 | -2510 | `event_2078@2026-01-06` | insurance / Insurance policy payment | projected | `recurrence:max_last_3` |
| 2026-01-06 | -2260.73 | `event_2100@2026-01-06` | groceries / Household groceries | projected | `recurrence:max_last_3` |
| 2026-01-08 | -1200 | `event_2080@2026-01-08` | streaming / Family streaming plan | projected | `recurrence:max_last_3` |
| 2026-01-09 | -1600.18 | `event_2133@2026-01-09` | transport / Metro and bus fares | projected | `recurrence:max_last_3` |
| 2026-01-10 | -1893.38 | `event_2155@2026-01-10` | dining / Coffee shop | projected | `recurrence:max_last_3` |
| 2026-01-11 | -355 | `event_2079@2026-01-11` | cloud_storage / Online backup subscription | projected | `recurrence:max_last_3` |
| 2026-01-11 | -2680.78 | `event_2081@2026-01-11` | shopping / Monthly shopping spend | projected | `recurrence:max_last_3` |
| 2026-01-11 | -1830 | `event_2166` | insurance / Scheduled insurance payment | explicit | `structured` |
| 2026-01-12 | -1750.91 | `event_2121@2026-01-12` | transport / Ride-hailing trip | projected | `recurrence:max_last_3` |
| 2026-01-13 | -1916.16 | `event_2082@2026-01-13` | entertainment / Local event tickets | projected | `recurrence:max_last_3` |

## `request_25` / `user_25`

- Safe amount: expected `1425000`, actual `0`, actual-minus-expected `-1425000`.
- Earliest full payment: expected `none`, actual `none`.
- Current limiting balance: `22772958.09` on `2024-03-14` with flow `-504697.37`.
- Expected implied limiting balance at the same minimum reserve: `24804100`.
- Ranked one/two-flow arithmetic candidates:
  - error `8112.66`: event_2247@2024-03-15 (695049.46 transport), event_2248@2024-03-31 (721837.88 transport)
  - error `8112.66`: event_2247@2024-03-15 (695049.46 transport), event_2248@2024-04-30 (721837.88 transport)
  - error `8112.66`: event_2247@2024-03-15 (695049.46 transport), event_2248@2024-05-31 (721837.88 transport)
- Cash flows through the current limiting date:

| Date | Signed home amount | Event | Category | Explicit/projected | Provenance |
|---|---:|---|---|---|---|
| 2024-03-06 | -1341541.39 | `event_2201@2024-03-06` | utilities / Household utility payment | projected | `recurrence:max_last_3` |
| 2024-03-06 | -949118.03 | `event_2283@2024-03-06` | dining / Coffee shop | projected | `recurrence:max_last_3` |
| 2024-03-07 | -904400 | `event_2202@2024-03-07` | insurance / Insurance policy payment | projected | `recurrence:max_last_3` |
| 2024-03-08 | -1369082.68 | `event_2223@2024-03-08` | groceries / Household groceries | projected | `recurrence:max_last_3` |
| 2024-03-08 | -1249486.33 | `event_2270@2024-03-08` | dining / Weekend food delivery | projected | `recurrence:max_last_3` |
| 2024-03-09 | -573800 | `event_2204@2024-03-09` | streaming / Video streaming plan | projected | `recurrence:max_last_3` |
| 2024-03-09 | -1101344.82 | `event_2218@2024-03-09` | groceries / Neighbourhood grocer | projected | `recurrence:max_last_3` |
| 2024-03-12 | -126350 | `event_2203@2024-03-12` | cloud_storage / Cloud storage plan | projected | `recurrence:max_last_3` |
| 2024-03-12 | -1170271.29 | `event_2205@2024-03-12` | shopping / Monthly shopping spend | projected | `recurrence:max_last_3` |
| 2024-03-14 | -504697.37 | `event_2206@2024-03-14` | entertainment / Games and recreation | projected | `recurrence:max_last_3` |

## Explicit-future versus projected collisions

These rows share user, direction, event type, category, currency, flexibility, and settlement date. Description differences do not prevent the audit.

| Request | Explicit | Date | Explicit amount/description | Projected | Projected amount/description | Both counted |
|---|---|---|---|---|---|---|
