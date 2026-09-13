# Phase-aware recurrence diagnostics

This is an analysis of `H_sequence_phase_partition`; it is not production behavior. History is bounded by `event_date <= request_date` after status/message filtering. `settlement_date` remains the cash-flow date. Active state is reported using the experiment criterion `request_date <= expected_next + max(2, cadence_days)` and is not promoted without solved-sample support.

## `user_01:debt_payment:debit:debt_repayment:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_04, event_10, event_16, event_22, event_29
- Dates: 2023-10-11, 2023-11-11, 2023-12-11, 2024-01-11, 2024-02-11
- Descriptions: Education loan instalment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2024-02-11` / `2024-03-11`
- Active as of request: `True`
- Amount: `3487` from `event_16, event_22, event_29`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:expense:debit:dining:ZAR:reducible:sequence:0`

- User/category/direction/type: `user_01` / `dining` / `debit` / `expense`
- Members: event_85, event_86, event_87, event_88, event_89, event_90, event_91, event_92, event_93, event_94, event_95, event_96, event_97
- Dates: 2023-09-10, 2023-09-24, 2023-10-08, 2023-10-22, 2023-11-05, 2023-11-19, 2023-12-03, 2023-12-17, 2023-12-31, 2024-01-14, 2024-01-28, 2024-02-11, 2024-02-25
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`7` residual_days=`0`
- Latest/expected next: `2024-02-25` / `2024-03-10`
- Active as of request: `True`
- Amount: `1222.49` from `event_95, event_96, event_97`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:expense:debit:education:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `education` / `debit` / `expense`
- Members: event_03, event_09, event_15, event_21, event_28
- Dates: 2023-10-08, 2023-11-08, 2023-12-08, 2024-01-08, 2024-02-08
- Descriptions: Professional training fee
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2024-02-08` / `2024-03-08`
- Active as of request: `True`
- Amount: `1821.6` from `event_15, event_21, event_28`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:expense:debit:groceries:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `groceries` / `debit` / `expense`
- Members: event_33, event_34, event_35, event_36, event_37, event_38, event_39, event_40, event_41, event_42, event_43, event_44, event_45, event_46, event_47, event_48, event_49, event_50, event_51, event_52, event_53, event_54, event_55, event_56, event_57, event_58
- Dates: 2023-09-08, 2023-09-15, 2023-09-22, 2023-09-29, 2023-10-06, 2023-10-13, 2023-10-20, 2023-10-27, 2023-11-03, 2023-11-10, 2023-11-17, 2023-11-24, 2023-12-01, 2023-12-08, 2023-12-15, 2023-12-22, 2023-12-29, 2024-01-05, 2024-01-12, 2024-01-19, 2024-01-26, 2024-02-02, 2024-02-09, 2024-02-16, 2024-02-23, 2024-03-01
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`5` residual_days=`0`
- Latest/expected next: `2024-03-01` / `2024-03-08`
- Active as of request: `True`
- Amount: `964.05` from `event_56, event_57, event_58`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:expense:debit:rent:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `rent` / `debit` / `expense`
- Members: event_01, event_07, event_13, event_19, event_26, event_32
- Dates: 2023-10-02, 2023-11-02, 2023-12-02, 2024-01-02, 2024-02-02, 2024-03-02
- Descriptions: Apartment rent transfer
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`2`
- Latest/expected next: `2024-03-02` / `2024-04-02`
- Active as of request: `True`
- Amount: `5148` from `event_19, event_26, event_32`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:expense:debit:transport:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `transport` / `debit` / `expense`
- Members: event_59, event_60, event_61, event_62, event_63, event_64, event_65, event_66, event_67, event_68, event_69, event_70, event_71, event_72, event_73, event_74, event_75, event_76, event_77, event_78, event_79, event_80, event_81, event_82, event_83, event_84, event_102
- Dates: 2023-09-09, 2023-09-16, 2023-09-23, 2023-09-30, 2023-10-07, 2023-10-14, 2023-10-21, 2023-10-28, 2023-11-04, 2023-11-11, 2023-11-18, 2023-11-25, 2023-12-02, 2023-12-09, 2023-12-16, 2023-12-23, 2023-12-30, 2024-01-06, 2024-01-13, 2024-01-20, 2024-01-27, 2024-02-03, 2024-02-10, 2024-02-17, 2024-02-24, 2024-03-02, 2024-03-02
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Pending fuel authorization, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`6` residual_days=`7`
- Latest/expected next: `2024-03-02` / `2024-03-09`
- Active as of request: `True`
- Amount: `567.6` from `event_83, event_84, event_102`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:expense:debit:utilities:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `utilities` / `debit` / `expense`
- Members: event_02, event_08, event_14, event_20, event_27
- Dates: 2023-10-06, 2023-11-06, 2023-12-06, 2024-01-06, 2024-02-06
- Descriptions: Household utility payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`1`
- Latest/expected next: `2024-02-06` / `2024-03-06`
- Active as of request: `True`
- Amount: `1651.81` from `event_14, event_20, event_27`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:subscription:debit:delivery_membership:ZAR:stoppable:sequence:0`

- User/category/direction/type: `user_01` / `delivery_membership` / `debit` / `subscription`
- Members: event_06, event_12, event_18, event_24, event_31
- Dates: 2023-10-13, 2023-11-13, 2023-12-13, 2024-01-13, 2024-02-13
- Descriptions: Delivery service plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2024-02-13` / `2024-03-13`
- Active as of request: `True`
- Amount: `306.9` from `event_18, event_24, event_31`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_01:subscription:debit:music_subscription:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_01` / `music_subscription` / `debit` / `subscription`
- Members: event_05, event_11, event_17, event_23, event_30
- Dates: 2023-10-11, 2023-11-11, 2023-12-11, 2024-01-11, 2024-02-11
- Descriptions: Music service subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2024-02-11` / `2024-03-11`
- Active as of request: `True`
- Amount: `235.4` from `event_17, event_23, event_30`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:dining:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `dining` / `debit` / `expense`
- Members: event_176, event_177, event_178, event_179, event_180, event_181, event_182, event_183, event_184
- Dates: 2025-02-12, 2025-03-05, 2025-03-26, 2025-04-16, 2025-05-07, 2025-05-28, 2025-06-18, 2025-07-09, 2025-07-30
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`10` residual_days=`0`
- Latest/expected next: `2025-07-30` / `2025-08-20`
- Active as of request: `True`
- Amount: `1204805.34` from `event_182, event_183, event_184`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:education:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `education` / `debit` / `expense`
- Members: event_108, event_116, event_124, event_132, event_140
- Dates: 2025-03-09, 2025-04-09, 2025-05-09, 2025-06-09, 2025-07-09
- Descriptions: Course tuition
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`1`
- Latest/expected next: `2025-07-09` / `2025-08-09`
- Active as of request: `True`
- Amount: `3040000` from `event_124, event_132, event_140`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:entertainment:IDR:reducible:sequence:0`

- User/category/direction/type: `user_02` / `entertainment` / `debit` / `expense`
- Members: event_110, event_118, event_126, event_134, event_142
- Dates: 2025-03-15, 2025-04-15, 2025-05-15, 2025-06-15, 2025-07-15
- Descriptions: Cinema and events
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-07-15` / `2025-08-15`
- Active as of request: `True`
- Amount: `1352563.79` from `event_126, event_134, event_142`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:groceries:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `groceries` / `debit` / `expense`
- Members: event_145, event_146, event_147, event_148, event_149, event_150, event_151, event_152, event_153, event_154, event_155, event_156, event_157, event_158, event_159, event_160, event_161, event_162
- Dates: 2025-02-10, 2025-02-20, 2025-03-02, 2025-03-12, 2025-03-22, 2025-04-01, 2025-04-11, 2025-04-21, 2025-05-01, 2025-05-11, 2025-05-21, 2025-05-31, 2025-06-10, 2025-06-20, 2025-06-30, 2025-07-10, 2025-07-20, 2025-07-30
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2025-07-30` / `2025-08-09`
- Active as of request: `True`
- Amount: `2365919.6` from `event_160, event_161, event_162`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:healthcare:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `healthcare` / `debit` / `expense`
- Members: event_109, event_117, event_125, event_133, event_141
- Dates: 2025-03-11, 2025-04-11, 2025-05-11, 2025-06-11, 2025-07-11
- Descriptions: Clinic payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2025-07-11` / `2025-08-11`
- Active as of request: `True`
- Amount: `1641668.72` from `event_125, event_133, event_141`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:housing:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `housing` / `debit` / `expense`
- Members: event_105, event_113, event_121, event_129, event_137, event_144
- Dates: 2025-03-04, 2025-04-04, 2025-05-04, 2025-06-04, 2025-07-04, 2025-08-04
- Descriptions: Home repair reserve
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`1`
- Latest/expected next: `2025-08-04` / `2025-09-04`
- Active as of request: `True`
- Amount: `3534000` from `event_129, event_137, event_144`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:insurance:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `insurance` / `debit` / `expense`
- Members: event_107, event_115, event_123, event_131, event_139
- Dates: 2025-03-08, 2025-04-08, 2025-05-08, 2025-06-08, 2025-07-08
- Descriptions: Household insurance
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2025-07-08` / `2025-08-08`
- Active as of request: `True`
- Amount: `1132400` from `event_123, event_131, event_139`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:transport:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `transport` / `debit` / `expense`
- Members: event_163, event_164, event_165, event_166, event_167, event_168, event_169, event_170, event_171, event_172, event_173, event_174, event_175
- Dates: 2025-02-11, 2025-02-25, 2025-03-11, 2025-03-25, 2025-04-08, 2025-04-22, 2025-05-06, 2025-05-20, 2025-06-03, 2025-06-17, 2025-07-01, 2025-07-15, 2025-07-29
- Descriptions: Commuter pass, Fuel refill, Metro and bus fares, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`9` residual_days=`0`
- Latest/expected next: `2025-07-29` / `2025-08-12`
- Active as of request: `True`
- Amount: `1327886.54` from `event_173, event_174, event_175`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:expense:debit:utilities:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `utilities` / `debit` / `expense`
- Members: event_106, event_114, event_122, event_130, event_138
- Dates: 2025-03-07, 2025-04-07, 2025-05-07, 2025-06-07, 2025-07-07
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2025-07-07` / `2025-08-07`
- Active as of request: `True`
- Amount: `2141849.94` from `event_122, event_130, event_138`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:income:credit:salary:IDR:fixed:sequence:0`

- User/category/direction/type: `user_02` / `salary` / `credit` / `income`
- Members: event_104, event_112, event_120, event_128, event_136
- Dates: 2025-03-15, 2025-04-15, 2025-05-15, 2025-06-15, 2025-07-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-07-15` / `2025-08-15`
- Active as of request: `True`
- Amount: `33345000` from `event_120, event_128, event_136`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_02:subscription:debit:cloud_storage:IDR:stoppable:sequence:0`

- User/category/direction/type: `user_02` / `cloud_storage` / `debit` / `subscription`
- Members: event_111, event_119, event_127, event_135, event_143
- Dates: 2025-03-13, 2025-04-13, 2025-05-13, 2025-06-13, 2025-07-13
- Descriptions: Shared storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-07-13` / `2025-08-13`
- Active as of request: `True`
- Amount: `369550` from `event_127, event_135, event_143`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:expense:debit:dining:IDR:fixed:sequence:0`

- User/category/direction/type: `user_03` / `dining` / `debit` / `expense`
- Members: event_244, event_245, event_246, event_247, event_248, event_249, event_250, event_251, event_252
- Dates: 2019-03-09, 2019-03-30, 2019-04-20, 2019-05-11, 2019-06-01, 2019-06-22, 2019-07-13, 2019-08-03, 2019-08-24
- Descriptions: Bakery and snacks, Coffee shop, Lunch with colleagues, Quick-service meal, Takeaway order
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2019-08-24` / `2019-09-14`
- Active as of request: `True`
- Amount: `171303.21` from `event_250, event_251, event_252`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:expense:debit:groceries:IDR:fixed:sequence:0`

- User/category/direction/type: `user_03` / `groceries` / `debit` / `expense`
- Members: event_217, event_218, event_219, event_220, event_221, event_222, event_223, event_224, event_225, event_226, event_227, event_228, event_229, event_230, event_231, event_232, event_233, event_234
- Dates: 2019-03-12, 2019-03-22, 2019-04-01, 2019-04-11, 2019-04-21, 2019-05-01, 2019-05-11, 2019-05-21, 2019-05-31, 2019-06-10, 2019-06-20, 2019-06-30, 2019-07-10, 2019-07-20, 2019-07-30, 2019-08-09, 2019-08-19, 2019-08-29
- Descriptions: Bulk pantry shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`0` residual_days=`0`
- Latest/expected next: `2019-08-29` / `2019-09-08`
- Active as of request: `True`
- Amount: `240706.45` from `event_232, event_233, event_234`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:expense:debit:rent:IDR:fixed:sequence:0`

- User/category/direction/type: `user_03` / `rent` / `debit` / `expense`
- Members: event_187, event_193, event_199, event_205, event_212
- Dates: 2019-04-04, 2019-05-04, 2019-06-04, 2019-07-04, 2019-08-04
- Descriptions: Landlord standing order
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`1`
- Latest/expected next: `2019-08-04` / `2019-09-04`
- Active as of request: `True`
- Amount: `1140000` from `event_199, event_205, event_212`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:expense:debit:shopping:IDR:reducible:sequence:0`

- User/category/direction/type: `user_03` / `shopping` / `debit` / `expense`
- Members: event_191, event_197, event_203, event_209, event_216
- Dates: 2019-04-14, 2019-05-14, 2019-06-14, 2019-07-14, 2019-08-14
- Descriptions: Clothing and household items
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2019-08-14` / `2019-09-14`
- Active as of request: `True`
- Amount: `180395.29` from `event_203, event_209, event_216`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:expense:debit:transport:IDR:fixed:sequence:0`

- User/category/direction/type: `user_03` / `transport` / `debit` / `expense`
- Members: event_235, event_236, event_237, event_238, event_239, event_240, event_241, event_242, event_243
- Dates: 2019-03-13, 2019-04-03, 2019-04-24, 2019-05-15, 2019-06-05, 2019-06-26, 2019-07-17, 2019-08-07, 2019-08-28
- Descriptions: Commuter pass, Fuel refill, Metro and bus fares, Parking and tolls, Rail pass, Vehicle charging
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`10` residual_days=`0`
- Latest/expected next: `2019-08-28` / `2019-09-18`
- Active as of request: `True`
- Amount: `106233.46` from `event_241, event_242, event_243`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:expense:debit:utilities:IDR:fixed:sequence:0`

- User/category/direction/type: `user_03` / `utilities` / `debit` / `expense`
- Members: event_188, event_194, event_200, event_206, event_213
- Dates: 2019-04-08, 2019-05-08, 2019-06-08, 2019-07-08, 2019-08-08
- Descriptions: Water and power payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2019-08-08` / `2019-09-08`
- Active as of request: `True`
- Amount: `303042.45` from `event_200, event_206, event_213`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:income:credit:salary:IDR:fixed:sequence:0`

- User/category/direction/type: `user_03` / `salary` / `credit` / `income`
- Members: event_186, event_192, event_198, event_204, event_210
- Dates: 2019-04-15, 2019-05-15, 2019-06-15, 2019-07-15, 2019-08-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2019-08-15` / `2019-09-15`
- Active as of request: `True`
- Amount: `4365000` from `event_198, event_204, event_210`
- Excluded outliers: `event_211, event_253`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:subscription:debit:cloud_storage:IDR:stoppable:sequence:0`

- User/category/direction/type: `user_03` / `cloud_storage` / `debit` / `subscription`
- Members: event_189, event_195, event_201, event_207, event_214
- Dates: 2019-04-14, 2019-05-14, 2019-06-14, 2019-07-14, 2019-08-14
- Descriptions: Shared storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2019-08-14` / `2019-09-14`
- Active as of request: `True`
- Amount: `20900` from `event_201, event_207, event_214`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_03:subscription:debit:streaming:IDR:reducible_or_stoppable:sequence:0`

- User/category/direction/type: `user_03` / `streaming` / `debit` / `subscription`
- Members: event_190, event_196, event_202, event_208, event_215
- Dates: 2019-04-11, 2019-05-11, 2019-06-11, 2019-07-11, 2019-08-11
- Descriptions: Video streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2019-08-11` / `2019-09-11`
- Active as of request: `True`
- Amount: `117800` from `event_202, event_208, event_215`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:expense:debit:dining:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `dining` / `debit` / `expense`
- Members: event_344, event_345, event_346, event_347, event_348, event_349, event_350, event_351, event_352, event_353, event_354, event_355, event_356
- Dates: 2023-12-11, 2023-12-25, 2024-01-08, 2024-01-22, 2024-02-05, 2024-02-19, 2024-03-04, 2024-03-18, 2024-04-01, 2024-04-15, 2024-04-29, 2024-05-13, 2024-05-27
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`1` residual_days=`0`
- Latest/expected next: `2024-05-27` / `2024-06-10`
- Active as of request: `True`
- Amount: `2108488.15` from `event_354, event_355, event_356`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:expense:debit:entertainment:IDR:reducible:sequence:0`

- User/category/direction/type: `user_04` / `entertainment` / `debit` / `expense`
- Members: event_261, event_268, event_276, event_283, event_290
- Dates: 2024-01-13, 2024-02-13, 2024-03-13, 2024-04-13, 2024-05-13
- Descriptions: Local event tickets
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`2`
- Latest/expected next: `2024-05-13` / `2024-06-13`
- Active as of request: `True`
- Amount: `1542620` from `event_276, event_283, event_290`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:expense:debit:groceries:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `groceries` / `debit` / `expense`
- Members: event_292, event_293, event_294, event_295, event_296, event_297, event_298, event_299, event_300, event_301, event_302, event_303, event_304, event_305, event_306, event_307, event_308, event_309, event_310, event_311, event_312, event_313, event_314, event_315, event_316, event_317
- Dates: 2023-12-09, 2023-12-16, 2023-12-23, 2023-12-30, 2024-01-06, 2024-01-13, 2024-01-20, 2024-01-27, 2024-02-03, 2024-02-10, 2024-02-17, 2024-02-24, 2024-03-02, 2024-03-09, 2024-03-16, 2024-03-23, 2024-03-30, 2024-04-06, 2024-04-13, 2024-04-20, 2024-04-27, 2024-05-04, 2024-05-11, 2024-05-18, 2024-05-25, 2024-06-01
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2024-06-01` / `2024-06-08`
- Active as of request: `True`
- Amount: `1809752.54` from `event_315, event_316, event_317`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:expense:debit:rent:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `rent` / `debit` / `expense`
- Members: event_256, event_263, event_271, event_278, event_285, event_291
- Dates: 2024-01-01, 2024-02-01, 2024-03-01, 2024-04-01, 2024-05-01, 2024-06-01
- Descriptions: Residential rent payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`1` residual_days=`2`
- Latest/expected next: `2024-06-01` / `2024-07-01`
- Active as of request: `True`
- Amount: `12293000` from `event_278, event_285, event_291`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:expense:debit:transport:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `transport` / `debit` / `expense`
- Members: event_318, event_319, event_320, event_321, event_322, event_323, event_324, event_325, event_326, event_327, event_328, event_329, event_330, event_331, event_332, event_333, event_334, event_335, event_336, event_337, event_338, event_339, event_340, event_341, event_342, event_343
- Dates: 2023-12-10, 2023-12-17, 2023-12-24, 2023-12-31, 2024-01-07, 2024-01-14, 2024-01-21, 2024-01-28, 2024-02-04, 2024-02-11, 2024-02-18, 2024-02-25, 2024-03-03, 2024-03-10, 2024-03-17, 2024-03-24, 2024-03-31, 2024-04-07, 2024-04-14, 2024-04-21, 2024-04-28, 2024-05-05, 2024-05-12, 2024-05-19, 2024-05-26, 2024-06-02
- Descriptions: Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`0` residual_days=`0`
- Latest/expected next: `2024-06-02` / `2024-06-09`
- Active as of request: `True`
- Amount: `1016425.58` from `event_341, event_342, event_343`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:expense:debit:utilities:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `utilities` / `debit` / `expense`
- Members: event_257, event_264, event_272, event_279, event_286
- Dates: 2024-01-05, 2024-02-05, 2024-03-05, 2024-04-05, 2024-05-05
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`2`
- Latest/expected next: `2024-05-05` / `2024-06-05`
- Active as of request: `True`
- Amount: `2033868.83` from `event_272, event_279, event_286`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:income:credit:salary:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `salary` / `credit` / `income`
- Members: event_255, event_262, event_269, event_277, event_284
- Dates: 2024-01-15, 2024-02-15, 2024-03-15, 2024-04-15, 2024-05-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`2`
- Latest/expected next: `2024-05-15` / `2024-06-15`
- Active as of request: `True`
- Amount: `38190000` from `event_269, event_277, event_284`
- Excluded outliers: `event_270`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:subscription:debit:delivery_membership:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `delivery_membership` / `debit` / `subscription`
- Members: event_259, event_266, event_274, event_281, event_288
- Dates: 2024-01-12, 2024-02-12, 2024-03-12, 2024-04-12, 2024-05-12
- Descriptions: Food delivery membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`2`
- Latest/expected next: `2024-05-12` / `2024-06-12`
- Active as of request: `True`
- Amount: `377150` from `event_274, event_281, event_288`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:subscription:debit:gym:IDR:fixed:sequence:0`

- User/category/direction/type: `user_04` / `gym` / `debit` / `subscription`
- Members: event_260, event_267, event_275, event_282, event_289
- Dates: 2024-01-09, 2024-02-09, 2024-03-09, 2024-04-09, 2024-05-09
- Descriptions: Gym membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`2`
- Latest/expected next: `2024-05-09` / `2024-06-09`
- Active as of request: `True`
- Amount: `1027900` from `event_275, event_282, event_289`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_04:subscription:debit:music_subscription:IDR:stoppable:sequence:0`

- User/category/direction/type: `user_04` / `music_subscription` / `debit` / `subscription`
- Members: event_258, event_265, event_273, event_280, event_287
- Dates: 2024-01-10, 2024-02-10, 2024-03-10, 2024-04-10, 2024-05-10
- Descriptions: Music service subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`2`
- Latest/expected next: `2024-05-10` / `2024-06-10`
- Active as of request: `True`
- Amount: `332500` from `event_273, event_280, event_287`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:debt_payment:debit:debt_repayment:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_361, event_369, event_377, event_385, event_393
- Dates: 2025-06-11, 2025-07-11, 2025-08-11, 2025-09-11, 2025-10-11
- Descriptions: Vehicle loan payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2025-10-11` / `2025-11-11`
- Active as of request: `True`
- Amount: `968` from `event_377, event_385, event_393`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:family_support:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `family_support` / `debit` / `expense`
- Members: event_363, event_371, event_379, event_387, event_395
- Dates: 2025-06-13, 2025-07-13, 2025-08-13, 2025-09-13, 2025-10-13
- Descriptions: Dependent care payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-10-13` / `2025-11-13`
- Active as of request: `True`
- Amount: `840.4` from `event_379, event_387, event_395`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:groceries:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `groceries` / `debit` / `expense`
- Members: event_399, event_400, event_401, event_402, event_403, event_404, event_405, event_406, event_407, event_408, event_409, event_410, event_411, event_412, event_413, event_414, event_415, event_416, event_417, event_418, event_419, event_420, event_421, event_422, event_423, event_424
- Dates: 2025-05-13, 2025-05-20, 2025-05-27, 2025-06-03, 2025-06-10, 2025-06-17, 2025-06-24, 2025-07-01, 2025-07-08, 2025-07-15, 2025-07-22, 2025-07-29, 2025-08-05, 2025-08-12, 2025-08-19, 2025-08-26, 2025-09-02, 2025-09-09, 2025-09-16, 2025-09-23, 2025-09-30, 2025-10-07, 2025-10-14, 2025-10-21, 2025-10-28, 2025-11-04
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2025-11-04` / `2025-11-11`
- Active as of request: `True`
- Amount: `720.51` from `event_422, event_423, event_424`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:healthcare:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `healthcare` / `debit` / `expense`
- Members: event_362, event_370, event_378, event_386, event_394
- Dates: 2025-06-10, 2025-07-10, 2025-08-10, 2025-09-10, 2025-10-10
- Descriptions: Therapy appointment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2025-10-10` / `2025-11-10`
- Active as of request: `True`
- Amount: `722.37` from `event_378, event_386, event_394`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:rent:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `rent` / `debit` / `expense`
- Members: event_359, event_367, event_375, event_383, event_391, event_398
- Dates: 2025-06-02, 2025-07-02, 2025-08-02, 2025-09-02, 2025-10-02, 2025-11-02
- Descriptions: Apartment rent transfer
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`1`
- Latest/expected next: `2025-11-02` / `2025-12-02`
- Active as of request: `True`
- Amount: `4972` from `event_383, event_391, event_398`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:shopping:ZAR:reducible:sequence:0`

- User/category/direction/type: `user_05` / `shopping` / `debit` / `expense`
- Members: event_365, event_373, event_381, event_389, event_397
- Dates: 2025-06-12, 2025-07-12, 2025-08-12, 2025-09-12, 2025-10-12
- Descriptions: Personal shopping
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2025-10-12` / `2025-11-12`
- Active as of request: `True`
- Amount: `422.67` from `event_381, event_389, event_397`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:transport:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `transport` / `debit` / `expense`
- Members: event_425, event_426, event_427, event_428, event_429, event_430, event_431, event_432, event_433, event_434, event_435, event_436, event_437
- Dates: 2025-05-14, 2025-05-28, 2025-06-11, 2025-06-25, 2025-07-09, 2025-07-23, 2025-08-06, 2025-08-20, 2025-09-03, 2025-09-17, 2025-10-01, 2025-10-15, 2025-10-29
- Descriptions: Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2025-10-29` / `2025-11-12`
- Active as of request: `True`
- Amount: `388.74` from `event_435, event_436, event_437`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:expense:debit:utilities:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `utilities` / `debit` / `expense`
- Members: event_360, event_368, event_376, event_384, event_392
- Dates: 2025-06-06, 2025-07-06, 2025-08-06, 2025-09-06, 2025-10-06
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`1`
- Latest/expected next: `2025-10-06` / `2025-11-06`
- Active as of request: `True`
- Amount: `750.89` from `event_376, event_384, event_392`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:income:credit:salary:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_05` / `salary` / `credit` / `income`
- Members: event_358, event_366, event_374, event_382, event_390
- Dates: 2025-06-15, 2025-07-15, 2025-08-15, 2025-09-15, 2025-10-15
- Descriptions: Final employer payroll, Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-10-15` / `2025-11-15`
- Active as of request: `True`
- Amount: `14740` from `event_374, event_382, event_390`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_05:subscription:debit:cloud_storage:ZAR:stoppable:sequence:0`

- User/category/direction/type: `user_05` / `cloud_storage` / `debit` / `subscription`
- Members: event_364, event_372, event_380, event_388, event_396
- Dates: 2025-06-12, 2025-07-12, 2025-08-12, 2025-09-12, 2025-10-12
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2025-10-12` / `2025-11-12`
- Active as of request: `True`
- Amount: `113.3` from `event_380, event_388, event_396`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:dining:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `dining` / `debit` / `expense`
- Members: event_532, event_533, event_534, event_535, event_536, event_537, event_538, event_539, event_540, event_541, event_542, event_543, event_544, event_545, event_546, event_547, event_548, event_549, event_550, event_551, event_552, event_553, event_554, event_555, event_556
- Dates: 2025-07-13, 2025-07-20, 2025-07-27, 2025-08-03, 2025-08-10, 2025-08-17, 2025-08-24, 2025-08-31, 2025-09-07, 2025-09-14, 2025-09-21, 2025-09-28, 2025-10-05, 2025-10-12, 2025-10-19, 2025-10-26, 2025-11-02, 2025-11-09, 2025-11-16, 2025-11-23, 2025-11-30, 2025-12-07, 2025-12-14, 2025-12-21, 2025-12-28
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`0` residual_days=`0`
- Latest/expected next: `2025-12-28` / `2026-01-04`
- Active as of request: `True`
- Amount: `57.28` from `event_554, event_555, event_556`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:entertainment:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `entertainment` / `debit` / `expense`
- Members: event_446, event_454, event_462, event_470, event_478
- Dates: 2025-08-15, 2025-09-15, 2025-10-15, 2025-11-15, 2025-12-15
- Descriptions: Monthly entertainment spend
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-12-15` / `2026-01-15`
- Active as of request: `True`
- Amount: `38.33` from `event_462, event_470, event_478`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `groceries` / `debit` / `expense`
- Members: event_479, event_480, event_481, event_482, event_483, event_484, event_485, event_486, event_487, event_488, event_489, event_490, event_491, event_492, event_493, event_494, event_495, event_496
- Dates: 2025-07-11, 2025-07-21, 2025-07-31, 2025-08-10, 2025-08-20, 2025-08-30, 2025-09-09, 2025-09-19, 2025-09-29, 2025-10-09, 2025-10-19, 2025-10-29, 2025-11-08, 2025-11-18, 2025-11-28, 2025-12-08, 2025-12-18, 2025-12-28
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2025-12-28` / `2026-01-07`
- Active as of request: `True`
- Amount: `52.76` from `event_494, event_495, event_496`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:insurance:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `insurance` / `debit` / `expense`
- Members: event_442, event_450, event_458, event_466, event_474
- Dates: 2025-08-08, 2025-09-08, 2025-10-08, 2025-11-08, 2025-12-08
- Descriptions: Vehicle insurance premium
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2025-12-08` / `2026-01-08`
- Active as of request: `True`
- Amount: `26` from `event_458, event_466, event_474`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `rent` / `debit` / `expense`
- Members: event_440, event_448, event_456, event_464, event_472
- Dates: 2025-08-03, 2025-09-03, 2025-10-03, 2025-11-03, 2025-12-03
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`3` residual_days=`1`
- Latest/expected next: `2025-12-03` / `2026-01-03`
- Active as of request: `True`
- Amount: `254.1` from `event_456, event_464, event_472`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:shopping:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `shopping` / `debit` / `expense`
- Members: event_445, event_453, event_461, event_469, event_477
- Dates: 2025-08-13, 2025-09-13, 2025-10-13, 2025-11-13, 2025-12-13
- Descriptions: Household shopping
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-12-13` / `2026-01-13`
- Active as of request: `True`
- Amount: `39.88` from `event_461, event_469, event_477`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `transport` / `debit` / `expense`
- Members: event_497, event_498, event_499, event_500, event_501, event_502, event_503, event_504, event_505, event_506, event_507, event_508, event_509, event_510, event_511, event_512, event_513, event_514, event_515, event_516, event_517, event_518, event_519, event_520, event_521, event_522, event_523, event_524, event_525, event_526, event_527, event_528, event_529, event_530, event_531
- Dates: 2025-07-12, 2025-07-17, 2025-07-22, 2025-07-27, 2025-08-01, 2025-08-06, 2025-08-11, 2025-08-16, 2025-08-21, 2025-08-26, 2025-08-31, 2025-09-05, 2025-09-10, 2025-09-15, 2025-09-20, 2025-09-25, 2025-09-30, 2025-10-05, 2025-10-10, 2025-10-15, 2025-10-20, 2025-10-25, 2025-10-30, 2025-11-04, 2025-11-09, 2025-11-14, 2025-11-19, 2025-11-24, 2025-11-29, 2025-12-04, 2025-12-09, 2025-12-14, 2025-12-19, 2025-12-24, 2025-12-29
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`5` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2025-12-29` / `2026-01-03`
- Active as of request: `True`
- Amount: `32.9` from `event_529, event_530, event_531`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `utilities` / `debit` / `expense`
- Members: event_441, event_449, event_457, event_465, event_473
- Dates: 2025-08-07, 2025-09-07, 2025-10-07, 2025-11-07, 2025-12-07
- Descriptions: Water and power payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2025-12-07` / `2026-01-07`
- Active as of request: `True`
- Amount: `58.98` from `event_457, event_465, event_473`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:income:credit:salary:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `salary` / `credit` / `income`
- Members: event_439, event_447, event_455, event_463, event_471
- Dates: 2025-08-15, 2025-09-15, 2025-10-15, 2025-11-15, 2025-12-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-12-15` / `2026-01-15`
- Active as of request: `True`
- Amount: `1441` from `event_455, event_463, event_471`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:subscription:debit:cloud_storage:EUR:fixed:sequence:0`

- User/category/direction/type: `user_06` / `cloud_storage` / `debit` / `subscription`
- Members: event_443, event_451, event_459, event_467, event_475
- Dates: 2025-08-13, 2025-09-13, 2025-10-13, 2025-11-13, 2025-12-13
- Descriptions: Shared storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-12-13` / `2026-01-13`
- Active as of request: `True`
- Amount: `5` from `event_459, event_467, event_475`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_06:subscription:debit:streaming:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_06` / `streaming` / `debit` / `subscription`
- Members: event_444, event_452, event_460, event_468, event_476
- Dates: 2025-08-10, 2025-09-10, 2025-10-10, 2025-11-10, 2025-12-10
- Descriptions: Family streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2025-12-10` / `2026-01-10`
- Active as of request: `True`
- Amount: `19` from `event_460, event_468, event_476`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:debt_payment:debit:debt_repayment:INR:fixed:sequence:0`

- User/category/direction/type: `user_07` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_561, event_566, event_571, event_576, event_581
- Dates: 2024-04-13, 2024-05-13, 2024-06-13, 2024-07-13, 2024-08-13
- Descriptions: Personal loan payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2024-08-13` / `2024-09-13`
- Active as of request: `True`
- Amount: `15650` from `event_571, event_576, event_581`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:expense:debit:dining:INR:reducible:sequence:0`

- User/category/direction/type: `user_07` / `dining` / `debit` / `expense`
- Members: event_606, event_607, event_608, event_609, event_610, event_611, event_612, event_613, event_614
- Dates: 2024-03-11, 2024-04-01, 2024-04-22, 2024-05-13, 2024-06-03, 2024-06-24, 2024-07-15, 2024-08-05, 2024-08-26
- Descriptions: Bakery and snacks, Family dinner, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`8` residual_days=`0`
- Latest/expected next: `2024-08-26` / `2024-09-16`
- Active as of request: `True`
- Amount: `6664.9` from `event_612, event_613, event_614`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_07` / `groceries` / `debit` / `expense`
- Members: event_584, event_585, event_586, event_587, event_588, event_589, event_590, event_591, event_592, event_593, event_594, event_595, event_596
- Dates: 2024-03-14, 2024-03-28, 2024-04-11, 2024-04-25, 2024-05-09, 2024-05-23, 2024-06-06, 2024-06-20, 2024-07-04, 2024-07-18, 2024-08-01, 2024-08-15, 2024-08-29
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`11` residual_days=`0`
- Latest/expected next: `2024-08-29` / `2024-09-12`
- Active as of request: `True`
- Amount: `7913.81` from `event_594, event_595, event_596`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:expense:debit:rent:INR:fixed:sequence:0`

- User/category/direction/type: `user_07` / `rent` / `debit` / `expense`
- Members: event_559, event_564, event_569, event_574, event_579, event_583
- Dates: 2024-04-04, 2024-05-04, 2024-06-04, 2024-07-04, 2024-08-04, 2024-09-04
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`1`
- Latest/expected next: `2024-09-04` / `2024-10-04`
- Active as of request: `True`
- Amount: `34200` from `event_574, event_579, event_583`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_07` / `transport` / `debit` / `expense`
- Members: event_597, event_598, event_599, event_600, event_601, event_602, event_603, event_604, event_605
- Dates: 2024-03-15, 2024-04-05, 2024-04-26, 2024-05-17, 2024-06-07, 2024-06-28, 2024-07-19, 2024-08-09, 2024-08-30
- Descriptions: Commuter pass, Fuel refill, Metro and bus fares, Rail pass, Vehicle charging
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`12` residual_days=`0`
- Latest/expected next: `2024-08-30` / `2024-09-20`
- Active as of request: `True`
- Amount: `3773.92` from `event_603, event_604, event_605`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_07` / `utilities` / `debit` / `expense`
- Members: event_560, event_565, event_570, event_575, event_580
- Dates: 2024-04-08, 2024-05-08, 2024-06-08, 2024-07-08, 2024-08-08
- Descriptions: Electricity bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2024-08-08` / `2024-09-08`
- Active as of request: `True`
- Amount: `7387.41` from `event_570, event_575, event_580`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_07` / `salary` / `credit` / `income`
- Members: event_558, event_563, event_568, event_573, event_578
- Dates: 2024-04-15, 2024-05-15, 2024-06-15, 2024-07-15, 2024-08-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-08-15` / `2024-09-15`
- Active as of request: `True`
- Amount: `149000` from `event_568, event_573, event_578`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_07:subscription:debit:music_subscription:INR:stoppable:sequence:0`

- User/category/direction/type: `user_07` / `music_subscription` / `debit` / `subscription`
- Members: event_562, event_567, event_572, event_577, event_582
- Dates: 2024-04-13, 2024-05-13, 2024-06-13, 2024-07-13, 2024-08-13
- Descriptions: Music subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2024-08-13` / `2024-09-13`
- Active as of request: `True`
- Amount: `1005` from `event_572, event_577, event_582`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:debt_payment:debit:debt_repayment:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_619, event_626, event_633, event_640, event_647
- Dates: 2024-09-10, 2024-10-10, 2024-11-10, 2024-12-10, 2025-01-10
- Descriptions: Personal loan payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2025-01-10` / `2025-02-10`
- Active as of request: `True`
- Amount: `177` from `event_633, event_640, event_647`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:expense:debit:dining:EUR:reducible:sequence:0`

- User/category/direction/type: `user_08` / `dining` / `debit` / `expense`
- Members: event_704, event_705, event_706, event_707, event_708, event_709, event_710, event_711, event_712, event_713, event_714, event_715, event_716
- Dates: 2024-08-15, 2024-08-29, 2024-09-12, 2024-09-26, 2024-10-10, 2024-10-24, 2024-11-07, 2024-11-21, 2024-12-05, 2024-12-19, 2025-01-02, 2025-01-16, 2025-01-30
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`11` residual_days=`0`
- Latest/expected next: `2025-01-30` / `2025-02-13`
- Active as of request: `True`
- Amount: `56.05` from `event_714, event_715, event_716`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:expense:debit:education:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `education` / `debit` / `expense`
- Members: event_618, event_625, event_632, event_639, event_646
- Dates: 2024-09-07, 2024-10-07, 2024-11-07, 2024-12-07, 2025-01-07
- Descriptions: School fee payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2025-01-07` / `2025-02-07`
- Active as of request: `True`
- Amount: `89` from `event_632, event_639, event_646`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `groceries` / `debit` / `expense`
- Members: event_652, event_653, event_654, event_655, event_656, event_657, event_658, event_659, event_660, event_661, event_662, event_663, event_664, event_665, event_666, event_667, event_668, event_669, event_670, event_671, event_672, event_673, event_674, event_675, event_676, event_677
- Dates: 2024-08-13, 2024-08-20, 2024-08-27, 2024-09-03, 2024-09-10, 2024-09-17, 2024-09-24, 2024-10-01, 2024-10-08, 2024-10-15, 2024-10-22, 2024-10-29, 2024-11-05, 2024-11-12, 2024-11-19, 2024-11-26, 2024-12-03, 2024-12-10, 2024-12-17, 2024-12-24, 2024-12-31, 2025-01-07, 2025-01-14, 2025-01-21, 2025-01-28, 2025-02-04
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2025-02-04` / `2025-02-11`
- Active as of request: `True`
- Amount: `72.38` from `event_675, event_676, event_677`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `rent` / `debit` / `expense`
- Members: event_616, event_623, event_630, event_637, event_644, event_650
- Dates: 2024-09-01, 2024-10-01, 2024-11-01, 2024-12-01, 2025-01-01, 2025-02-01
- Descriptions: Apartment rent transfer
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`1` residual_days=`1`
- Latest/expected next: `2025-02-01` / `2025-03-01`
- Active as of request: `True`
- Amount: `467.5` from `event_637, event_644, event_650`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `transport` / `debit` / `expense`
- Members: event_678, event_679, event_680, event_681, event_682, event_683, event_684, event_685, event_686, event_687, event_688, event_689, event_690, event_691, event_692, event_693, event_694, event_695, event_696, event_697, event_698, event_699, event_700, event_701, event_702, event_703
- Dates: 2024-08-14, 2024-08-21, 2024-08-28, 2024-09-04, 2024-09-11, 2024-09-18, 2024-09-25, 2024-10-02, 2024-10-09, 2024-10-16, 2024-10-23, 2024-10-30, 2024-11-06, 2024-11-13, 2024-11-20, 2024-11-27, 2024-12-04, 2024-12-11, 2024-12-18, 2024-12-25, 2025-01-01, 2025-01-08, 2025-01-15, 2025-01-22, 2025-01-29, 2025-02-05
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2025-02-05` / `2025-02-12`
- Active as of request: `True`
- Amount: `47.21` from `event_701, event_702, event_703`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `utilities` / `debit` / `expense`
- Members: event_617, event_624, event_631, event_638, event_645, event_651
- Dates: 2024-09-05, 2024-10-05, 2024-11-05, 2024-12-05, 2025-01-05, 2025-02-05
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`1`
- Latest/expected next: `2025-02-05` / `2025-03-05`
- Active as of request: `True`
- Amount: `82.61` from `event_638, event_645, event_651`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:income:credit:salary:EUR:fixed:sequence:0`

- User/category/direction/type: `user_08` / `salary` / `credit` / `income`
- Members: event_615, event_622, event_629, event_636, event_643
- Dates: 2024-09-15, 2024-10-15, 2024-11-15, 2024-12-15, 2025-01-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-01-15` / `2025-02-15`
- Active as of request: `True`
- Amount: `1422.85` from `event_629, event_636, event_643`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:subscription:debit:delivery_membership:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_08` / `delivery_membership` / `debit` / `subscription`
- Members: event_621, event_628, event_635, event_642, event_649
- Dates: 2024-09-12, 2024-10-12, 2024-11-12, 2024-12-12, 2025-01-12
- Descriptions: Grocery delivery membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2025-01-12` / `2025-02-12`
- Active as of request: `True`
- Amount: `24` from `event_635, event_642, event_649`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_08:subscription:debit:music_subscription:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_08` / `music_subscription` / `debit` / `subscription`
- Members: event_620, event_627, event_634, event_641, event_648
- Dates: 2024-09-10, 2024-10-10, 2024-11-10, 2024-12-10, 2025-01-10
- Descriptions: Music subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2025-01-10` / `2025-02-10`
- Active as of request: `True`
- Amount: `14` from `event_634, event_641, event_648`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:expense:debit:dining:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `dining` / `debit` / `expense`
- Members: event_780, event_781, event_782, event_783, event_784, event_785, event_786, event_787, event_788
- Dates: 2026-01-10, 2026-01-31, 2026-02-21, 2026-03-14, 2026-04-04, 2026-04-25, 2026-05-16, 2026-06-06, 2026-06-27
- Descriptions: Coffee shop, Family dinner, Lunch with colleagues, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2026-06-27` / `2026-07-18`
- Active as of request: `True`
- Amount: `35.49` from `event_786, event_787, event_788`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `groceries` / `debit` / `expense`
- Members: event_753, event_754, event_755, event_756, event_757, event_758, event_759, event_760, event_761, event_762, event_763, event_764, event_765, event_766, event_767, event_768, event_769, event_770
- Dates: 2026-01-08, 2026-01-18, 2026-01-28, 2026-02-07, 2026-02-17, 2026-02-27, 2026-03-09, 2026-03-19, 2026-03-29, 2026-04-08, 2026-04-18, 2026-04-28, 2026-05-08, 2026-05-18, 2026-05-28, 2026-06-07, 2026-06-17, 2026-06-27
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2026-06-27` / `2026-07-07`
- Active as of request: `True`
- Amount: `51.3` from `event_768, event_769, event_770`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `rent` / `debit` / `expense`
- Members: event_719, event_726, event_733, event_740, event_747, event_752
- Dates: 2026-02-02, 2026-03-02, 2026-04-02, 2026-05-02, 2026-06-02, 2026-07-02
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`3`
- Latest/expected next: `2026-07-02` / `2026-08-02`
- Active as of request: `True`
- Amount: `211.2` from `event_740, event_747, event_752`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:expense:debit:shopping:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `shopping` / `debit` / `expense`
- Members: event_723, event_730, event_737, event_744, event_751
- Dates: 2026-02-12, 2026-03-12, 2026-04-12, 2026-05-12, 2026-06-12
- Descriptions: Household shopping
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`3`
- Latest/expected next: `2026-06-12` / `2026-07-12`
- Active as of request: `True`
- Amount: `28.32` from `event_737, event_744, event_751`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `transport` / `debit` / `expense`
- Members: event_771, event_772, event_773, event_774, event_775, event_776, event_777, event_778, event_779
- Dates: 2026-01-09, 2026-01-30, 2026-02-20, 2026-03-13, 2026-04-03, 2026-04-24, 2026-05-15, 2026-06-05, 2026-06-26
- Descriptions: Commuter pass, Local taxi, Parking and tolls, Rail pass, Vehicle charging
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`5` residual_days=`0`
- Latest/expected next: `2026-06-26` / `2026-07-17`
- Active as of request: `True`
- Amount: `28.34` from `event_777, event_778, event_779`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `utilities` / `debit` / `expense`
- Members: event_720, event_727, event_734, event_741, event_748
- Dates: 2026-02-06, 2026-03-06, 2026-04-06, 2026-05-06, 2026-06-06
- Descriptions: Water and power payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`3`
- Latest/expected next: `2026-06-06` / `2026-07-06`
- Active as of request: `True`
- Amount: `71.04` from `event_734, event_741, event_748`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:income:credit:salary:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `salary` / `credit` / `income`
- Members: event_717, event_724, event_731, event_738, event_745
- Dates: 2026-02-07, 2026-03-07, 2026-04-07, 2026-05-07, 2026-06-07
- Descriptions: Consulting invoice payment, Design contract payment, Freelance milestone payment, Website project payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`3`
- Latest/expected next: `2026-06-07` / `2026-07-07`
- Active as of request: `True`
- Amount: `582.12` from `event_731, event_738, event_745`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:income:credit:salary:EUR:fixed:sequence:1`

- User/category/direction/type: `user_09` / `salary` / `credit` / `income`
- Members: event_718, event_725, event_732, event_739, event_746
- Dates: 2026-02-20, 2026-03-20, 2026-04-20, 2026-05-20, 2026-06-20
- Descriptions: Application project payment, Client retainer payment, Content contract payment, Independent work payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`20` residual_days=`3`
- Latest/expected next: `2026-06-20` / `2026-07-20`
- Active as of request: `True`
- Amount: `441.96` from `event_732, event_739, event_746`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:subscription:debit:cloud_storage:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `cloud_storage` / `debit` / `subscription`
- Members: event_721, event_728, event_735, event_742, event_749
- Dates: 2026-02-12, 2026-03-12, 2026-04-12, 2026-05-12, 2026-06-12
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`3`
- Latest/expected next: `2026-06-12` / `2026-07-12`
- Active as of request: `True`
- Amount: `5` from `event_735, event_742, event_749`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_09:subscription:debit:streaming:EUR:fixed:sequence:0`

- User/category/direction/type: `user_09` / `streaming` / `debit` / `subscription`
- Members: event_722, event_729, event_736, event_743, event_750
- Dates: 2026-02-09, 2026-03-09, 2026-04-09, 2026-05-09, 2026-06-09
- Descriptions: Video streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`3`
- Latest/expected next: `2026-06-09` / `2026-07-09`
- Active as of request: `True`
- Amount: `20` from `event_736, event_743, event_750`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:expense:debit:dining:INR:reducible:sequence:0`

- User/category/direction/type: `user_10` / `dining` / `debit` / `expense`
- Members: event_892, event_893, event_894, event_895, event_896, event_897, event_898, event_899, event_900, event_901, event_902, event_903, event_904
- Dates: 2024-06-15, 2024-06-29, 2024-07-13, 2024-07-27, 2024-08-10, 2024-08-24, 2024-09-07, 2024-09-21, 2024-10-05, 2024-10-19, 2024-11-02, 2024-11-16, 2024-11-30
- Descriptions: Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2024-11-30` / `2024-12-14`
- Active as of request: `True`
- Amount: `10370.83` from `event_902, event_903, event_904`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:expense:debit:entertainment:INR:reducible:sequence:0`

- User/category/direction/type: `user_10` / `entertainment` / `debit` / `expense`
- Members: event_798, event_808, event_818, event_828, event_838
- Dates: 2024-07-15, 2024-08-15, 2024-09-15, 2024-10-15, 2024-11-15
- Descriptions: Cinema and events
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-11-15` / `2024-12-15`
- Active as of request: `True`
- Amount: `4883.78` from `event_818, event_828, event_838`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_10` / `groceries` / `debit` / `expense`
- Members: event_841, event_842, event_843, event_844, event_845, event_846, event_847, event_848, event_849, event_850, event_851, event_852, event_853, event_854, event_855, event_856, event_857, event_858, event_859, event_860, event_861, event_862, event_863, event_864, event_865, event_866
- Dates: 2024-06-13, 2024-06-20, 2024-06-27, 2024-07-04, 2024-07-11, 2024-07-18, 2024-07-25, 2024-08-01, 2024-08-08, 2024-08-15, 2024-08-22, 2024-08-29, 2024-09-05, 2024-09-12, 2024-09-19, 2024-09-26, 2024-10-03, 2024-10-10, 2024-10-17, 2024-10-24, 2024-10-31, 2024-11-07, 2024-11-14, 2024-11-21, 2024-11-28, 2024-12-05
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2024-12-05` / `2024-12-12`
- Active as of request: `True`
- Amount: `8755.75` from `event_864, event_865, event_866`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:expense:debit:rent:INR:fixed:sequence:0`

- User/category/direction/type: `user_10` / `rent` / `debit` / `expense`
- Members: event_793, event_803, event_813, event_823, event_833, event_840
- Dates: 2024-07-03, 2024-08-03, 2024-09-03, 2024-10-03, 2024-11-03, 2024-12-03
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`3` residual_days=`1`
- Latest/expected next: `2024-12-03` / `2025-01-03`
- Active as of request: `True`
- Amount: `69100` from `event_823, event_833, event_840`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_10` / `transport` / `debit` / `expense`
- Members: event_867, event_868, event_869, event_870, event_871, event_872, event_873, event_874, event_875, event_876, event_877, event_878, event_879, event_880, event_881, event_882, event_883, event_884, event_885, event_886, event_887, event_888, event_889, event_890, event_891
- Dates: 2024-06-14, 2024-06-21, 2024-06-28, 2024-07-05, 2024-07-12, 2024-07-19, 2024-07-26, 2024-08-02, 2024-08-09, 2024-08-16, 2024-08-23, 2024-08-30, 2024-09-06, 2024-09-13, 2024-09-20, 2024-09-27, 2024-10-04, 2024-10-11, 2024-10-18, 2024-10-25, 2024-11-01, 2024-11-08, 2024-11-15, 2024-11-22, 2024-11-29
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`5` residual_days=`0`
- Latest/expected next: `2024-11-29` / `2024-12-06`
- Active as of request: `True`
- Amount: `6359.49` from `event_889, event_890, event_891`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_10` / `utilities` / `debit` / `expense`
- Members: event_794, event_804, event_814, event_824, event_834
- Dates: 2024-07-07, 2024-08-07, 2024-09-07, 2024-10-07, 2024-11-07
- Descriptions: Electricity and water bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2024-11-07` / `2024-12-07`
- Active as of request: `True`
- Amount: `17771.13` from `event_814, event_824, event_834`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_10` / `salary` / `credit` / `income`
- Members: event_789, event_799, event_809, event_819, event_829, event_839
- Dates: 2024-07-04, 2024-08-04, 2024-09-04, 2024-10-04, 2024-11-04, 2024-12-04
- Descriptions: Delivery platform payout, Driver platform payout, Task marketplace payout
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`1`
- Latest/expected next: `2024-12-04` / `2025-01-04`
- Active as of request: `True`
- Amount: `78226.16` from `event_819, event_829, event_839`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:income:credit:salary:INR:fixed:sequence:1`

- User/category/direction/type: `user_10` / `salary` / `credit` / `income`
- Members: event_790, event_800, event_810, event_820, event_830
- Dates: 2024-07-11, 2024-08-11, 2024-09-11, 2024-10-11, 2024-11-11
- Descriptions: Delivery platform payout, Task marketplace payout, Weekly app earnings
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2024-11-11` / `2024-12-11`
- Active as of request: `True`
- Amount: `67741.04` from `event_810, event_820, event_830`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:income:credit:salary:INR:fixed:sequence:2`

- User/category/direction/type: `user_10` / `salary` / `credit` / `income`
- Members: event_791, event_801, event_811, event_821, event_831
- Dates: 2024-07-18, 2024-08-18, 2024-09-18, 2024-10-18, 2024-11-18
- Descriptions: Delivery platform payout, Driver platform payout, Task marketplace payout
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`18` residual_days=`1`
- Latest/expected next: `2024-11-18` / `2024-12-18`
- Active as of request: `True`
- Amount: `79168.24` from `event_811, event_821, event_831`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:income:credit:salary:INR:fixed:sequence:3`

- User/category/direction/type: `user_10` / `salary` / `credit` / `income`
- Members: event_792, event_802, event_812, event_822, event_832
- Dates: 2024-07-25, 2024-08-25, 2024-09-25, 2024-10-25, 2024-11-25
- Descriptions: Delivery platform payout, Task marketplace payout, Weekly app earnings
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`25` residual_days=`1`
- Latest/expected next: `2024-11-25` / `2024-12-25`
- Active as of request: `True`
- Amount: `82667.27` from `event_812, event_822, event_832`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:subscription:debit:delivery_membership:INR:stoppable:sequence:0`

- User/category/direction/type: `user_10` / `delivery_membership` / `debit` / `subscription`
- Members: event_796, event_806, event_816, event_826, event_836
- Dates: 2024-07-14, 2024-08-14, 2024-09-14, 2024-10-14, 2024-11-14
- Descriptions: Delivery service plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2024-11-14` / `2024-12-14`
- Active as of request: `True`
- Amount: `1895` from `event_816, event_826, event_836`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:subscription:debit:gym:INR:reducible:sequence:0`

- User/category/direction/type: `user_10` / `gym` / `debit` / `subscription`
- Members: event_797, event_807, event_817, event_827, event_837
- Dates: 2024-07-11, 2024-08-11, 2024-09-11, 2024-10-11, 2024-11-11
- Descriptions: Community fitness plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2024-11-11` / `2024-12-11`
- Active as of request: `True`
- Amount: `4860` from `event_817, event_827, event_837`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_10:subscription:debit:music_subscription:INR:stoppable:sequence:0`

- User/category/direction/type: `user_10` / `music_subscription` / `debit` / `subscription`
- Members: event_795, event_805, event_815, event_825, event_835
- Dates: 2024-07-12, 2024-08-12, 2024-09-12, 2024-10-12, 2024-11-12
- Descriptions: Music subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2024-11-12` / `2024-12-12`
- Active as of request: `True`
- Amount: `2800` from `event_815, event_825, event_835`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:dining:IDR:reducible:sequence:0`

- User/category/direction/type: `user_11` / `dining` / `debit` / `expense`
- Members: event_981, event_982, event_983, event_984, event_985, event_986, event_987, event_988, event_989
- Dates: 2024-11-06, 2024-11-27, 2024-12-18, 2025-01-08, 2025-01-29, 2025-02-19, 2025-03-12, 2025-04-02, 2025-04-23
- Descriptions: Bakery and snacks, Coffee shop, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Weekend food delivery
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`17` residual_days=`0`
- Latest/expected next: `2025-04-23` / `2025-05-14`
- Active as of request: `True`
- Amount: `1503635.49` from `event_987, event_988, event_989`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:education:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `education` / `debit` / `expense`
- Members: event_910, event_919, event_928, event_937, event_946
- Dates: 2024-12-10, 2025-01-10, 2025-02-10, 2025-03-10, 2025-04-10
- Descriptions: Child education fee
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`3`
- Latest/expected next: `2025-04-10` / `2025-05-10`
- Active as of request: `True`
- Amount: `2544100` from `event_928, event_937, event_946`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:entertainment:IDR:reducible:sequence:0`

- User/category/direction/type: `user_11` / `entertainment` / `debit` / `expense`
- Members: event_912, event_921, event_930, event_939, event_948
- Dates: 2024-12-16, 2025-01-16, 2025-02-16, 2025-03-16, 2025-04-16
- Descriptions: Games and recreation
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`16` residual_days=`3`
- Latest/expected next: `2025-04-16` / `2025-05-16`
- Active as of request: `True`
- Amount: `1674887.61` from `event_930, event_939, event_948`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:groceries:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `groceries` / `debit` / `expense`
- Members: event_950, event_951, event_952, event_953, event_954, event_955, event_956, event_957, event_958, event_959, event_960, event_961, event_962, event_963, event_964, event_965, event_966, event_967
- Dates: 2024-11-09, 2024-11-19, 2024-11-29, 2024-12-09, 2024-12-19, 2024-12-29, 2025-01-08, 2025-01-18, 2025-01-28, 2025-02-07, 2025-02-17, 2025-02-27, 2025-03-09, 2025-03-19, 2025-03-29, 2025-04-08, 2025-04-18, 2025-04-28
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`9` residual_days=`0`
- Latest/expected next: `2025-04-28` / `2025-05-08`
- Active as of request: `True`
- Amount: `1590529.64` from `event_965, event_966, event_967`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:healthcare:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `healthcare` / `debit` / `expense`
- Members: event_911, event_920, event_929, event_938, event_947
- Dates: 2024-12-12, 2025-01-12, 2025-02-12, 2025-03-12, 2025-04-12
- Descriptions: Regular medicine purchase
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`3`
- Latest/expected next: `2025-04-12` / `2025-05-12`
- Active as of request: `True`
- Amount: `3165638.3` from `event_929, event_938, event_947`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:housing:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `housing` / `debit` / `expense`
- Members: event_907, event_916, event_925, event_934, event_943
- Dates: 2024-12-05, 2025-01-05, 2025-02-05, 2025-03-05, 2025-04-05
- Descriptions: Home association fee
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`3`
- Latest/expected next: `2025-04-05` / `2025-05-05`
- Active as of request: `True`
- Amount: `2954500` from `event_925, event_934, event_943`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:insurance:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `insurance` / `debit` / `expense`
- Members: event_909, event_918, event_927, event_936, event_945
- Dates: 2024-12-09, 2025-01-09, 2025-02-09, 2025-03-09, 2025-04-09
- Descriptions: Vehicle insurance premium
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`3`
- Latest/expected next: `2025-04-09` / `2025-05-09`
- Active as of request: `True`
- Amount: `1881000` from `event_927, event_936, event_945`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:transport:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `transport` / `debit` / `expense`
- Members: event_968, event_969, event_970, event_971, event_972, event_973, event_974, event_975, event_976, event_977, event_978, event_979, event_980
- Dates: 2024-11-10, 2024-11-24, 2024-12-08, 2024-12-22, 2025-01-05, 2025-01-19, 2025-02-02, 2025-02-16, 2025-03-02, 2025-03-16, 2025-03-30, 2025-04-13, 2025-04-27
- Descriptions: Local taxi, Metro and bus fares, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`0` residual_days=`0`
- Latest/expected next: `2025-04-27` / `2025-05-11`
- Active as of request: `True`
- Amount: `1244835.69` from `event_978, event_979, event_980`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:expense:debit:utilities:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `utilities` / `debit` / `expense`
- Members: event_908, event_917, event_926, event_935, event_944
- Dates: 2024-12-08, 2025-01-08, 2025-02-08, 2025-03-08, 2025-04-08
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`3`
- Latest/expected next: `2025-04-08` / `2025-05-08`
- Active as of request: `True`
- Amount: `2796165.18` from `event_926, event_935, event_944`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:income:credit:salary:IDR:fixed:sequence:0`

- User/category/direction/type: `user_11` / `salary` / `credit` / `income`
- Members: event_905, event_914, event_923, event_932, event_941
- Dates: 2024-12-15, 2025-01-15, 2025-02-15, 2025-03-15, 2025-04-15
- Descriptions: Base salary
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`3`
- Latest/expected next: `2025-04-15` / `2025-05-15`
- Active as of request: `True`
- Amount: `23256000` from `event_923, event_932, event_941`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:income:credit:salary:IDR:fixed:sequence:1`

- User/category/direction/type: `user_11` / `salary` / `credit` / `income`
- Members: event_906, event_915, event_924, event_933, event_942
- Dates: 2024-12-24, 2025-01-24, 2025-02-24, 2025-03-24, 2025-04-24
- Descriptions: Monthly sales commission, Performance commission
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`24` residual_days=`3`
- Latest/expected next: `2025-04-24` / `2025-05-24`
- Active as of request: `True`
- Amount: `20012106.46` from `event_924, event_933, event_942`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_11:subscription:debit:cloud_storage:IDR:stoppable:sequence:0`

- User/category/direction/type: `user_11` / `cloud_storage` / `debit` / `subscription`
- Members: event_913, event_922, event_931, event_940, event_949
- Dates: 2024-12-14, 2025-01-14, 2025-02-14, 2025-03-14, 2025-04-14
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`3`
- Latest/expected next: `2025-04-14` / `2025-05-14`
- Active as of request: `True`
- Amount: `168150` from `event_931, event_940, event_949`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:expense:debit:dining:ZAR:reducible:sequence:0`

- User/category/direction/type: `user_12` / `dining` / `debit` / `expense`
- Members: event_1046, event_1047, event_1048, event_1049, event_1050, event_1051, event_1052, event_1053, event_1054
- Dates: 2025-10-11, 2025-11-01, 2025-11-22, 2025-12-13, 2026-01-03, 2026-01-24, 2026-02-14, 2026-03-07, 2026-03-28
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Takeaway order
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`20` residual_days=`0`
- Latest/expected next: `2026-03-28` / `2026-04-18`
- Active as of request: `True`
- Amount: `2089.92` from `event_1052, event_1053, event_1054`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:expense:debit:groceries:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_12` / `groceries` / `debit` / `expense`
- Members: event_1019, event_1020, event_1021, event_1022, event_1023, event_1024, event_1025, event_1026, event_1027, event_1028, event_1029, event_1030, event_1031, event_1032, event_1033, event_1034, event_1035, event_1036
- Dates: 2025-10-09, 2025-10-19, 2025-10-29, 2025-11-08, 2025-11-18, 2025-11-28, 2025-12-08, 2025-12-18, 2025-12-28, 2026-01-07, 2026-01-17, 2026-01-27, 2026-02-06, 2026-02-16, 2026-02-26, 2026-03-08, 2026-03-18, 2026-03-28
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2026-03-28` / `2026-04-07`
- Active as of request: `True`
- Amount: `2469.4` from `event_1034, event_1035, event_1036`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:expense:debit:rent:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_12` / `rent` / `debit` / `expense`
- Members: event_991, event_997, event_1003, event_1008, event_1013, event_1018
- Dates: 2025-11-01, 2025-12-01, 2026-01-01, 2026-02-01, 2026-03-01, 2026-04-01
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`1` residual_days=`3`
- Latest/expected next: `2026-04-01` / `2026-05-01`
- Active as of request: `True`
- Amount: `11792` from `event_1008, event_1013, event_1018`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:expense:debit:shopping:ZAR:reducible:sequence:0`

- User/category/direction/type: `user_12` / `shopping` / `debit` / `expense`
- Members: event_995, event_1001, event_1007, event_1012, event_1017
- Dates: 2025-11-11, 2025-12-11, 2026-01-11, 2026-02-11, 2026-03-11
- Descriptions: Monthly shopping spend
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`3`
- Latest/expected next: `2026-03-11` / `2026-04-11`
- Active as of request: `True`
- Amount: `1401.99` from `event_1007, event_1012, event_1017`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:expense:debit:transport:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_12` / `transport` / `debit` / `expense`
- Members: event_1037, event_1038, event_1039, event_1040, event_1041, event_1042, event_1043, event_1044, event_1045
- Dates: 2025-10-10, 2025-10-31, 2025-11-21, 2025-12-12, 2026-01-02, 2026-01-23, 2026-02-13, 2026-03-06, 2026-03-27
- Descriptions: Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Vehicle charging
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`19` residual_days=`0`
- Latest/expected next: `2026-03-27` / `2026-04-17`
- Active as of request: `True`
- Amount: `1684.28` from `event_1043, event_1044, event_1045`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:expense:debit:utilities:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_12` / `utilities` / `debit` / `expense`
- Members: event_992, event_998, event_1004, event_1009, event_1014
- Dates: 2025-11-05, 2025-12-05, 2026-01-05, 2026-02-05, 2026-03-05
- Descriptions: Water and power payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`3`
- Latest/expected next: `2026-03-05` / `2026-04-05`
- Active as of request: `True`
- Amount: `3755.96` from `event_1004, event_1009, event_1014`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:income:credit:salary:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_12` / `salary` / `credit` / `income`
- Members: event_990, event_996, event_1002
- Dates: 2025-11-15, 2025-12-15, 2026-01-15
- Descriptions: Seasonal contract payment, Temporary assignment pay
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2026-01-15` / `2026-02-15`
- Active as of request: `False`
- Amount: `61315.12` from `event_990, event_996, event_1002`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:subscription:debit:cloud_storage:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_12` / `cloud_storage` / `debit` / `subscription`
- Members: event_993, event_999, event_1005, event_1010, event_1015
- Dates: 2025-11-11, 2025-12-11, 2026-01-11, 2026-02-11, 2026-03-11
- Descriptions: Shared storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`3`
- Latest/expected next: `2026-03-11` / `2026-04-11`
- Active as of request: `True`
- Amount: `447.7` from `event_1005, event_1010, event_1015`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_12:subscription:debit:streaming:ZAR:stoppable:sequence:0`

- User/category/direction/type: `user_12` / `streaming` / `debit` / `subscription`
- Members: event_994, event_1000, event_1006, event_1011, event_1016
- Dates: 2025-11-08, 2025-12-08, 2026-01-08, 2026-02-08, 2026-03-08
- Descriptions: Family streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`3`
- Latest/expected next: `2026-03-08` / `2026-04-08`
- Active as of request: `True`
- Amount: `1504.8` from `event_1006, event_1011, event_1016`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:expense:debit:dining:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `dining` / `debit` / `expense`
- Members: event_1148, event_1149, event_1150, event_1151, event_1152, event_1153, event_1154, event_1155, event_1156, event_1157, event_1158, event_1159, event_1160
- Dates: 2023-09-14, 2023-09-28, 2023-10-12, 2023-10-26, 2023-11-09, 2023-11-23, 2023-12-07, 2023-12-21, 2024-01-04, 2024-01-18, 2024-02-01, 2024-02-15, 2024-02-29
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`11` residual_days=`0`
- Latest/expected next: `2024-02-29` / `2024-03-14`
- Active as of request: `True`
- Amount: `61.28` from `event_1158, event_1159, event_1160`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:expense:debit:entertainment:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `entertainment` / `debit` / `expense`
- Members: event_1062, event_1070, event_1078, event_1086, event_1093
- Dates: 2023-10-14, 2023-11-14, 2023-12-14, 2024-01-14, 2024-02-14
- Descriptions: Local event tickets
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2024-02-14` / `2024-03-14`
- Active as of request: `True`
- Amount: `37.9` from `event_1078, event_1086, event_1093`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `groceries` / `debit` / `expense`
- Members: event_1096, event_1097, event_1098, event_1099, event_1100, event_1101, event_1102, event_1103, event_1104, event_1105, event_1106, event_1107, event_1108, event_1109, event_1110, event_1111, event_1112, event_1113, event_1114, event_1115, event_1116, event_1117, event_1118, event_1119, event_1120, event_1121
- Dates: 2023-09-12, 2023-09-19, 2023-09-26, 2023-10-03, 2023-10-10, 2023-10-17, 2023-10-24, 2023-10-31, 2023-11-07, 2023-11-14, 2023-11-21, 2023-11-28, 2023-12-05, 2023-12-12, 2023-12-19, 2023-12-26, 2024-01-02, 2024-01-09, 2024-01-16, 2024-01-23, 2024-01-30, 2024-02-06, 2024-02-13, 2024-02-20, 2024-02-27, 2024-03-05
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2024-03-05` / `2024-03-12`
- Active as of request: `True`
- Amount: `118.36` from `event_1119, event_1120, event_1121`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `rent` / `debit` / `expense`
- Members: event_1057, event_1065, event_1073, event_1081, event_1088, event_1094
- Dates: 2023-10-02, 2023-11-02, 2023-12-02, 2024-01-02, 2024-02-02, 2024-03-02
- Descriptions: Shared housing rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`2`
- Latest/expected next: `2024-03-02` / `2024-04-02`
- Active as of request: `True`
- Amount: `622.6` from `event_1081, event_1088, event_1094`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `transport` / `debit` / `expense`
- Members: event_1122, event_1123, event_1124, event_1125, event_1126, event_1127, event_1128, event_1129, event_1130, event_1131, event_1132, event_1133, event_1134, event_1135, event_1136, event_1137, event_1138, event_1139, event_1140, event_1141, event_1142, event_1143, event_1144, event_1145, event_1146, event_1147
- Dates: 2023-09-13, 2023-09-20, 2023-09-27, 2023-10-04, 2023-10-11, 2023-10-18, 2023-10-25, 2023-11-01, 2023-11-08, 2023-11-15, 2023-11-22, 2023-11-29, 2023-12-06, 2023-12-13, 2023-12-20, 2023-12-27, 2024-01-03, 2024-01-10, 2024-01-17, 2024-01-24, 2024-01-31, 2024-02-07, 2024-02-14, 2024-02-21, 2024-02-28, 2024-03-06
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2024-03-06` / `2024-03-13`
- Active as of request: `True`
- Amount: `50.46` from `event_1145, event_1146, event_1147`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `utilities` / `debit` / `expense`
- Members: event_1058, event_1066, event_1074, event_1082, event_1089, event_1095
- Dates: 2023-10-06, 2023-11-06, 2023-12-06, 2024-01-06, 2024-02-06, 2024-03-06
- Descriptions: Water and power payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`2`
- Latest/expected next: `2024-03-06` / `2024-04-06`
- Active as of request: `True`
- Amount: `143.7` from `event_1082, event_1089, event_1095`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:income:credit:salary:EUR:fixed:sequence:0`

- User/category/direction/type: `user_13` / `salary` / `credit` / `income`
- Members: event_1055, event_1063, event_1071, event_1079, event_1087
- Dates: 2023-10-15, 2023-11-15, 2023-12-15, 2024-01-15, 2024-02-15
- Descriptions: Primary household salary
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-02-15` / `2024-03-15`
- Active as of request: `True`
- Amount: `1343.54` from `event_1071, event_1079, event_1087`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:income:credit:salary:EUR:fixed:sequence:1`

- User/category/direction/type: `user_13` / `salary` / `credit` / `income`
- Members: event_1056, event_1064, event_1072, event_1080
- Dates: 2023-10-20, 2023-11-20, 2023-12-20, 2024-01-20
- Descriptions: Second household income
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`20` residual_days=`1`
- Latest/expected next: `2024-01-20` / `2024-02-20`
- Active as of request: `False`
- Amount: `948.46` from `event_1064, event_1072, event_1080`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:subscription:debit:delivery_membership:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_13` / `delivery_membership` / `debit` / `subscription`
- Members: event_1060, event_1068, event_1076, event_1084, event_1091
- Dates: 2023-10-13, 2023-11-13, 2023-12-13, 2024-01-13, 2024-02-13
- Descriptions: Delivery service plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2024-02-13` / `2024-03-13`
- Active as of request: `True`
- Amount: `21` from `event_1076, event_1084, event_1091`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:subscription:debit:gym:EUR:reducible:sequence:0`

- User/category/direction/type: `user_13` / `gym` / `debit` / `subscription`
- Members: event_1061, event_1069, event_1077, event_1085, event_1092
- Dates: 2023-10-10, 2023-11-10, 2023-12-10, 2024-01-10, 2024-02-10
- Descriptions: Community fitness plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2024-02-10` / `2024-03-10`
- Active as of request: `True`
- Amount: `61` from `event_1077, event_1085, event_1092`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_13:subscription:debit:music_subscription:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_13` / `music_subscription` / `debit` / `subscription`
- Members: event_1059, event_1067, event_1075, event_1083, event_1090
- Dates: 2023-10-11, 2023-11-11, 2023-12-11, 2024-01-11, 2024-02-11
- Descriptions: Music subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2024-02-11` / `2024-03-11`
- Active as of request: `True`
- Amount: `29` from `event_1075, event_1083, event_1090`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:debt_payment:debit:debt_repayment:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_1165, event_1173, event_1180, event_1187, event_1195
- Dates: 2025-03-12, 2025-04-12, 2025-05-12, 2025-06-12, 2025-07-12
- Descriptions: Credit card repayment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2025-07-12` / `2025-08-12`
- Active as of request: `True`
- Amount: `350` from `event_1180, event_1187, event_1195`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:family_support:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `family_support` / `debit` / `expense`
- Members: event_1167, event_1175, event_1182, event_1189, event_1197
- Dates: 2025-03-14, 2025-04-14, 2025-05-14, 2025-06-14, 2025-07-14
- Descriptions: Family support payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2025-07-14` / `2025-08-14`
- Active as of request: `True`
- Amount: `226` from `event_1182, event_1189, event_1197`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `groceries` / `debit` / `expense`
- Members: event_1201, event_1202, event_1203, event_1204, event_1205, event_1206, event_1207, event_1208, event_1209, event_1210, event_1211, event_1212, event_1213, event_1214, event_1215, event_1216, event_1217, event_1218, event_1219, event_1220, event_1221, event_1222, event_1223, event_1224, event_1225, event_1226
- Dates: 2025-02-09, 2025-02-16, 2025-02-23, 2025-03-02, 2025-03-09, 2025-03-16, 2025-03-23, 2025-03-30, 2025-04-06, 2025-04-13, 2025-04-20, 2025-04-27, 2025-05-04, 2025-05-11, 2025-05-18, 2025-05-25, 2025-06-01, 2025-06-08, 2025-06-15, 2025-06-22, 2025-06-29, 2025-07-06, 2025-07-13, 2025-07-20, 2025-07-27, 2025-08-03
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`0` residual_days=`0`
- Latest/expected next: `2025-08-03` / `2025-08-10`
- Active as of request: `True`
- Amount: `129.56` from `event_1224, event_1225, event_1226`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:healthcare:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `healthcare` / `debit` / `expense`
- Members: event_1166, event_1174, event_1181, event_1188, event_1196
- Dates: 2025-03-11, 2025-04-11, 2025-05-11, 2025-06-11, 2025-07-11
- Descriptions: Family healthcare expense
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2025-07-11` / `2025-08-11`
- Active as of request: `True`
- Amount: `95.17` from `event_1181, event_1188, event_1196`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `rent` / `debit` / `expense`
- Members: event_1163, event_1171, event_1178, event_1185, event_1193, event_1200
- Dates: 2025-03-03, 2025-04-03, 2025-05-03, 2025-06-03, 2025-07-03, 2025-08-03
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`3` residual_days=`1`
- Latest/expected next: `2025-08-03` / `2025-09-03`
- Active as of request: `True`
- Amount: `688.6` from `event_1185, event_1193, event_1200`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:shopping:EUR:reducible:sequence:0`

- User/category/direction/type: `user_14` / `shopping` / `debit` / `expense`
- Members: event_1169, event_1177, event_1184, event_1191, event_1199
- Dates: 2025-03-13, 2025-04-13, 2025-05-13, 2025-06-13, 2025-07-13
- Descriptions: Online retail purchases
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-07-13` / `2025-08-13`
- Active as of request: `True`
- Amount: `140.39` from `event_1184, event_1191, event_1199`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `transport` / `debit` / `expense`
- Members: event_1227, event_1228, event_1229, event_1230, event_1231, event_1232, event_1233, event_1234, event_1235, event_1236, event_1237, event_1238, event_1239
- Dates: 2025-02-10, 2025-02-24, 2025-03-10, 2025-03-24, 2025-04-07, 2025-04-21, 2025-05-05, 2025-05-19, 2025-06-02, 2025-06-16, 2025-06-30, 2025-07-14, 2025-07-28
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`8` residual_days=`0`
- Latest/expected next: `2025-07-28` / `2025-08-11`
- Active as of request: `True`
- Amount: `62.3` from `event_1237, event_1238, event_1239`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_14` / `utilities` / `debit` / `expense`
- Members: event_1164, event_1172, event_1179, event_1186, event_1194
- Dates: 2025-03-07, 2025-04-07, 2025-05-07, 2025-06-07, 2025-07-07
- Descriptions: Energy provider bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2025-07-07` / `2025-08-07`
- Active as of request: `True`
- Amount: `153.69` from `event_1179, event_1186, event_1194`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_14:subscription:debit:cloud_storage:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_14` / `cloud_storage` / `debit` / `subscription`
- Members: event_1168, event_1176, event_1183, event_1190, event_1198
- Dates: 2025-03-13, 2025-04-13, 2025-05-13, 2025-06-13, 2025-07-13
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-07-13` / `2025-08-13`
- Active as of request: `True`
- Amount: `14` from `event_1183, event_1190, event_1198`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:debt_payment:debit:debt_repayment:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_1243, event_1249, event_1255, event_1262, event_1269
- Dates: 2025-08-13, 2025-09-13, 2025-10-13, 2025-11-13, 2025-12-13
- Descriptions: Credit card repayment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-12-13` / `2026-01-13`
- Active as of request: `True`
- Amount: `84` from `event_1255, event_1262, event_1269`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:expense:debit:dining:EUR:reducible:sequence:0`

- User/category/direction/type: `user_15` / `dining` / `debit` / `expense`
- Members: event_1323, event_1324, event_1325, event_1326, event_1327, event_1328, event_1329, event_1330, event_1331, event_1332, event_1333, event_1334, event_1335
- Dates: 2025-07-12, 2025-07-26, 2025-08-09, 2025-08-23, 2025-09-06, 2025-09-20, 2025-10-04, 2025-10-18, 2025-11-01, 2025-11-15, 2025-11-29, 2025-12-13, 2025-12-27
- Descriptions: Bakery and snacks, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2025-12-27` / `2026-01-10`
- Active as of request: `True`
- Amount: `49.35` from `event_1333, event_1334, event_1335`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:expense:debit:education:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `education` / `debit` / `expense`
- Members: event_1242, event_1248, event_1254, event_1261, event_1268
- Dates: 2025-08-10, 2025-09-10, 2025-10-10, 2025-11-10, 2025-12-10
- Descriptions: School fee payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2025-12-10` / `2026-01-10`
- Active as of request: `True`
- Amount: `159` from `event_1254, event_1261, event_1268`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `groceries` / `debit` / `expense`
- Members: event_1273, event_1274, event_1275, event_1276, event_1277, event_1278, event_1279, event_1280, event_1281, event_1282, event_1283, event_1284, event_1285, event_1286, event_1287, event_1288, event_1289, event_1290, event_1291, event_1292, event_1293, event_1294, event_1295, event_1296, event_1297
- Dates: 2025-07-15, 2025-07-22, 2025-07-29, 2025-08-05, 2025-08-12, 2025-08-19, 2025-08-26, 2025-09-02, 2025-09-09, 2025-09-16, 2025-09-23, 2025-09-30, 2025-10-07, 2025-10-14, 2025-10-21, 2025-10-28, 2025-11-04, 2025-11-11, 2025-11-18, 2025-11-25, 2025-12-02, 2025-12-09, 2025-12-16, 2025-12-23, 2025-12-30
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2025-12-30` / `2026-01-06`
- Active as of request: `True`
- Amount: `64.42` from `event_1295, event_1296, event_1297`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `rent` / `debit` / `expense`
- Members: event_1240, event_1246, event_1252, event_1259, event_1266, event_1272
- Dates: 2025-08-04, 2025-09-04, 2025-10-04, 2025-11-04, 2025-12-04, 2026-01-04
- Descriptions: Landlord standing order
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`1`
- Latest/expected next: `2026-01-04` / `2026-02-04`
- Active as of request: `True`
- Amount: `435.6` from `event_1259, event_1266, event_1272`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `transport` / `debit` / `expense`
- Members: event_1298, event_1299, event_1300, event_1301, event_1302, event_1303, event_1304, event_1305, event_1306, event_1307, event_1308, event_1309, event_1310, event_1311, event_1312, event_1313, event_1314, event_1315, event_1316, event_1317, event_1318, event_1319, event_1320, event_1321, event_1322
- Dates: 2025-07-16, 2025-07-23, 2025-07-30, 2025-08-06, 2025-08-13, 2025-08-20, 2025-08-27, 2025-09-03, 2025-09-10, 2025-09-17, 2025-09-24, 2025-10-01, 2025-10-08, 2025-10-15, 2025-10-22, 2025-10-29, 2025-11-05, 2025-11-12, 2025-11-19, 2025-11-26, 2025-12-03, 2025-12-10, 2025-12-17, 2025-12-24, 2025-12-31
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2025-12-31` / `2026-01-07`
- Active as of request: `True`
- Amount: `36.86` from `event_1320, event_1321, event_1322`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `utilities` / `debit` / `expense`
- Members: event_1241, event_1247, event_1253, event_1260, event_1267
- Dates: 2025-08-08, 2025-09-08, 2025-10-08, 2025-11-08, 2025-12-08
- Descriptions: Energy provider bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2025-12-08` / `2026-01-08`
- Active as of request: `True`
- Amount: `90.39` from `event_1253, event_1260, event_1267`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:subscription:debit:delivery_membership:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `delivery_membership` / `debit` / `subscription`
- Members: event_1245, event_1251, event_1257, event_1264, event_1271
- Dates: 2025-08-15, 2025-09-15, 2025-10-15, 2025-11-15, 2025-12-15
- Descriptions: Food delivery membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-12-15` / `2026-01-15`
- Active as of request: `True`
- Amount: `27` from `event_1257, event_1264, event_1271`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_15:subscription:debit:music_subscription:EUR:fixed:sequence:0`

- User/category/direction/type: `user_15` / `music_subscription` / `debit` / `subscription`
- Members: event_1244, event_1250, event_1256, event_1263, event_1270
- Dates: 2025-08-13, 2025-09-13, 2025-10-13, 2025-11-13, 2025-12-13
- Descriptions: Music subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-12-13` / `2026-01-13`
- Active as of request: `True`
- Amount: `11` from `event_1256, event_1263, event_1270`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:debt_payment:debit:debt_repayment:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_1339, event_1346, event_1353, event_1360, event_1367, event_1373
- Dates: 2023-03-10, 2023-04-10, 2023-05-10, 2023-06-10, 2023-07-10, 2023-08-10
- Descriptions: Vehicle loan payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`1`
- Latest/expected next: `2023-08-10` / `2023-09-10`
- Active as of request: `True`
- Amount: `17750` from `event_1360, event_1367, event_1373`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:expense:debit:dining:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `dining` / `debit` / `expense`
- Members: event_1429, event_1430, event_1431, event_1432, event_1433, event_1434, event_1435, event_1436, event_1437, event_1438, event_1439, event_1440, event_1441
- Dates: 2023-02-17, 2023-03-03, 2023-03-17, 2023-03-31, 2023-04-14, 2023-04-28, 2023-05-12, 2023-05-26, 2023-06-09, 2023-06-23, 2023-07-07, 2023-07-21, 2023-08-04
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`12` residual_days=`0`
- Latest/expected next: `2023-08-04` / `2023-08-18`
- Active as of request: `True`
- Amount: `6354.26` from `event_1439, event_1440, event_1441`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `groceries` / `debit` / `expense`
- Members: event_1377, event_1378, event_1379, event_1380, event_1381, event_1382, event_1383, event_1384, event_1385, event_1386, event_1387, event_1388, event_1389, event_1390, event_1391, event_1392, event_1393, event_1394, event_1395, event_1396, event_1397, event_1398, event_1399, event_1400, event_1401, event_1402
- Dates: 2023-02-15, 2023-02-22, 2023-03-01, 2023-03-08, 2023-03-15, 2023-03-22, 2023-03-29, 2023-04-05, 2023-04-12, 2023-04-19, 2023-04-26, 2023-05-03, 2023-05-10, 2023-05-17, 2023-05-24, 2023-05-31, 2023-06-07, 2023-06-14, 2023-06-21, 2023-06-28, 2023-07-05, 2023-07-12, 2023-07-19, 2023-07-26, 2023-08-02, 2023-08-09
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2023-08-09` / `2023-08-16`
- Active as of request: `True`
- Amount: `8883.15` from `event_1400, event_1401, event_1402`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:expense:debit:rent:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `rent` / `debit` / `expense`
- Members: event_1337, event_1344, event_1351, event_1358, event_1365, event_1371
- Dates: 2023-03-01, 2023-04-01, 2023-05-01, 2023-06-01, 2023-07-01, 2023-08-01
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`1` residual_days=`1`
- Latest/expected next: `2023-08-01` / `2023-09-01`
- Active as of request: `True`
- Amount: `57100` from `event_1358, event_1365, event_1371`
- Excluded outliers: `event_1442`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:expense:debit:shopping:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `shopping` / `debit` / `expense`
- Members: event_1342, event_1349, event_1356, event_1363, event_1370, event_1376
- Dates: 2023-03-11, 2023-04-11, 2023-05-11, 2023-06-11, 2023-07-11, 2023-08-11
- Descriptions: Clothing and household items
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2023-08-11` / `2023-09-11`
- Active as of request: `True`
- Amount: `10178.56` from `event_1363, event_1370, event_1376`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `transport` / `debit` / `expense`
- Members: event_1403, event_1404, event_1405, event_1406, event_1407, event_1408, event_1409, event_1410, event_1411, event_1412, event_1413, event_1414, event_1415, event_1416, event_1417, event_1418, event_1419, event_1420, event_1421, event_1422, event_1423, event_1424, event_1425, event_1426, event_1427, event_1428
- Dates: 2023-02-16, 2023-02-23, 2023-03-02, 2023-03-09, 2023-03-16, 2023-03-23, 2023-03-30, 2023-04-06, 2023-04-13, 2023-04-20, 2023-04-27, 2023-05-04, 2023-05-11, 2023-05-18, 2023-05-25, 2023-06-01, 2023-06-08, 2023-06-15, 2023-06-22, 2023-06-29, 2023-07-06, 2023-07-13, 2023-07-20, 2023-07-27, 2023-08-03, 2023-08-10
- Descriptions: Commuter pass, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2023-08-10` / `2023-08-17`
- Active as of request: `True`
- Amount: `5368.95` from `event_1426, event_1427, event_1428`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `utilities` / `debit` / `expense`
- Members: event_1338, event_1345, event_1352, event_1359, event_1366, event_1372
- Dates: 2023-03-05, 2023-04-05, 2023-05-05, 2023-06-05, 2023-07-05, 2023-08-05
- Descriptions: Energy provider bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`1`
- Latest/expected next: `2023-08-05` / `2023-09-05`
- Active as of request: `True`
- Amount: `11512.87` from `event_1359, event_1366, event_1372`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `salary` / `credit` / `income`
- Members: event_1336, event_1343, event_1350, event_1357, event_1364
- Dates: 2023-03-15, 2023-04-15, 2023-05-15, 2023-06-15, 2023-07-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2023-07-15` / `2023-08-15`
- Active as of request: `True`
- Amount: `173000` from `event_1350, event_1357, event_1364`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:subscription:debit:cloud_storage:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `cloud_storage` / `debit` / `subscription`
- Members: event_1341, event_1348, event_1355, event_1362, event_1369, event_1375
- Dates: 2023-03-11, 2023-04-11, 2023-05-11, 2023-06-11, 2023-07-11, 2023-08-11
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2023-08-11` / `2023-09-11`
- Active as of request: `True`
- Amount: `1055` from `event_1362, event_1369, event_1375`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_16:subscription:debit:streaming:INR:fixed:sequence:0`

- User/category/direction/type: `user_16` / `streaming` / `debit` / `subscription`
- Members: event_1340, event_1347, event_1354, event_1361, event_1368, event_1374
- Dates: 2023-03-08, 2023-04-08, 2023-05-08, 2023-06-08, 2023-07-08, 2023-08-08
- Descriptions: Video streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2023-08-08` / `2023-09-08`
- Active as of request: `True`
- Amount: `3510` from `event_1361, event_1368, event_1374`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:debt_payment:debit:debt_repayment:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_1447, event_1454, event_1461, event_1468, event_1475
- Dates: 2025-10-11, 2025-11-11, 2025-12-11, 2026-01-11, 2026-02-11
- Descriptions: Credit card repayment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2026-02-11` / `2026-03-11`
- Active as of request: `True`
- Amount: `30200` from `event_1461, event_1468, event_1475`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:expense:debit:dining:INR:reducible:sequence:0`

- User/category/direction/type: `user_17` / `dining` / `debit` / `expense`
- Members: event_1530, event_1531, event_1532, event_1533, event_1534, event_1535, event_1536, event_1537, event_1538, event_1539, event_1540, event_1541, event_1542
- Dates: 2025-09-07, 2025-09-21, 2025-10-05, 2025-10-19, 2025-11-02, 2025-11-16, 2025-11-30, 2025-12-14, 2025-12-28, 2026-01-11, 2026-01-25, 2026-02-08, 2026-02-22
- Descriptions: Bakery and snacks, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`7` residual_days=`0`
- Latest/expected next: `2026-02-22` / `2026-03-08`
- Active as of request: `True`
- Amount: `6688.81` from `event_1540, event_1541, event_1542`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:expense:debit:education:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `education` / `debit` / `expense`
- Members: event_1446, event_1453, event_1460, event_1467, event_1474
- Dates: 2025-10-08, 2025-11-08, 2025-12-08, 2026-01-08, 2026-02-08
- Descriptions: Course tuition
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2026-02-08` / `2026-03-08`
- Active as of request: `True`
- Amount: `13660` from `event_1460, event_1467, event_1474`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `groceries` / `debit` / `expense`
- Members: event_1478, event_1479, event_1480, event_1481, event_1482, event_1483, event_1484, event_1485, event_1486, event_1487, event_1488, event_1489, event_1490, event_1491, event_1492, event_1493, event_1494, event_1495, event_1496, event_1497, event_1498, event_1499, event_1500, event_1501, event_1502, event_1503, event_1545
- Dates: 2025-09-05, 2025-09-12, 2025-09-19, 2025-09-26, 2025-10-03, 2025-10-10, 2025-10-17, 2025-10-24, 2025-10-31, 2025-11-07, 2025-11-14, 2025-11-21, 2025-11-28, 2025-12-05, 2025-12-12, 2025-12-19, 2025-12-26, 2026-01-02, 2026-01-09, 2026-01-16, 2026-01-23, 2026-01-30, 2026-02-06, 2026-02-13, 2026-02-20, 2026-02-27, 2026-02-27
- Descriptions: Bulk groceries and pantry purchase, Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`5` residual_days=`7`
- Latest/expected next: `2026-02-27` / `2026-03-06`
- Active as of request: `True`
- Amount: `41272` from `event_1502, event_1503, event_1545`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:expense:debit:rent:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `rent` / `debit` / `expense`
- Members: event_1444, event_1451, event_1458, event_1465, event_1472
- Dates: 2025-10-02, 2025-11-02, 2025-12-02, 2026-01-02, 2026-02-02
- Descriptions: Apartment rent transfer
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`1`
- Latest/expected next: `2026-02-02` / `2026-03-02`
- Active as of request: `True`
- Amount: `49600` from `event_1458, event_1465, event_1472`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `transport` / `debit` / `expense`
- Members: event_1504, event_1505, event_1506, event_1507, event_1508, event_1509, event_1510, event_1511, event_1512, event_1513, event_1514, event_1515, event_1516, event_1517, event_1518, event_1519, event_1520, event_1521, event_1522, event_1523, event_1524, event_1525, event_1526, event_1527, event_1528, event_1529
- Dates: 2025-09-06, 2025-09-13, 2025-09-20, 2025-09-27, 2025-10-04, 2025-10-11, 2025-10-18, 2025-10-25, 2025-11-01, 2025-11-08, 2025-11-15, 2025-11-22, 2025-11-29, 2025-12-06, 2025-12-13, 2025-12-20, 2025-12-27, 2026-01-03, 2026-01-10, 2026-01-17, 2026-01-24, 2026-01-31, 2026-02-07, 2026-02-14, 2026-02-21, 2026-02-28
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2026-02-28` / `2026-03-07`
- Active as of request: `True`
- Amount: `5741.08` from `event_1527, event_1528, event_1529`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `utilities` / `debit` / `expense`
- Members: event_1445, event_1452, event_1459, event_1466, event_1473
- Dates: 2025-10-06, 2025-11-06, 2025-12-06, 2026-01-06, 2026-02-06
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`1`
- Latest/expected next: `2026-02-06` / `2026-03-06`
- Active as of request: `True`
- Amount: `10246.53` from `event_1459, event_1466, event_1473`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_17` / `salary` / `credit` / `income`
- Members: event_1443, event_1450, event_1457, event_1464, event_1471
- Dates: 2025-10-15, 2025-11-15, 2025-12-15, 2026-01-15, 2026-02-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2026-02-15` / `2026-03-15`
- Active as of request: `True`
- Amount: `206000` from `event_1457, event_1464, event_1471`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:subscription:debit:delivery_membership:INR:stoppable:sequence:0`

- User/category/direction/type: `user_17` / `delivery_membership` / `debit` / `subscription`
- Members: event_1449, event_1456, event_1463, event_1470, event_1477
- Dates: 2025-10-13, 2025-11-13, 2025-12-13, 2026-01-13, 2026-02-13
- Descriptions: Food delivery membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2026-02-13` / `2026-03-13`
- Active as of request: `True`
- Amount: `1675` from `event_1463, event_1470, event_1477`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_17:subscription:debit:music_subscription:INR:stoppable:sequence:0`

- User/category/direction/type: `user_17` / `music_subscription` / `debit` / `subscription`
- Members: event_1448, event_1455, event_1462, event_1469, event_1476
- Dates: 2025-10-11, 2025-11-11, 2025-12-11, 2026-01-11, 2026-02-11
- Descriptions: Music subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2026-02-11` / `2026-03-11`
- Active as of request: `True`
- Amount: `2055` from `event_1462, event_1469, event_1476`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:dining:EUR:reducible:sequence:0`

- User/category/direction/type: `user_18` / `dining` / `debit` / `expense`
- Members: event_1609, event_1610, event_1611, event_1612, event_1613, event_1614, event_1615, event_1616, event_1617, event_1618, event_1619, event_1620, event_1621
- Dates: 2026-01-14, 2026-01-28, 2026-02-11, 2026-02-25, 2026-03-11, 2026-03-25, 2026-04-08, 2026-04-22, 2026-05-06, 2026-05-20, 2026-06-03, 2026-06-17, 2026-07-01
- Descriptions: Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`10` residual_days=`0`
- Latest/expected next: `2026-07-01` / `2026-07-15`
- Active as of request: `True`
- Amount: `101.88` from `event_1619, event_1620, event_1621`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `groceries` / `debit` / `expense`
- Members: event_1578, event_1579, event_1580, event_1581, event_1582, event_1583, event_1584, event_1585, event_1586, event_1587, event_1588, event_1589, event_1590, event_1591, event_1592, event_1593, event_1594, event_1595
- Dates: 2026-01-12, 2026-01-22, 2026-02-01, 2026-02-11, 2026-02-21, 2026-03-03, 2026-03-13, 2026-03-23, 2026-04-02, 2026-04-12, 2026-04-22, 2026-05-02, 2026-05-12, 2026-05-22, 2026-06-01, 2026-06-11, 2026-06-21, 2026-07-01
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`8` residual_days=`0`
- Latest/expected next: `2026-07-01` / `2026-07-11`
- Active as of request: `True`
- Amount: `111.41` from `event_1593, event_1594, event_1595`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:healthcare:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `healthcare` / `debit` / `expense`
- Members: event_1551, event_1557, event_1563, event_1569, event_1575
- Dates: 2026-02-11, 2026-03-11, 2026-04-11, 2026-05-11, 2026-06-11
- Descriptions: Clinic payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`3`
- Latest/expected next: `2026-06-11` / `2026-07-11`
- Active as of request: `True`
- Amount: `162.41` from `event_1563, event_1569, event_1575`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:housing:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `housing` / `debit` / `expense`
- Members: event_1548, event_1554, event_1560, event_1566, event_1572, event_1577
- Dates: 2026-02-04, 2026-03-04, 2026-04-04, 2026-05-04, 2026-06-04, 2026-07-04
- Descriptions: Building maintenance payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`3`
- Latest/expected next: `2026-07-04` / `2026-08-04`
- Active as of request: `True`
- Amount: `167` from `event_1566, event_1572, event_1577`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:insurance:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `insurance` / `debit` / `expense`
- Members: event_1550, event_1556, event_1562, event_1568, event_1574
- Dates: 2026-02-08, 2026-03-08, 2026-04-08, 2026-05-08, 2026-06-08
- Descriptions: Household insurance
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`3`
- Latest/expected next: `2026-06-08` / `2026-07-08`
- Active as of request: `True`
- Amount: `68` from `event_1562, event_1568, event_1574`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `transport` / `debit` / `expense`
- Members: event_1596, event_1597, event_1598, event_1599, event_1600, event_1601, event_1602, event_1603, event_1604, event_1605, event_1606, event_1607, event_1608
- Dates: 2026-01-13, 2026-01-27, 2026-02-10, 2026-02-24, 2026-03-10, 2026-03-24, 2026-04-07, 2026-04-21, 2026-05-05, 2026-05-19, 2026-06-02, 2026-06-16, 2026-06-30
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`9` residual_days=`0`
- Latest/expected next: `2026-06-30` / `2026-07-14`
- Active as of request: `True`
- Amount: `49.04` from `event_1606, event_1607, event_1608`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `utilities` / `debit` / `expense`
- Members: event_1549, event_1555, event_1561, event_1567, event_1573
- Dates: 2026-02-07, 2026-03-07, 2026-04-07, 2026-05-07, 2026-06-07
- Descriptions: Energy provider bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`3`
- Latest/expected next: `2026-06-07` / `2026-07-07`
- Active as of request: `True`
- Amount: `125.4` from `event_1561, event_1567, event_1573`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:income:credit:salary:EUR:fixed:sequence:0`

- User/category/direction/type: `user_18` / `salary` / `credit` / `income`
- Members: event_1547, event_1553, event_1559, event_1565, event_1571
- Dates: 2026-02-15, 2026-03-15, 2026-04-15, 2026-05-15, 2026-06-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`3`
- Latest/expected next: `2026-06-15` / `2026-07-15`
- Active as of request: `True`
- Amount: `2310` from `event_1559, event_1565, event_1571`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_18:subscription:debit:streaming:EUR:reducible_or_stoppable:sequence:0`

- User/category/direction/type: `user_18` / `streaming` / `debit` / `subscription`
- Members: event_1552, event_1558, event_1564, event_1570, event_1576
- Dates: 2026-02-10, 2026-03-10, 2026-04-10, 2026-05-10, 2026-06-10
- Descriptions: Family streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`10` residual_days=`3`
- Latest/expected next: `2026-06-10` / `2026-07-10`
- Active as of request: `True`
- Amount: `68` from `event_1564, event_1570, event_1576`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:debt_payment:debit:debt_repayment:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_1625, event_1633, event_1641, event_1649, event_1657
- Dates: 2024-04-13, 2024-05-13, 2024-06-13, 2024-07-13, 2024-08-13
- Descriptions: Loan repayment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2024-08-13` / `2024-09-13`
- Active as of request: `True`
- Amount: `11850` from `event_1641, event_1649, event_1657`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:family_support:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `family_support` / `debit` / `expense`
- Members: event_1627, event_1635, event_1643, event_1651, event_1659
- Dates: 2024-04-15, 2024-05-15, 2024-06-15, 2024-07-15, 2024-08-15
- Descriptions: Childcare contribution
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-08-15` / `2024-09-15`
- Active as of request: `True`
- Amount: `12650` from `event_1643, event_1651, event_1659`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `groceries` / `debit` / `expense`
- Members: event_1662, event_1663, event_1664, event_1665, event_1666, event_1667, event_1668, event_1669, event_1670, event_1671, event_1672, event_1673, event_1674, event_1675, event_1676, event_1677, event_1678, event_1679, event_1680, event_1681, event_1682, event_1683, event_1684, event_1685, event_1686
- Dates: 2024-03-13, 2024-03-20, 2024-03-27, 2024-04-03, 2024-04-10, 2024-04-17, 2024-04-24, 2024-05-01, 2024-05-08, 2024-05-15, 2024-05-22, 2024-05-29, 2024-06-05, 2024-06-12, 2024-06-19, 2024-06-26, 2024-07-03, 2024-07-10, 2024-07-17, 2024-07-24, 2024-07-31, 2024-08-07, 2024-08-14, 2024-08-21, 2024-08-28
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2024-08-28` / `2024-09-04`
- Active as of request: `True`
- Amount: `4963.39` from `event_1684, event_1685, event_1686`
- Excluded outliers: `event_1700`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:healthcare:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `healthcare` / `debit` / `expense`
- Members: event_1626, event_1634, event_1642, event_1650, event_1658
- Dates: 2024-04-12, 2024-05-12, 2024-06-12, 2024-07-12, 2024-08-12
- Descriptions: Clinic payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2024-08-12` / `2024-09-12`
- Active as of request: `True`
- Amount: `8645.36` from `event_1642, event_1650, event_1658`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:rent:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `rent` / `debit` / `expense`
- Members: event_1623, event_1631, event_1639, event_1647, event_1655
- Dates: 2024-04-04, 2024-05-04, 2024-06-04, 2024-07-04, 2024-08-04
- Descriptions: Residential rent payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`1`
- Latest/expected next: `2024-08-04` / `2024-09-04`
- Active as of request: `True`
- Amount: `36100` from `event_1639, event_1647, event_1655`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:shopping:INR:reducible:sequence:0`

- User/category/direction/type: `user_19` / `shopping` / `debit` / `expense`
- Members: event_1629, event_1637, event_1645, event_1653, event_1661
- Dates: 2024-04-14, 2024-05-14, 2024-06-14, 2024-07-14, 2024-08-14
- Descriptions: Clothing and household items
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2024-08-14` / `2024-09-14`
- Active as of request: `True`
- Amount: `6069.58` from `event_1645, event_1653, event_1661`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `transport` / `debit` / `expense`
- Members: event_1687, event_1688, event_1689, event_1690, event_1691, event_1692, event_1693, event_1694, event_1695, event_1696, event_1697, event_1698, event_1699
- Dates: 2024-03-14, 2024-03-28, 2024-04-11, 2024-04-25, 2024-05-09, 2024-05-23, 2024-06-06, 2024-06-20, 2024-07-04, 2024-07-18, 2024-08-01, 2024-08-15, 2024-08-29
- Descriptions: Fuel refill, Local taxi, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`11` residual_days=`0`
- Latest/expected next: `2024-08-29` / `2024-09-12`
- Active as of request: `True`
- Amount: `2765.93` from `event_1697, event_1698, event_1699`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `utilities` / `debit` / `expense`
- Members: event_1624, event_1632, event_1640, event_1648, event_1656
- Dates: 2024-04-08, 2024-05-08, 2024-06-08, 2024-07-08, 2024-08-08
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2024-08-08` / `2024-09-08`
- Active as of request: `True`
- Amount: `6129.19` from `event_1640, event_1648, event_1656`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_19` / `salary` / `credit` / `income`
- Members: event_1622, event_1630, event_1638, event_1646, event_1654
- Dates: 2024-04-15, 2024-05-15, 2024-06-15, 2024-07-15, 2024-08-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-08-15` / `2024-09-15`
- Active as of request: `True`
- Amount: `131000` from `event_1638, event_1646, event_1654`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_19:subscription:debit:cloud_storage:INR:stoppable:sequence:0`

- User/category/direction/type: `user_19` / `cloud_storage` / `debit` / `subscription`
- Members: event_1628, event_1636, event_1644, event_1652, event_1660
- Dates: 2024-04-14, 2024-05-14, 2024-06-14, 2024-07-14, 2024-08-14
- Descriptions: Online backup subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2024-08-14` / `2024-09-14`
- Active as of request: `True`
- Amount: `395` from `event_1644, event_1652, event_1660`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:dining:INR:reducible:sequence:0`

- User/category/direction/type: `user_20` / `dining` / `debit` / `expense`
- Members: event_1775, event_1776, event_1777, event_1778, event_1779, event_1780, event_1781, event_1782, event_1783
- Dates: 2025-08-15, 2025-09-05, 2025-09-26, 2025-10-17, 2025-11-07, 2025-11-28, 2025-12-19, 2026-01-09, 2026-01-30
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Neighbourhood restaurant, Quick-service meal, Takeaway order
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`5` residual_days=`0`
- Latest/expected next: `2026-01-30` / `2026-02-20`
- Active as of request: `True`
- Amount: `3803.95` from `event_1781, event_1782, event_1783`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:education:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `education` / `debit` / `expense`
- Members: event_1705, event_1713, event_1721, event_1729, event_1737
- Dates: 2025-09-07, 2025-10-07, 2025-11-07, 2025-12-07, 2026-01-07
- Descriptions: School fee payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2026-01-07` / `2026-02-07`
- Active as of request: `True`
- Amount: `8740` from `event_1721, event_1729, event_1737`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:entertainment:INR:reducible:sequence:0`

- User/category/direction/type: `user_20` / `entertainment` / `debit` / `expense`
- Members: event_1707, event_1715, event_1723, event_1731, event_1739
- Dates: 2025-09-13, 2025-10-13, 2025-11-13, 2025-12-13, 2026-01-13
- Descriptions: Cinema and events
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2026-01-13` / `2026-02-13`
- Active as of request: `True`
- Amount: `2115.92` from `event_1723, event_1731, event_1739`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `groceries` / `debit` / `expense`
- Members: event_1744, event_1745, event_1746, event_1747, event_1748, event_1749, event_1750, event_1751, event_1752, event_1753, event_1754, event_1755, event_1756, event_1757, event_1758, event_1759, event_1760, event_1761
- Dates: 2025-08-13, 2025-08-23, 2025-09-02, 2025-09-12, 2025-09-22, 2025-10-02, 2025-10-12, 2025-10-22, 2025-11-01, 2025-11-11, 2025-11-21, 2025-12-01, 2025-12-11, 2025-12-21, 2025-12-31, 2026-01-10, 2026-01-20, 2026-01-30
- Descriptions: Bulk pantry shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2026-01-30` / `2026-02-09`
- Active as of request: `True`
- Amount: `4719.22` from `event_1759, event_1760, event_1761`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:healthcare:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `healthcare` / `debit` / `expense`
- Members: event_1706, event_1714, event_1722, event_1730, event_1738
- Dates: 2025-09-09, 2025-10-09, 2025-11-09, 2025-12-09, 2026-01-09
- Descriptions: Family healthcare expense
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`1`
- Latest/expected next: `2026-01-09` / `2026-02-09`
- Active as of request: `True`
- Amount: `6654.33` from `event_1722, event_1730, event_1738`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:housing:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `housing` / `debit` / `expense`
- Members: event_1702, event_1710, event_1718, event_1726, event_1734, event_1741
- Dates: 2025-09-02, 2025-10-02, 2025-11-02, 2025-12-02, 2026-01-02, 2026-02-02
- Descriptions: Home association fee
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`1`
- Latest/expected next: `2026-02-02` / `2026-03-02`
- Active as of request: `True`
- Amount: `7950` from `event_1726, event_1734, event_1741`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:insurance:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `insurance` / `debit` / `expense`
- Members: event_1704, event_1712, event_1720, event_1728, event_1736, event_1743
- Dates: 2025-09-06, 2025-10-06, 2025-11-06, 2025-12-06, 2026-01-06, 2026-02-06
- Descriptions: Household insurance
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`1`
- Latest/expected next: `2026-02-06` / `2026-03-06`
- Active as of request: `True`
- Amount: `3290` from `event_1728, event_1736, event_1743`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `transport` / `debit` / `expense`
- Members: event_1762, event_1763, event_1764, event_1765, event_1766, event_1767, event_1768, event_1769, event_1770, event_1771, event_1772, event_1773, event_1774
- Dates: 2025-08-14, 2025-08-28, 2025-09-11, 2025-09-25, 2025-10-09, 2025-10-23, 2025-11-06, 2025-11-20, 2025-12-04, 2025-12-18, 2026-01-01, 2026-01-15, 2026-01-29
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`11` residual_days=`0`
- Latest/expected next: `2026-01-29` / `2026-02-12`
- Active as of request: `True`
- Amount: `3243.84` from `event_1772, event_1773, event_1774`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `utilities` / `debit` / `expense`
- Members: event_1703, event_1711, event_1719, event_1727, event_1735, event_1742
- Dates: 2025-09-05, 2025-10-05, 2025-11-05, 2025-12-05, 2026-01-05, 2026-02-05
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`1`
- Latest/expected next: `2026-02-05` / `2026-03-05`
- Active as of request: `True`
- Amount: `7769.87` from `event_1727, event_1735, event_1742`
- Excluded outliers: `event_1786`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_20` / `salary` / `credit` / `income`
- Members: event_1701, event_1709, event_1717, event_1725, event_1733
- Dates: 2025-09-15, 2025-10-15, 2025-11-15, 2025-12-15, 2026-01-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2026-01-15` / `2026-02-15`
- Active as of request: `True`
- Amount: `108000` from `event_1717, event_1725, event_1733`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_20:subscription:debit:cloud_storage:INR:stoppable:sequence:0`

- User/category/direction/type: `user_20` / `cloud_storage` / `debit` / `subscription`
- Members: event_1708, event_1716, event_1724, event_1732, event_1740
- Dates: 2025-09-11, 2025-10-11, 2025-11-11, 2025-12-11, 2026-01-11
- Descriptions: Shared storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2026-01-11` / `2026-02-11`
- Active as of request: `True`
- Amount: `365` from `event_1724, event_1732, event_1740`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:expense:debit:dining:USD:reducible:sequence:0`

- User/category/direction/type: `user_21` / `dining` / `debit` / `expense`
- Members: event_1846, event_1847, event_1848, event_1849, event_1850, event_1851, event_1852, event_1853, event_1854
- Dates: 2025-10-10, 2025-10-31, 2025-11-21, 2025-12-12, 2026-01-02, 2026-01-23, 2026-02-13, 2026-03-06, 2026-03-27
- Descriptions: Bakery and snacks, Coffee shop, Neighbourhood restaurant, Quick-service meal, Takeaway order
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`19` residual_days=`0`
- Latest/expected next: `2026-03-27` / `2026-04-17`
- Active as of request: `True`
- Amount: `98.39` from `event_1852, event_1853, event_1854`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:expense:debit:groceries:USD:fixed:sequence:0`

- User/category/direction/type: `user_21` / `groceries` / `debit` / `expense`
- Members: event_1819, event_1820, event_1821, event_1822, event_1823, event_1824, event_1825, event_1826, event_1827, event_1828, event_1829, event_1830, event_1831, event_1832, event_1833, event_1834, event_1835, event_1836
- Dates: 2025-10-08, 2025-10-18, 2025-10-28, 2025-11-07, 2025-11-17, 2025-11-27, 2025-12-07, 2025-12-17, 2025-12-27, 2026-01-06, 2026-01-16, 2026-01-26, 2026-02-05, 2026-02-15, 2026-02-25, 2026-03-07, 2026-03-17, 2026-03-27
- Descriptions: Bulk pantry shop, Fresh food shop, Household groceries, Local market purchase, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2026-03-27` / `2026-04-06`
- Active as of request: `True`
- Amount: `97.55` from `event_1834, event_1835, event_1836`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:expense:debit:rent:USD:fixed:sequence:0`

- User/category/direction/type: `user_21` / `rent` / `debit` / `expense`
- Members: event_1789, event_1795, event_1801, event_1807, event_1813, event_1818
- Dates: 2025-11-02, 2025-12-02, 2026-01-02, 2026-02-02, 2026-03-02, 2026-04-02
- Descriptions: Residential rent payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`3`
- Latest/expected next: `2026-04-02` / `2026-05-02`
- Active as of request: `True`
- Amount: `718.8` from `event_1807, event_1813, event_1818`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:expense:debit:shopping:USD:reducible:sequence:0`

- User/category/direction/type: `user_21` / `shopping` / `debit` / `expense`
- Members: event_1793, event_1799, event_1805, event_1811, event_1817
- Dates: 2025-11-12, 2025-12-12, 2026-01-12, 2026-02-12, 2026-03-12
- Descriptions: Monthly shopping spend
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`3`
- Latest/expected next: `2026-03-12` / `2026-04-12`
- Active as of request: `True`
- Amount: `126.38` from `event_1805, event_1811, event_1817`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:expense:debit:transport:USD:fixed:sequence:0`

- User/category/direction/type: `user_21` / `transport` / `debit` / `expense`
- Members: event_1837, event_1838, event_1839, event_1840, event_1841, event_1842, event_1843, event_1844, event_1845
- Dates: 2025-10-09, 2025-10-30, 2025-11-20, 2025-12-11, 2026-01-01, 2026-01-22, 2026-02-12, 2026-03-05, 2026-03-26
- Descriptions: Commuter pass, Fuel refill, Local taxi, Parking and tolls, Rail pass, Vehicle charging
- Recurrence: `gap` cadence_days=`21` phase_or_anchor=`18` residual_days=`0`
- Latest/expected next: `2026-03-26` / `2026-04-16`
- Active as of request: `True`
- Amount: `51.42` from `event_1843, event_1844, event_1845`
- Excluded outliers: `event_1857`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:expense:debit:utilities:USD:fixed:sequence:0`

- User/category/direction/type: `user_21` / `utilities` / `debit` / `expense`
- Members: event_1790, event_1796, event_1802, event_1808, event_1814
- Dates: 2025-11-06, 2025-12-06, 2026-01-06, 2026-02-06, 2026-03-06
- Descriptions: Municipal utilities
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`3`
- Latest/expected next: `2026-03-06` / `2026-04-06`
- Active as of request: `True`
- Amount: `124.08` from `event_1802, event_1808, event_1814`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:income:credit:salary:USD:fixed:sequence:0`

- User/category/direction/type: `user_21` / `salary` / `credit` / `income`
- Members: event_1788, event_1794, event_1800, event_1806, event_1812
- Dates: 2025-11-15, 2025-12-15, 2026-01-15, 2026-02-15, 2026-03-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`3`
- Latest/expected next: `2026-03-15` / `2026-04-15`
- Active as of request: `True`
- Amount: `2256` from `event_1800, event_1806, event_1812`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:subscription:debit:cloud_storage:USD:stoppable:sequence:0`

- User/category/direction/type: `user_21` / `cloud_storage` / `debit` / `subscription`
- Members: event_1791, event_1797, event_1803, event_1809, event_1815
- Dates: 2025-11-12, 2025-12-12, 2026-01-12, 2026-02-12, 2026-03-12
- Descriptions: Online backup subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`3`
- Latest/expected next: `2026-03-12` / `2026-04-12`
- Active as of request: `True`
- Amount: `11` from `event_1803, event_1809, event_1815`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_21:subscription:debit:streaming:USD:reducible_or_stoppable:sequence:0`

- User/category/direction/type: `user_21` / `streaming` / `debit` / `subscription`
- Members: event_1792, event_1798, event_1804, event_1810, event_1816
- Dates: 2025-11-09, 2025-12-09, 2026-01-09, 2026-02-09, 2026-03-09
- Descriptions: Streaming subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`3`
- Latest/expected next: `2026-03-09` / `2026-04-09`
- Active as of request: `True`
- Amount: `47` from `event_1804, event_1810, event_1816`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:expense:debit:dining:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `dining` / `debit` / `expense`
- Members: event_1946, event_1947, event_1948, event_1949, event_1950, event_1951, event_1952, event_1953, event_1954, event_1955, event_1956, event_1957, event_1958
- Dates: 2024-06-14, 2024-06-28, 2024-07-12, 2024-07-26, 2024-08-09, 2024-08-23, 2024-09-06, 2024-09-20, 2024-10-04, 2024-10-18, 2024-11-01, 2024-11-15, 2024-11-29
- Descriptions: Coffee shop, Family dinner, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`5` residual_days=`0`
- Latest/expected next: `2024-11-29` / `2024-12-13`
- Active as of request: `True`
- Amount: `18.41` from `event_1956, event_1957, event_1958`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:expense:debit:entertainment:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `entertainment` / `debit` / `expense`
- Members: event_1865, event_1872, event_1879, event_1886, event_1893
- Dates: 2024-07-15, 2024-08-15, 2024-09-15, 2024-10-15, 2024-11-15
- Descriptions: Weekend entertainment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-11-15` / `2024-12-15`
- Active as of request: `True`
- Amount: `23.29` from `event_1879, event_1886, event_1893`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:expense:debit:groceries:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `groceries` / `debit` / `expense`
- Members: event_1895, event_1896, event_1897, event_1898, event_1899, event_1900, event_1901, event_1902, event_1903, event_1904, event_1905, event_1906, event_1907, event_1908, event_1909, event_1910, event_1911, event_1912, event_1913, event_1914, event_1915, event_1916, event_1917, event_1918, event_1919, event_1920
- Dates: 2024-06-12, 2024-06-19, 2024-06-26, 2024-07-03, 2024-07-10, 2024-07-17, 2024-07-24, 2024-07-31, 2024-08-07, 2024-08-14, 2024-08-21, 2024-08-28, 2024-09-04, 2024-09-11, 2024-09-18, 2024-09-25, 2024-10-02, 2024-10-09, 2024-10-16, 2024-10-23, 2024-10-30, 2024-11-06, 2024-11-13, 2024-11-20, 2024-11-27, 2024-12-04
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2024-12-04` / `2024-12-11`
- Active as of request: `True`
- Amount: `26.82` from `event_1918, event_1919, event_1920`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:expense:debit:rent:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `rent` / `debit` / `expense`
- Members: event_1860, event_1867, event_1874, event_1881, event_1888, event_1894
- Dates: 2024-07-03, 2024-08-03, 2024-09-03, 2024-10-03, 2024-11-03, 2024-12-03
- Descriptions: Apartment rent transfer
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`3` residual_days=`1`
- Latest/expected next: `2024-12-03` / `2025-01-03`
- Active as of request: `True`
- Amount: `178.2` from `event_1881, event_1888, event_1894`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:expense:debit:transport:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `transport` / `debit` / `expense`
- Members: event_1921, event_1922, event_1923, event_1924, event_1925, event_1926, event_1927, event_1928, event_1929, event_1930, event_1931, event_1932, event_1933, event_1934, event_1935, event_1936, event_1937, event_1938, event_1939, event_1940, event_1941, event_1942, event_1943, event_1944, event_1945
- Dates: 2024-06-13, 2024-06-20, 2024-06-27, 2024-07-04, 2024-07-11, 2024-07-18, 2024-07-25, 2024-08-01, 2024-08-08, 2024-08-15, 2024-08-22, 2024-08-29, 2024-09-05, 2024-09-12, 2024-09-19, 2024-09-26, 2024-10-03, 2024-10-10, 2024-10-17, 2024-10-24, 2024-10-31, 2024-11-07, 2024-11-14, 2024-11-21, 2024-11-28
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2024-11-28` / `2024-12-05`
- Active as of request: `True`
- Amount: `15.87` from `event_1943, event_1944, event_1945`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:expense:debit:utilities:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `utilities` / `debit` / `expense`
- Members: event_1861, event_1868, event_1875, event_1882, event_1889
- Dates: 2024-07-07, 2024-08-07, 2024-09-07, 2024-10-07, 2024-11-07
- Descriptions: Electricity and water bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2024-11-07` / `2024-12-07`
- Active as of request: `True`
- Amount: `31.52` from `event_1875, event_1882, event_1889`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:income:credit:salary:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `salary` / `credit` / `income`
- Members: event_1859, event_1866, event_1873, event_1880, event_1887
- Dates: 2024-07-15, 2024-08-15, 2024-09-15, 2024-10-15, 2024-11-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-11-15` / `2024-12-15`
- Active as of request: `True`
- Amount: `616` from `event_1873, event_1880, event_1887`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:subscription:debit:delivery_membership:EUR:fixed:sequence:0`

- User/category/direction/type: `user_22` / `delivery_membership` / `debit` / `subscription`
- Members: event_1863, event_1870, event_1877, event_1884, event_1891
- Dates: 2024-07-14, 2024-08-14, 2024-09-14, 2024-10-14, 2024-11-14
- Descriptions: Food delivery membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2024-11-14` / `2024-12-14`
- Active as of request: `True`
- Amount: `5` from `event_1877, event_1884, event_1891`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:subscription:debit:gym:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_22` / `gym` / `debit` / `subscription`
- Members: event_1864, event_1871, event_1878, event_1885, event_1892
- Dates: 2024-07-11, 2024-08-11, 2024-09-11, 2024-10-11, 2024-11-11
- Descriptions: Gym membership
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2024-11-11` / `2024-12-11`
- Active as of request: `True`
- Amount: `17` from `event_1878, event_1885, event_1892`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_22:subscription:debit:music_subscription:EUR:stoppable:sequence:0`

- User/category/direction/type: `user_22` / `music_subscription` / `debit` / `subscription`
- Members: event_1862, event_1869, event_1876, event_1883, event_1890
- Dates: 2024-07-12, 2024-08-12, 2024-09-12, 2024-10-12, 2024-11-12
- Descriptions: Music service subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2024-11-12` / `2024-12-12`
- Active as of request: `True`
- Amount: `6` from `event_1876, event_1883, event_1890`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:debt_payment:debit:debt_repayment:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `debt_repayment` / `debit` / `debt_payment`
- Members: event_1965, event_1973, event_1981, event_1989, event_1997
- Dates: 2024-12-13, 2025-01-13, 2025-02-13, 2025-03-13, 2025-04-13
- Descriptions: Education loan instalment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`3`
- Latest/expected next: `2025-04-13` / `2025-05-13`
- Active as of request: `True`
- Amount: `5852` from `event_1981, event_1989, event_1997`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:family_support:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `family_support` / `debit` / `expense`
- Members: event_1967, event_1975, event_1983, event_1991, event_1999
- Dates: 2024-12-15, 2025-01-15, 2025-02-15, 2025-03-15, 2025-04-15
- Descriptions: Childcare contribution
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`3`
- Latest/expected next: `2025-04-15` / `2025-05-15`
- Active as of request: `True`
- Amount: `4270.2` from `event_1983, event_1991, event_1999`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:groceries:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `groceries` / `debit` / `expense`
- Members: event_2003, event_2004, event_2005, event_2006, event_2007, event_2008, event_2009, event_2010, event_2011, event_2012, event_2013, event_2014, event_2015, event_2016, event_2017, event_2018, event_2019, event_2020, event_2021, event_2022, event_2023, event_2024, event_2025, event_2026, event_2027
- Dates: 2024-11-13, 2024-11-20, 2024-11-27, 2024-12-04, 2024-12-11, 2024-12-18, 2024-12-25, 2025-01-01, 2025-01-08, 2025-01-15, 2025-01-22, 2025-01-29, 2025-02-05, 2025-02-12, 2025-02-19, 2025-02-26, 2025-03-05, 2025-03-12, 2025-03-19, 2025-03-26, 2025-04-02, 2025-04-09, 2025-04-16, 2025-04-23, 2025-04-30
- Descriptions: Bulk pantry shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2025-04-30` / `2025-05-07`
- Active as of request: `True`
- Amount: `1678.37` from `event_2025, event_2026, event_2027`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:healthcare:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `healthcare` / `debit` / `expense`
- Members: event_1966, event_1974, event_1982, event_1990, event_1998
- Dates: 2024-12-12, 2025-01-12, 2025-02-12, 2025-03-12, 2025-04-12
- Descriptions: Clinic payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`3`
- Latest/expected next: `2025-04-12` / `2025-05-12`
- Active as of request: `True`
- Amount: `1439.91` from `event_1982, event_1990, event_1998`
- Excluded outliers: `event_2042`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:rent:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `rent` / `debit` / `expense`
- Members: event_1963, event_1971, event_1979, event_1987, event_1995, event_2002
- Dates: 2024-12-04, 2025-01-04, 2025-02-04, 2025-03-04, 2025-04-04, 2025-05-04
- Descriptions: Shared housing rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`4` residual_days=`3`
- Latest/expected next: `2025-05-04` / `2025-06-04`
- Active as of request: `True`
- Amount: `15312` from `event_1987, event_1995, event_2002`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:shopping:ZAR:reducible:sequence:0`

- User/category/direction/type: `user_23` / `shopping` / `debit` / `expense`
- Members: event_1969, event_1977, event_1985, event_1993, event_2001
- Dates: 2024-12-14, 2025-01-14, 2025-02-14, 2025-03-14, 2025-04-14
- Descriptions: Personal shopping
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`3`
- Latest/expected next: `2025-04-14` / `2025-05-14`
- Active as of request: `True`
- Amount: `1389.39` from `event_1985, event_1993, event_2001`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:transport:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `transport` / `debit` / `expense`
- Members: event_2028, event_2029, event_2030, event_2031, event_2032, event_2033, event_2034, event_2035, event_2036, event_2037, event_2038, event_2039, event_2040
- Dates: 2024-11-14, 2024-11-28, 2024-12-12, 2024-12-26, 2025-01-09, 2025-01-23, 2025-02-06, 2025-02-20, 2025-03-06, 2025-03-20, 2025-04-03, 2025-04-17, 2025-05-01
- Descriptions: Commuter pass, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`14` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2025-05-01` / `2025-05-15`
- Active as of request: `True`
- Amount: `1092.98` from `event_2038, event_2039, event_2040`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:expense:debit:utilities:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `utilities` / `debit` / `expense`
- Members: event_1964, event_1972, event_1980, event_1988, event_1996
- Dates: 2024-12-08, 2025-01-08, 2025-02-08, 2025-03-08, 2025-04-08
- Descriptions: Electricity bill
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`3`
- Latest/expected next: `2025-04-08` / `2025-05-08`
- Active as of request: `True`
- Amount: `2915.67` from `event_1980, event_1988, event_1996`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:income:credit:salary:ZAR:fixed:sequence:0`

- User/category/direction/type: `user_23` / `salary` / `credit` / `income`
- Members: event_1962, event_1970, event_1978, event_1986, event_1994
- Dates: 2024-12-15, 2025-01-15, 2025-02-15, 2025-03-15, 2025-04-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`3`
- Latest/expected next: `2025-04-15` / `2025-05-15`
- Active as of request: `True`
- Amount: `45760` from `event_1978, event_1986, event_1994`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_23:subscription:debit:cloud_storage:ZAR:stoppable:sequence:0`

- User/category/direction/type: `user_23` / `cloud_storage` / `debit` / `subscription`
- Members: event_1968, event_1976, event_1984, event_1992, event_2000
- Dates: 2024-12-14, 2025-01-14, 2025-02-14, 2025-03-14, 2025-04-14
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`3`
- Latest/expected next: `2025-04-14` / `2025-05-14`
- Active as of request: `True`
- Amount: `295.9` from `event_1984, event_1992, event_2000`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:dining:INR:reducible:sequence:0`

- User/category/direction/type: `user_24` / `dining` / `debit` / `expense`
- Members: event_2138, event_2139, event_2140, event_2141, event_2142, event_2143, event_2144, event_2145, event_2146, event_2147, event_2148, event_2149, event_2150, event_2151, event_2152, event_2153, event_2154, event_2155, event_2156, event_2157, event_2158, event_2159, event_2160, event_2161, event_2162, event_2163
- Dates: 2025-07-12, 2025-07-19, 2025-07-26, 2025-08-02, 2025-08-09, 2025-08-16, 2025-08-23, 2025-08-30, 2025-09-06, 2025-09-13, 2025-09-20, 2025-09-27, 2025-10-04, 2025-10-11, 2025-10-18, 2025-10-25, 2025-11-01, 2025-11-08, 2025-11-15, 2025-11-22, 2025-11-29, 2025-12-06, 2025-12-13, 2025-12-20, 2025-12-27, 2026-01-03
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`6` residual_days=`0`
- Latest/expected next: `2026-01-03` / `2026-01-10`
- Active as of request: `True`
- Amount: `2184.47` from `event_2161, event_2162, event_2163`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:entertainment:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `entertainment` / `debit` / `expense`
- Members: event_2050, event_2058, event_2066, event_2074, event_2082
- Dates: 2025-08-13, 2025-09-13, 2025-10-13, 2025-11-13, 2025-12-13
- Descriptions: Local event tickets
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`13` residual_days=`1`
- Latest/expected next: `2025-12-13` / `2026-01-13`
- Active as of request: `True`
- Amount: `1916.16` from `event_2066, event_2074, event_2082`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:groceries:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `groceries` / `debit` / `expense`
- Members: event_2084, event_2085, event_2086, event_2087, event_2088, event_2089, event_2090, event_2091, event_2092, event_2093, event_2094, event_2095, event_2096, event_2097, event_2098, event_2099, event_2100, event_2101
- Dates: 2025-07-10, 2025-07-20, 2025-07-30, 2025-08-09, 2025-08-19, 2025-08-29, 2025-09-08, 2025-09-18, 2025-09-28, 2025-10-08, 2025-10-18, 2025-10-28, 2025-11-07, 2025-11-17, 2025-11-27, 2025-12-07, 2025-12-17, 2025-12-27
- Descriptions: Bulk pantry shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`2` residual_days=`0`
- Latest/expected next: `2025-12-27` / `2026-01-06`
- Active as of request: `True`
- Amount: `2321.31` from `event_2099, event_2100, event_2101`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:insurance:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `insurance` / `debit` / `expense`
- Members: event_2046, event_2054, event_2062, event_2070, event_2078
- Dates: 2025-08-06, 2025-09-06, 2025-10-06, 2025-11-06, 2025-12-06
- Descriptions: Insurance policy payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`1`
- Latest/expected next: `2025-12-06` / `2026-01-06`
- Active as of request: `True`
- Amount: `2510` from `event_2062, event_2070, event_2078`
- Excluded outliers: `event_2166`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:rent:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `rent` / `debit` / `expense`
- Members: event_2044, event_2052, event_2060, event_2068, event_2076, event_2083
- Dates: 2025-08-01, 2025-09-01, 2025-10-01, 2025-11-01, 2025-12-01, 2026-01-01
- Descriptions: Landlord standing order
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`1` residual_days=`1`
- Latest/expected next: `2026-01-01` / `2026-02-01`
- Active as of request: `True`
- Amount: `18600` from `event_2068, event_2076, event_2083`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:shopping:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `shopping` / `debit` / `expense`
- Members: event_2049, event_2057, event_2065, event_2073, event_2081
- Dates: 2025-08-11, 2025-09-11, 2025-10-11, 2025-11-11, 2025-12-11
- Descriptions: Monthly shopping spend
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2025-12-11` / `2026-01-11`
- Active as of request: `True`
- Amount: `2680.78` from `event_2065, event_2073, event_2081`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:transport:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `transport` / `debit` / `expense`
- Members: event_2102, event_2103, event_2104, event_2105, event_2106, event_2107, event_2108, event_2109, event_2110, event_2111, event_2112, event_2113, event_2114, event_2115, event_2116, event_2117, event_2118, event_2119, event_2120, event_2121, event_2122, event_2123, event_2124, event_2125, event_2126, event_2127, event_2128, event_2129, event_2130, event_2131, event_2132, event_2133, event_2134, event_2135, event_2136, event_2137
- Dates: 2025-07-11, 2025-07-16, 2025-07-21, 2025-07-26, 2025-07-31, 2025-08-05, 2025-08-10, 2025-08-15, 2025-08-20, 2025-08-25, 2025-08-30, 2025-09-04, 2025-09-09, 2025-09-14, 2025-09-19, 2025-09-24, 2025-09-29, 2025-10-04, 2025-10-09, 2025-10-14, 2025-10-19, 2025-10-24, 2025-10-29, 2025-11-03, 2025-11-08, 2025-11-13, 2025-11-18, 2025-11-23, 2025-11-28, 2025-12-03, 2025-12-08, 2025-12-13, 2025-12-18, 2025-12-23, 2025-12-28, 2026-01-02
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`5` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2026-01-02` / `2026-01-07`
- Active as of request: `True`
- Amount: `1593.41` from `event_2135, event_2136, event_2137`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:expense:debit:utilities:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `utilities` / `debit` / `expense`
- Members: event_2045, event_2053, event_2061, event_2069, event_2077
- Dates: 2025-08-05, 2025-09-05, 2025-10-05, 2025-11-05, 2025-12-05
- Descriptions: Household utility payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`5` residual_days=`1`
- Latest/expected next: `2025-12-05` / `2026-01-05`
- Active as of request: `True`
- Amount: `3490.5` from `event_2061, event_2069, event_2077`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:income:credit:salary:INR:fixed:sequence:0`

- User/category/direction/type: `user_24` / `salary` / `credit` / `income`
- Members: event_2043, event_2051, event_2059, event_2067, event_2075
- Dates: 2025-08-15, 2025-09-15, 2025-10-15, 2025-11-15, 2025-12-15
- Descriptions: Payroll credit
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2025-12-15` / `2026-01-15`
- Active as of request: `True`
- Amount: `61000` from `event_2059, event_2067, event_2075`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:subscription:debit:cloud_storage:INR:stoppable:sequence:0`

- User/category/direction/type: `user_24` / `cloud_storage` / `debit` / `subscription`
- Members: event_2047, event_2055, event_2063, event_2071, event_2079
- Dates: 2025-08-11, 2025-09-11, 2025-10-11, 2025-11-11, 2025-12-11
- Descriptions: Online backup subscription
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`11` residual_days=`1`
- Latest/expected next: `2025-12-11` / `2026-01-11`
- Active as of request: `True`
- Amount: `355` from `event_2063, event_2071, event_2079`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_24:subscription:debit:streaming:INR:reducible_or_stoppable:sequence:0`

- User/category/direction/type: `user_24` / `streaming` / `debit` / `subscription`
- Members: event_2048, event_2056, event_2064, event_2072, event_2080
- Dates: 2025-08-08, 2025-09-08, 2025-10-08, 2025-11-08, 2025-12-08
- Descriptions: Family streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`8` residual_days=`1`
- Latest/expected next: `2025-12-08` / `2026-01-08`
- Active as of request: `True`
- Amount: `1200` from `event_2064, event_2072, event_2080`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:dining:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `dining` / `debit` / `expense`
- Members: event_2262, event_2263, event_2264, event_2265, event_2266, event_2267, event_2268, event_2269, event_2270, event_2271, event_2272, event_2273, event_2274, event_2275, event_2276, event_2277, event_2278, event_2279, event_2280, event_2281, event_2282, event_2283, event_2284, event_2285, event_2286
- Dates: 2023-09-13, 2023-09-20, 2023-09-27, 2023-10-04, 2023-10-11, 2023-10-18, 2023-10-25, 2023-11-01, 2023-11-08, 2023-11-15, 2023-11-22, 2023-11-29, 2023-12-06, 2023-12-13, 2023-12-20, 2023-12-27, 2024-01-03, 2024-01-10, 2024-01-17, 2024-01-24, 2024-01-31, 2024-02-07, 2024-02-14, 2024-02-21, 2024-02-28
- Descriptions: Bakery and snacks, Coffee shop, Family dinner, Lunch with colleagues, Neighbourhood restaurant, Quick-service meal, Takeaway order, Weekend food delivery
- Recurrence: `gap` cadence_days=`7` phase_or_anchor=`3` residual_days=`0`
- Latest/expected next: `2024-02-28` / `2024-03-06`
- Active as of request: `True`
- Amount: `1133036.68` from `event_2284, event_2285, event_2286`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:entertainment:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `entertainment` / `debit` / `expense`
- Members: event_2174, event_2182, event_2190, event_2198, event_2206
- Dates: 2023-10-14, 2023-11-14, 2023-12-14, 2024-01-14, 2024-02-14
- Descriptions: Games and recreation
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`14` residual_days=`1`
- Latest/expected next: `2024-02-14` / `2024-03-14`
- Active as of request: `True`
- Amount: `504697.37` from `event_2190, event_2198, event_2206`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:groceries:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `groceries` / `debit` / `expense`
- Members: event_2208, event_2209, event_2210, event_2211, event_2212, event_2213, event_2214, event_2215, event_2216, event_2217, event_2218, event_2219, event_2220, event_2221, event_2222, event_2223, event_2224, event_2225
- Dates: 2023-09-11, 2023-09-21, 2023-10-01, 2023-10-11, 2023-10-21, 2023-10-31, 2023-11-10, 2023-11-20, 2023-11-30, 2023-12-10, 2023-12-20, 2023-12-30, 2024-01-09, 2024-01-19, 2024-01-29, 2024-02-08, 2024-02-18, 2024-02-28
- Descriptions: Bulk pantry shop, Fresh food shop, Grocery delivery, Household groceries, Local market purchase, Neighbourhood grocer, Supermarket basket, Weekly produce market
- Recurrence: `gap` cadence_days=`10` phase_or_anchor=`4` residual_days=`0`
- Latest/expected next: `2024-02-28` / `2024-03-09`
- Active as of request: `True`
- Amount: `1472349.1` from `event_2223, event_2224, event_2225`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:insurance:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `insurance` / `debit` / `expense`
- Members: event_2170, event_2178, event_2186, event_2194, event_2202
- Dates: 2023-10-07, 2023-11-07, 2023-12-07, 2024-01-07, 2024-02-07
- Descriptions: Insurance policy payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`7` residual_days=`1`
- Latest/expected next: `2024-02-07` / `2024-03-07`
- Active as of request: `True`
- Amount: `904400` from `event_2186, event_2194, event_2202`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:rent:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `rent` / `debit` / `expense`
- Members: event_2168, event_2176, event_2184, event_2192, event_2200, event_2207
- Dates: 2023-10-02, 2023-11-02, 2023-12-02, 2024-01-02, 2024-02-02, 2024-03-02
- Descriptions: Monthly rent
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`2` residual_days=`2`
- Latest/expected next: `2024-03-02` / `2024-04-02`
- Active as of request: `True`
- Amount: `6954000` from `event_2192, event_2200, event_2207`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:shopping:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `shopping` / `debit` / `expense`
- Members: event_2173, event_2181, event_2189, event_2197, event_2205
- Dates: 2023-10-12, 2023-11-12, 2023-12-12, 2024-01-12, 2024-02-12
- Descriptions: Monthly shopping spend
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2024-02-12` / `2024-03-12`
- Active as of request: `True`
- Amount: `1170271.29` from `event_2189, event_2197, event_2205`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:transport:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `transport` / `debit` / `expense`
- Members: event_2226, event_2227, event_2228, event_2229, event_2230, event_2231, event_2232, event_2233, event_2234, event_2235, event_2236, event_2237, event_2238, event_2239, event_2240, event_2241, event_2242, event_2243, event_2244, event_2245, event_2246, event_2247, event_2248, event_2249, event_2250, event_2251, event_2252, event_2253, event_2254, event_2255, event_2256, event_2257, event_2258, event_2259, event_2260, event_2261
- Dates: 2023-09-12, 2023-09-17, 2023-09-22, 2023-09-27, 2023-10-02, 2023-10-07, 2023-10-12, 2023-10-17, 2023-10-22, 2023-10-27, 2023-11-01, 2023-11-06, 2023-11-11, 2023-11-16, 2023-11-21, 2023-11-26, 2023-12-01, 2023-12-06, 2023-12-11, 2023-12-16, 2023-12-21, 2023-12-26, 2023-12-31, 2024-01-05, 2024-01-10, 2024-01-15, 2024-01-20, 2024-01-25, 2024-01-30, 2024-02-04, 2024-02-09, 2024-02-14, 2024-02-19, 2024-02-24, 2024-02-29, 2024-03-05
- Descriptions: Commuter pass, Fuel refill, Local taxi, Metro and bus fares, Parking and tolls, Rail pass, Ride-hailing trip, Vehicle charging
- Recurrence: `gap` cadence_days=`5` phase_or_anchor=`0` residual_days=`0`
- Latest/expected next: `2024-03-05` / `2024-03-10`
- Active as of request: `True`
- Amount: `729004.44` from `event_2259, event_2260, event_2261`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:expense:debit:utilities:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `utilities` / `debit` / `expense`
- Members: event_2169, event_2177, event_2185, event_2193, event_2201
- Dates: 2023-10-06, 2023-11-06, 2023-12-06, 2024-01-06, 2024-02-06
- Descriptions: Household utility payment
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`6` residual_days=`1`
- Latest/expected next: `2024-02-06` / `2024-03-06`
- Active as of request: `True`
- Amount: `1341541.39` from `event_2185, event_2193, event_2201`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:income:credit:salary:USD:fixed:sequence:0`

- User/category/direction/type: `user_25` / `salary` / `credit` / `income`
- Members: event_2167, event_2175, event_2183, event_2191, event_2199
- Dates: 2023-10-15, 2023-11-15, 2023-12-15, 2024-01-15, 2024-02-15
- Descriptions: International employer payroll
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`15` residual_days=`1`
- Latest/expected next: `2024-02-15` / `2024-03-15`
- Active as of request: `True`
- Amount: `1800` from `event_2183, event_2191, event_2199`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:subscription:debit:cloud_storage:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `cloud_storage` / `debit` / `subscription`
- Members: event_2171, event_2179, event_2187, event_2195, event_2203
- Dates: 2023-10-12, 2023-11-12, 2023-12-12, 2024-01-12, 2024-02-12
- Descriptions: Cloud storage plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`12` residual_days=`1`
- Latest/expected next: `2024-02-12` / `2024-03-12`
- Active as of request: `True`
- Amount: `126350` from `event_2187, event_2195, event_2203`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership

## `user_25:subscription:debit:streaming:IDR:fixed:sequence:0`

- User/category/direction/type: `user_25` / `streaming` / `debit` / `subscription`
- Members: event_2172, event_2180, event_2188, event_2196, event_2204
- Dates: 2023-10-09, 2023-11-09, 2023-12-09, 2024-01-09, 2024-02-09
- Descriptions: Video streaming plan
- Recurrence: `month` cadence_days=`None` phase_or_anchor=`9` residual_days=`1`
- Latest/expected next: `2024-02-09` / `2024-03-09`
- Active as of request: `True`
- Amount: `573800` from `event_2188, event_2196, event_2204`
- Excluded outliers: `none`
- Evidence: deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership
