# Deterministic dataset inventory

Generated from participant-facing `dataset/` only.

## exchange_rates.csv
Rows: 134

- `rate_date`: dtype=date; null=0/134 (0.000000); unique=39
  - values: '2023-10-15' (3), '2023-11-15' (3), '2023-12-15' (3), '2024-01-15' (4), '2024-02-15' (4), '2024-03-15' (4), '2024-04-15' (5), '2024-05-15' (5), '2024-06-15' (3), '2024-07-15' (3), '2024-08-15' (3), '2024-09-15' (4), '2024-10-15' (4), '2024-11-15' (4), '2024-12-15' (4), '2025-01-15' (4), '2025-02-15' (4), '2025-03-15' (2), '2025-04-15' (2), '2025-05-15' (2), '2025-06-15' (4), '2025-07-15' (4), '2025-08-15' (5), '2025-09-15' (5), '2025-10-01' (1), '2025-10-15' (5), '2025-11-15' (5), '2025-12-15' (5), '2026-01-15' (5), '2026-02-15' (4), '2026-03-15' (4), '2026-04-15' (3), '2026-05-15' (3), '2026-06-15' (3), '2026-07-15' (2), '2026-08-15' (2), '2026-09-15' (2), '2026-10-15' (1), '2026-11-15' (1)
- `from_currency`: dtype=string; null=0/134 (0.000000); unique=2
  - values: 'EUR' (46), 'USD' (88)
- `to_currency`: dtype=string; null=0/134 (0.000000); unique=5
  - values: 'EUR' (25), 'IDR' (30), 'INR' (33), 'USD' (24), 'ZAR' (22)
- `rate`: dtype=decimal; null=0/134 (0.000000); unique=5
  - values: '0.92' (25), '1.09' (24), '15833.33' (30), '20' (22), '83.33' (33)

## financial_events.csv
Rows: 25342

- `event_id`: dtype=string; null=0/25342 (0.000000); unique=25342
- `user_id`: dtype=string; null=0/25342 (0.000000); unique=275
- `event_type`: dtype=string; null=0/25342 (0.000000); unique=8
  - values: 'debt_payment' (567), 'expense' (20525), 'income' (1696), 'investment_purchase' (29), 'investment_sale' (5), 'investment_valuation' (10), 'refund' (22), 'subscription' (2488)
- `description`: dtype=string; null=0/25342 (0.000000); unique=164
- `category`: dtype=string; null=0/25342 (0.000000); unique=22
  - values: 'cloud_storage' (833), 'debt_repayment' (553), 'delivery_membership' (351), 'dining' (3479), 'education' (306), 'entertainment' (521), 'family_support' (125), 'groceries' (5812), 'gym' (170), 'healthcare' (356), 'housing' (246), 'insurance' (456), 'investment' (44), 'music_subscription' (451), 'rent' (1355), 'salary' (1690), 'shopping' (813), 'streaming' (683), 'transport' (5626), 'utilities' (1452), 'windfall' (6), 'work_expense' (14)
- `direction`: dtype=string; null=0/25342 (0.000000); unique=3
  - values: 'credit' (1723), 'debit' (23609), 'non_cash' (10)
- `amount`: dtype=decimal; null=16/25342 (0.000631); unique=17786
- `currency`: dtype=string; null=0/25342 (0.000000); unique=5
  - values: 'EUR' (5585), 'IDR' (4992), 'INR' (6457), 'USD' (3819), 'ZAR' (4489)
- `event_date`: dtype=date; null=0/25342 (0.000000); unique=1308
- `settlement_date`: dtype=date; null=10/25342 (0.000395); unique=1311
- `status`: dtype=string; null=0/25342 (0.000000); unique=6
  - values: 'cancelled' (22), 'failed' (21), 'pending' (71), 'scheduled' (70), 'settled' (25148), 'unrealized' (10)
- `linked_event_id`: dtype=string; null=25284/25342 (0.997711); unique=59
- `flexibility`: dtype=string; null=0/25342 (0.000000); unique=4
  - values: 'fixed' (21138), 'reducible' (2682), 'reducible_or_stoppable' (225), 'stoppable' (1297)
- `minimum_allowed_amount`: dtype=decimal; null=22435/25342 (0.885289); unique=302

## financial_profiles.csv
Rows: 275

- `user_id`: dtype=string; null=0/275 (0.000000); unique=275
- `home_currency`: dtype=string; null=0/275 (0.000000); unique=5
  - values: 'EUR' (62), 'IDR' (55), 'INR' (67), 'USD' (40), 'ZAR' (51)
- `current_available_balance`: dtype=decimal; null=0/275 (0.000000); unique=275
- `minimum_balance_to_keep`: dtype=decimal; null=0/275 (0.000000); unique=192
- `financial_priorities`: dtype=string; null=0/275 (0.000000); unique=9
  - values: 'debt_repayment|emergency_savings' (20), 'education|debt_repayment' (36), 'education|emergency_savings' (34), 'education|family_support' (24), 'emergency_savings|housing' (29), 'emergency_savings|travel' (46), 'healthcare|family_support' (25), 'healthcare|retirement_investment' (19), 'retirement_investment|emergency_savings' (42)
- `expense_categories_to_protect`: dtype=string; null=0/275 (0.000000); unique=8
  - values: 'housing|healthcare|utilities' (19), 'housing|utilities|education' (24), 'rent|education|groceries|debt_repayment' (36), 'rent|groceries|transport' (63), 'rent|healthcare|family_support|groceries' (25), 'rent|insurance|transport' (46), 'rent|utilities|debt_repayment' (20), 'rent|utilities|groceries' (42)
- `expense_categories_user_is_willing_to_reduce`: dtype=string; null=39/275 (0.141818); unique=19
  - values: '' (39), 'dining' (80), 'dining|entertainment' (20), 'dining|gym' (2), 'dining|gym|entertainment' (4), 'dining|shopping' (10), 'dining|shopping|entertainment' (2), 'dining|streaming' (22), 'dining|streaming|entertainment' (1), 'dining|streaming|shopping' (12), 'entertainment' (5), 'gym' (6), 'gym|entertainment' (2), 'shopping' (35), 'shopping|entertainment' (4), 'streaming' (17), 'streaming|entertainment' (5), 'streaming|shopping' (8), 'streaming|shopping|entertainment' (1)
- `expense_categories_user_is_willing_to_stop`: dtype=string; null=62/275 (0.225455); unique=11
  - values: '' (62), 'cloud_storage' (57), 'delivery_membership' (10), 'gym' (1), 'gym|delivery_membership' (3), 'gym|music_subscription' (4), 'gym|music_subscription|delivery_membership' (4), 'music_subscription' (26), 'music_subscription|delivery_membership' (24), 'streaming' (32), 'streaming|cloud_storage' (52)
- `payment_methods_user_will_consider`: dtype=string; null=0/275 (0.000000); unique=7
  - values: 'full_payment' (60), 'full_payment|installments' (35), 'full_payment|partial_payment' (40), 'full_payment|partial_payment|installments' (28), 'installments' (41), 'partial_payment' (19), 'partial_payment|installments' (52)
- `max_installment_months`: dtype=decimal; null=119/275 (0.432727); unique=12
  - values: '' (119), '10' (12), '11' (16), '12' (16), '2' (15), '3' (18), '4' (17), '5' (16), '6' (13), '7' (14), '8' (10), '9' (9)

## images.csv
Rows: 16

- `image_id`: dtype=string; null=0/16 (0.000000); unique=16
  - values: 'image_01' (1), 'image_02' (1), 'image_03' (1), 'image_04' (1), 'image_05' (1), 'image_06' (1), 'image_07' (1), 'image_08' (1), 'image_09' (1), 'image_10' (1), 'image_11' (1), 'image_12' (1), 'image_13' (1), 'image_14' (1), 'image_15' (1), 'image_16' (1)
- `user_id`: dtype=string; null=0/16 (0.000000); unique=16
  - values: 'user_03' (1), 'user_101' (1), 'user_105' (1), 'user_113' (1), 'user_16' (1), 'user_17' (1), 'user_19' (1), 'user_20' (1), 'user_33' (1), 'user_35' (1), 'user_48' (1), 'user_55' (1), 'user_64' (1), 'user_73' (1), 'user_78' (1), 'user_84' (1)
- `request_id`: dtype=string; null=0/16 (0.000000); unique=16
  - values: 'request_03' (1), 'request_101' (1), 'request_105' (1), 'request_113' (1), 'request_16' (1), 'request_17' (1), 'request_19' (1), 'request_20' (1), 'request_33' (1), 'request_35' (1), 'request_48' (1), 'request_55' (1), 'request_64' (1), 'request_73' (1), 'request_78' (1), 'request_84' (1)
- `related_event_id`: dtype=string; null=0/16 (0.000000); unique=16
  - values: 'event_10521' (1), 'event_1442' (1), 'event_1545' (1), 'event_1700' (1), 'event_1786' (1), 'event_253' (1), 'event_3051' (1), 'event_3231' (1), 'event_4535' (1), 'event_5170' (1), 'event_6033' (1), 'event_6859' (1), 'event_7307' (1), 'event_7941' (1), 'event_9421' (1), 'event_9806' (1)

## messages.csv
Rows: 215

- `message_id`: dtype=string; null=0/215 (0.000000); unique=215
- `user_id`: dtype=string; null=0/215 (0.000000); unique=215
- `request_id`: dtype=string; null=87/215 (0.404651); unique=129
- `related_event_id`: dtype=string; null=176/215 (0.818605); unique=40
  - values: '' (176), 'event_10521' (1), 'event_10699' (1), 'event_11129' (1), 'event_11925' (1), 'event_12709' (1), 'event_13032' (1), 'event_13207' (1), 'event_13663' (1), 'event_14026' (1), 'event_14399' (1), 'event_17401' (1), 'event_17662' (1), 'event_1785' (1), 'event_18269' (1), 'event_19182' (1), 'event_19334' (1), 'event_1960' (1), 'event_20379' (1), 'event_20615' (1), 'event_21101' (1), 'event_21582' (1), 'event_2165' (1), 'event_21785' (1), 'event_23203' (1), 'event_23306' (1), 'event_23855' (1), 'event_24352' (1), 'event_24534' (1), 'event_25342' (1), 'event_3230' (1), 'event_3491' (1), 'event_4535' (1), 'event_4994' (1), 'event_6532' (1), 'event_7186' (1), 'event_7941' (1), 'event_8575' (1), 'event_9420' (1), 'event_9805' (1)
- `sent_at`: dtype=string; null=0/215 (0.000000); unique=120
- `source_type`: dtype=string; null=0/215 (0.000000); unique=5
  - values: 'bank' (18), 'employer' (126), 'financial_service' (23), 'merchant' (17), 'service_provider' (31)
- `message_text`: dtype=string; null=0/215 (0.000000); unique=215

## output.csv
Rows: 250

- `request_id`: dtype=string; null=0/250 (0.000000); unique=250
- `amount_safe_to_pay`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)
- `affordability_status`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)
- `recommended_payment_method`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)
- `payment_plan`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)
- `earliest_date_for_full_payment`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)
- `spending_changes_needed`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)
- `decision_explanation`: dtype=null; null=250/250 (1.000000); unique=1
  - values: '' (250)

## request_payment_options.csv
Rows: 790

- `payment_option_id`: dtype=string; null=0/790 (0.000000); unique=790
- `request_id`: dtype=string; null=0/790 (0.000000); unique=275
- `payment_method`: dtype=string; null=0/790 (0.000000); unique=2
  - values: 'full_payment' (275), 'installments' (515)
- `payment_amount`: dtype=decimal; null=0/790 (0.000000); unique=787
- `number_of_payments`: dtype=decimal; null=0/790 (0.000000); unique=9
  - values: '1' (275), '15' (89), '18' (87), '2' (7), '21' (88), '24' (96), '3' (80), '4' (3), '6' (65)
- `first_payment_date`: dtype=date; null=0/790 (0.000000); unique=194
- `payment_frequency_days`: dtype=decimal; null=275/790 (0.348101); unique=4
  - values: '' (275), '28' (180), '30' (166), '31' (169)
- `financing_fee`: dtype=decimal; null=0/790 (0.000000); unique=515
- `total_payable_amount`: dtype=decimal; null=0/790 (0.000000); unique=787

## requests.csv
Rows: 250

- `request_id`: dtype=string; null=0/250 (0.000000); unique=250
- `user_id`: dtype=string; null=0/250 (0.000000); unique=250
- `request_date`: dtype=date; null=0/250 (0.000000); unique=61
- `request_type`: dtype=string; null=0/250 (0.000000); unique=9
  - values: 'debt_repayment' (28), 'education' (28), 'emergency_expense' (27), 'family_transfer' (28), 'housing' (28), 'investment' (28), 'other' (27), 'purchase' (28), 'travel' (28)
- `requested_amount`: dtype=decimal; null=0/250 (0.000000); unique=248
- `desired_completion_date`: dtype=date; null=0/250 (0.000000); unique=170
- `allows_partial_payment`: dtype=string; null=0/250 (0.000000); unique=2
  - values: 'false' (170), 'true' (80)
- `request_text`: dtype=string; null=0/250 (0.000000); unique=250

## sample_requests.csv
Rows: 25

- `request_id`: dtype=string; null=0/25 (0.000000); unique=25
  - values: 'request_01' (1), 'request_02' (1), 'request_03' (1), 'request_04' (1), 'request_05' (1), 'request_06' (1), 'request_07' (1), 'request_08' (1), 'request_09' (1), 'request_10' (1), 'request_11' (1), 'request_12' (1), 'request_13' (1), 'request_14' (1), 'request_15' (1), 'request_16' (1), 'request_17' (1), 'request_18' (1), 'request_19' (1), 'request_20' (1), 'request_21' (1), 'request_22' (1), 'request_23' (1), 'request_24' (1), 'request_25' (1)
- `user_id`: dtype=string; null=0/25 (0.000000); unique=25
  - values: 'user_01' (1), 'user_02' (1), 'user_03' (1), 'user_04' (1), 'user_05' (1), 'user_06' (1), 'user_07' (1), 'user_08' (1), 'user_09' (1), 'user_10' (1), 'user_11' (1), 'user_12' (1), 'user_13' (1), 'user_14' (1), 'user_15' (1), 'user_16' (1), 'user_17' (1), 'user_18' (1), 'user_19' (1), 'user_20' (1), 'user_21' (1), 'user_22' (1), 'user_23' (1), 'user_24' (1), 'user_25' (1)
- `request_date`: dtype=date; null=0/25 (0.000000); unique=25
  - values: '2019-09-03' (1), '2023-08-12' (1), '2024-03-03' (1), '2024-03-06' (1), '2024-03-07' (1), '2024-06-04' (1), '2024-09-04' (1), '2024-09-05' (1), '2024-12-05' (1), '2024-12-06' (1), '2025-02-07' (1), '2025-05-03' (1), '2025-05-07' (1), '2025-08-04' (1), '2025-08-05' (1), '2025-11-06' (1), '2026-01-03' (1), '2026-01-04' (1), '2026-01-06' (1), '2026-02-07' (1), '2026-03-01' (1), '2026-04-03' (1), '2026-04-05' (1), '2026-07-04' (1), '2026-07-07' (1)
- `request_type`: dtype=string; null=0/25 (0.000000); unique=9
  - values: 'debt_repayment' (3), 'education' (3), 'emergency_expense' (2), 'family_transfer' (3), 'housing' (3), 'investment' (3), 'other' (2), 'purchase' (3), 'travel' (3)
- `requested_amount`: dtype=decimal; null=0/25 (0.000000); unique=25
  - values: '109600' (1), '122500' (1), '12693000' (1), '13110000' (1), '15488' (1), '1574.4' (1), '166.61' (1), '197400' (1), '25256' (1), '266700' (1), '274600' (1), '303700' (1), '3246.1' (1), '3685' (1), '38016' (1), '39660' (1), '46018000' (1), '5414.2' (1), '5491000' (1), '60496000' (1), '620.4' (1), '65164' (1), '731.5' (1), '941.6' (1), '996.6' (1)
- `desired_completion_date`: dtype=date; null=0/25 (0.000000); unique=24
  - values: '2019-11-15' (1), '2023-10-11' (1), '2024-03-20' (1), '2024-04-17' (1), '2024-05-15' (1), '2024-06-19' (1), '2024-10-04' (1), '2024-11-14' (1), '2025-02-10' (2), '2025-04-15' (1), '2025-06-12' (1), '2025-07-15' (1), '2025-10-04' (1), '2025-10-10' (1), '2026-01-12' (1), '2026-01-14' (1), '2026-02-01' (1), '2026-02-08' (1), '2026-02-22' (1), '2026-04-14' (1), '2026-05-04' (1), '2026-06-20' (1), '2026-07-23' (1), '2026-09-15' (1)
- `allows_partial_payment`: dtype=string; null=0/25 (0.000000); unique=2
  - values: 'false' (13), 'true' (12)
- `request_text`: dtype=string; null=0/25 (0.000000); unique=25
  - values: "Can I buy the laptop now without making next month's bills tight? I need to decide by 4 October 2024. I've been quoted INR 39,660 for the laptop." (1), "Can I clear this additional amount without putting upcoming bills at risk? The extra repayment I'm considering is ZAR 15,488." (1), 'Can I complete this family transfer and still keep my minimum balance? I want to send EUR 941.60 to my family.' (1), "Does paying for the trip now leave enough for the rest of the month? I need to decide by 12 June 2025. I'm planning a family trip that costs IDR 13,110,000." (1), 'How much can I invest now without affecting essential payments? I need to decide by 1 February 2026. I have an opportunity to invest EUR 3,685.' (1), 'How much extra can I put toward the loan today? I need to decide by 15 July 2025. The additional loan payment would be ZAR 38,016.' (1), 'How much of the rental deposit can I safely pay today? I need to decide by 14 November 2024. The rental deposit is INR 197,400.' (1), 'I can book the family trip for INR 303,700. Would it be safer to book the trip now or wait until more money comes in?' (1), 'I want to put EUR 620.40 into an investment. I need to complete it by 14 January 2026. Is it safer to invest now, invest a smaller amount, or wait?' (1), "I'm considering setting aside INR 109,600 for an investment. Would investing this amount leave my upcoming bills covered?" (1), "I'm planning an extra loan payment of EUR 5,414.20. I need to complete it by 4 October 2025. Would paying this much toward the loan leave enough for the rest of the month?" (1), 'Is it safe to cover the full course fee by the deadline? Enrolment for the course comes to USD 1,574.40.' (1), 'Is the deposit affordable now, or do I need more time? I need IDR 60,496,000 for the rental deposit.' (1), 'Is the full membership fee affordable today, or should I wait? The annual membership costs EUR 166.61.' (1), 'Should I pay for the course now, use installments, or wait? I need to decide by 15 November 2019. The course I want to take is IDR 5,491,000.' (1), 'The amount I want to send is IDR 12,693,000. Would sending the money now leave enough for my upcoming expenses?' (1), 'The annual plan comes to EUR 3,246.10. I need to complete it by 15 September 2026. Can I take the membership and still keep my minimum balance intact?' (1), 'The current quote for the trip is IDR 46,018,000. I need to complete it by 10 October 2025. Can I afford the full trip without putting upcoming bills at risk?' (1), 'The landlord has asked for a deposit of INR 122,500. Can I pay the rental deposit by the requested date?' (1), 'The price of the laptop is INR 266,700. I need to complete it by 10 February 2025. How much of the laptop price can I safely cover today?' (1), 'The professional course costs ZAR 65,164. Can I pay for the course before enrolment closes?' (1), 'The repair I need is priced at EUR 996.60. Can I cover the full repair now and still manage my essential expenses?' (1), 'The transfer I have in mind is EUR 731.50. I need to complete it by 10 February 2025. Can I make the full transfer without falling short on my own bills?' (1), 'What is the most I can put toward this repair right now? The latest estimate for the repair is INR 274,600.' (1), "Would paying for the laptop today leave enough for my regular expenses? The laptop I'm looking at is ZAR 25,256." (1)
- `amount_safe_to_pay`: dtype=decimal; null=0/25 (0.000000); unique=25
  - values: '122500' (1), '12510645' (1), '12700' (1), '13420' (1), '1425000' (1), '1543.35' (1), '166.61' (1), '17229139.2' (1), '243849.58' (1), '25256' (1), '284.57' (1), '28820' (1), '433.4' (1), '462' (1), '475.46' (1), '5400' (1), '597.74' (1), '603.3' (1), '65164' (1), '737' (1), '83.05' (1), '8401800' (1), '87170.56' (1), '873000' (1), '9152' (1)
- `affordability_status`: dtype=string; null=0/25 (0.000000); unique=4
  - values: 'affordable_later' (6), 'affordable_now' (3), 'affordable_with_plan' (9), 'not_affordable' (7)
- `recommended_payment_method`: dtype=string; null=0/25 (0.000000); unique=5
  - values: 'full_payment' (6), 'installments' (5), 'not_recommended' (7), 'partial_payment' (1), 'wait' (6)
- `payment_plan`: dtype=string; null=0/25 (0.000000); unique=19
  - values: '2019-11-15:5491000' (1), '2023-08-12:122500' (1), '2024-03-03:25256' (1), '2024-05-15:941.60' (1), '2024-06-15:12693000' (1), '2024-09-04:28820|2024-09-15:10840' (1), '2024-09-12:68432|2024-10-10:68432|2024-11-07:68432' (1), '2024-12-08:253.59|2025-01-05:253.59|2025-02-02:253.59' (1), '2025-04-15:996.60' (1), '2025-05-03:13110000' (1), '2025-07-15:38016' (1), '2025-08-08:15952906.67|2025-09-07:15952906.67|2025-10-07:15952906.67' (1), '2026-01-03:620.40' (1), '2026-03-01:95194.67|2026-03-31:95194.67|2026-04-30:95194.67' (1), '2026-04-03:1574.40' (1), '2026-04-19:22590.19|2026-05-20:22590.19|2026-06-20:22590.19' (1), '2026-07-04:166.61' (1), '2026-09-15:3246.10' (1), 'none' (7)
- `earliest_date_for_full_payment`: dtype=date; null=7/25 (0.280000); unique=18
  - values: '' (7), '2019-11-15' (1), '2023-08-12' (1), '2024-03-03' (1), '2024-05-15' (1), '2024-06-15' (1), '2024-09-15' (1), '2024-10-23' (1), '2025-01-15' (1), '2025-04-15' (1), '2025-07-15' (2), '2025-09-15' (1), '2026-01-15' (1), '2026-03-15' (1), '2026-04-05' (1), '2026-04-15' (1), '2026-07-04' (1), '2026-09-15' (1)
- `spending_changes_needed`: dtype=string; null=0/25 (0.000000); unique=4
  - values: 'none' (22), 'reduce_to:event_989:665950' (1), 'stop:event_1815|reduce_to:event_1816:23.50' (1), 'stop:event_476' (1)
- `decision_explanation`: dtype=string; null=0/25 (0.000000); unique=25
  - values: 'Do not make this payment by 1 February 2026. None of the available options keeps the EUR 1,200 minimum protected.' (1), 'Do not make this payment by 10 February 2025. None of the available options keeps the INR 225,400 minimum protected.' (1), 'Do not make this payment by 12 January 2026. None of the available options keeps the ZAR 13,100 minimum protected.' (1), 'Do not make this payment by 17 April 2024. None of the available options keeps the IDR 23,379,100 minimum protected.' (1), 'Do not make this payment by 22 February 2026. None of the available options keeps the INR 64,500 minimum protected.' (1), 'Do not proceed with the EUR 5,414.20 request. Although EUR 597.74 is available today, the full amount cannot be completed safely within 90 days.' (1), 'Do not proceed with the INR 109,600 request. Although INR 13,420 is available today, the full amount cannot be completed safely within 90 days.' (1), 'Pay EUR 166.61 today. This keeps the EUR 600 minimum available over the next 90 days.' (1), 'Pay EUR 3,246.10 in full on 15 September 2026. Paying earlier would take the balance below the EUR 1,400 minimum.' (1), 'Pay EUR 941.60 in full on 15 May 2024. Paying earlier would take the balance below the EUR 1,300 minimum.' (1), 'Pay EUR 996.60 in full on 15 April 2025. Paying earlier would take the balance below the EUR 800 minimum.' (1), 'Pay IDR 5,491,000 in full on 15 November 2019. Paying earlier would take the balance below the IDR 2,668,700 minimum.' (1), 'Pay INR 122,500 today. This leaves at least INR 122,400 available over the next 90 days.' (1), 'Pay INR 28,820 today and the remaining INR 10,840 on 15 September 2024. This completes the full request and keeps the INR 92,800 minimum protected.' (1), 'Pay ZAR 25,256 today. This leaves at least ZAR 18,000 available over the next 90 days.' (1), 'Pay ZAR 38,016 in full on 15 July 2025. Paying earlier would take the balance below the ZAR 27,000 minimum.' (1), 'Reduce the weekend food delivery to IDR 665,950, then pay IDR 13,110,000 today. This leaves at least IDR 34,140,600 available.' (1), 'Stop the family streaming plan, then pay EUR 620.40 today. This leaves at least EUR 800 available.' (1), 'Stop the online backup subscription and reduce the streaming subscription to USD 23.50, then pay USD 1,574.40 today. This leaves at least USD 1,800 available.' (1), 'Use 3 installments of EUR 253.59, starting 8 December 2024. This leaves at least EUR 500 available.' (1), 'Use 3 installments of IDR 15,952,906.67, starting 8 August 2025. This leaves at least IDR 29,158,400 available.' (1), 'Use 3 installments of INR 68,432, starting 12 September 2024. This leaves at least INR 93,000 available.' (1), 'Use 3 installments of INR 95,194.67, starting 1 March 2026. This leaves at least INR 166,100 available.' (1), 'Use 3 installments of ZAR 22,590.19, starting 19 April 2026. This leaves at least ZAR 43,200 available.' (1), 'Wait until 15 June 2024, then pay IDR 12,693,000 in full. Paying sooner would put the IDR 30,686,600 minimum at risk.' (1)

## Cross-file assertions

```json
{
  "direction_exact_domain": true,
  "event_value_counts": {
    "category": {
      "cloud_storage": 833,
      "debt_repayment": 553,
      "delivery_membership": 351,
      "dining": 3479,
      "education": 306,
      "entertainment": 521,
      "family_support": 125,
      "groceries": 5812,
      "gym": 170,
      "healthcare": 356,
      "housing": 246,
      "insurance": 456,
      "investment": 44,
      "music_subscription": 451,
      "rent": 1355,
      "salary": 1690,
      "shopping": 813,
      "streaming": 683,
      "transport": 5626,
      "utilities": 1452,
      "windfall": 6,
      "work_expense": 14
    },
    "event_type": {
      "debt_payment": 567,
      "expense": 20525,
      "income": 1696,
      "investment_purchase": 29,
      "investment_sale": 5,
      "investment_valuation": 10,
      "refund": 22,
      "subscription": 2488
    },
    "flexibility": {
      "fixed": 21138,
      "reducible": 2682,
      "reducible_or_stoppable": 225,
      "stoppable": 1297
    },
    "status": {
      "cancelled": 22,
      "failed": 21,
      "pending": 71,
      "scheduled": 70,
      "settled": 25148,
      "unrealized": 10
    }
  },
  "exchange_rate_date_range": {
    "distinct_count": 39,
    "granularity_days": [
      0,
      14,
      16,
      28,
      29,
      30,
      31
    ],
    "max": "2026-11-15",
    "min": "2023-10-15"
  },
  "exchange_rate_pairs": {
    "EUR->USD": 24,
    "EUR->ZAR": 22,
    "USD->EUR": 25,
    "USD->IDR": 30,
    "USD->INR": 33
  },
  "home_currency": {
    "EUR": 62,
    "IDR": 55,
    "INR": 67,
    "USD": 40,
    "ZAR": 51
  },
  "image_paths_exist": true,
  "linkage": {
    "events_without_profiles": [],
    "images_to_missing_events": [],
    "messages_to_missing_events": [],
    "requests_without_options": []
  },
  "linked_event_id": {
    "cycle_count": 0,
    "maximum_chain_length": 1,
    "populated": 58
  },
  "max_installment_months": {
    "distribution": {
      "": 119,
      "10": 12,
      "11": 16,
      "12": 16,
      "2": 15,
      "3": 18,
      "4": 17,
      "5": 16,
      "6": 13,
      "7": 14,
      "8": 10,
      "9": 9
    },
    "null_count": 119
  },
  "message_language_counts": {
    "english_like": 170,
    "non_english_like": 45
  },
  "message_related_event_null_count": 176,
  "message_source_type": {
    "bank": 18,
    "employer": 126,
    "financial_service": 23,
    "merchant": 17,
    "service_provider": 31
  },
  "minimum_allowed_amount": {
    "distribution": {
      "": 22435,
      "10.5": 22,
      "1000": 5,
      "1013.76": 5,
      "1028.5": 5,
      "1038.4": 9,
      "1048": 5,
      "1058.2": 5,
      "1065.9": 13,
      "1072.5": 9,
      "1085": 5,
      "11": 10,
      "11.5": 14,
      "11.6": 5,
      "1100": 9,
      "1180": 9,
      "1181.4": 13,
      "1190": 9,
      "1197.9": 13,
      "12": 5,
      "12.5": 14,
      "1245": 13,
      "1250": 9,
      "1272": 5,
      "13": 18,
      "1335": 13,
      "14": 15,
      "1425": 6,
      "1450": 5,
      "1480": 5,
      "148200": 5,
      "1490": 5,
      "15": 13,
      "15.2": 5,
      "15.5": 5,
      "1504": 5,
      "1565": 5,
      "16": 28,
      "16.4": 5,
      "16.5": 14,
      "16.8": 5,
      "161.04": 5,
      "1610": 13,
      "1616": 5,
      "1620": 5,
      "1632": 5,
      "1635": 5,
      "1665": 5,
      "17": 5,
      "17.5": 53,
      "1720": 5,
      "1730": 26,
      "1784": 5,
      "1790": 5,
      "1796": 5,
      "18": 5,
      "18.5": 27,
      "1805": 9,
      "180500": 13,
      "186200": 5,
      "1875": 9,
      "1890": 5,
      "19.5": 18,
      "1928": 5,
      "193.6": 10,
      "197600": 5,
      "20": 22,
      "20.5": 27,
      "2015": 5,
      "2020": 13,
      "203300": 18,
      "2060": 5,
      "2068": 5,
      "2070": 5,
      "2075": 25,
      "21": 5,
      "21.2": 5,
      "21.5": 10,
      "2105": 25,
      "210900": 5,
      "216600": 5,
      "2195": 5,
      "22": 26,
      "223.3": 25,
      "2230": 5,
      "2240": 5,
      "2255": 13,
      "2260": 5,
      "23": 5,
      "23.5": 5,
      "234.3": 13,
      "234.96": 5,
      "2360": 5,
      "236360": 5,
      "2370": 9,
      "24": 15,
      "24.5": 13,
      "24.8": 5,
      "2405": 13,
      "242": 5,
      "2420": 13,
      "2430": 5,
      "2432": 5,
      "2475": 5,
      "25": 5,
      "25.5": 14,
      "2536": 5,
      "259350": 9,
      "26": 5,
      "26.5": 10,
      "2645": 13,
      "2650": 13,
      "265050": 9,
      "2655": 5,
      "2660": 5,
      "266760": 5,
      "269.5": 13,
      "2695": 25,
      "27": 5,
      "27.2": 10,
      "27.5": 5,
      "27.6": 5,
      "271.7": 5,
      "2728": 5,
      "274550": 13,
      "275": 9,
      "2750": 13,
      "2790": 5,
      "28": 9,
      "28.5": 9,
      "280250": 5,
      "2835": 14,
      "29": 9,
      "29.2": 5,
      "29.5": 18,
      "2920": 5,
      "2935": 13,
      "30": 9,
      "30.5": 14,
      "3110": 5,
      "314450": 5,
      "315400": 5,
      "3184": 5,
      "32": 25,
      "322.08": 5,
      "3225": 9,
      "323950": 13,
      "325.6": 9,
      "3255": 9,
      "325850": 5,
      "3280": 5,
      "3295": 9,
      "33": 13,
      "33.5": 13,
      "3335": 13,
      "335350": 9,
      "34": 5,
      "34.4": 5,
      "34.5": 18,
      "34.8": 5,
      "341": 5,
      "342.1": 5,
      "342000": 5,
      "3490": 13,
      "35": 15,
      "350550": 5,
      "3552": 5,
      "356250": 13,
      "36": 5,
      "36.5": 13,
      "3620": 5,
      "365560": 5,
      "367.4": 5,
      "368600": 10,
      "369.6": 5,
      "37": 13,
      "37.5": 26,
      "3700": 5,
      "370880": 5,
      "376200": 5,
      "38": 31,
      "382850": 5,
      "388.3": 13,
      "39": 18,
      "39.5": 9,
      "390.5": 5,
      "391400": 5,
      "3930": 13,
      "394250": 5,
      "396.88": 5,
      "40.5": 13,
      "402.6": 5,
      "407": 13,
      "41": 9,
      "410.3": 13,
      "415150": 5,
      "419.76": 5,
      "42.5": 13,
      "421.3": 5,
      "4210": 9,
      "4220": 5,
      "43": 25,
      "43.2": 5,
      "43.5": 18,
      "434150": 5,
      "4395": 25,
      "44": 13,
      "44.5": 13,
      "4410": 13,
      "45.2": 10,
      "45.5": 13,
      "451250": 9,
      "46.4": 5,
      "463.1": 9,
      "47": 9,
      "472150": 5,
      "478040": 5,
      "479.6": 5,
      "4796": 5,
      "48": 9,
      "489.5": 13,
      "49.6": 5,
      "493050": 9,
      "499.4": 13,
      "50": 13,
      "50.8": 5,
      "501600": 22,
      "506": 5,
      "508.2": 5,
      "508.64": 5,
      "51": 13,
      "51.6": 5,
      "511.28": 5,
      "525.8": 5,
      "53": 5,
      "53.5": 9,
      "530": 5,
      "530.2": 13,
      "531.3": 13,
      "536.8": 13,
      "541500": 5,
      "545": 5,
      "545.6": 25,
      "548720": 10,
      "556700": 13,
      "558.8": 10,
      "561.44": 5,
      "57": 9,
      "576.4": 5,
      "576650": 13,
      "577.5": 9,
      "578550": 25,
      "58900": 5,
      "589000": 26,
      "593750": 9,
      "597550": 13,
      "600": 5,
      "603440": 5,
      "605150": 5,
      "608.3": 9,
      "609.4": 5,
      "620.4": 5,
      "622250": 9,
      "623.7": 25,
      "633650": 9,
      "64.5": 13,
      "655.6": 9,
      "660": 5,
      "66120": 5,
      "663.3": 13,
      "664050": 13,
      "665950": 9,
      "670700": 5,
      "692550": 5,
      "696350": 13,
      "712.8": 14,
      "716.1": 9,
      "747650": 13,
      "753350": 5,
      "755": 9,
      "755250": 5,
      "763800": 13,
      "770450": 13,
      "773.3": 13,
      "779950": 13,
      "784.3": 9,
      "8": 5,
      "805": 5,
      "810350": 13,
      "840": 13,
      "845.9": 26,
      "863.5": 9,
      "895": 26,
      "9": 5,
      "9.2": 5,
      "9.5": 10,
      "910.8": 9,
      "913.44": 5,
      "925": 6,
      "926.64": 5,
      "950": 5,
      "991.1": 9
    },
    "populated": 2907
  },
  "non_cash": {
    "count": 10,
    "semantics": [
      "investment_valuation/unrealized"
    ],
    "supported_semantics": true
  },
  "option_frequency_anomaly": [],
  "option_frequency_days": {
    "": 275,
    "28": 180,
    "30": 166,
    "31": 169
  },
  "option_number_of_payments": {
    "1": 275,
    "15": 89,
    "18": 87,
    "2": 7,
    "21": 88,
    "24": 96,
    "3": 80,
    "4": 3,
    "6": 65
  },
  "option_payment_method": {
    "full_payment": 275,
    "installments": 515
  },
  "payment_methods_user_will_consider": {
    "full_payment": 60,
    "full_payment|installments": 35,
    "full_payment|partial_payment": 40,
    "full_payment|partial_payment|installments": 28,
    "installments": 41,
    "partial_payment": 19,
    "partial_payment|installments": 52
  },
  "permitted_categories_not_observed": [],
  "profile_category_tokens": {
    "expense_categories_to_protect": {
      "absent_from_event_categories": [],
      "observed": [
        "debt_repayment",
        "education",
        "family_support",
        "groceries",
        "healthcare",
        "housing",
        "insurance",
        "rent",
        "transport",
        "utilities"
      ]
    },
    "expense_categories_user_is_willing_to_reduce": {
      "absent_from_event_categories": [],
      "observed": [
        "dining",
        "entertainment",
        "gym",
        "shopping",
        "streaming"
      ]
    },
    "expense_categories_user_is_willing_to_stop": {
      "absent_from_event_categories": [],
      "observed": [
        "cloud_storage",
        "delivery_membership",
        "gym",
        "music_subscription",
        "streaming"
      ]
    }
  }
}
```
