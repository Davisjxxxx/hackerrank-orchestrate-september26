# S16 exact mismatch matrix

| request_id | differing field | expected | actual | likely root cause |
|---|---|---:|---:|---|
| `request_02` | `amount_safe_to_pay` | `17229139.2` | `18479330.16` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_03` | `amount_safe_to_pay` | `873000` | `1050071.39` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_04` | `amount_safe_to_pay` | `8401800` | `11584778.17` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_04` | `decision_explanation` | `Wait until 15 June 2024, then pay IDR 12,693,000 in full. Paying sooner would put the IDR 30,686,600 minimum at risk.` | `Pay IDR 12,693,000 in full on 15 June 2024. Paying earlier would take the balance below the IDR 30,686,600 minimum.` | deterministic explanation family follows the selected decision |
| `request_05` | `amount_safe_to_pay` | `737` | `7006.21` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_05` | `decision_explanation` | `Do not make this payment by 12 January 2026. None of the available options keeps the ZAR 13,100 minimum protected.` | `Do not proceed with the ZAR 15,488 request. Although ZAR 7,006.21 is available today, the full amount cannot be completed safely within 90 days.` | deterministic explanation family follows the selected decision |
| `request_06` | `amount_safe_to_pay` | `603.3` | `620.4` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_06` | `affordability_status` | `affordable_with_plan` | `affordable_now` | planner eligibility/status derived from the forecast predicate |
| `request_06` | `earliest_date_for_full_payment` | `2026-01-15` | `2026-01-03` | forecast date calculation / same-day ordering |
| `request_06` | `spending_changes_needed` | `stop:event_476` | `none` | spending-change legality/enumeration or binding forecast trough |
| `request_06` | `decision_explanation` | `Stop the family streaming plan, then pay EUR 620.40 today. This leaves at least EUR 800 available.` | `Pay EUR 620.40 today. This leaves at least EUR 800 available over the next 90 days.` | deterministic explanation family follows the selected decision |
| `request_07` | `amount_safe_to_pay` | `87170.56` | `98080.53` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_08` | `amount_safe_to_pay` | `284.57` | `383.59` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_09` | `decision_explanation` | `Pay EUR 166.61 today. This keeps the EUR 600 minimum available over the next 90 days.` | `Pay EUR 166.61 today. This leaves at least EUR 600 available over the next 90 days.` | deterministic explanation family follows the selected decision |
| `request_10` | `amount_safe_to_pay` | `12700` | `266700` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_10` | `earliest_date_for_full_payment` | `` | `2024-12-06` | forecast date calculation / same-day ordering |
| `request_10` | `decision_explanation` | `Do not make this payment by 10 February 2025. None of the available options keeps the INR 225,400 minimum protected.` | `Do not proceed with the INR 266,700 request. Although INR 266,700 is available today, the full amount cannot be completed safely within 90 days.` | deterministic explanation family follows the selected decision |
| `request_11` | `amount_safe_to_pay` | `12510645` | `13110000` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_11` | `affordability_status` | `affordable_with_plan` | `affordable_now` | planner eligibility/status derived from the forecast predicate |
| `request_11` | `earliest_date_for_full_payment` | `2025-07-15` | `2025-05-03` | forecast date calculation / same-day ordering |
| `request_11` | `spending_changes_needed` | `reduce_to:event_989:665950` | `none` | spending-change legality/enumeration or binding forecast trough |
| `request_11` | `decision_explanation` | `Reduce the weekend food delivery to IDR 665,950, then pay IDR 13,110,000 today. This leaves at least IDR 34,140,600 available.` | `Pay IDR 13,110,000 today. This leaves at least IDR 34,140,600 available over the next 90 days.` | deterministic explanation family follows the selected decision |
| `request_13` | `amount_safe_to_pay` | `433.4` | `941.6` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_13` | `affordability_status` | `affordable_later` | `affordable_now` | planner eligibility/status derived from the forecast predicate |
| `request_13` | `recommended_payment_method` | `wait` | `full_payment` | planner candidate eligibility/ranking derived from the forecast predicate |
| `request_13` | `payment_plan` | `2024-05-15:941.60` | `2024-03-07:941.60` | planner date/amount construction or field-specific serialization |
| `request_13` | `earliest_date_for_full_payment` | `2024-05-15` | `2024-03-07` | forecast date calculation / same-day ordering |
| `request_13` | `decision_explanation` | `Pay EUR 941.60 in full on 15 May 2024. Paying earlier would take the balance below the EUR 1,300 minimum.` | `Pay EUR 941.60 today. This leaves at least EUR 1,300 available over the next 90 days.` | deterministic explanation family follows the selected decision |
| `request_14` | `amount_safe_to_pay` | `597.74` | `613.64` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_14` | `decision_explanation` | `Do not proceed with the EUR 5,414.20 request. Although EUR 597.74 is available today, the full amount cannot be completed safely within 90 days.` | `Do not proceed with the EUR 5,414.20 request. Although EUR 613.64 is available today, the full amount cannot be completed safely within 90 days.` | deterministic explanation family follows the selected decision |
| `request_15` | `amount_safe_to_pay` | `83.05` | `225.66` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_15` | `decision_explanation` | `Do not make this payment by 1 February 2026. None of the available options keeps the EUR 1,200 minimum protected.` | `Do not proceed with the EUR 3,685 request. Although EUR 225.66 is available today, the full amount cannot be completed safely within 90 days.` | deterministic explanation family follows the selected decision |
| `request_17` | `amount_safe_to_pay` | `243849.58` | `248325.96` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_18` | `amount_safe_to_pay` | `462` | `662.19` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_18` | `payment_plan` | `2026-09-15:3246.10` | `2026-08-15:3246.10` | planner date/amount construction or field-specific serialization |
| `request_18` | `earliest_date_for_full_payment` | `2026-09-15` | `2026-08-15` | forecast date calculation / same-day ordering |
| `request_18` | `decision_explanation` | `Pay EUR 3,246.10 in full on 15 September 2026. Paying earlier would take the balance below the EUR 1,400 minimum.` | `Pay EUR 3,246.10 in full on 15 August 2026. Paying earlier would take the balance below the EUR 1,400 minimum.` | deterministic explanation family follows the selected decision |
| `request_19` | `amount_safe_to_pay` | `28820` | `37555.87` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_19` | `payment_plan` | `2024-09-04:28820|2024-09-15:10840` | `2024-09-04:37555.87|2024-09-15:2104.13` | planner date/amount construction or field-specific serialization |
| `request_19` | `decision_explanation` | `Pay INR 28,820 today and the remaining INR 10,840 on 15 September 2024. This completes the full request and keeps the INR 92,800 minimum protected.` | `Pay INR 37,555.87 today and the remaining INR 2,104.13 on 15 September 2024. This completes the full request and keeps the INR 92,800 minimum protected.` | deterministic explanation family follows the selected decision |
| `request_20` | `amount_safe_to_pay` | `5400` | `14941.75` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_20` | `decision_explanation` | `Do not make this payment by 22 February 2026. None of the available options keeps the INR 64,500 minimum protected.` | `Do not proceed with the INR 303,700 request. Although INR 14,941.75 is available today, the full amount cannot be completed safely within 90 days.` | deterministic explanation family follows the selected decision |
| `request_21` | `amount_safe_to_pay` | `1543.35` | `1574.4` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_21` | `affordability_status` | `affordable_with_plan` | `affordable_now` | planner eligibility/status derived from the forecast predicate |
| `request_21` | `earliest_date_for_full_payment` | `2026-04-15` | `2026-04-03` | forecast date calculation / same-day ordering |
| `request_21` | `spending_changes_needed` | `stop:event_1815|reduce_to:event_1816:23.50` | `none` | spending-change legality/enumeration or binding forecast trough |
| `request_21` | `decision_explanation` | `Stop the online backup subscription and reduce the streaming subscription to USD 23.50, then pay USD 1,574.40 today. This leaves at least USD 1,800 available.` | `Pay USD 1,574.40 today. This leaves at least USD 1,800 available over the next 90 days.` | deterministic explanation family follows the selected decision |
| `request_22` | `amount_safe_to_pay` | `475.46` | `514.86` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_22` | `earliest_date_for_full_payment` | `2025-01-15` | `2024-12-15` | forecast date calculation / same-day ordering |
| `request_23` | `amount_safe_to_pay` | `9152` | `9303.91` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_24` | `amount_safe_to_pay` | `13420` | `12557.36` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |
| `request_24` | `decision_explanation` | `Do not proceed with the INR 109,600 request. Although INR 13,420 is available today, the full amount cannot be completed safely within 90 days.` | `Do not proceed with the INR 109,600 request. Although INR 12,557.36 is available today, the full amount cannot be completed safely within 90 days.` | deterministic explanation family follows the selected decision |
| `request_25` | `amount_safe_to_pay` | `1425000` | `0` | forecast semantics: recurrence/lifecycle/evidence affects the binding trough |

## Field counts

- `affordability_status`: 4
- `amount_safe_to_pay`: 21
- `decision_explanation`: 14
- `earliest_date_for_full_payment`: 7
- `payment_plan`: 3
- `recommended_payment_method`: 1
- `spending_changes_needed`: 3

## Shared clusters

- **deterministic explanation family follows the selected decision**: `request_04`, `request_05`, `request_06`, `request_09`, `request_10`, `request_11`, `request_13`, `request_14`, `request_15`, `request_18`, `request_19`, `request_20`, `request_21`, `request_24`
- **forecast date calculation / same-day ordering**: `request_06`, `request_10`, `request_11`, `request_13`, `request_18`, `request_21`, `request_22`
- **forecast semantics: recurrence/lifecycle/evidence affects the binding trough**: `request_02`, `request_03`, `request_04`, `request_05`, `request_06`, `request_07`, `request_08`, `request_10`, `request_11`, `request_13`, `request_14`, `request_15`, `request_17`, `request_18`, `request_19`, `request_20`, `request_21`, `request_22`, `request_23`, `request_24`, `request_25`
- **planner candidate eligibility/ranking derived from the forecast predicate**: `request_13`
- **planner date/amount construction or field-specific serialization**: `request_13`, `request_18`, `request_19`
- **planner eligibility/status derived from the forecast predicate**: `request_06`, `request_11`, `request_13`, `request_21`
- **spending-change legality/enumeration or binding forecast trough**: `request_06`, `request_11`, `request_21`
