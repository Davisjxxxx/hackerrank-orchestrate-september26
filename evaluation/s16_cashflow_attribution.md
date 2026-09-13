# S16 cash-flow attribution

Current production path only. Each section lists every non-zero canonical future cash flow and resulting daily balance. The phase-aware policy remains experimental and is not silently substituted.

## `request_02` / `user_02`

- Opening/minimum: `60383889.2` / `29158400`
- Expected safe amount: `17229139.2`; actual: `18479330.16`
- Expected earliest: `2025-09-15`; actual: `2025-09-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2025-08-07 flow=-2141849.94 balance=58242039.26
2025-08-08 flow=-2783500 balance=55458539.26
2025-08-09 flow=-3040000 balance=52418539.26
2025-08-11 flow=-1641668.72 balance=50776870.54
2025-08-12 flow=-2769590.38 balance=48007280.16
2025-08-13 flow=-369550 balance=47637730.16
2025-08-15 flow=41397436.21 balance=89035166.37
2025-08-26 flow=-2769590.38 balance=86265575.99
2025-09-04 flow=-3534000 balance=82731575.99
2025-09-07 flow=-2141849.94 balance=80589726.05
2025-09-08 flow=-1132400 balance=79457326.05
2025-09-09 flow=-5809590.38 balance=73647735.67
2025-09-11 flow=-1641668.72 balance=72006066.95
2025-09-13 flow=-369550 balance=71636516.95
2025-09-15 flow=31992436.21 balance=103628953.16
2025-09-23 flow=-2769590.38 balance=100859362.78
2025-10-04 flow=-3534000 balance=97325362.78
2025-10-07 flow=-4911440.32 balance=92413922.46
2025-10-08 flow=-1132400 balance=91281522.46
2025-10-09 flow=-3040000 balance=88241522.46
2025-10-11 flow=-1641668.72 balance=86599853.74
2025-10-13 flow=-369550 balance=86230303.74
2025-10-15 flow=31992436.21 balance=118222739.95
2025-10-21 flow=-2769590.38 balance=115453149.57
```
- Projected event attribution:
```json
[
  {
    "amount": "2141849.94",
    "category": "utilities",
    "currency": "IDR",
    "date": "2025-08-07",
    "description": "Municipal utilities",
    "event_id": "event_138@2025-08-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_138"
  },
  {
    "amount": "1132400",
    "category": "insurance",
    "currency": "IDR",
    "date": "2025-08-08",
    "description": "Household insurance",
    "event_id": "event_139@2025-08-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_139"
  },
  {
    "amount": "3040000",
    "category": "education",
    "currency": "IDR",
    "date": "2025-08-09",
    "description": "Course tuition",
    "event_id": "event_140@2025-08-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_140"
  },
  {
    "amount": "1641668.72",
    "category": "healthcare",
    "currency": "IDR",
    "date": "2025-08-11",
    "description": "Clinic payment",
    "event_id": "event_141@2025-08-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_141"
  },
  {
    "amount": "1440242.94",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-08-12",
    "description": "Ride-hailing trip",
    "event_id": "event_168@2025-08-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_168"
  },
  {
    "amount": "1329347.44",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-08-12",
    "description": "Commuter pass",
    "event_id": "event_174@2025-08-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_174"
  },
  {
    "amount": "369550",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2025-08-13",
    "description": "Shared storage plan",
    "event_id": "event_143@2025-08-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_143"
  },
  {
    "amount": "1352563.79",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2025-08-15",
    "description": "Cinema and events",
    "event_id": "event_142@2025-08-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_142"
  },
  {
    "amount": "1440242.94",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-08-26",
    "description": "Ride-hailing trip",
    "event_id": "event_168@2025-08-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_168"
  },
  {
    "amount": "1329347.44",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-08-26",
    "description": "Commuter pass",
    "event_id": "event_174@2025-08-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_174"
  },
  {
    "amount": "3534000",
    "category": "housing",
    "currency": "IDR",
    "date": "2025-09-04",
    "description": "Home repair reserve",
    "event_id": "event_144@2025-09-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_144"
  },
  {
    "amount": "2141849.94",
    "category": "utilities",
    "currency": "IDR",
    "date": "2025-09-07",
    "description": "Municipal utilities",
    "event_id": "event_138@2025-09-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_138"
  },
  {
    "amount": "1132400",
    "category": "insurance",
    "currency": "IDR",
    "date": "2025-09-08",
    "description": "Household insurance",
    "event_id": "event_139@2025-09-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_139"
  },
  {
    "amount": "3040000",
    "category": "education",
    "currency": "IDR",
    "date": "2025-09-09",
    "description": "Course tuition",
    "event_id": "event_140@2025-09-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_140"
  },
  {
    "amount": "1440242.94",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-09-09",
    "description": "Ride-hailing trip",
    "event_id": "event_168@2025-09-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_168"
  },
  {
    "amount": "1329347.44",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-09-09",
    "description": "Commuter pass",
    "event_id": "event_174@2025-09-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_174"
  },
  {
    "amount": "1641668.72",
    "category": "healthcare",
    "currency": "IDR",
    "date": "2025-09-11",
    "description": "Clinic payment",
    "event_id": "event_141@2025-09-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_141"
  },
  {
    "amount": "369550",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2025-09-13",
    "description": "Shared storage plan",
    "event_id": "event_143@2025-09-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_143"
  },
  {
    "amount": "33345000",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-09-15",
    "description": "Payroll credit",
    "event_id": "event_136@2025-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_136"
  },
  {
    "amount": "1352563.79",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2025-09-15",
    "description": "Cinema and events",
    "event_id": "event_142@2025-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_142"
  },
  {
    "amount": "1440242.94",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-09-23",
    "description": "Ride-hailing trip",
    "event_id": "event_168@2025-09-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_168"
  },
  {
    "amount": "1329347.44",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-09-23",
    "description": "Commuter pass",
    "event_id": "event_174@2025-09-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_174"
  },
  {
    "amount": "3534000",
    "category": "housing",
    "currency": "IDR",
    "date": "2025-10-04",
    "description": "Home repair reserve",
    "event_id": "event_144@2025-10-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_144"
  },
  {
    "amount": "2141849.94",
    "category": "utilities",
    "currency": "IDR",
    "date": "2025-10-07",
    "description": "Municipal utilities",
    "event_id": "event_138@2025-10-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_138"
  },
  {
    "amount": "1440242.94",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-10-07",
    "description": "Ride-hailing trip",
    "event_id": "event_168@2025-10-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_168"
  },
  {
    "amount": "1329347.44",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-10-07",
    "description": "Commuter pass",
    "event_id": "event_174@2025-10-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_174"
  },
  {
    "amount": "1132400",
    "category": "insurance",
    "currency": "IDR",
    "date": "2025-10-08",
    "description": "Household insurance",
    "event_id": "event_139@2025-10-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_139"
  },
  {
    "amount": "3040000",
    "category": "education",
    "currency": "IDR",
    "date": "2025-10-09",
    "description": "Course tuition",
    "event_id": "event_140@2025-10-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_140"
  },
  {
    "amount": "1641668.72",
    "category": "healthcare",
    "currency": "IDR",
    "date": "2025-10-11",
    "description": "Clinic payment",
    "event_id": "event_141@2025-10-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_141"
  },
  {
    "amount": "369550",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2025-10-13",
    "description": "Shared storage plan",
    "event_id": "event_143@2025-10-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_143"
  },
  {
    "amount": "33345000",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-10-15",
    "description": "Payroll credit",
    "event_id": "event_136@2025-10-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_136"
  },
  {
    "amount": "1352563.79",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2025-10-15",
    "description": "Cinema and events",
    "event_id": "event_142@2025-10-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_142"
  },
  {
    "amount": "1440242.94",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-10-21",
    "description": "Ride-hailing trip",
    "event_id": "event_168@2025-10-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_168"
  },
  {
    "amount": "1329347.44",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-10-21",
    "description": "Commuter pass",
    "event_id": "event_174@2025-10-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_174"
  }
]
```

## `request_03` / `user_03`

- Opening/minimum: `5810300` / `2668700`
- Expected safe amount: `873000`; actual: `1050071.39`
- Expected earliest: `2019-11-15`; actual: `2019-11-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2019-09-04 flow=-1140000 balance=4670300
2019-09-07 flow=-95000 balance=4575300
2019-09-08 flow=-537433.32 balance=4037866.68
2019-09-11 flow=-117800 balance=3920066.68
2019-09-14 flow=-201295.29 balance=3718771.39
2019-09-15 flow=4365000 balance=8083771.39
2019-09-18 flow=-234390.87 balance=7849380.52
2019-09-19 flow=-240706.45 balance=7608674.07
2019-09-28 flow=-234390.87 balance=7374283.2
2019-10-04 flow=-1140000 balance=6234283.2
2019-10-08 flow=-537433.32 balance=5696849.88
2019-10-11 flow=-117800 balance=5579049.88
2019-10-14 flow=-201295.29 balance=5377754.59
2019-10-15 flow=4365000 balance=9742754.59
2019-10-18 flow=-234390.87 balance=9508363.72
2019-10-19 flow=-240706.45 balance=9267657.27
2019-10-28 flow=-234390.87 balance=9033266.4
2019-11-04 flow=-1140000 balance=7893266.4
2019-11-07 flow=-234390.87 balance=7658875.53
2019-11-08 flow=-303042.45 balance=7355833.08
2019-11-11 flow=-117800 balance=7238033.08
2019-11-14 flow=-201295.29 balance=7036737.79
2019-11-15 flow=4365000 balance=11401737.79
2019-11-17 flow=-234390.87 balance=11167346.92
2019-11-19 flow=-240706.45 balance=10926640.47
2019-11-27 flow=-234390.87 balance=10692249.6
```
- Projected event attribution:
```json
[
  {
    "amount": "1140000",
    "category": "rent",
    "currency": "IDR",
    "date": "2019-09-04",
    "description": "Landlord standing order",
    "event_id": "event_212@2019-09-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_212"
  },
  {
    "amount": "303042.45",
    "category": "utilities",
    "currency": "IDR",
    "date": "2019-09-08",
    "description": "Water and power payment",
    "event_id": "event_213@2019-09-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_213"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-09-08",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-09-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "117800",
    "category": "streaming",
    "currency": "IDR",
    "date": "2019-09-11",
    "description": "Video streaming plan",
    "event_id": "event_215@2019-09-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_215"
  },
  {
    "amount": "20900",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2019-09-14",
    "description": "Shared storage plan",
    "event_id": "event_214@2019-09-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_214"
  },
  {
    "amount": "180395.29",
    "category": "shopping",
    "currency": "IDR",
    "date": "2019-09-14",
    "description": "Clothing and household items",
    "event_id": "event_216@2019-09-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_216"
  },
  {
    "amount": "4365000",
    "category": "salary",
    "currency": "IDR",
    "date": "2019-09-15",
    "description": "Payroll credit",
    "event_id": "event_210@2019-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_210"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-09-18",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-09-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "240706.45",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-09-19",
    "description": "Local market purchase",
    "event_id": "event_233@2019-09-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_233"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-09-28",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-09-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "1140000",
    "category": "rent",
    "currency": "IDR",
    "date": "2019-10-04",
    "description": "Landlord standing order",
    "event_id": "event_212@2019-10-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_212"
  },
  {
    "amount": "303042.45",
    "category": "utilities",
    "currency": "IDR",
    "date": "2019-10-08",
    "description": "Water and power payment",
    "event_id": "event_213@2019-10-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_213"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-10-08",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-10-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "117800",
    "category": "streaming",
    "currency": "IDR",
    "date": "2019-10-11",
    "description": "Video streaming plan",
    "event_id": "event_215@2019-10-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_215"
  },
  {
    "amount": "20900",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2019-10-14",
    "description": "Shared storage plan",
    "event_id": "event_214@2019-10-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_214"
  },
  {
    "amount": "180395.29",
    "category": "shopping",
    "currency": "IDR",
    "date": "2019-10-14",
    "description": "Clothing and household items",
    "event_id": "event_216@2019-10-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_216"
  },
  {
    "amount": "4365000",
    "category": "salary",
    "currency": "IDR",
    "date": "2019-10-15",
    "description": "Payroll credit",
    "event_id": "event_210@2019-10-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_210"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-10-18",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-10-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "240706.45",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-10-19",
    "description": "Local market purchase",
    "event_id": "event_233@2019-10-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_233"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-10-28",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-10-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "1140000",
    "category": "rent",
    "currency": "IDR",
    "date": "2019-11-04",
    "description": "Landlord standing order",
    "event_id": "event_212@2019-11-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_212"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-11-07",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-11-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "303042.45",
    "category": "utilities",
    "currency": "IDR",
    "date": "2019-11-08",
    "description": "Water and power payment",
    "event_id": "event_213@2019-11-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_213"
  },
  {
    "amount": "117800",
    "category": "streaming",
    "currency": "IDR",
    "date": "2019-11-11",
    "description": "Video streaming plan",
    "event_id": "event_215@2019-11-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_215"
  },
  {
    "amount": "20900",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2019-11-14",
    "description": "Shared storage plan",
    "event_id": "event_214@2019-11-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_214"
  },
  {
    "amount": "180395.29",
    "category": "shopping",
    "currency": "IDR",
    "date": "2019-11-14",
    "description": "Clothing and household items",
    "event_id": "event_216@2019-11-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_216"
  },
  {
    "amount": "4365000",
    "category": "salary",
    "currency": "IDR",
    "date": "2019-11-15",
    "description": "Payroll credit",
    "event_id": "event_210@2019-11-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_210"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-11-17",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-11-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  },
  {
    "amount": "240706.45",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-11-19",
    "description": "Local market purchase",
    "event_id": "event_233@2019-11-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_233"
  },
  {
    "amount": "234390.87",
    "category": "groceries",
    "currency": "IDR",
    "date": "2019-11-27",
    "description": "Bulk pantry shop",
    "event_id": "event_219@2019-11-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_219"
  }
]
```

## `request_04` / `user_04`

- Opening/minimum: `52206950` / `30686600`
- Expected safe amount: `8401800`; actual: `11584778.17`
- Expected earliest: `2024-06-15`; actual: `2024-06-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2024-06-05 flow=-2033868.83 balance=50173081.17
2024-06-09 flow=-2058276.9 balance=48114804.27
2024-06-10 flow=-332500 balance=47782304.27
2024-06-11 flow=-1704300 balance=46078004.27
2024-06-12 flow=-377150 balance=45700854.27
2024-06-13 flow=-3429476.1 balance=42271378.17
2024-06-15 flow=38190000 balance=80461378.17
2024-06-16 flow=-1030376.9 balance=79431001.27
2024-06-23 flow=-1030376.9 balance=78400624.37
2024-06-26 flow=-889762.96 balance=77510861.41
2024-06-29 flow=-1809752.54 balance=75701108.87
2024-06-30 flow=-1030376.9 balance=74670731.97
2024-07-01 flow=-12293000 balance=62377731.97
2024-07-05 flow=-2033868.83 balance=60343863.14
2024-07-07 flow=-1030376.9 balance=59313486.24
2024-07-09 flow=-1027900 balance=58285586.24
2024-07-10 flow=-332500 balance=57953086.24
2024-07-12 flow=-377150 balance=57575936.24
2024-07-13 flow=-3429476.1 balance=54146460.14
2024-07-14 flow=-1030376.9 balance=53116083.24
2024-07-15 flow=38190000 balance=91306083.24
2024-07-21 flow=-1030376.9 balance=90275706.34
2024-07-27 flow=-889762.96 balance=89385943.38
2024-07-28 flow=-1030376.9 balance=88355566.48
2024-08-01 flow=-12293000 balance=76062566.48
2024-08-03 flow=-1809752.54 balance=74252813.94
2024-08-04 flow=-1030376.9 balance=73222437.04
2024-08-05 flow=-2033868.83 balance=71188568.21
2024-08-09 flow=-1027900 balance=70160668.21
2024-08-10 flow=-332500 balance=69828168.21
2024-08-11 flow=-1030376.9 balance=68797791.31
2024-08-12 flow=-377150 balance=68420641.31
2024-08-13 flow=-3429476.1 balance=64991165.21
2024-08-15 flow=38190000 balance=103181165.21
2024-08-18 flow=-1030376.9 balance=102150788.31
2024-08-25 flow=-1030376.9 balance=101120411.41
2024-08-27 flow=-889762.96 balance=100230648.45
2024-09-01 flow=-13323376.9 balance=86907271.55
```
- Projected event attribution:
```json
[
  {
    "amount": "2033868.83",
    "category": "utilities",
    "currency": "IDR",
    "date": "2024-06-05",
    "description": "Municipal utilities",
    "event_id": "event_286@2024-06-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_286"
  },
  {
    "amount": "1027900",
    "category": "gym",
    "currency": "IDR",
    "date": "2024-06-09",
    "description": "Gym membership",
    "event_id": "event_289@2024-06-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_289"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-09",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-06-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "332500",
    "category": "music_subscription",
    "currency": "IDR",
    "date": "2024-06-10",
    "description": "Music service subscription",
    "event_id": "event_287@2024-06-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_287"
  },
  {
    "amount": "377150",
    "category": "delivery_membership",
    "currency": "IDR",
    "date": "2024-06-12",
    "description": "Food delivery membership",
    "event_id": "event_288@2024-06-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_288"
  },
  {
    "amount": "1542620",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2024-06-13",
    "description": "Local event tickets",
    "event_id": "event_290@2024-06-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_290"
  },
  {
    "amount": "1886856.1",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-06-13",
    "description": "Bakery and snacks",
    "event_id": "event_355@2024-06-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_355"
  },
  {
    "amount": "38190000",
    "category": "salary",
    "currency": "IDR",
    "date": "2024-06-15",
    "description": "Payroll credit",
    "event_id": "event_284@2024-06-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_284"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-16",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-06-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-23",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-06-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "889762.96",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-26",
    "description": "Parking and tolls",
    "event_id": "event_342@2024-06-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_342"
  },
  {
    "amount": "1809752.54",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-06-29",
    "description": "Local market purchase",
    "event_id": "event_316@2024-06-29",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_316"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-30",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-06-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "12293000",
    "category": "rent",
    "currency": "IDR",
    "date": "2024-07-01",
    "description": "Residential rent payment",
    "event_id": "event_291@2024-07-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_291"
  },
  {
    "amount": "2033868.83",
    "category": "utilities",
    "currency": "IDR",
    "date": "2024-07-05",
    "description": "Municipal utilities",
    "event_id": "event_286@2024-07-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_286"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-07-07",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-07-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "1027900",
    "category": "gym",
    "currency": "IDR",
    "date": "2024-07-09",
    "description": "Gym membership",
    "event_id": "event_289@2024-07-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_289"
  },
  {
    "amount": "332500",
    "category": "music_subscription",
    "currency": "IDR",
    "date": "2024-07-10",
    "description": "Music service subscription",
    "event_id": "event_287@2024-07-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_287"
  },
  {
    "amount": "377150",
    "category": "delivery_membership",
    "currency": "IDR",
    "date": "2024-07-12",
    "description": "Food delivery membership",
    "event_id": "event_288@2024-07-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_288"
  },
  {
    "amount": "1542620",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2024-07-13",
    "description": "Local event tickets",
    "event_id": "event_290@2024-07-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_290"
  },
  {
    "amount": "1886856.1",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-07-13",
    "description": "Bakery and snacks",
    "event_id": "event_355@2024-07-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_355"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-07-14",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-07-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "38190000",
    "category": "salary",
    "currency": "IDR",
    "date": "2024-07-15",
    "description": "Payroll credit",
    "event_id": "event_284@2024-07-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_284"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-07-21",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-07-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "889762.96",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-07-27",
    "description": "Parking and tolls",
    "event_id": "event_342@2024-07-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_342"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-07-28",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-07-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "12293000",
    "category": "rent",
    "currency": "IDR",
    "date": "2024-08-01",
    "description": "Residential rent payment",
    "event_id": "event_291@2024-08-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_291"
  },
  {
    "amount": "1809752.54",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-08-03",
    "description": "Local market purchase",
    "event_id": "event_316@2024-08-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_316"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-08-04",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-08-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "2033868.83",
    "category": "utilities",
    "currency": "IDR",
    "date": "2024-08-05",
    "description": "Municipal utilities",
    "event_id": "event_286@2024-08-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_286"
  },
  {
    "amount": "1027900",
    "category": "gym",
    "currency": "IDR",
    "date": "2024-08-09",
    "description": "Gym membership",
    "event_id": "event_289@2024-08-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_289"
  },
  {
    "amount": "332500",
    "category": "music_subscription",
    "currency": "IDR",
    "date": "2024-08-10",
    "description": "Music service subscription",
    "event_id": "event_287@2024-08-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_287"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-08-11",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-08-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "377150",
    "category": "delivery_membership",
    "currency": "IDR",
    "date": "2024-08-12",
    "description": "Food delivery membership",
    "event_id": "event_288@2024-08-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_288"
  },
  {
    "amount": "1542620",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2024-08-13",
    "description": "Local event tickets",
    "event_id": "event_290@2024-08-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_290"
  },
  {
    "amount": "1886856.1",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-08-13",
    "description": "Bakery and snacks",
    "event_id": "event_355@2024-08-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_355"
  },
  {
    "amount": "38190000",
    "category": "salary",
    "currency": "IDR",
    "date": "2024-08-15",
    "description": "Payroll credit",
    "event_id": "event_284@2024-08-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_284"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-08-18",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-08-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-08-25",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-08-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  },
  {
    "amount": "889762.96",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-08-27",
    "description": "Parking and tolls",
    "event_id": "event_342@2024-08-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_342"
  },
  {
    "amount": "12293000",
    "category": "rent",
    "currency": "IDR",
    "date": "2024-09-01",
    "description": "Residential rent payment",
    "event_id": "event_291@2024-09-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_291"
  },
  {
    "amount": "1030376.9",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-09-01",
    "description": "Ride-hailing trip",
    "event_id": "event_341@2024-09-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_341"
  }
]
```

## `request_05` / `user_05`

- Opening/minimum: `46475.1` / `13100`
- Expected safe amount: `737`; actual: `7006.21`
- Expected earliest: ``; actual: ``
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2025-11-06 flow=-750.89 balance=45724.21
2025-11-10 flow=-722.37 balance=45001.84
2025-11-11 flow=-968 balance=44033.84
2025-11-12 flow=-535.97 balance=43497.87
2025-11-13 flow=-840.4 balance=42657.47
2025-12-02 flow=-4972 balance=37685.47
2025-12-06 flow=-750.89 balance=36934.58
2025-12-10 flow=-722.37 balance=36212.21
2025-12-11 flow=-968 balance=35244.21
2025-12-12 flow=-535.97 balance=34708.24
2025-12-13 flow=-840.4 balance=33867.84
2026-01-02 flow=-4972 balance=28895.84
2026-01-06 flow=-750.89 balance=28144.95
2026-01-10 flow=-722.37 balance=27422.58
2026-01-11 flow=-968 balance=26454.58
2026-01-12 flow=-535.97 balance=25918.61
2026-01-13 flow=-840.4 balance=25078.21
2026-02-02 flow=-4972 balance=20106.21
```
- Projected event attribution:
```json
[
  {
    "amount": "750.89",
    "category": "utilities",
    "currency": "ZAR",
    "date": "2025-11-06",
    "description": "Municipal utilities",
    "event_id": "event_392@2025-11-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_392"
  },
  {
    "amount": "722.37",
    "category": "healthcare",
    "currency": "ZAR",
    "date": "2025-11-10",
    "description": "Therapy appointment",
    "event_id": "event_394@2025-11-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_394"
  },
  {
    "amount": "968",
    "category": "debt_repayment",
    "currency": "ZAR",
    "date": "2025-11-11",
    "description": "Vehicle loan payment",
    "event_id": "event_393@2025-11-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_393"
  },
  {
    "amount": "113.3",
    "category": "cloud_storage",
    "currency": "ZAR",
    "date": "2025-11-12",
    "description": "Cloud storage plan",
    "event_id": "event_396@2025-11-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_396"
  },
  {
    "amount": "422.67",
    "category": "shopping",
    "currency": "ZAR",
    "date": "2025-11-12",
    "description": "Personal shopping",
    "event_id": "event_397@2025-11-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_397"
  },
  {
    "amount": "840.4",
    "category": "family_support",
    "currency": "ZAR",
    "date": "2025-11-13",
    "description": "Dependent care payment",
    "event_id": "event_395@2025-11-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_395"
  },
  {
    "amount": "4972",
    "category": "rent",
    "currency": "ZAR",
    "date": "2025-12-02",
    "description": "Apartment rent transfer",
    "event_id": "event_398@2025-12-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_398"
  },
  {
    "amount": "750.89",
    "category": "utilities",
    "currency": "ZAR",
    "date": "2025-12-06",
    "description": "Municipal utilities",
    "event_id": "event_392@2025-12-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_392"
  },
  {
    "amount": "722.37",
    "category": "healthcare",
    "currency": "ZAR",
    "date": "2025-12-10",
    "description": "Therapy appointment",
    "event_id": "event_394@2025-12-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_394"
  },
  {
    "amount": "968",
    "category": "debt_repayment",
    "currency": "ZAR",
    "date": "2025-12-11",
    "description": "Vehicle loan payment",
    "event_id": "event_393@2025-12-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_393"
  },
  {
    "amount": "113.3",
    "category": "cloud_storage",
    "currency": "ZAR",
    "date": "2025-12-12",
    "description": "Cloud storage plan",
    "event_id": "event_396@2025-12-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_396"
  },
  {
    "amount": "422.67",
    "category": "shopping",
    "currency": "ZAR",
    "date": "2025-12-12",
    "description": "Personal shopping",
    "event_id": "event_397@2025-12-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_397"
  },
  {
    "amount": "840.4",
    "category": "family_support",
    "currency": "ZAR",
    "date": "2025-12-13",
    "description": "Dependent care payment",
    "event_id": "event_395@2025-12-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_395"
  },
  {
    "amount": "4972",
    "category": "rent",
    "currency": "ZAR",
    "date": "2026-01-02",
    "description": "Apartment rent transfer",
    "event_id": "event_398@2026-01-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_398"
  },
  {
    "amount": "750.89",
    "category": "utilities",
    "currency": "ZAR",
    "date": "2026-01-06",
    "description": "Municipal utilities",
    "event_id": "event_392@2026-01-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_392"
  },
  {
    "amount": "722.37",
    "category": "healthcare",
    "currency": "ZAR",
    "date": "2026-01-10",
    "description": "Therapy appointment",
    "event_id": "event_394@2026-01-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_394"
  },
  {
    "amount": "968",
    "category": "debt_repayment",
    "currency": "ZAR",
    "date": "2026-01-11",
    "description": "Vehicle loan payment",
    "event_id": "event_393@2026-01-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_393"
  },
  {
    "amount": "113.3",
    "category": "cloud_storage",
    "currency": "ZAR",
    "date": "2026-01-12",
    "description": "Cloud storage plan",
    "event_id": "event_396@2026-01-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_396"
  },
  {
    "amount": "422.67",
    "category": "shopping",
    "currency": "ZAR",
    "date": "2026-01-12",
    "description": "Personal shopping",
    "event_id": "event_397@2026-01-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_397"
  },
  {
    "amount": "840.4",
    "category": "family_support",
    "currency": "ZAR",
    "date": "2026-01-13",
    "description": "Dependent care payment",
    "event_id": "event_395@2026-01-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_395"
  },
  {
    "amount": "4972",
    "category": "rent",
    "currency": "ZAR",
    "date": "2026-02-02",
    "description": "Apartment rent transfer",
    "event_id": "event_398@2026-02-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_398"
  }
]
```

## `request_06` / `user_06`

- Opening/minimum: `1942.4` / `800`
- Expected safe amount: `603.3`; actual: `620.4`
- Expected earliest: `2026-01-15`; actual: `2026-01-03`
- Classified differences:
```json
{
  "affordability_status": "safe-payment eligibility derived from the forecast predicate",
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate",
  "spending_changes_needed": "spending-change enumeration/provenance or forecast binding trough"
}
```
- Future flow and balance path:
```text
2026-01-03 flow=-254.1 balance=1688.3
2026-01-07 flow=-110.53 balance=1577.77
2026-01-08 flow=-26 balance=1551.77
2026-01-10 flow=-19 balance=1532.77
2026-01-11 flow=-57.57 balance=1475.2
2026-01-13 flow=-44.88 balance=1430.32
2026-01-15 flow=967.5 balance=2397.82
2026-01-17 flow=-51.55 balance=2346.27
2026-01-19 flow=-48.32 balance=2297.95
2026-01-25 flow=-57.57 balance=2240.38
2026-01-27 flow=-51.55 balance=2188.83
2026-02-03 flow=-254.1 balance=1934.73
2026-02-06 flow=-51.55 balance=1883.18
2026-02-07 flow=-58.98 balance=1824.2
2026-02-08 flow=-83.57 balance=1740.63
2026-02-10 flow=-19 balance=1721.63
2026-02-13 flow=-44.88 balance=1676.75
2026-02-15 flow=1402.67 balance=3079.42
2026-02-16 flow=-83.24 balance=2996.18
2026-02-19 flow=-48.32 balance=2947.86
2026-02-22 flow=-57.57 balance=2890.29
2026-02-26 flow=-51.55 balance=2838.74
2026-03-03 flow=-254.1 balance=2584.64
2026-03-07 flow=-58.98 balance=2525.66
2026-03-08 flow=-135.12 balance=2390.54
2026-03-10 flow=-19 balance=2371.54
2026-03-13 flow=-44.88 balance=2326.66
2026-03-15 flow=1402.67 balance=3729.33
2026-03-18 flow=-51.55 balance=3677.78
2026-03-19 flow=-48.32 balance=3629.46
2026-03-20 flow=-31.69 balance=3597.77
2026-03-22 flow=-57.57 balance=3540.2
2026-03-28 flow=-51.55 balance=3488.65
```
- Projected event attribution:
```json
[
  {
    "amount": "254.1",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-01-03",
    "description": "Monthly rent",
    "event_id": "event_472@2026-01-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_472"
  },
  {
    "amount": "58.98",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-01-07",
    "description": "Water and power payment",
    "event_id": "event_473@2026-01-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_473"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-01-07",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-01-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "26",
    "category": "insurance",
    "currency": "EUR",
    "date": "2026-01-08",
    "description": "Vehicle insurance premium",
    "event_id": "event_474@2026-01-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_474"
  },
  {
    "amount": "19",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-01-10",
    "description": "Family streaming plan",
    "event_id": "event_476@2026-01-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_476"
  },
  {
    "amount": "57.57",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-01-11",
    "description": "Neighbourhood restaurant",
    "event_id": "event_552@2026-01-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_552"
  },
  {
    "amount": "5",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2026-01-13",
    "description": "Shared storage plan",
    "event_id": "event_475@2026-01-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_475"
  },
  {
    "amount": "39.88",
    "category": "shopping",
    "currency": "EUR",
    "date": "2026-01-13",
    "description": "Household shopping",
    "event_id": "event_477@2026-01-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_477"
  },
  {
    "amount": "38.33",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2026-01-15",
    "description": "Monthly entertainment spend",
    "event_id": "event_478@2026-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_478"
  },
  {
    "amount": "31.69",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-01-15",
    "description": "Metro and bus fares",
    "event_id": "event_528@2026-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_528"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-01-17",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-01-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "48.32",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-01-19",
    "description": "Grocery delivery",
    "event_id": "event_486@2026-01-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_486"
  },
  {
    "amount": "57.57",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-01-25",
    "description": "Neighbourhood restaurant",
    "event_id": "event_552@2026-01-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_552"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-01-27",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-01-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "254.1",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-02-03",
    "description": "Monthly rent",
    "event_id": "event_472@2026-02-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_472"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-02-06",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-02-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "58.98",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-02-07",
    "description": "Water and power payment",
    "event_id": "event_473@2026-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_473"
  },
  {
    "amount": "26",
    "category": "insurance",
    "currency": "EUR",
    "date": "2026-02-08",
    "description": "Vehicle insurance premium",
    "event_id": "event_474@2026-02-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_474"
  },
  {
    "amount": "57.57",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-02-08",
    "description": "Neighbourhood restaurant",
    "event_id": "event_552@2026-02-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_552"
  },
  {
    "amount": "19",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-02-10",
    "description": "Family streaming plan",
    "event_id": "event_476@2026-02-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_476"
  },
  {
    "amount": "5",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2026-02-13",
    "description": "Shared storage plan",
    "event_id": "event_475@2026-02-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_475"
  },
  {
    "amount": "39.88",
    "category": "shopping",
    "currency": "EUR",
    "date": "2026-02-13",
    "description": "Household shopping",
    "event_id": "event_477@2026-02-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_477"
  },
  {
    "amount": "1441",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-02-15",
    "description": "Payroll credit",
    "event_id": "event_471@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_471"
  },
  {
    "amount": "38.33",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2026-02-15",
    "description": "Monthly entertainment spend",
    "event_id": "event_478@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_478"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-02-16",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-02-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "31.69",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-02-16",
    "description": "Metro and bus fares",
    "event_id": "event_528@2026-02-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_528"
  },
  {
    "amount": "48.32",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-02-19",
    "description": "Grocery delivery",
    "event_id": "event_486@2026-02-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_486"
  },
  {
    "amount": "57.57",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-02-22",
    "description": "Neighbourhood restaurant",
    "event_id": "event_552@2026-02-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_552"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-02-26",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-02-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "254.1",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-03-03",
    "description": "Monthly rent",
    "event_id": "event_472@2026-03-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_472"
  },
  {
    "amount": "58.98",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-03-07",
    "description": "Water and power payment",
    "event_id": "event_473@2026-03-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_473"
  },
  {
    "amount": "26",
    "category": "insurance",
    "currency": "EUR",
    "date": "2026-03-08",
    "description": "Vehicle insurance premium",
    "event_id": "event_474@2026-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_474"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-03-08",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "57.57",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-03-08",
    "description": "Neighbourhood restaurant",
    "event_id": "event_552@2026-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_552"
  },
  {
    "amount": "19",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-03-10",
    "description": "Family streaming plan",
    "event_id": "event_476@2026-03-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_476"
  },
  {
    "amount": "5",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2026-03-13",
    "description": "Shared storage plan",
    "event_id": "event_475@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_475"
  },
  {
    "amount": "39.88",
    "category": "shopping",
    "currency": "EUR",
    "date": "2026-03-13",
    "description": "Household shopping",
    "event_id": "event_477@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_477"
  },
  {
    "amount": "1441",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-03-15",
    "description": "Payroll credit",
    "event_id": "event_471@2026-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_471"
  },
  {
    "amount": "38.33",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2026-03-15",
    "description": "Monthly entertainment spend",
    "event_id": "event_478@2026-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_478"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-03-18",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-03-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  },
  {
    "amount": "48.32",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-03-19",
    "description": "Grocery delivery",
    "event_id": "event_486@2026-03-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_486"
  },
  {
    "amount": "31.69",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-03-20",
    "description": "Metro and bus fares",
    "event_id": "event_528@2026-03-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_528"
  },
  {
    "amount": "57.57",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-03-22",
    "description": "Neighbourhood restaurant",
    "event_id": "event_552@2026-03-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_552"
  },
  {
    "amount": "51.55",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-03-28",
    "description": "Fresh food shop",
    "event_id": "event_489@2026-03-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_489"
  }
]
```

## `request_07` / `user_07`

- Opening/minimum: `218945.56` / `93000`
- Expected safe amount: `87170.56`; actual: `98080.53`
- Expected earliest: `2024-10-23`; actual: `2024-10-23`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2024-09-08 flow=-7387.41 balance=211558.15
2024-09-13 flow=-16655 balance=194903.15
2024-09-20 flow=-3822.62 balance=191080.53
2024-09-23 flow=149000 balance=340080.53
2024-10-04 flow=-34200 balance=305880.53
2024-10-08 flow=-7387.41 balance=298493.12
2024-10-11 flow=-3822.62 balance=294670.5
2024-10-13 flow=-16655 balance=278015.5
2024-10-23 flow=149000 balance=427015.5
2024-11-01 flow=-3822.62 balance=423192.88
2024-11-04 flow=-34200 balance=388992.88
2024-11-08 flow=-7387.41 balance=381605.47
2024-11-13 flow=-16655 balance=364950.47
2024-11-22 flow=-3822.62 balance=361127.85
2024-11-23 flow=149000 balance=510127.85
```
- Projected event attribution:
```json
[
  {
    "amount": "7387.41",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-09-08",
    "description": "Electricity bill",
    "event_id": "event_580@2024-09-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_580"
  },
  {
    "amount": "15650",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2024-09-13",
    "description": "Personal loan payment",
    "event_id": "event_581@2024-09-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_581"
  },
  {
    "amount": "1005",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2024-09-13",
    "description": "Music subscription",
    "event_id": "event_582@2024-09-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_582"
  },
  {
    "amount": "3822.62",
    "category": "transport",
    "currency": "INR",
    "date": "2024-09-20",
    "description": "Rail pass",
    "event_id": "event_604@2024-09-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_604"
  },
  {
    "amount": "34200",
    "category": "rent",
    "currency": "INR",
    "date": "2024-10-04",
    "description": "Monthly rent",
    "event_id": "event_583@2024-10-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_583"
  },
  {
    "amount": "7387.41",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-10-08",
    "description": "Electricity bill",
    "event_id": "event_580@2024-10-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_580"
  },
  {
    "amount": "3822.62",
    "category": "transport",
    "currency": "INR",
    "date": "2024-10-11",
    "description": "Rail pass",
    "event_id": "event_604@2024-10-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_604"
  },
  {
    "amount": "15650",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2024-10-13",
    "description": "Personal loan payment",
    "event_id": "event_581@2024-10-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_581"
  },
  {
    "amount": "1005",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2024-10-13",
    "description": "Music subscription",
    "event_id": "event_582@2024-10-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_582"
  },
  {
    "amount": "149000",
    "category": "salary",
    "currency": "INR",
    "date": "2024-10-23",
    "description": "Payroll credit",
    "event_id": "event_578@2024-10-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_578"
  },
  {
    "amount": "3822.62",
    "category": "transport",
    "currency": "INR",
    "date": "2024-11-01",
    "description": "Rail pass",
    "event_id": "event_604@2024-11-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_604"
  },
  {
    "amount": "34200",
    "category": "rent",
    "currency": "INR",
    "date": "2024-11-04",
    "description": "Monthly rent",
    "event_id": "event_583@2024-11-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_583"
  },
  {
    "amount": "7387.41",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-11-08",
    "description": "Electricity bill",
    "event_id": "event_580@2024-11-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_580"
  },
  {
    "amount": "15650",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2024-11-13",
    "description": "Personal loan payment",
    "event_id": "event_581@2024-11-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_581"
  },
  {
    "amount": "1005",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2024-11-13",
    "description": "Music subscription",
    "event_id": "event_582@2024-11-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_582"
  },
  {
    "amount": "3822.62",
    "category": "transport",
    "currency": "INR",
    "date": "2024-11-22",
    "description": "Rail pass",
    "event_id": "event_604@2024-11-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_604"
  },
  {
    "amount": "149000",
    "category": "salary",
    "currency": "INR",
    "date": "2024-11-23",
    "description": "Payroll credit",
    "event_id": "event_578@2024-11-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_578"
  }
]
```

## `request_08` / `user_08`

- Opening/minimum: `1536.57` / `800`
- Expected safe amount: `284.57`; actual: `383.59`
- Expected earliest: `2025-04-15`; actual: `2025-04-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2025-02-07 flow=-89 balance=1447.57
2025-02-10 flow=-239.98 balance=1207.59
2025-02-12 flow=-24 balance=1183.59
2025-02-15 flow=1422.85 balance=2606.44
2025-02-18 flow=-74.35 balance=2532.09
2025-02-26 flow=-106.74 balance=2425.35
2025-03-01 flow=-467.5 balance=1957.85
2025-03-04 flow=-74.35 balance=1883.5
2025-03-05 flow=-82.61 balance=1800.89
2025-03-07 flow=-89 balance=1711.89
2025-03-10 flow=-239.98 balance=1471.91
2025-03-12 flow=-24 balance=1447.91
2025-03-15 flow=1422.85 balance=2870.76
2025-03-18 flow=-74.35 balance=2796.41
2025-03-19 flow=-46.08 balance=2750.33
2025-03-26 flow=-60.66 balance=2689.67
2025-04-01 flow=-541.85 balance=2147.82
2025-04-05 flow=-82.61 balance=2065.21
2025-04-07 flow=-89 balance=1976.21
2025-04-09 flow=-46.08 balance=1930.13
2025-04-10 flow=-239.98 balance=1690.15
2025-04-12 flow=-24 balance=1666.15
2025-04-15 flow=1348.5 balance=3014.65
2025-04-26 flow=-60.66 balance=2953.99
2025-04-29 flow=-74.35 balance=2879.64
2025-04-30 flow=-46.08 balance=2833.56
2025-05-01 flow=-467.5 balance=2366.06
2025-05-05 flow=-82.61 balance=2283.45
2025-05-07 flow=-89 balance=2194.45
```
- Projected event attribution:
```json
[
  {
    "amount": "89",
    "category": "education",
    "currency": "EUR",
    "date": "2025-02-07",
    "description": "School fee payment",
    "event_id": "event_646@2025-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_646"
  },
  {
    "amount": "177",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2025-02-10",
    "description": "Personal loan payment",
    "event_id": "event_647@2025-02-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_647"
  },
  {
    "amount": "14",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2025-02-10",
    "description": "Music subscription",
    "event_id": "event_648@2025-02-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_648"
  },
  {
    "amount": "48.98",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-02-10",
    "description": "Neighbourhood restaurant",
    "event_id": "event_708@2025-02-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_708"
  },
  {
    "amount": "24",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2025-02-12",
    "description": "Grocery delivery membership",
    "event_id": "event_649@2025-02-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_649"
  },
  {
    "amount": "74.35",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-02-18",
    "description": "Fresh food shop",
    "event_id": "event_661@2025-02-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_661"
  },
  {
    "amount": "46.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-02-26",
    "description": "Parking and tolls",
    "event_id": "event_697@2025-02-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_697"
  },
  {
    "amount": "60.66",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-02-26",
    "description": "Family dinner",
    "event_id": "event_707@2025-02-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_707"
  },
  {
    "amount": "467.5",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-03-01",
    "description": "Apartment rent transfer",
    "event_id": "event_650@2025-03-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_650"
  },
  {
    "amount": "74.35",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-03-04",
    "description": "Fresh food shop",
    "event_id": "event_661@2025-03-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_661"
  },
  {
    "amount": "82.61",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-03-05",
    "description": "Municipal utilities",
    "event_id": "event_651@2025-03-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_651"
  },
  {
    "amount": "89",
    "category": "education",
    "currency": "EUR",
    "date": "2025-03-07",
    "description": "School fee payment",
    "event_id": "event_646@2025-03-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_646"
  },
  {
    "amount": "177",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2025-03-10",
    "description": "Personal loan payment",
    "event_id": "event_647@2025-03-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_647"
  },
  {
    "amount": "14",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2025-03-10",
    "description": "Music subscription",
    "event_id": "event_648@2025-03-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_648"
  },
  {
    "amount": "48.98",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-03-10",
    "description": "Neighbourhood restaurant",
    "event_id": "event_708@2025-03-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_708"
  },
  {
    "amount": "24",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2025-03-12",
    "description": "Grocery delivery membership",
    "event_id": "event_649@2025-03-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_649"
  },
  {
    "amount": "1422.85",
    "category": "salary",
    "currency": "EUR",
    "date": "2025-03-15",
    "description": "Payroll credit",
    "event_id": "event_643@2025-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_643"
  },
  {
    "amount": "74.35",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-03-18",
    "description": "Fresh food shop",
    "event_id": "event_661@2025-03-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_661"
  },
  {
    "amount": "46.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-03-19",
    "description": "Parking and tolls",
    "event_id": "event_697@2025-03-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_697"
  },
  {
    "amount": "60.66",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-03-26",
    "description": "Family dinner",
    "event_id": "event_707@2025-03-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_707"
  },
  {
    "amount": "467.5",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-04-01",
    "description": "Apartment rent transfer",
    "event_id": "event_650@2025-04-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_650"
  },
  {
    "amount": "74.35",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-04-01",
    "description": "Fresh food shop",
    "event_id": "event_661@2025-04-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_661"
  },
  {
    "amount": "82.61",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-04-05",
    "description": "Municipal utilities",
    "event_id": "event_651@2025-04-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_651"
  },
  {
    "amount": "89",
    "category": "education",
    "currency": "EUR",
    "date": "2025-04-07",
    "description": "School fee payment",
    "event_id": "event_646@2025-04-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_646"
  },
  {
    "amount": "46.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-04-09",
    "description": "Parking and tolls",
    "event_id": "event_697@2025-04-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_697"
  },
  {
    "amount": "177",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2025-04-10",
    "description": "Personal loan payment",
    "event_id": "event_647@2025-04-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_647"
  },
  {
    "amount": "14",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2025-04-10",
    "description": "Music subscription",
    "event_id": "event_648@2025-04-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_648"
  },
  {
    "amount": "48.98",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-04-10",
    "description": "Neighbourhood restaurant",
    "event_id": "event_708@2025-04-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_708"
  },
  {
    "amount": "24",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2025-04-12",
    "description": "Grocery delivery membership",
    "event_id": "event_649@2025-04-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_649"
  },
  {
    "amount": "1422.85",
    "category": "salary",
    "currency": "EUR",
    "date": "2025-04-15",
    "description": "Payroll credit",
    "event_id": "event_643@2025-04-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_643"
  },
  {
    "amount": "74.35",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-04-15",
    "description": "Fresh food shop",
    "event_id": "event_661@2025-04-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_661"
  },
  {
    "amount": "60.66",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-04-26",
    "description": "Family dinner",
    "event_id": "event_707@2025-04-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_707"
  },
  {
    "amount": "74.35",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-04-29",
    "description": "Fresh food shop",
    "event_id": "event_661@2025-04-29",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_661"
  },
  {
    "amount": "46.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-04-30",
    "description": "Parking and tolls",
    "event_id": "event_697@2025-04-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_697"
  },
  {
    "amount": "467.5",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-05-01",
    "description": "Apartment rent transfer",
    "event_id": "event_650@2025-05-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_650"
  },
  {
    "amount": "82.61",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-05-05",
    "description": "Municipal utilities",
    "event_id": "event_651@2025-05-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_651"
  },
  {
    "amount": "89",
    "category": "education",
    "currency": "EUR",
    "date": "2025-05-07",
    "description": "School fee payment",
    "event_id": "event_646@2025-05-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_646"
  }
]
```

## `request_09` / `user_09`

- Opening/minimum: `2231.1` / `600`
- Expected safe amount: `166.61`; actual: `166.61`
- Expected earliest: `2026-07-04`; actual: `2026-07-04`
- Classified differences:
```json
{
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2026-07-06 flow=-71.04 balance=2160.06
2026-07-09 flow=-20 balance=2140.06
2026-07-12 flow=-33.32 balance=2106.74
2026-07-19 flow=-54.9 balance=2051.84
2026-07-20 flow=441.96 balance=2493.8
2026-08-02 flow=-211.2 balance=2282.6
2026-08-06 flow=-71.04 balance=2211.56
2026-08-09 flow=-20 balance=2191.56
2026-08-12 flow=-33.32 balance=2158.24
2026-08-19 flow=-54.9 balance=2103.34
2026-08-20 flow=441.96 balance=2545.3
2026-09-02 flow=-211.2 balance=2334.1
2026-09-06 flow=-71.04 balance=2263.06
2026-09-09 flow=-20 balance=2243.06
2026-09-12 flow=-33.32 balance=2209.74
2026-09-19 flow=-54.9 balance=2154.84
2026-09-20 flow=441.96 balance=2596.8
```
- Projected event attribution:
```json
[
  {
    "amount": "71.04",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-07-06",
    "description": "Water and power payment",
    "event_id": "event_748@2026-07-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_748"
  },
  {
    "amount": "20",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-07-09",
    "description": "Video streaming plan",
    "event_id": "event_750@2026-07-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_750"
  },
  {
    "amount": "5",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2026-07-12",
    "description": "Cloud storage plan",
    "event_id": "event_749@2026-07-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_749"
  },
  {
    "amount": "28.32",
    "category": "shopping",
    "currency": "EUR",
    "date": "2026-07-12",
    "description": "Household shopping",
    "event_id": "event_751@2026-07-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_751"
  },
  {
    "amount": "54.9",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-07-19",
    "description": "Local market purchase",
    "event_id": "event_760@2026-07-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_760"
  },
  {
    "amount": "441.96",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-07-20",
    "description": "Application project payment",
    "event_id": "event_739@2026-07-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_739"
  },
  {
    "amount": "211.2",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-08-02",
    "description": "Monthly rent",
    "event_id": "event_752@2026-08-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_752"
  },
  {
    "amount": "71.04",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-08-06",
    "description": "Water and power payment",
    "event_id": "event_748@2026-08-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_748"
  },
  {
    "amount": "20",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-08-09",
    "description": "Video streaming plan",
    "event_id": "event_750@2026-08-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_750"
  },
  {
    "amount": "5",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2026-08-12",
    "description": "Cloud storage plan",
    "event_id": "event_749@2026-08-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_749"
  },
  {
    "amount": "28.32",
    "category": "shopping",
    "currency": "EUR",
    "date": "2026-08-12",
    "description": "Household shopping",
    "event_id": "event_751@2026-08-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_751"
  },
  {
    "amount": "54.9",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-08-19",
    "description": "Local market purchase",
    "event_id": "event_760@2026-08-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_760"
  },
  {
    "amount": "441.96",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-08-20",
    "description": "Application project payment",
    "event_id": "event_739@2026-08-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_739"
  },
  {
    "amount": "211.2",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-09-02",
    "description": "Monthly rent",
    "event_id": "event_752@2026-09-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_752"
  },
  {
    "amount": "71.04",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-09-06",
    "description": "Water and power payment",
    "event_id": "event_748@2026-09-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_748"
  },
  {
    "amount": "20",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-09-09",
    "description": "Video streaming plan",
    "event_id": "event_750@2026-09-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_750"
  },
  {
    "amount": "5",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2026-09-12",
    "description": "Cloud storage plan",
    "event_id": "event_749@2026-09-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_749"
  },
  {
    "amount": "28.32",
    "category": "shopping",
    "currency": "EUR",
    "date": "2026-09-12",
    "description": "Household shopping",
    "event_id": "event_751@2026-09-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_751"
  },
  {
    "amount": "54.9",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-09-19",
    "description": "Local market purchase",
    "event_id": "event_760@2026-09-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_760"
  },
  {
    "amount": "441.96",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-09-20",
    "description": "Application project payment",
    "event_id": "event_739@2026-09-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_739"
  }
]
```

## `request_10` / `user_10`

- Opening/minimum: `750155` / `225400`
- Expected safe amount: `12700`; actual: `266700`
- Expected earliest: ``; actual: `2024-12-06`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate"
}
```
- Future flow and balance path:
```text
2024-12-06 flow=-6582.39 balance=743572.61
2024-12-07 flow=-17771.13 balance=725801.48
2024-12-10 flow=82667.27 balance=808468.75
2024-12-11 flow=76895.75 balance=885364.5
2024-12-12 flow=-14892.24 balance=870472.26
2024-12-14 flow=-1895 balance=868577.26
2024-12-15 flow=-4883.78 balance=863693.48
2024-12-20 flow=60877.41 balance=924570.89
2024-12-21 flow=81755.75 balance=1006326.64
2024-12-25 flow=82667.27 balance=1088993.91
2024-12-26 flow=-12092.24 balance=1076901.67
2024-12-27 flow=-6582.39 balance=1070319.28
2024-12-31 flow=81755.75 balance=1152075.03
2025-01-03 flow=-69100 balance=1082975.03
2025-01-05 flow=60877.41 balance=1143852.44
2025-01-07 flow=-17771.13 balance=1126081.31
2025-01-09 flow=70575.03 balance=1196656.34
2025-01-10 flow=81755.75 balance=1278412.09
2025-01-11 flow=-4860 balance=1273552.09
2025-01-12 flow=-2800 balance=1270752.09
2025-01-14 flow=-1895 balance=1268857.09
2025-01-15 flow=-4883.78 balance=1263973.31
2025-01-17 flow=-6582.39 balance=1257390.92
2025-01-20 flow=81755.75 balance=1339146.67
2025-01-21 flow=60877.41 balance=1400024.08
2025-01-23 flow=-12092.24 balance=1387931.84
2025-01-24 flow=82667.27 balance=1470599.11
2025-01-30 flow=81755.75 balance=1552354.86
2025-02-03 flow=-69100 balance=1483254.86
2025-02-06 flow=48785.17 balance=1532040.03
2025-02-07 flow=-24353.52 balance=1507686.51
2025-02-08 flow=82667.27 balance=1590353.78
2025-02-09 flow=81755.75 balance=1672109.53
2025-02-11 flow=-4860 balance=1667249.53
2025-02-12 flow=-2800 balance=1664449.53
2025-02-14 flow=-1895 balance=1662554.53
2025-02-15 flow=-4883.78 balance=1657670.75
2025-02-19 flow=81755.75 balance=1739426.5
2025-02-20 flow=-12092.24 balance=1727334.26
2025-02-22 flow=60877.41 balance=1788211.67
2025-02-23 flow=82667.27 balance=1870878.94
2025-02-28 flow=-6582.39 balance=1864296.55
2025-03-01 flow=81755.75 balance=1946052.3
2025-03-03 flow=-69100 balance=1876952.3
```
- Projected event attribution:
```json
[
  {
    "amount": "6582.39",
    "category": "transport",
    "currency": "INR",
    "date": "2024-12-06",
    "description": "Local taxi",
    "event_id": "event_883@2024-12-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_883"
  },
  {
    "amount": "17771.13",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-12-07",
    "description": "Electricity and water bill",
    "event_id": "event_834@2024-12-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_834"
  },
  {
    "amount": "82667.27",
    "category": "salary",
    "currency": "INR",
    "date": "2024-12-10",
    "description": "Delivery platform payout",
    "event_id": "event_832@2024-12-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_832"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2024-12-11",
    "description": "Task marketplace payout",
    "event_id": "event_830@2024-12-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "4860",
    "category": "gym",
    "currency": "INR",
    "date": "2024-12-11",
    "description": "Community fitness plan",
    "event_id": "event_837@2024-12-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_837"
  },
  {
    "amount": "2800",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2024-12-12",
    "description": "Music subscription",
    "event_id": "event_835@2024-12-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_835"
  },
  {
    "amount": "12092.24",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-12-12",
    "description": "Fresh food shop",
    "event_id": "event_865@2024-12-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_865"
  },
  {
    "amount": "1895",
    "category": "delivery_membership",
    "currency": "INR",
    "date": "2024-12-14",
    "description": "Delivery service plan",
    "event_id": "event_836@2024-12-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_836"
  },
  {
    "amount": "4883.78",
    "category": "entertainment",
    "currency": "INR",
    "date": "2024-12-15",
    "description": "Cinema and events",
    "event_id": "event_838@2024-12-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_838"
  },
  {
    "amount": "60877.41",
    "category": "salary",
    "currency": "INR",
    "date": "2024-12-20",
    "description": "Driver platform payout",
    "event_id": "event_839@2024-12-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_839"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2024-12-21",
    "description": "Task marketplace payout",
    "event_id": "event_830@2024-12-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "82667.27",
    "category": "salary",
    "currency": "INR",
    "date": "2024-12-25",
    "description": "Delivery platform payout",
    "event_id": "event_832@2024-12-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_832"
  },
  {
    "amount": "12092.24",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-12-26",
    "description": "Fresh food shop",
    "event_id": "event_865@2024-12-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_865"
  },
  {
    "amount": "6582.39",
    "category": "transport",
    "currency": "INR",
    "date": "2024-12-27",
    "description": "Local taxi",
    "event_id": "event_883@2024-12-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_883"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2024-12-31",
    "description": "Task marketplace payout",
    "event_id": "event_830@2024-12-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "69100",
    "category": "rent",
    "currency": "INR",
    "date": "2025-01-03",
    "description": "Monthly rent",
    "event_id": "event_840@2025-01-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_840"
  },
  {
    "amount": "60877.41",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-05",
    "description": "Driver platform payout",
    "event_id": "event_839@2025-01-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_839"
  },
  {
    "amount": "17771.13",
    "category": "utilities",
    "currency": "INR",
    "date": "2025-01-07",
    "description": "Electricity and water bill",
    "event_id": "event_834@2025-01-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_834"
  },
  {
    "amount": "82667.27",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-09",
    "description": "Delivery platform payout",
    "event_id": "event_832@2025-01-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_832"
  },
  {
    "amount": "12092.24",
    "category": "groceries",
    "currency": "INR",
    "date": "2025-01-09",
    "description": "Fresh food shop",
    "event_id": "event_865@2025-01-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_865"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-10",
    "description": "Task marketplace payout",
    "event_id": "event_830@2025-01-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "4860",
    "category": "gym",
    "currency": "INR",
    "date": "2025-01-11",
    "description": "Community fitness plan",
    "event_id": "event_837@2025-01-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_837"
  },
  {
    "amount": "2800",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2025-01-12",
    "description": "Music subscription",
    "event_id": "event_835@2025-01-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_835"
  },
  {
    "amount": "1895",
    "category": "delivery_membership",
    "currency": "INR",
    "date": "2025-01-14",
    "description": "Delivery service plan",
    "event_id": "event_836@2025-01-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_836"
  },
  {
    "amount": "4883.78",
    "category": "entertainment",
    "currency": "INR",
    "date": "2025-01-15",
    "description": "Cinema and events",
    "event_id": "event_838@2025-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_838"
  },
  {
    "amount": "6582.39",
    "category": "transport",
    "currency": "INR",
    "date": "2025-01-17",
    "description": "Local taxi",
    "event_id": "event_883@2025-01-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_883"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-20",
    "description": "Task marketplace payout",
    "event_id": "event_830@2025-01-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "60877.41",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-21",
    "description": "Driver platform payout",
    "event_id": "event_839@2025-01-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_839"
  },
  {
    "amount": "12092.24",
    "category": "groceries",
    "currency": "INR",
    "date": "2025-01-23",
    "description": "Fresh food shop",
    "event_id": "event_865@2025-01-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_865"
  },
  {
    "amount": "82667.27",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-24",
    "description": "Delivery platform payout",
    "event_id": "event_832@2025-01-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_832"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2025-01-30",
    "description": "Task marketplace payout",
    "event_id": "event_830@2025-01-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "69100",
    "category": "rent",
    "currency": "INR",
    "date": "2025-02-03",
    "description": "Monthly rent",
    "event_id": "event_840@2025-02-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_840"
  },
  {
    "amount": "60877.41",
    "category": "salary",
    "currency": "INR",
    "date": "2025-02-06",
    "description": "Driver platform payout",
    "event_id": "event_839@2025-02-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_839"
  },
  {
    "amount": "12092.24",
    "category": "groceries",
    "currency": "INR",
    "date": "2025-02-06",
    "description": "Fresh food shop",
    "event_id": "event_865@2025-02-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_865"
  },
  {
    "amount": "17771.13",
    "category": "utilities",
    "currency": "INR",
    "date": "2025-02-07",
    "description": "Electricity and water bill",
    "event_id": "event_834@2025-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_834"
  },
  {
    "amount": "6582.39",
    "category": "transport",
    "currency": "INR",
    "date": "2025-02-07",
    "description": "Local taxi",
    "event_id": "event_883@2025-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_883"
  },
  {
    "amount": "82667.27",
    "category": "salary",
    "currency": "INR",
    "date": "2025-02-08",
    "description": "Delivery platform payout",
    "event_id": "event_832@2025-02-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_832"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2025-02-09",
    "description": "Task marketplace payout",
    "event_id": "event_830@2025-02-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "4860",
    "category": "gym",
    "currency": "INR",
    "date": "2025-02-11",
    "description": "Community fitness plan",
    "event_id": "event_837@2025-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_837"
  },
  {
    "amount": "2800",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2025-02-12",
    "description": "Music subscription",
    "event_id": "event_835@2025-02-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_835"
  },
  {
    "amount": "1895",
    "category": "delivery_membership",
    "currency": "INR",
    "date": "2025-02-14",
    "description": "Delivery service plan",
    "event_id": "event_836@2025-02-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_836"
  },
  {
    "amount": "4883.78",
    "category": "entertainment",
    "currency": "INR",
    "date": "2025-02-15",
    "description": "Cinema and events",
    "event_id": "event_838@2025-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_838"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2025-02-19",
    "description": "Task marketplace payout",
    "event_id": "event_830@2025-02-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "12092.24",
    "category": "groceries",
    "currency": "INR",
    "date": "2025-02-20",
    "description": "Fresh food shop",
    "event_id": "event_865@2025-02-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_865"
  },
  {
    "amount": "60877.41",
    "category": "salary",
    "currency": "INR",
    "date": "2025-02-22",
    "description": "Driver platform payout",
    "event_id": "event_839@2025-02-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_839"
  },
  {
    "amount": "82667.27",
    "category": "salary",
    "currency": "INR",
    "date": "2025-02-23",
    "description": "Delivery platform payout",
    "event_id": "event_832@2025-02-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_832"
  },
  {
    "amount": "6582.39",
    "category": "transport",
    "currency": "INR",
    "date": "2025-02-28",
    "description": "Local taxi",
    "event_id": "event_883@2025-02-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_883"
  },
  {
    "amount": "81755.75",
    "category": "salary",
    "currency": "INR",
    "date": "2025-03-01",
    "description": "Task marketplace payout",
    "event_id": "event_830@2025-03-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_830"
  },
  {
    "amount": "69100",
    "category": "rent",
    "currency": "INR",
    "date": "2025-03-03",
    "description": "Monthly rent",
    "event_id": "event_840@2025-03-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_840"
  }
]
```

## `request_11` / `user_11`

- Opening/minimum: `63531795` / `34140600`
- Expected safe amount: `12510645`; actual: `13110000`
- Expected earliest: `2025-07-15`; actual: `2025-05-03`
- Classified differences:
```json
{
  "affordability_status": "safe-payment eligibility derived from the forecast predicate",
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate",
  "spending_changes_needed": "spending-change enumeration/provenance or forecast binding trough"
}
```
- Future flow and balance path:
```text
2025-05-05 flow=-4167404.33 balance=59364390.67
2025-05-08 flow=-2796165.18 balance=56568225.49
2025-05-09 flow=-1881000 balance=54687225.49
2025-05-10 flow=-2544100 balance=52143125.49
2025-05-12 flow=-3165638.3 balance=48977487.19
2025-05-14 flow=-168150 balance=48809337.19
2025-05-15 flow=23256000 balance=72065337.19
2025-05-16 flow=-1674887.61 balance=70390449.58
2025-05-24 flow=36727690.62 balance=107118140.2
2025-06-05 flow=-4167404.33 balance=102950735.87
2025-06-08 flow=-2796165.18 balance=100154570.69
2025-06-09 flow=-1881000 balance=98273570.69
2025-06-10 flow=-2544100 balance=95729470.69
2025-06-12 flow=-3165638.3 balance=92563832.39
2025-06-14 flow=-168150 balance=92395682.39
2025-06-15 flow=23256000 balance=115651682.39
2025-06-16 flow=-1674887.61 balance=113976794.78
2025-06-24 flow=36727690.62 balance=150704485.4
2025-07-05 flow=-4167404.33 balance=146537081.07
2025-07-08 flow=-2796165.18 balance=143740915.89
2025-07-09 flow=-1881000 balance=141859915.89
2025-07-10 flow=-2544100 balance=139315815.89
2025-07-12 flow=-3165638.3 balance=136150177.59
2025-07-14 flow=-168150 balance=135982027.59
2025-07-15 flow=23256000 balance=159238027.59
2025-07-16 flow=-1674887.61 balance=157563139.98
2025-07-24 flow=36727690.62 balance=194290830.6
```
- Projected event attribution:
```json
[
  {
    "amount": "2954500",
    "category": "housing",
    "currency": "IDR",
    "date": "2025-05-05",
    "description": "Home association fee",
    "event_id": "event_943@2025-05-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_943"
  },
  {
    "amount": "1212904.33",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-05-05",
    "description": "Metro and bus fares",
    "event_id": "event_972@2025-05-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_972"
  },
  {
    "amount": "2796165.18",
    "category": "utilities",
    "currency": "IDR",
    "date": "2025-05-08",
    "description": "Municipal utilities",
    "event_id": "event_944@2025-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_944"
  },
  {
    "amount": "1881000",
    "category": "insurance",
    "currency": "IDR",
    "date": "2025-05-09",
    "description": "Vehicle insurance premium",
    "event_id": "event_945@2025-05-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_945"
  },
  {
    "amount": "2544100",
    "category": "education",
    "currency": "IDR",
    "date": "2025-05-10",
    "description": "Child education fee",
    "event_id": "event_946@2025-05-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_946"
  },
  {
    "amount": "3165638.3",
    "category": "healthcare",
    "currency": "IDR",
    "date": "2025-05-12",
    "description": "Regular medicine purchase",
    "event_id": "event_947@2025-05-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_947"
  },
  {
    "amount": "168150",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2025-05-14",
    "description": "Cloud storage plan",
    "event_id": "event_949@2025-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_949"
  },
  {
    "amount": "23256000",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-05-15",
    "description": "Base salary",
    "event_id": "event_941@2025-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_941"
  },
  {
    "amount": "1674887.61",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2025-05-16",
    "description": "Games and recreation",
    "event_id": "event_948@2025-05-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_948"
  },
  {
    "amount": "16715584.16",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-05-24",
    "description": "Performance commission",
    "event_id": "event_924@2025-05-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_924"
  },
  {
    "amount": "20012106.46",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-05-24",
    "description": "Monthly sales commission",
    "event_id": "event_942@2025-05-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_942"
  },
  {
    "amount": "2954500",
    "category": "housing",
    "currency": "IDR",
    "date": "2025-06-05",
    "description": "Home association fee",
    "event_id": "event_943@2025-06-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_943"
  },
  {
    "amount": "1212904.33",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-06-05",
    "description": "Metro and bus fares",
    "event_id": "event_972@2025-06-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_972"
  },
  {
    "amount": "2796165.18",
    "category": "utilities",
    "currency": "IDR",
    "date": "2025-06-08",
    "description": "Municipal utilities",
    "event_id": "event_944@2025-06-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_944"
  },
  {
    "amount": "1881000",
    "category": "insurance",
    "currency": "IDR",
    "date": "2025-06-09",
    "description": "Vehicle insurance premium",
    "event_id": "event_945@2025-06-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_945"
  },
  {
    "amount": "2544100",
    "category": "education",
    "currency": "IDR",
    "date": "2025-06-10",
    "description": "Child education fee",
    "event_id": "event_946@2025-06-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_946"
  },
  {
    "amount": "3165638.3",
    "category": "healthcare",
    "currency": "IDR",
    "date": "2025-06-12",
    "description": "Regular medicine purchase",
    "event_id": "event_947@2025-06-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_947"
  },
  {
    "amount": "168150",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2025-06-14",
    "description": "Cloud storage plan",
    "event_id": "event_949@2025-06-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_949"
  },
  {
    "amount": "23256000",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-06-15",
    "description": "Base salary",
    "event_id": "event_941@2025-06-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_941"
  },
  {
    "amount": "1674887.61",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2025-06-16",
    "description": "Games and recreation",
    "event_id": "event_948@2025-06-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_948"
  },
  {
    "amount": "16715584.16",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-06-24",
    "description": "Performance commission",
    "event_id": "event_924@2025-06-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_924"
  },
  {
    "amount": "20012106.46",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-06-24",
    "description": "Monthly sales commission",
    "event_id": "event_942@2025-06-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_942"
  },
  {
    "amount": "2954500",
    "category": "housing",
    "currency": "IDR",
    "date": "2025-07-05",
    "description": "Home association fee",
    "event_id": "event_943@2025-07-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_943"
  },
  {
    "amount": "1212904.33",
    "category": "transport",
    "currency": "IDR",
    "date": "2025-07-05",
    "description": "Metro and bus fares",
    "event_id": "event_972@2025-07-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_972"
  },
  {
    "amount": "2796165.18",
    "category": "utilities",
    "currency": "IDR",
    "date": "2025-07-08",
    "description": "Municipal utilities",
    "event_id": "event_944@2025-07-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_944"
  },
  {
    "amount": "1881000",
    "category": "insurance",
    "currency": "IDR",
    "date": "2025-07-09",
    "description": "Vehicle insurance premium",
    "event_id": "event_945@2025-07-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_945"
  },
  {
    "amount": "2544100",
    "category": "education",
    "currency": "IDR",
    "date": "2025-07-10",
    "description": "Child education fee",
    "event_id": "event_946@2025-07-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_946"
  },
  {
    "amount": "3165638.3",
    "category": "healthcare",
    "currency": "IDR",
    "date": "2025-07-12",
    "description": "Regular medicine purchase",
    "event_id": "event_947@2025-07-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_947"
  },
  {
    "amount": "168150",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2025-07-14",
    "description": "Cloud storage plan",
    "event_id": "event_949@2025-07-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_949"
  },
  {
    "amount": "23256000",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-07-15",
    "description": "Base salary",
    "event_id": "event_941@2025-07-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_941"
  },
  {
    "amount": "1674887.61",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2025-07-16",
    "description": "Games and recreation",
    "event_id": "event_948@2025-07-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_948"
  },
  {
    "amount": "16715584.16",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-07-24",
    "description": "Performance commission",
    "event_id": "event_924@2025-07-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_924"
  },
  {
    "amount": "20012106.46",
    "category": "salary",
    "currency": "IDR",
    "date": "2025-07-24",
    "description": "Monthly sales commission",
    "event_id": "event_942@2025-07-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_942"
  }
]
```

## `request_13` / `user_13`

- Opening/minimum: `2789.52` / `1300`
- Expected safe amount: `433.4`; actual: `941.6`
- Expected earliest: `2024-05-15`; actual: `2024-03-07`
- Classified differences:
```json
{
  "affordability_status": "safe-payment eligibility derived from the forecast predicate",
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate",
  "payment_plan": "plan construction downstream of status/earliest date",
  "recommended_payment_method": "planner candidate eligibility/ranking downstream of forecast"
}
```
- Future flow and balance path:
```text
2024-03-10 flow=-61 balance=2728.52
2024-03-11 flow=-29 balance=2699.52
2024-03-12 flow=-102.25 balance=2597.27
2024-03-13 flow=-21 balance=2576.27
2024-03-14 flow=-37.9 balance=2538.37
2024-03-15 flow=1343.54 balance=3881.91
2024-03-20 flow=948.46 balance=4830.37
2024-04-02 flow=-622.6 balance=4207.77
2024-04-06 flow=-143.7 balance=4064.07
2024-04-09 flow=-102.25 balance=3961.82
2024-04-10 flow=-61 balance=3900.82
2024-04-11 flow=-29 balance=3871.82
2024-04-13 flow=-21 balance=3850.82
2024-04-14 flow=-37.9 balance=3812.92
2024-04-15 flow=1343.54 balance=5156.46
2024-04-20 flow=948.46 balance=6104.92
2024-05-02 flow=-622.6 balance=5482.32
2024-05-06 flow=-143.7 balance=5338.62
2024-05-07 flow=-102.25 balance=5236.37
2024-05-10 flow=-61 balance=5175.37
2024-05-11 flow=-29 balance=5146.37
2024-05-13 flow=-21 balance=5125.37
2024-05-14 flow=-37.9 balance=5087.47
2024-05-15 flow=1343.54 balance=6431.01
2024-05-20 flow=948.46 balance=7379.47
2024-06-02 flow=-622.6 balance=6756.87
2024-06-04 flow=-102.25 balance=6654.62
```
- Projected event attribution:
```json
[
  {
    "amount": "61",
    "category": "gym",
    "currency": "EUR",
    "date": "2024-03-10",
    "description": "Community fitness plan",
    "event_id": "event_1092@2024-03-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1092"
  },
  {
    "amount": "29",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2024-03-11",
    "description": "Music subscription",
    "event_id": "event_1090@2024-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1090"
  },
  {
    "amount": "102.25",
    "category": "groceries",
    "currency": "EUR",
    "date": "2024-03-12",
    "description": "Local market purchase",
    "event_id": "event_1114@2024-03-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1114"
  },
  {
    "amount": "21",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2024-03-13",
    "description": "Delivery service plan",
    "event_id": "event_1091@2024-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1091"
  },
  {
    "amount": "37.9",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2024-03-14",
    "description": "Local event tickets",
    "event_id": "event_1093@2024-03-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1093"
  },
  {
    "amount": "948.46",
    "category": "salary",
    "currency": "EUR",
    "date": "2024-03-20",
    "description": "Second household income",
    "event_id": "event_1080@2024-03-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1080"
  },
  {
    "amount": "622.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2024-04-02",
    "description": "Shared housing rent",
    "event_id": "event_1094@2024-04-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1094"
  },
  {
    "amount": "143.7",
    "category": "utilities",
    "currency": "EUR",
    "date": "2024-04-06",
    "description": "Water and power payment",
    "event_id": "event_1095@2024-04-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1095"
  },
  {
    "amount": "102.25",
    "category": "groceries",
    "currency": "EUR",
    "date": "2024-04-09",
    "description": "Local market purchase",
    "event_id": "event_1114@2024-04-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1114"
  },
  {
    "amount": "61",
    "category": "gym",
    "currency": "EUR",
    "date": "2024-04-10",
    "description": "Community fitness plan",
    "event_id": "event_1092@2024-04-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1092"
  },
  {
    "amount": "29",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2024-04-11",
    "description": "Music subscription",
    "event_id": "event_1090@2024-04-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1090"
  },
  {
    "amount": "21",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2024-04-13",
    "description": "Delivery service plan",
    "event_id": "event_1091@2024-04-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1091"
  },
  {
    "amount": "37.9",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2024-04-14",
    "description": "Local event tickets",
    "event_id": "event_1093@2024-04-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1093"
  },
  {
    "amount": "1343.54",
    "category": "salary",
    "currency": "EUR",
    "date": "2024-04-15",
    "description": "Primary household salary",
    "event_id": "event_1087@2024-04-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1087"
  },
  {
    "amount": "948.46",
    "category": "salary",
    "currency": "EUR",
    "date": "2024-04-20",
    "description": "Second household income",
    "event_id": "event_1080@2024-04-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1080"
  },
  {
    "amount": "622.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2024-05-02",
    "description": "Shared housing rent",
    "event_id": "event_1094@2024-05-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1094"
  },
  {
    "amount": "143.7",
    "category": "utilities",
    "currency": "EUR",
    "date": "2024-05-06",
    "description": "Water and power payment",
    "event_id": "event_1095@2024-05-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1095"
  },
  {
    "amount": "102.25",
    "category": "groceries",
    "currency": "EUR",
    "date": "2024-05-07",
    "description": "Local market purchase",
    "event_id": "event_1114@2024-05-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1114"
  },
  {
    "amount": "61",
    "category": "gym",
    "currency": "EUR",
    "date": "2024-05-10",
    "description": "Community fitness plan",
    "event_id": "event_1092@2024-05-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1092"
  },
  {
    "amount": "29",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2024-05-11",
    "description": "Music subscription",
    "event_id": "event_1090@2024-05-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1090"
  },
  {
    "amount": "21",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2024-05-13",
    "description": "Delivery service plan",
    "event_id": "event_1091@2024-05-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1091"
  },
  {
    "amount": "37.9",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2024-05-14",
    "description": "Local event tickets",
    "event_id": "event_1093@2024-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1093"
  },
  {
    "amount": "1343.54",
    "category": "salary",
    "currency": "EUR",
    "date": "2024-05-15",
    "description": "Primary household salary",
    "event_id": "event_1087@2024-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1087"
  },
  {
    "amount": "948.46",
    "category": "salary",
    "currency": "EUR",
    "date": "2024-05-20",
    "description": "Second household income",
    "event_id": "event_1080@2024-05-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1080"
  },
  {
    "amount": "622.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2024-06-02",
    "description": "Shared housing rent",
    "event_id": "event_1094@2024-06-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1094"
  },
  {
    "amount": "102.25",
    "category": "groceries",
    "currency": "EUR",
    "date": "2024-06-04",
    "description": "Local market purchase",
    "event_id": "event_1114@2024-06-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1114"
  }
]
```

## `request_14` / `user_14`

- Opening/minimum: `3931.74` / `2200`
- Expected safe amount: `597.74`; actual: `613.64`
- Expected earliest: ``; actual: ``
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2025-08-07 flow=-153.69 balance=3778.05
2025-08-10 flow=-138.85 balance=3639.2
2025-08-11 flow=-95.17 balance=3544.03
2025-08-12 flow=-350 balance=3194.03
2025-08-13 flow=-154.39 balance=3039.64
2025-08-14 flow=-226 balance=2813.64
2025-08-15 flow=2717 balance=5530.64
2025-08-24 flow=-138.85 balance=5391.79
2025-09-03 flow=-688.6 balance=4703.19
2025-09-07 flow=-292.54 balance=4410.65
2025-09-11 flow=-95.17 balance=4315.48
2025-09-12 flow=-350 balance=3965.48
2025-09-13 flow=-154.39 balance=3811.09
2025-09-14 flow=-226 balance=3585.09
2025-09-15 flow=2717 balance=6302.09
2025-09-21 flow=-138.85 balance=6163.24
2025-10-03 flow=-688.6 balance=5474.64
2025-10-05 flow=-138.85 balance=5335.79
2025-10-07 flow=-153.69 balance=5182.1
2025-10-11 flow=-95.17 balance=5086.93
2025-10-12 flow=-350 balance=4736.93
2025-10-13 flow=-154.39 balance=4582.54
2025-10-14 flow=-226 balance=4356.54
2025-10-15 flow=2717 balance=7073.54
2025-10-19 flow=-138.85 balance=6934.69
```
- Projected event attribution:
```json
[
  {
    "amount": "153.69",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-08-07",
    "description": "Energy provider bill",
    "event_id": "event_1194@2025-08-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1194"
  },
  {
    "amount": "138.85",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-08-10",
    "description": "Weekly produce market",
    "event_id": "event_1225@2025-08-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1225"
  },
  {
    "amount": "95.17",
    "category": "healthcare",
    "currency": "EUR",
    "date": "2025-08-11",
    "description": "Family healthcare expense",
    "event_id": "event_1196@2025-08-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1196"
  },
  {
    "amount": "350",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2025-08-12",
    "description": "Credit card repayment",
    "event_id": "event_1195@2025-08-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1195"
  },
  {
    "amount": "14",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2025-08-13",
    "description": "Cloud storage plan",
    "event_id": "event_1198@2025-08-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1198"
  },
  {
    "amount": "140.39",
    "category": "shopping",
    "currency": "EUR",
    "date": "2025-08-13",
    "description": "Online retail purchases",
    "event_id": "event_1199@2025-08-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1199"
  },
  {
    "amount": "226",
    "category": "family_support",
    "currency": "EUR",
    "date": "2025-08-14",
    "description": "Family support payment",
    "event_id": "event_1197@2025-08-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1197"
  },
  {
    "amount": "138.85",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-08-24",
    "description": "Weekly produce market",
    "event_id": "event_1225@2025-08-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1225"
  },
  {
    "amount": "688.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-09-03",
    "description": "Monthly rent",
    "event_id": "event_1200@2025-09-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1200"
  },
  {
    "amount": "153.69",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-09-07",
    "description": "Energy provider bill",
    "event_id": "event_1194@2025-09-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1194"
  },
  {
    "amount": "138.85",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-09-07",
    "description": "Weekly produce market",
    "event_id": "event_1225@2025-09-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1225"
  },
  {
    "amount": "95.17",
    "category": "healthcare",
    "currency": "EUR",
    "date": "2025-09-11",
    "description": "Family healthcare expense",
    "event_id": "event_1196@2025-09-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1196"
  },
  {
    "amount": "350",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2025-09-12",
    "description": "Credit card repayment",
    "event_id": "event_1195@2025-09-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1195"
  },
  {
    "amount": "14",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2025-09-13",
    "description": "Cloud storage plan",
    "event_id": "event_1198@2025-09-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1198"
  },
  {
    "amount": "140.39",
    "category": "shopping",
    "currency": "EUR",
    "date": "2025-09-13",
    "description": "Online retail purchases",
    "event_id": "event_1199@2025-09-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1199"
  },
  {
    "amount": "226",
    "category": "family_support",
    "currency": "EUR",
    "date": "2025-09-14",
    "description": "Family support payment",
    "event_id": "event_1197@2025-09-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1197"
  },
  {
    "amount": "2717",
    "category": "salary",
    "currency": "EUR",
    "date": "2025-09-15",
    "description": "Payroll before leave",
    "event_id": "event_1170@2025-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1170"
  },
  {
    "amount": "138.85",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-09-21",
    "description": "Weekly produce market",
    "event_id": "event_1225@2025-09-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1225"
  },
  {
    "amount": "688.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-10-03",
    "description": "Monthly rent",
    "event_id": "event_1200@2025-10-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1200"
  },
  {
    "amount": "138.85",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-10-05",
    "description": "Weekly produce market",
    "event_id": "event_1225@2025-10-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1225"
  },
  {
    "amount": "153.69",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-10-07",
    "description": "Energy provider bill",
    "event_id": "event_1194@2025-10-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1194"
  },
  {
    "amount": "95.17",
    "category": "healthcare",
    "currency": "EUR",
    "date": "2025-10-11",
    "description": "Family healthcare expense",
    "event_id": "event_1196@2025-10-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1196"
  },
  {
    "amount": "350",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2025-10-12",
    "description": "Credit card repayment",
    "event_id": "event_1195@2025-10-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1195"
  },
  {
    "amount": "14",
    "category": "cloud_storage",
    "currency": "EUR",
    "date": "2025-10-13",
    "description": "Cloud storage plan",
    "event_id": "event_1198@2025-10-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1198"
  },
  {
    "amount": "140.39",
    "category": "shopping",
    "currency": "EUR",
    "date": "2025-10-13",
    "description": "Online retail purchases",
    "event_id": "event_1199@2025-10-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1199"
  },
  {
    "amount": "226",
    "category": "family_support",
    "currency": "EUR",
    "date": "2025-10-14",
    "description": "Family support payment",
    "event_id": "event_1197@2025-10-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1197"
  },
  {
    "amount": "2717",
    "category": "salary",
    "currency": "EUR",
    "date": "2025-10-15",
    "description": "Payroll before leave",
    "event_id": "event_1170@2025-10-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1170"
  },
  {
    "amount": "138.85",
    "category": "groceries",
    "currency": "EUR",
    "date": "2025-10-19",
    "description": "Weekly produce market",
    "event_id": "event_1225@2025-10-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1225"
  }
]
```

## `request_15` / `user_15`

- Opening/minimum: `1770.05` / `1200`
- Expected safe amount: `83.05`; actual: `225.66`
- Expected earliest: ``; actual: ``
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2026-01-08 flow=-90.39 balance=1679.66
2026-01-10 flow=-159 balance=1520.66
2026-01-13 flow=-95 balance=1425.66
2026-01-15 flow=1634 balance=3059.66
2026-01-21 flow=-41.35 balance=3018.31
2026-02-01 flow=-38.56 balance=2979.75
2026-02-03 flow=-56.7 balance=2923.05
2026-02-04 flow=-435.6 balance=2487.45
2026-02-05 flow=-31.09 balance=2456.36
2026-02-08 flow=-90.39 balance=2365.97
2026-02-10 flow=-159 balance=2206.97
2026-02-11 flow=-41.35 balance=2165.62
2026-02-13 flow=-95 balance=2070.62
2026-02-15 flow=1634 balance=3704.62
2026-03-01 flow=-38.56 balance=3666.06
2026-03-04 flow=-476.95 balance=3189.11
2026-03-05 flow=-31.09 balance=3158.02
2026-03-08 flow=-90.39 balance=3067.63
2026-03-10 flow=-159 balance=2908.63
2026-03-13 flow=-95 balance=2813.63
2026-03-15 flow=1634 balance=4447.63
2026-03-17 flow=-56.7 balance=4390.93
2026-03-25 flow=-41.35 balance=4349.58
2026-04-01 flow=-38.56 balance=4311.02
2026-04-04 flow=-435.6 balance=3875.42
2026-04-05 flow=-31.09 balance=3844.33
```
- Projected event attribution:
```json
[
  {
    "amount": "90.39",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-01-08",
    "description": "Energy provider bill",
    "event_id": "event_1267@2026-01-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1267"
  },
  {
    "amount": "159",
    "category": "education",
    "currency": "EUR",
    "date": "2026-01-10",
    "description": "School fee payment",
    "event_id": "event_1268@2026-01-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1268"
  },
  {
    "amount": "84",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2026-01-13",
    "description": "Credit card repayment",
    "event_id": "event_1269@2026-01-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1269"
  },
  {
    "amount": "11",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2026-01-13",
    "description": "Music subscription",
    "event_id": "event_1270@2026-01-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1270"
  },
  {
    "amount": "27",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2026-01-15",
    "description": "Food delivery membership",
    "event_id": "event_1271@2026-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1271"
  },
  {
    "amount": "41.35",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-01-21",
    "description": "Ride-hailing trip",
    "event_id": "event_1322@2026-01-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1322"
  },
  {
    "amount": "38.56",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-02-01",
    "description": "Neighbourhood restaurant",
    "event_id": "event_1331@2026-02-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1331"
  },
  {
    "amount": "56.7",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-02-03",
    "description": "Grocery delivery",
    "event_id": "event_1296@2026-02-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1296"
  },
  {
    "amount": "435.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-02-04",
    "description": "Landlord standing order",
    "event_id": "event_1272@2026-02-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1272"
  },
  {
    "amount": "31.09",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-02-05",
    "description": "Local taxi",
    "event_id": "event_1314@2026-02-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1314"
  },
  {
    "amount": "90.39",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-02-08",
    "description": "Energy provider bill",
    "event_id": "event_1267@2026-02-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1267"
  },
  {
    "amount": "159",
    "category": "education",
    "currency": "EUR",
    "date": "2026-02-10",
    "description": "School fee payment",
    "event_id": "event_1268@2026-02-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1268"
  },
  {
    "amount": "41.35",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-02-11",
    "description": "Ride-hailing trip",
    "event_id": "event_1322@2026-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1322"
  },
  {
    "amount": "84",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2026-02-13",
    "description": "Credit card repayment",
    "event_id": "event_1269@2026-02-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1269"
  },
  {
    "amount": "11",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2026-02-13",
    "description": "Music subscription",
    "event_id": "event_1270@2026-02-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1270"
  },
  {
    "amount": "1661",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-02-15",
    "description": "First-job payroll",
    "event_id": "event_1265@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1265"
  },
  {
    "amount": "27",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2026-02-15",
    "description": "Food delivery membership",
    "event_id": "event_1271@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1271"
  },
  {
    "amount": "38.56",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-03-01",
    "description": "Neighbourhood restaurant",
    "event_id": "event_1331@2026-03-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1331"
  },
  {
    "amount": "435.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-03-04",
    "description": "Landlord standing order",
    "event_id": "event_1272@2026-03-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1272"
  },
  {
    "amount": "41.35",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-03-04",
    "description": "Ride-hailing trip",
    "event_id": "event_1322@2026-03-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1322"
  },
  {
    "amount": "31.09",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-03-05",
    "description": "Local taxi",
    "event_id": "event_1314@2026-03-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1314"
  },
  {
    "amount": "90.39",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-03-08",
    "description": "Energy provider bill",
    "event_id": "event_1267@2026-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1267"
  },
  {
    "amount": "159",
    "category": "education",
    "currency": "EUR",
    "date": "2026-03-10",
    "description": "School fee payment",
    "event_id": "event_1268@2026-03-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1268"
  },
  {
    "amount": "84",
    "category": "debt_repayment",
    "currency": "EUR",
    "date": "2026-03-13",
    "description": "Credit card repayment",
    "event_id": "event_1269@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1269"
  },
  {
    "amount": "11",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2026-03-13",
    "description": "Music subscription",
    "event_id": "event_1270@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1270"
  },
  {
    "amount": "1661",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-03-15",
    "description": "First-job payroll",
    "event_id": "event_1265@2026-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1265"
  },
  {
    "amount": "27",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2026-03-15",
    "description": "Food delivery membership",
    "event_id": "event_1271@2026-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1271"
  },
  {
    "amount": "56.7",
    "category": "groceries",
    "currency": "EUR",
    "date": "2026-03-17",
    "description": "Grocery delivery",
    "event_id": "event_1296@2026-03-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1296"
  },
  {
    "amount": "41.35",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-03-25",
    "description": "Ride-hailing trip",
    "event_id": "event_1322@2026-03-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1322"
  },
  {
    "amount": "38.56",
    "category": "dining",
    "currency": "EUR",
    "date": "2026-04-01",
    "description": "Neighbourhood restaurant",
    "event_id": "event_1331@2026-04-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1331"
  },
  {
    "amount": "435.6",
    "category": "rent",
    "currency": "EUR",
    "date": "2026-04-04",
    "description": "Landlord standing order",
    "event_id": "event_1272@2026-04-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1272"
  },
  {
    "amount": "31.09",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-04-05",
    "description": "Local taxi",
    "event_id": "event_1314@2026-04-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1314"
  }
]
```

## `request_17` / `user_17`

- Opening/minimum: `550379.58` / `166100`
- Expected safe amount: `243849.58`; actual: `248325.96`
- Expected earliest: `2026-03-15`; actual: `2026-03-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2026-03-01 flow=-11433.33 balance=538946.25
2026-03-02 flow=-49600 balance=489346.25
2026-03-06 flow=-10246.53 balance=479099.72
2026-03-08 flow=-13660 balance=465439.72
2026-03-09 flow=-5650.43 balance=459789.29
2026-03-11 flow=-43688.33 balance=416100.96
2026-03-13 flow=-1675 balance=414425.96
2026-03-15 flow=206000 balance=620425.96
2026-03-19 flow=-5650.43 balance=614775.53
2026-03-21 flow=-11433.33 balance=603342.2
2026-03-29 flow=-5650.43 balance=597691.77
2026-03-31 flow=-11433.33 balance=586258.44
2026-04-02 flow=-49600 balance=536658.44
2026-04-06 flow=-10246.53 balance=526411.91
2026-04-08 flow=-19310.43 balance=507101.48
2026-04-10 flow=-11433.33 balance=495668.15
2026-04-11 flow=-32255 balance=463413.15
2026-04-13 flow=-1675 balance=461738.15
2026-04-15 flow=206000 balance=667738.15
2026-04-18 flow=-5650.43 balance=662087.72
2026-04-20 flow=-11433.33 balance=650654.39
2026-04-28 flow=-5650.43 balance=645003.96
2026-04-30 flow=-11433.33 balance=633570.63
2026-05-02 flow=-49600 balance=583970.63
2026-05-06 flow=-10246.53 balance=573724.1
2026-05-08 flow=-19310.43 balance=554413.67
2026-05-10 flow=-11433.33 balance=542980.34
2026-05-11 flow=-32255 balance=510725.34
2026-05-13 flow=-1675 balance=509050.34
2026-05-15 flow=206000 balance=715050.34
2026-05-18 flow=-5650.43 balance=709399.91
2026-05-20 flow=-11433.33 balance=697966.58
2026-05-28 flow=-5650.43 balance=692316.15
```
- Projected event attribution:
```json
[
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-01",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-03-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "49600",
    "category": "rent",
    "currency": "INR",
    "date": "2026-03-02",
    "description": "Apartment rent transfer",
    "event_id": "event_1472@2026-03-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1472"
  },
  {
    "amount": "10246.53",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-03-06",
    "description": "Municipal utilities",
    "event_id": "event_1473@2026-03-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1473"
  },
  {
    "amount": "13660",
    "category": "education",
    "currency": "INR",
    "date": "2026-03-08",
    "description": "Course tuition",
    "event_id": "event_1474@2026-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1474"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-09",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-03-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "30200",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2026-03-11",
    "description": "Credit card repayment",
    "event_id": "event_1475@2026-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1475"
  },
  {
    "amount": "2055",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2026-03-11",
    "description": "Music subscription",
    "event_id": "event_1476@2026-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1476"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-11",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "1675",
    "category": "delivery_membership",
    "currency": "INR",
    "date": "2026-03-13",
    "description": "Food delivery membership",
    "event_id": "event_1477@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1477"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-19",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-03-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-21",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-03-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-29",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-03-29",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-31",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-03-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "49600",
    "category": "rent",
    "currency": "INR",
    "date": "2026-04-02",
    "description": "Apartment rent transfer",
    "event_id": "event_1472@2026-04-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1472"
  },
  {
    "amount": "10246.53",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-04-06",
    "description": "Municipal utilities",
    "event_id": "event_1473@2026-04-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1473"
  },
  {
    "amount": "13660",
    "category": "education",
    "currency": "INR",
    "date": "2026-04-08",
    "description": "Course tuition",
    "event_id": "event_1474@2026-04-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1474"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-04-08",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-04-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-04-10",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-04-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "30200",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2026-04-11",
    "description": "Credit card repayment",
    "event_id": "event_1475@2026-04-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1475"
  },
  {
    "amount": "2055",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2026-04-11",
    "description": "Music subscription",
    "event_id": "event_1476@2026-04-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1476"
  },
  {
    "amount": "1675",
    "category": "delivery_membership",
    "currency": "INR",
    "date": "2026-04-13",
    "description": "Food delivery membership",
    "event_id": "event_1477@2026-04-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1477"
  },
  {
    "amount": "206000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-04-15",
    "description": "Payroll credit",
    "event_id": "event_1471@2026-04-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1471"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-04-18",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-04-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-04-20",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-04-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-04-28",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-04-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-04-30",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-04-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "49600",
    "category": "rent",
    "currency": "INR",
    "date": "2026-05-02",
    "description": "Apartment rent transfer",
    "event_id": "event_1472@2026-05-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1472"
  },
  {
    "amount": "10246.53",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-05-06",
    "description": "Municipal utilities",
    "event_id": "event_1473@2026-05-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1473"
  },
  {
    "amount": "13660",
    "category": "education",
    "currency": "INR",
    "date": "2026-05-08",
    "description": "Course tuition",
    "event_id": "event_1474@2026-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1474"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-05-08",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-05-10",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-05-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "30200",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2026-05-11",
    "description": "Credit card repayment",
    "event_id": "event_1475@2026-05-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1475"
  },
  {
    "amount": "2055",
    "category": "music_subscription",
    "currency": "INR",
    "date": "2026-05-11",
    "description": "Music subscription",
    "event_id": "event_1476@2026-05-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1476"
  },
  {
    "amount": "1675",
    "category": "delivery_membership",
    "currency": "INR",
    "date": "2026-05-13",
    "description": "Food delivery membership",
    "event_id": "event_1477@2026-05-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1477"
  },
  {
    "amount": "206000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-05-15",
    "description": "Payroll credit",
    "event_id": "event_1471@2026-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1471"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-05-18",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-05-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  },
  {
    "amount": "11433.33",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-05-20",
    "description": "Local market purchase",
    "event_id": "event_1499@2026-05-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1499"
  },
  {
    "amount": "5650.43",
    "category": "transport",
    "currency": "INR",
    "date": "2026-05-28",
    "description": "Metro and bus fares",
    "event_id": "event_1526@2026-05-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1526"
  }
]
```

## `request_18` / `user_18`

- Opening/minimum: `2486` / `1400`
- Expected safe amount: `462`; actual: `662.19`
- Expected earliest: `2026-09-15`; actual: `2026-08-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate",
  "payment_plan": "plan construction downstream of status/earliest date"
}
```
- Future flow and balance path:
```text
2026-07-07 flow=-125.4 balance=2360.6
2026-07-08 flow=-68 balance=2292.6
2026-07-10 flow=-68 balance=2224.6
2026-07-11 flow=-162.41 balance=2062.19
2026-07-15 flow=2310 balance=4372.19
2026-07-28 flow=-50.57 balance=4321.62
2026-08-04 flow=-167 balance=4154.62
2026-08-07 flow=-125.4 balance=4029.22
2026-08-08 flow=-68 balance=3961.22
2026-08-10 flow=-68 balance=3893.22
2026-08-11 flow=-162.41 balance=3730.81
2026-08-15 flow=2310 balance=6040.81
2026-08-25 flow=-50.57 balance=5990.24
2026-09-04 flow=-167 balance=5823.24
2026-09-07 flow=-125.4 balance=5697.84
2026-09-08 flow=-68 balance=5629.84
2026-09-10 flow=-68 balance=5561.84
2026-09-11 flow=-162.41 balance=5399.43
2026-09-15 flow=2310 balance=7709.43
2026-09-22 flow=-50.57 balance=7658.86
2026-10-04 flow=-167 balance=7491.86
```
- Projected event attribution:
```json
[
  {
    "amount": "125.4",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-07-07",
    "description": "Energy provider bill",
    "event_id": "event_1573@2026-07-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1573"
  },
  {
    "amount": "68",
    "category": "insurance",
    "currency": "EUR",
    "date": "2026-07-08",
    "description": "Household insurance",
    "event_id": "event_1574@2026-07-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1574"
  },
  {
    "amount": "68",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-07-10",
    "description": "Family streaming plan",
    "event_id": "event_1576@2026-07-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1576"
  },
  {
    "amount": "162.41",
    "category": "healthcare",
    "currency": "EUR",
    "date": "2026-07-11",
    "description": "Clinic payment",
    "event_id": "event_1575@2026-07-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1575"
  },
  {
    "amount": "2310",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-07-15",
    "description": "Payroll credit",
    "event_id": "event_1571@2026-07-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1571"
  },
  {
    "amount": "50.57",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-07-28",
    "description": "Vehicle charging",
    "event_id": "event_1606@2026-07-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1606"
  },
  {
    "amount": "167",
    "category": "housing",
    "currency": "EUR",
    "date": "2026-08-04",
    "description": "Building maintenance payment",
    "event_id": "event_1577@2026-08-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1577"
  },
  {
    "amount": "125.4",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-08-07",
    "description": "Energy provider bill",
    "event_id": "event_1573@2026-08-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1573"
  },
  {
    "amount": "68",
    "category": "insurance",
    "currency": "EUR",
    "date": "2026-08-08",
    "description": "Household insurance",
    "event_id": "event_1574@2026-08-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1574"
  },
  {
    "amount": "68",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-08-10",
    "description": "Family streaming plan",
    "event_id": "event_1576@2026-08-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1576"
  },
  {
    "amount": "162.41",
    "category": "healthcare",
    "currency": "EUR",
    "date": "2026-08-11",
    "description": "Clinic payment",
    "event_id": "event_1575@2026-08-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1575"
  },
  {
    "amount": "2310",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-08-15",
    "description": "Payroll credit",
    "event_id": "event_1571@2026-08-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1571"
  },
  {
    "amount": "50.57",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-08-25",
    "description": "Vehicle charging",
    "event_id": "event_1606@2026-08-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1606"
  },
  {
    "amount": "167",
    "category": "housing",
    "currency": "EUR",
    "date": "2026-09-04",
    "description": "Building maintenance payment",
    "event_id": "event_1577@2026-09-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1577"
  },
  {
    "amount": "125.4",
    "category": "utilities",
    "currency": "EUR",
    "date": "2026-09-07",
    "description": "Energy provider bill",
    "event_id": "event_1573@2026-09-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1573"
  },
  {
    "amount": "68",
    "category": "insurance",
    "currency": "EUR",
    "date": "2026-09-08",
    "description": "Household insurance",
    "event_id": "event_1574@2026-09-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1574"
  },
  {
    "amount": "68",
    "category": "streaming",
    "currency": "EUR",
    "date": "2026-09-10",
    "description": "Family streaming plan",
    "event_id": "event_1576@2026-09-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1576"
  },
  {
    "amount": "162.41",
    "category": "healthcare",
    "currency": "EUR",
    "date": "2026-09-11",
    "description": "Clinic payment",
    "event_id": "event_1575@2026-09-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1575"
  },
  {
    "amount": "2310",
    "category": "salary",
    "currency": "EUR",
    "date": "2026-09-15",
    "description": "Payroll credit",
    "event_id": "event_1571@2026-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1571"
  },
  {
    "amount": "50.57",
    "category": "transport",
    "currency": "EUR",
    "date": "2026-09-22",
    "description": "Vehicle charging",
    "event_id": "event_1606@2026-09-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1606"
  },
  {
    "amount": "167",
    "category": "housing",
    "currency": "EUR",
    "date": "2026-10-04",
    "description": "Building maintenance payment",
    "event_id": "event_1577@2026-10-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1577"
  }
]
```

## `request_19` / `user_19`

- Opening/minimum: `199545` / `92800`
- Expected safe amount: `28820`; actual: `37555.87`
- Expected earliest: `2024-09-15`; actual: `2024-09-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "payment_plan": "plan construction downstream of status/earliest date"
}
```
- Future flow and balance path:
```text
2024-09-04 flow=-36100 balance=163445
2024-09-08 flow=-6129.19 balance=157315.81
2024-09-12 flow=-8645.36 balance=148670.45
2024-09-13 flow=-11850 balance=136820.45
2024-09-14 flow=-6464.58 balance=130355.87
2024-09-15 flow=118350 balance=248705.87
2024-09-17 flow=-4871.72 balance=243834.15
2024-09-18 flow=-4667.68 balance=239166.47
2024-09-20 flow=-3432.81 balance=235733.66
2024-09-25 flow=-3849.5 balance=231884.16
2024-10-04 flow=-36100 balance=195784.16
2024-10-08 flow=-6129.19 balance=189654.97
2024-10-09 flow=-4667.68 balance=184987.29
2024-10-12 flow=-8645.36 balance=176341.93
2024-10-13 flow=-11850 balance=164491.93
2024-10-14 flow=-6464.58 balance=158027.35
2024-10-15 flow=118350 balance=276377.35
2024-10-17 flow=-4871.72 balance=271505.63
2024-10-20 flow=-3432.81 balance=268072.82
2024-10-25 flow=-3849.5 balance=264223.32
2024-10-30 flow=-4667.68 balance=259555.64
2024-11-04 flow=-36100 balance=223455.64
2024-11-08 flow=-6129.19 balance=217326.45
2024-11-12 flow=-8645.36 balance=208681.09
2024-11-13 flow=-11850 balance=196831.09
2024-11-14 flow=-6464.58 balance=190366.51
2024-11-15 flow=118350 balance=308716.51
2024-11-17 flow=-4871.72 balance=303844.79
2024-11-20 flow=-8100.49 balance=295744.3
2024-11-25 flow=-3849.5 balance=291894.8
```
- Projected event attribution:
```json
[
  {
    "amount": "36100",
    "category": "rent",
    "currency": "INR",
    "date": "2024-09-04",
    "description": "Residential rent payment",
    "event_id": "event_1655@2024-09-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1655"
  },
  {
    "amount": "6129.19",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-09-08",
    "description": "Municipal utilities",
    "event_id": "event_1656@2024-09-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1656"
  },
  {
    "amount": "8645.36",
    "category": "healthcare",
    "currency": "INR",
    "date": "2024-09-12",
    "description": "Clinic payment",
    "event_id": "event_1658@2024-09-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1658"
  },
  {
    "amount": "11850",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2024-09-13",
    "description": "Loan repayment",
    "event_id": "event_1657@2024-09-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1657"
  },
  {
    "amount": "395",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2024-09-14",
    "description": "Online backup subscription",
    "event_id": "event_1660@2024-09-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1660"
  },
  {
    "amount": "6069.58",
    "category": "shopping",
    "currency": "INR",
    "date": "2024-09-14",
    "description": "Clothing and household items",
    "event_id": "event_1661@2024-09-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1661"
  },
  {
    "amount": "131000",
    "category": "salary",
    "currency": "INR",
    "date": "2024-09-15",
    "description": "Payroll credit",
    "event_id": "event_1654@2024-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1654"
  },
  {
    "amount": "12650",
    "category": "family_support",
    "currency": "INR",
    "date": "2024-09-15",
    "description": "Childcare contribution",
    "event_id": "event_1659@2024-09-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1659"
  },
  {
    "amount": "4871.72",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-09-17",
    "description": "Neighbourhood grocer",
    "event_id": "event_1667@2024-09-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1667"
  },
  {
    "amount": "4667.68",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-09-18",
    "description": "Local market purchase",
    "event_id": "event_1686@2024-09-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1686"
  },
  {
    "amount": "3432.81",
    "category": "transport",
    "currency": "INR",
    "date": "2024-09-20",
    "description": "Rail pass",
    "event_id": "event_1694@2024-09-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1694"
  },
  {
    "amount": "3849.5",
    "category": "transport",
    "currency": "INR",
    "date": "2024-09-25",
    "description": "Ride-hailing trip",
    "event_id": "event_1690@2024-09-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1690"
  },
  {
    "amount": "36100",
    "category": "rent",
    "currency": "INR",
    "date": "2024-10-04",
    "description": "Residential rent payment",
    "event_id": "event_1655@2024-10-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1655"
  },
  {
    "amount": "6129.19",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-10-08",
    "description": "Municipal utilities",
    "event_id": "event_1656@2024-10-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1656"
  },
  {
    "amount": "4667.68",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-10-09",
    "description": "Local market purchase",
    "event_id": "event_1686@2024-10-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1686"
  },
  {
    "amount": "8645.36",
    "category": "healthcare",
    "currency": "INR",
    "date": "2024-10-12",
    "description": "Clinic payment",
    "event_id": "event_1658@2024-10-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1658"
  },
  {
    "amount": "11850",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2024-10-13",
    "description": "Loan repayment",
    "event_id": "event_1657@2024-10-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1657"
  },
  {
    "amount": "395",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2024-10-14",
    "description": "Online backup subscription",
    "event_id": "event_1660@2024-10-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1660"
  },
  {
    "amount": "6069.58",
    "category": "shopping",
    "currency": "INR",
    "date": "2024-10-14",
    "description": "Clothing and household items",
    "event_id": "event_1661@2024-10-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1661"
  },
  {
    "amount": "131000",
    "category": "salary",
    "currency": "INR",
    "date": "2024-10-15",
    "description": "Payroll credit",
    "event_id": "event_1654@2024-10-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1654"
  },
  {
    "amount": "12650",
    "category": "family_support",
    "currency": "INR",
    "date": "2024-10-15",
    "description": "Childcare contribution",
    "event_id": "event_1659@2024-10-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1659"
  },
  {
    "amount": "4871.72",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-10-17",
    "description": "Neighbourhood grocer",
    "event_id": "event_1667@2024-10-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1667"
  },
  {
    "amount": "3432.81",
    "category": "transport",
    "currency": "INR",
    "date": "2024-10-20",
    "description": "Rail pass",
    "event_id": "event_1694@2024-10-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1694"
  },
  {
    "amount": "3849.5",
    "category": "transport",
    "currency": "INR",
    "date": "2024-10-25",
    "description": "Ride-hailing trip",
    "event_id": "event_1690@2024-10-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1690"
  },
  {
    "amount": "4667.68",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-10-30",
    "description": "Local market purchase",
    "event_id": "event_1686@2024-10-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1686"
  },
  {
    "amount": "36100",
    "category": "rent",
    "currency": "INR",
    "date": "2024-11-04",
    "description": "Residential rent payment",
    "event_id": "event_1655@2024-11-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1655"
  },
  {
    "amount": "6129.19",
    "category": "utilities",
    "currency": "INR",
    "date": "2024-11-08",
    "description": "Municipal utilities",
    "event_id": "event_1656@2024-11-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1656"
  },
  {
    "amount": "8645.36",
    "category": "healthcare",
    "currency": "INR",
    "date": "2024-11-12",
    "description": "Clinic payment",
    "event_id": "event_1658@2024-11-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1658"
  },
  {
    "amount": "11850",
    "category": "debt_repayment",
    "currency": "INR",
    "date": "2024-11-13",
    "description": "Loan repayment",
    "event_id": "event_1657@2024-11-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1657"
  },
  {
    "amount": "395",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2024-11-14",
    "description": "Online backup subscription",
    "event_id": "event_1660@2024-11-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1660"
  },
  {
    "amount": "6069.58",
    "category": "shopping",
    "currency": "INR",
    "date": "2024-11-14",
    "description": "Clothing and household items",
    "event_id": "event_1661@2024-11-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1661"
  },
  {
    "amount": "131000",
    "category": "salary",
    "currency": "INR",
    "date": "2024-11-15",
    "description": "Payroll credit",
    "event_id": "event_1654@2024-11-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1654"
  },
  {
    "amount": "12650",
    "category": "family_support",
    "currency": "INR",
    "date": "2024-11-15",
    "description": "Childcare contribution",
    "event_id": "event_1659@2024-11-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1659"
  },
  {
    "amount": "4871.72",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-11-17",
    "description": "Neighbourhood grocer",
    "event_id": "event_1667@2024-11-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1667"
  },
  {
    "amount": "4667.68",
    "category": "groceries",
    "currency": "INR",
    "date": "2024-11-20",
    "description": "Local market purchase",
    "event_id": "event_1686@2024-11-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1686"
  },
  {
    "amount": "3432.81",
    "category": "transport",
    "currency": "INR",
    "date": "2024-11-20",
    "description": "Rail pass",
    "event_id": "event_1694@2024-11-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1694"
  },
  {
    "amount": "3849.5",
    "category": "transport",
    "currency": "INR",
    "date": "2024-11-25",
    "description": "Ride-hailing trip",
    "event_id": "event_1690@2024-11-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1690"
  }
]
```

## `request_20` / `user_20`

- Opening/minimum: `102609.05` / `64500`
- Expected safe amount: `5400`; actual: `14941.75`
- Expected earliest: ``; actual: ``
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2026-02-07 flow=-8740 balance=93869.05
2026-02-08 flow=-4470 balance=89399.05
2026-02-09 flow=-7476.38 balance=81922.67
2026-02-11 flow=-365 balance=81557.67
2026-02-13 flow=-2115.92 balance=79441.75
2026-02-15 flow=108000 balance=187441.75
2026-03-01 flow=-4719.22 balance=182722.53
2026-03-02 flow=-7950 balance=174772.53
2026-03-05 flow=-7769.87 balance=167002.66
2026-03-06 flow=-3290 balance=163712.66
2026-03-07 flow=-8740 balance=154972.66
2026-03-09 flow=-6654.33 balance=148318.33
2026-03-11 flow=-365 balance=147953.33
2026-03-13 flow=-2115.92 balance=145837.41
2026-03-15 flow=108000 balance=253837.41
2026-03-31 flow=-8421.38 balance=245416.03
2026-04-02 flow=-7950 balance=237466.03
2026-04-05 flow=-7769.87 balance=229696.16
2026-04-06 flow=-3290 balance=226406.16
2026-04-07 flow=-8740 balance=217666.16
2026-04-09 flow=-6654.33 balance=211011.83
2026-04-11 flow=-365 balance=210646.83
2026-04-13 flow=-2115.92 balance=208530.91
2026-04-15 flow=108000 balance=316530.91
2026-04-30 flow=-4719.22 balance=311811.69
2026-05-02 flow=-7950 balance=303861.69
2026-05-05 flow=-7769.87 balance=296091.82
2026-05-06 flow=-3290 balance=292801.82
2026-05-07 flow=-8740 balance=284061.82
```
- Projected event attribution:
```json
[
  {
    "amount": "8740",
    "category": "education",
    "currency": "INR",
    "date": "2026-02-07",
    "description": "School fee payment",
    "event_id": "event_1737@2026-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1737"
  },
  {
    "amount": "6654.33",
    "category": "healthcare",
    "currency": "INR",
    "date": "2026-02-09",
    "description": "Family healthcare expense",
    "event_id": "event_1738@2026-02-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1738"
  },
  {
    "amount": "365",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2026-02-11",
    "description": "Shared storage plan",
    "event_id": "event_1740@2026-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1740"
  },
  {
    "amount": "2115.92",
    "category": "entertainment",
    "currency": "INR",
    "date": "2026-02-13",
    "description": "Cinema and events",
    "event_id": "event_1739@2026-02-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1739"
  },
  {
    "amount": "108000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-02-15",
    "description": "Payroll credit",
    "event_id": "event_1733@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1733"
  },
  {
    "amount": "4719.22",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-01",
    "description": "Household groceries",
    "event_id": "event_1761@2026-03-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1761"
  },
  {
    "amount": "7950",
    "category": "housing",
    "currency": "INR",
    "date": "2026-03-02",
    "description": "Home association fee",
    "event_id": "event_1741@2026-03-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1741"
  },
  {
    "amount": "7769.87",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-03-05",
    "description": "Municipal utilities",
    "event_id": "event_1742@2026-03-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1742"
  },
  {
    "amount": "3290",
    "category": "insurance",
    "currency": "INR",
    "date": "2026-03-06",
    "description": "Household insurance",
    "event_id": "event_1743@2026-03-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1743"
  },
  {
    "amount": "8740",
    "category": "education",
    "currency": "INR",
    "date": "2026-03-07",
    "description": "School fee payment",
    "event_id": "event_1737@2026-03-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1737"
  },
  {
    "amount": "6654.33",
    "category": "healthcare",
    "currency": "INR",
    "date": "2026-03-09",
    "description": "Family healthcare expense",
    "event_id": "event_1738@2026-03-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1738"
  },
  {
    "amount": "365",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2026-03-11",
    "description": "Shared storage plan",
    "event_id": "event_1740@2026-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1740"
  },
  {
    "amount": "2115.92",
    "category": "entertainment",
    "currency": "INR",
    "date": "2026-03-13",
    "description": "Cinema and events",
    "event_id": "event_1739@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1739"
  },
  {
    "amount": "108000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-03-15",
    "description": "Payroll credit",
    "event_id": "event_1733@2026-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1733"
  },
  {
    "amount": "3702.16",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-31",
    "description": "Grocery delivery",
    "event_id": "event_1760@2026-03-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1760"
  },
  {
    "amount": "4719.22",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-31",
    "description": "Household groceries",
    "event_id": "event_1761@2026-03-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1761"
  },
  {
    "amount": "7950",
    "category": "housing",
    "currency": "INR",
    "date": "2026-04-02",
    "description": "Home association fee",
    "event_id": "event_1741@2026-04-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1741"
  },
  {
    "amount": "7769.87",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-04-05",
    "description": "Municipal utilities",
    "event_id": "event_1742@2026-04-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1742"
  },
  {
    "amount": "3290",
    "category": "insurance",
    "currency": "INR",
    "date": "2026-04-06",
    "description": "Household insurance",
    "event_id": "event_1743@2026-04-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1743"
  },
  {
    "amount": "8740",
    "category": "education",
    "currency": "INR",
    "date": "2026-04-07",
    "description": "School fee payment",
    "event_id": "event_1737@2026-04-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1737"
  },
  {
    "amount": "6654.33",
    "category": "healthcare",
    "currency": "INR",
    "date": "2026-04-09",
    "description": "Family healthcare expense",
    "event_id": "event_1738@2026-04-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1738"
  },
  {
    "amount": "365",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2026-04-11",
    "description": "Shared storage plan",
    "event_id": "event_1740@2026-04-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1740"
  },
  {
    "amount": "2115.92",
    "category": "entertainment",
    "currency": "INR",
    "date": "2026-04-13",
    "description": "Cinema and events",
    "event_id": "event_1739@2026-04-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1739"
  },
  {
    "amount": "108000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-04-15",
    "description": "Payroll credit",
    "event_id": "event_1733@2026-04-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1733"
  },
  {
    "amount": "4719.22",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-04-30",
    "description": "Household groceries",
    "event_id": "event_1761@2026-04-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1761"
  },
  {
    "amount": "7950",
    "category": "housing",
    "currency": "INR",
    "date": "2026-05-02",
    "description": "Home association fee",
    "event_id": "event_1741@2026-05-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1741"
  },
  {
    "amount": "7769.87",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-05-05",
    "description": "Municipal utilities",
    "event_id": "event_1742@2026-05-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1742"
  },
  {
    "amount": "3290",
    "category": "insurance",
    "currency": "INR",
    "date": "2026-05-06",
    "description": "Household insurance",
    "event_id": "event_1743@2026-05-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1743"
  },
  {
    "amount": "8740",
    "category": "education",
    "currency": "INR",
    "date": "2026-05-07",
    "description": "School fee payment",
    "event_id": "event_1737@2026-05-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1737"
  }
]
```

## `request_21` / `user_21`

- Opening/minimum: `3911.35` / `1800`
- Expected safe amount: `1543.35`; actual: `1574.4`
- Expected earliest: `2026-04-15`; actual: `2026-04-03`
- Classified differences:
```json
{
  "affordability_status": "safe-payment eligibility derived from the forecast predicate",
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate",
  "spending_changes_needed": "spending-change enumeration/provenance or forecast binding trough"
}
```
- Future flow and balance path:
```text
2026-04-05 flow=-53 balance=3858.35
2026-04-06 flow=-228.27 balance=3630.08
2026-04-09 flow=-47 balance=3583.08
2026-04-12 flow=-137.38 balance=3445.7
2026-04-15 flow=2256 balance=5701.7
2026-04-16 flow=-90.57 balance=5611.13
2026-05-02 flow=-718.8 balance=4892.33
2026-05-06 flow=-228.27 balance=4664.06
2026-05-09 flow=-47 balance=4617.06
2026-05-12 flow=-137.38 balance=4479.68
2026-05-15 flow=2256 balance=6735.68
2026-05-16 flow=-90.57 balance=6645.11
2026-06-02 flow=-718.8 balance=5926.31
2026-06-05 flow=-104.19 balance=5822.12
2026-06-06 flow=-124.08 balance=5698.04
2026-06-09 flow=-47 balance=5651.04
2026-06-12 flow=-137.38 balance=5513.66
2026-06-15 flow=2165.43 balance=7679.09
```
- Projected event attribution:
```json
[
  {
    "amount": "124.08",
    "category": "utilities",
    "currency": "USD",
    "date": "2026-04-06",
    "description": "Municipal utilities",
    "event_id": "event_1814@2026-04-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1814"
  },
  {
    "amount": "104.19",
    "category": "groceries",
    "currency": "USD",
    "date": "2026-04-06",
    "description": "Weekly produce market",
    "event_id": "event_1831@2026-04-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1831"
  },
  {
    "amount": "47",
    "category": "streaming",
    "currency": "USD",
    "date": "2026-04-09",
    "description": "Streaming subscription",
    "event_id": "event_1816@2026-04-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1816"
  },
  {
    "amount": "11",
    "category": "cloud_storage",
    "currency": "USD",
    "date": "2026-04-12",
    "description": "Online backup subscription",
    "event_id": "event_1815@2026-04-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1815"
  },
  {
    "amount": "126.38",
    "category": "shopping",
    "currency": "USD",
    "date": "2026-04-12",
    "description": "Monthly shopping spend",
    "event_id": "event_1817@2026-04-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1817"
  },
  {
    "amount": "90.57",
    "category": "groceries",
    "currency": "USD",
    "date": "2026-04-16",
    "description": "Fresh food shop",
    "event_id": "event_1835@2026-04-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1835"
  },
  {
    "amount": "718.8",
    "category": "rent",
    "currency": "USD",
    "date": "2026-05-02",
    "description": "Residential rent payment",
    "event_id": "event_1818@2026-05-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1818"
  },
  {
    "amount": "124.08",
    "category": "utilities",
    "currency": "USD",
    "date": "2026-05-06",
    "description": "Municipal utilities",
    "event_id": "event_1814@2026-05-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1814"
  },
  {
    "amount": "104.19",
    "category": "groceries",
    "currency": "USD",
    "date": "2026-05-06",
    "description": "Weekly produce market",
    "event_id": "event_1831@2026-05-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1831"
  },
  {
    "amount": "47",
    "category": "streaming",
    "currency": "USD",
    "date": "2026-05-09",
    "description": "Streaming subscription",
    "event_id": "event_1816@2026-05-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1816"
  },
  {
    "amount": "11",
    "category": "cloud_storage",
    "currency": "USD",
    "date": "2026-05-12",
    "description": "Online backup subscription",
    "event_id": "event_1815@2026-05-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1815"
  },
  {
    "amount": "126.38",
    "category": "shopping",
    "currency": "USD",
    "date": "2026-05-12",
    "description": "Monthly shopping spend",
    "event_id": "event_1817@2026-05-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1817"
  },
  {
    "amount": "2256",
    "category": "salary",
    "currency": "USD",
    "date": "2026-05-15",
    "description": "Payroll credit",
    "event_id": "event_1812@2026-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1812"
  },
  {
    "amount": "90.57",
    "category": "groceries",
    "currency": "USD",
    "date": "2026-05-16",
    "description": "Fresh food shop",
    "event_id": "event_1835@2026-05-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1835"
  },
  {
    "amount": "718.8",
    "category": "rent",
    "currency": "USD",
    "date": "2026-06-02",
    "description": "Residential rent payment",
    "event_id": "event_1818@2026-06-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1818"
  },
  {
    "amount": "104.19",
    "category": "groceries",
    "currency": "USD",
    "date": "2026-06-05",
    "description": "Weekly produce market",
    "event_id": "event_1831@2026-06-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1831"
  },
  {
    "amount": "124.08",
    "category": "utilities",
    "currency": "USD",
    "date": "2026-06-06",
    "description": "Municipal utilities",
    "event_id": "event_1814@2026-06-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1814"
  },
  {
    "amount": "47",
    "category": "streaming",
    "currency": "USD",
    "date": "2026-06-09",
    "description": "Streaming subscription",
    "event_id": "event_1816@2026-06-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1816"
  },
  {
    "amount": "11",
    "category": "cloud_storage",
    "currency": "USD",
    "date": "2026-06-12",
    "description": "Online backup subscription",
    "event_id": "event_1815@2026-06-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1815"
  },
  {
    "amount": "126.38",
    "category": "shopping",
    "currency": "USD",
    "date": "2026-06-12",
    "description": "Monthly shopping spend",
    "event_id": "event_1817@2026-06-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1817"
  },
  {
    "amount": "2256",
    "category": "salary",
    "currency": "USD",
    "date": "2026-06-15",
    "description": "Payroll credit",
    "event_id": "event_1812@2026-06-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1812"
  },
  {
    "amount": "90.57",
    "category": "groceries",
    "currency": "USD",
    "date": "2026-06-15",
    "description": "Fresh food shop",
    "event_id": "event_1835@2026-06-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1835"
  }
]
```

## `request_22` / `user_22`

- Opening/minimum: `1132.46` / `500`
- Expected safe amount: `475.46`; actual: `514.86`
- Expected earliest: `2025-01-15`; actual: `2024-12-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "earliest_date_for_full_payment": "earliest-full-date calculation from the baseline cash predicate"
}
```
- Future flow and balance path:
```text
2024-12-05 flow=-15.08 balance=1117.38
2024-12-07 flow=-31.52 balance=1085.86
2024-12-08 flow=-43 balance=1042.86
2024-12-11 flow=-17 balance=1025.86
2024-12-12 flow=-6 balance=1019.86
2024-12-14 flow=-5 balance=1014.86
2024-12-15 flow=574.18 balance=1589.04
2024-12-26 flow=-15.08 balance=1573.96
2025-01-03 flow=-178.2 balance=1395.76
2025-01-07 flow=-31.52 balance=1364.24
2025-01-11 flow=-17 balance=1347.24
2025-01-12 flow=-6 balance=1341.24
2025-01-14 flow=-5 balance=1336.24
2025-01-15 flow=574.18 balance=1910.42
2025-01-16 flow=-15.08 balance=1895.34
2025-02-03 flow=-178.2 balance=1717.14
2025-02-06 flow=-15.08 balance=1702.06
2025-02-07 flow=-31.52 balance=1670.54
2025-02-11 flow=-17 balance=1653.54
2025-02-12 flow=-6 balance=1647.54
2025-02-14 flow=-5 balance=1642.54
2025-02-15 flow=574.18 balance=2216.72
2025-02-27 flow=-15.08 balance=2201.64
2025-03-03 flow=-178.2 balance=2023.44
```
- Projected event attribution:
```json
[
  {
    "amount": "15.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2024-12-05",
    "description": "Ride-hailing trip",
    "event_id": "event_1943@2024-12-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1943"
  },
  {
    "amount": "31.52",
    "category": "utilities",
    "currency": "EUR",
    "date": "2024-12-07",
    "description": "Electricity and water bill",
    "event_id": "event_1889@2024-12-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1889"
  },
  {
    "amount": "17",
    "category": "gym",
    "currency": "EUR",
    "date": "2024-12-11",
    "description": "Gym membership",
    "event_id": "event_1892@2024-12-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1892"
  },
  {
    "amount": "6",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2024-12-12",
    "description": "Music service subscription",
    "event_id": "event_1890@2024-12-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1890"
  },
  {
    "amount": "5",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2024-12-14",
    "description": "Food delivery membership",
    "event_id": "event_1891@2024-12-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1891"
  },
  {
    "amount": "616",
    "category": "salary",
    "currency": "EUR",
    "date": "2024-12-15",
    "description": "Payroll credit",
    "event_id": "event_1887@2024-12-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1887"
  },
  {
    "amount": "23.29",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2024-12-15",
    "description": "Weekend entertainment",
    "event_id": "event_1893@2024-12-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1893"
  },
  {
    "amount": "18.53",
    "category": "dining",
    "currency": "EUR",
    "date": "2024-12-15",
    "description": "Weekend food delivery",
    "event_id": "event_1957@2024-12-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1957"
  },
  {
    "amount": "15.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2024-12-26",
    "description": "Ride-hailing trip",
    "event_id": "event_1943@2024-12-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1943"
  },
  {
    "amount": "178.2",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-01-03",
    "description": "Apartment rent transfer",
    "event_id": "event_1894@2025-01-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1894"
  },
  {
    "amount": "31.52",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-01-07",
    "description": "Electricity and water bill",
    "event_id": "event_1889@2025-01-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1889"
  },
  {
    "amount": "17",
    "category": "gym",
    "currency": "EUR",
    "date": "2025-01-11",
    "description": "Gym membership",
    "event_id": "event_1892@2025-01-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1892"
  },
  {
    "amount": "6",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2025-01-12",
    "description": "Music service subscription",
    "event_id": "event_1890@2025-01-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1890"
  },
  {
    "amount": "5",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2025-01-14",
    "description": "Food delivery membership",
    "event_id": "event_1891@2025-01-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1891"
  },
  {
    "amount": "616",
    "category": "salary",
    "currency": "EUR",
    "date": "2025-01-15",
    "description": "Payroll credit",
    "event_id": "event_1887@2025-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1887"
  },
  {
    "amount": "23.29",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2025-01-15",
    "description": "Weekend entertainment",
    "event_id": "event_1893@2025-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1893"
  },
  {
    "amount": "18.53",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-01-15",
    "description": "Weekend food delivery",
    "event_id": "event_1957@2025-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1957"
  },
  {
    "amount": "15.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-01-16",
    "description": "Ride-hailing trip",
    "event_id": "event_1943@2025-01-16",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1943"
  },
  {
    "amount": "178.2",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-02-03",
    "description": "Apartment rent transfer",
    "event_id": "event_1894@2025-02-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1894"
  },
  {
    "amount": "15.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-02-06",
    "description": "Ride-hailing trip",
    "event_id": "event_1943@2025-02-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1943"
  },
  {
    "amount": "31.52",
    "category": "utilities",
    "currency": "EUR",
    "date": "2025-02-07",
    "description": "Electricity and water bill",
    "event_id": "event_1889@2025-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1889"
  },
  {
    "amount": "17",
    "category": "gym",
    "currency": "EUR",
    "date": "2025-02-11",
    "description": "Gym membership",
    "event_id": "event_1892@2025-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1892"
  },
  {
    "amount": "6",
    "category": "music_subscription",
    "currency": "EUR",
    "date": "2025-02-12",
    "description": "Music service subscription",
    "event_id": "event_1890@2025-02-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1890"
  },
  {
    "amount": "5",
    "category": "delivery_membership",
    "currency": "EUR",
    "date": "2025-02-14",
    "description": "Food delivery membership",
    "event_id": "event_1891@2025-02-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1891"
  },
  {
    "amount": "616",
    "category": "salary",
    "currency": "EUR",
    "date": "2025-02-15",
    "description": "Payroll credit",
    "event_id": "event_1887@2025-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1887"
  },
  {
    "amount": "23.29",
    "category": "entertainment",
    "currency": "EUR",
    "date": "2025-02-15",
    "description": "Weekend entertainment",
    "event_id": "event_1893@2025-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1893"
  },
  {
    "amount": "18.53",
    "category": "dining",
    "currency": "EUR",
    "date": "2025-02-15",
    "description": "Weekend food delivery",
    "event_id": "event_1957@2025-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1957"
  },
  {
    "amount": "15.08",
    "category": "transport",
    "currency": "EUR",
    "date": "2025-02-27",
    "description": "Ride-hailing trip",
    "event_id": "event_1943@2025-02-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1943"
  },
  {
    "amount": "178.2",
    "category": "rent",
    "currency": "EUR",
    "date": "2025-03-03",
    "description": "Apartment rent transfer",
    "event_id": "event_1894@2025-03-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1894"
  }
]
```

## `request_23` / `user_23`

- Opening/minimum: `51957.9` / `27000`
- Expected safe amount: `9152`; actual: `9303.91`
- Expected earliest: `2025-07-15`; actual: `2025-07-15`
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2025-05-08 flow=-2915.67 balance=49042.23
2025-05-11 flow=-1553.2 balance=47489.03
2025-05-12 flow=-1439.91 balance=46049.12
2025-05-13 flow=-5852 balance=40197.12
2025-05-14 flow=-3893.21 balance=36303.91
2025-05-15 flow=41489.8 balance=77793.71
2025-05-28 flow=-2207.92 balance=75585.79
2025-06-04 flow=-15312 balance=60273.79
2025-06-08 flow=-2915.67 balance=57358.12
2025-06-11 flow=-2207.92 balance=55150.2
2025-06-12 flow=-2486.47 balance=52663.73
2025-06-13 flow=-5852 balance=46811.73
2025-06-14 flow=-1685.29 balance=45126.44
2025-06-15 flow=41489.8 balance=86616.24
2025-06-25 flow=-2207.92 balance=84408.32
2025-07-04 flow=-15312 balance=69096.32
2025-07-08 flow=-2915.67 balance=66180.65
2025-07-09 flow=-2207.92 balance=63972.73
2025-07-12 flow=-1439.91 balance=62532.82
2025-07-13 flow=-5852 balance=56680.82
2025-07-14 flow=-1685.29 balance=54995.53
2025-07-15 flow=41489.8 balance=96485.33
2025-07-23 flow=-2207.92 balance=94277.41
2025-07-24 flow=-1046.56 balance=93230.85
2025-08-04 flow=-15312 balance=77918.85
```
- Projected event attribution:
```json
[
  {
    "amount": "2915.67",
    "category": "utilities",
    "currency": "ZAR",
    "date": "2025-05-08",
    "description": "Electricity bill",
    "event_id": "event_1996@2025-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1996"
  },
  {
    "amount": "1439.91",
    "category": "healthcare",
    "currency": "ZAR",
    "date": "2025-05-12",
    "description": "Clinic payment",
    "event_id": "event_1998@2025-05-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1998"
  },
  {
    "amount": "5852",
    "category": "debt_repayment",
    "currency": "ZAR",
    "date": "2025-05-13",
    "description": "Education loan instalment",
    "event_id": "event_1997@2025-05-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1997"
  },
  {
    "amount": "295.9",
    "category": "cloud_storage",
    "currency": "ZAR",
    "date": "2025-05-14",
    "description": "Cloud storage plan",
    "event_id": "event_2000@2025-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2000"
  },
  {
    "amount": "1389.39",
    "category": "shopping",
    "currency": "ZAR",
    "date": "2025-05-14",
    "description": "Personal shopping",
    "event_id": "event_2001@2025-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2001"
  },
  {
    "amount": "2207.92",
    "category": "groceries",
    "currency": "ZAR",
    "date": "2025-05-14",
    "description": "Supermarket basket",
    "event_id": "event_2021@2025-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2021"
  },
  {
    "amount": "45760",
    "category": "salary",
    "currency": "ZAR",
    "date": "2025-05-15",
    "description": "Payroll credit",
    "event_id": "event_1994@2025-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1994"
  },
  {
    "amount": "4270.2",
    "category": "family_support",
    "currency": "ZAR",
    "date": "2025-05-15",
    "description": "Childcare contribution",
    "event_id": "event_1999@2025-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1999"
  },
  {
    "amount": "2207.92",
    "category": "groceries",
    "currency": "ZAR",
    "date": "2025-05-28",
    "description": "Supermarket basket",
    "event_id": "event_2021@2025-05-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2021"
  },
  {
    "amount": "15312",
    "category": "rent",
    "currency": "ZAR",
    "date": "2025-06-04",
    "description": "Shared housing rent",
    "event_id": "event_2002@2025-06-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2002"
  },
  {
    "amount": "2915.67",
    "category": "utilities",
    "currency": "ZAR",
    "date": "2025-06-08",
    "description": "Electricity bill",
    "event_id": "event_1996@2025-06-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1996"
  },
  {
    "amount": "2207.92",
    "category": "groceries",
    "currency": "ZAR",
    "date": "2025-06-11",
    "description": "Supermarket basket",
    "event_id": "event_2021@2025-06-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2021"
  },
  {
    "amount": "1439.91",
    "category": "healthcare",
    "currency": "ZAR",
    "date": "2025-06-12",
    "description": "Clinic payment",
    "event_id": "event_1998@2025-06-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1998"
  },
  {
    "amount": "1046.56",
    "category": "transport",
    "currency": "ZAR",
    "date": "2025-06-12",
    "description": "Metro and bus fares",
    "event_id": "event_2040@2025-06-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2040"
  },
  {
    "amount": "5852",
    "category": "debt_repayment",
    "currency": "ZAR",
    "date": "2025-06-13",
    "description": "Education loan instalment",
    "event_id": "event_1997@2025-06-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1997"
  },
  {
    "amount": "295.9",
    "category": "cloud_storage",
    "currency": "ZAR",
    "date": "2025-06-14",
    "description": "Cloud storage plan",
    "event_id": "event_2000@2025-06-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2000"
  },
  {
    "amount": "1389.39",
    "category": "shopping",
    "currency": "ZAR",
    "date": "2025-06-14",
    "description": "Personal shopping",
    "event_id": "event_2001@2025-06-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2001"
  },
  {
    "amount": "45760",
    "category": "salary",
    "currency": "ZAR",
    "date": "2025-06-15",
    "description": "Payroll credit",
    "event_id": "event_1994@2025-06-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1994"
  },
  {
    "amount": "4270.2",
    "category": "family_support",
    "currency": "ZAR",
    "date": "2025-06-15",
    "description": "Childcare contribution",
    "event_id": "event_1999@2025-06-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1999"
  },
  {
    "amount": "2207.92",
    "category": "groceries",
    "currency": "ZAR",
    "date": "2025-06-25",
    "description": "Supermarket basket",
    "event_id": "event_2021@2025-06-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2021"
  },
  {
    "amount": "15312",
    "category": "rent",
    "currency": "ZAR",
    "date": "2025-07-04",
    "description": "Shared housing rent",
    "event_id": "event_2002@2025-07-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2002"
  },
  {
    "amount": "2915.67",
    "category": "utilities",
    "currency": "ZAR",
    "date": "2025-07-08",
    "description": "Electricity bill",
    "event_id": "event_1996@2025-07-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1996"
  },
  {
    "amount": "2207.92",
    "category": "groceries",
    "currency": "ZAR",
    "date": "2025-07-09",
    "description": "Supermarket basket",
    "event_id": "event_2021@2025-07-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2021"
  },
  {
    "amount": "1439.91",
    "category": "healthcare",
    "currency": "ZAR",
    "date": "2025-07-12",
    "description": "Clinic payment",
    "event_id": "event_1998@2025-07-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1998"
  },
  {
    "amount": "5852",
    "category": "debt_repayment",
    "currency": "ZAR",
    "date": "2025-07-13",
    "description": "Education loan instalment",
    "event_id": "event_1997@2025-07-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1997"
  },
  {
    "amount": "295.9",
    "category": "cloud_storage",
    "currency": "ZAR",
    "date": "2025-07-14",
    "description": "Cloud storage plan",
    "event_id": "event_2000@2025-07-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2000"
  },
  {
    "amount": "1389.39",
    "category": "shopping",
    "currency": "ZAR",
    "date": "2025-07-14",
    "description": "Personal shopping",
    "event_id": "event_2001@2025-07-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2001"
  },
  {
    "amount": "45760",
    "category": "salary",
    "currency": "ZAR",
    "date": "2025-07-15",
    "description": "Payroll credit",
    "event_id": "event_1994@2025-07-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1994"
  },
  {
    "amount": "4270.2",
    "category": "family_support",
    "currency": "ZAR",
    "date": "2025-07-15",
    "description": "Childcare contribution",
    "event_id": "event_1999@2025-07-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_1999"
  },
  {
    "amount": "2207.92",
    "category": "groceries",
    "currency": "ZAR",
    "date": "2025-07-23",
    "description": "Supermarket basket",
    "event_id": "event_2021@2025-07-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2021"
  },
  {
    "amount": "1046.56",
    "category": "transport",
    "currency": "ZAR",
    "date": "2025-07-24",
    "description": "Metro and bus fares",
    "event_id": "event_2040@2025-07-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2040"
  },
  {
    "amount": "15312",
    "category": "rent",
    "currency": "ZAR",
    "date": "2025-08-04",
    "description": "Shared housing rent",
    "event_id": "event_2002@2025-08-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2002"
  }
]
```

## `request_24` / `user_24`

- Opening/minimum: `85045` / `51000`
- Expected safe amount: `13420`; actual: `12557.36`
- Expected earliest: ``; actual: ``
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution",
  "decision_explanation": "deterministic explanation-family/serialization downstream of decision"
}
```
- Future flow and balance path:
```text
2026-01-05 flow=-3490.5 balance=81554.5
2026-01-06 flow=-4770.73 balance=76783.77
2026-01-08 flow=-1200 balance=75583.77
2026-01-09 flow=-1600.18 balance=73983.59
2026-01-10 flow=-1893.38 balance=72090.21
2026-01-11 flow=-4865.78 balance=67224.43
2026-01-12 flow=-1750.91 balance=65473.52
2026-01-13 flow=-1916.16 balance=63557.36
2026-01-15 flow=61000 balance=124557.36
2026-01-17 flow=-1893.38 balance=122663.98
2026-01-22 flow=-1750.91 balance=120913.07
2026-01-24 flow=-1893.38 balance=119019.69
2026-01-26 flow=-6135.67 balance=112884.02
2026-01-31 flow=-1893.38 balance=110990.64
2026-02-01 flow=-20350.91 balance=90639.73
2026-02-05 flow=-5090.68 balance=85549.05
2026-02-06 flow=-2510 balance=83039.05
2026-02-07 flow=-1893.38 balance=81145.67
2026-02-08 flow=-1200 balance=79945.67
2026-02-11 flow=-4786.69 balance=75158.98
2026-02-13 flow=-1916.16 balance=73242.82
2026-02-14 flow=-1893.38 balance=71349.44
2026-02-15 flow=58739.27 balance=130088.71
2026-02-21 flow=-3644.29 balance=126444.42
2026-02-25 flow=-2113.95 balance=124330.47
2026-02-28 flow=-1893.38 balance=122437.09
2026-03-01 flow=-18600 balance=103837.09
2026-03-03 flow=-1750.91 balance=102086.18
2026-03-04 flow=-1600.18 balance=100486
2026-03-05 flow=-3490.5 balance=96995.5
2026-03-06 flow=-2510 balance=94485.5
2026-03-07 flow=-4154.11 balance=90331.39
2026-03-08 flow=-1200 balance=89131.39
2026-03-11 flow=-3035.78 balance=86095.61
2026-03-13 flow=-3667.07 balance=82428.54
2026-03-14 flow=-3654.37 balance=78774.17
2026-03-15 flow=61000 balance=139774.17
2026-03-21 flow=-1893.38 balance=137880.79
2026-03-23 flow=-1750.91 balance=136129.88
2026-03-27 flow=-4374.68 balance=131755.2
2026-03-28 flow=-1893.38 balance=129861.82
2026-03-31 flow=-1600.18 balance=128261.64
2026-04-01 flow=-18600 balance=109661.64
2026-04-02 flow=-1750.91 balance=107910.73
```
- Projected event attribution:
```json
[
  {
    "amount": "3490.5",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-01-05",
    "description": "Household utility payment",
    "event_id": "event_2077@2026-01-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2077"
  },
  {
    "amount": "2510",
    "category": "insurance",
    "currency": "INR",
    "date": "2026-01-06",
    "description": "Insurance policy payment",
    "event_id": "event_2078@2026-01-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2078"
  },
  {
    "amount": "2260.73",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-01-06",
    "description": "Household groceries",
    "event_id": "event_2100@2026-01-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2100"
  },
  {
    "amount": "1200",
    "category": "streaming",
    "currency": "INR",
    "date": "2026-01-08",
    "description": "Family streaming plan",
    "event_id": "event_2080@2026-01-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2080"
  },
  {
    "amount": "1600.18",
    "category": "transport",
    "currency": "INR",
    "date": "2026-01-09",
    "description": "Metro and bus fares",
    "event_id": "event_2133@2026-01-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2133"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-01-10",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-01-10",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "355",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2026-01-11",
    "description": "Online backup subscription",
    "event_id": "event_2079@2026-01-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2079"
  },
  {
    "amount": "2680.78",
    "category": "shopping",
    "currency": "INR",
    "date": "2026-01-11",
    "description": "Monthly shopping spend",
    "event_id": "event_2081@2026-01-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2081"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-01-12",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-01-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "1916.16",
    "category": "entertainment",
    "currency": "INR",
    "date": "2026-01-13",
    "description": "Local event tickets",
    "event_id": "event_2082@2026-01-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2082"
  },
  {
    "amount": "61000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-01-15",
    "description": "Payroll credit",
    "event_id": "event_2075@2026-01-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2075"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-01-17",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-01-17",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-01-22",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-01-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-01-24",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-01-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "2113.95",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-01-26",
    "description": "Neighbourhood grocer",
    "event_id": "event_2098@2026-01-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2098"
  },
  {
    "amount": "2260.73",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-01-26",
    "description": "Household groceries",
    "event_id": "event_2100@2026-01-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2100"
  },
  {
    "amount": "1760.99",
    "category": "transport",
    "currency": "INR",
    "date": "2026-01-26",
    "description": "Local taxi",
    "event_id": "event_2123@2026-01-26",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2123"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-01-31",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-01-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "18600",
    "category": "rent",
    "currency": "INR",
    "date": "2026-02-01",
    "description": "Landlord standing order",
    "event_id": "event_2083@2026-02-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2083"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-02-01",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-02-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "3490.5",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-02-05",
    "description": "Household utility payment",
    "event_id": "event_2077@2026-02-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2077"
  },
  {
    "amount": "1600.18",
    "category": "transport",
    "currency": "INR",
    "date": "2026-02-05",
    "description": "Metro and bus fares",
    "event_id": "event_2133@2026-02-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2133"
  },
  {
    "amount": "2510",
    "category": "insurance",
    "currency": "INR",
    "date": "2026-02-06",
    "description": "Insurance policy payment",
    "event_id": "event_2078@2026-02-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2078"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-02-07",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-02-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "1200",
    "category": "streaming",
    "currency": "INR",
    "date": "2026-02-08",
    "description": "Family streaming plan",
    "event_id": "event_2080@2026-02-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2080"
  },
  {
    "amount": "355",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2026-02-11",
    "description": "Online backup subscription",
    "event_id": "event_2079@2026-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2079"
  },
  {
    "amount": "2680.78",
    "category": "shopping",
    "currency": "INR",
    "date": "2026-02-11",
    "description": "Monthly shopping spend",
    "event_id": "event_2081@2026-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2081"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-02-11",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-02-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "1916.16",
    "category": "entertainment",
    "currency": "INR",
    "date": "2026-02-13",
    "description": "Local event tickets",
    "event_id": "event_2082@2026-02-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2082"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-02-14",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-02-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "61000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-02-15",
    "description": "Payroll credit",
    "event_id": "event_2075@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2075"
  },
  {
    "amount": "2260.73",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-02-15",
    "description": "Household groceries",
    "event_id": "event_2100@2026-02-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2100"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-02-21",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-02-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-02-21",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-02-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "2113.95",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-02-25",
    "description": "Neighbourhood grocer",
    "event_id": "event_2098@2026-02-25",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2098"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-02-28",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-02-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "18600",
    "category": "rent",
    "currency": "INR",
    "date": "2026-03-01",
    "description": "Landlord standing order",
    "event_id": "event_2083@2026-03-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2083"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-03",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-03-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "1600.18",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-04",
    "description": "Metro and bus fares",
    "event_id": "event_2133@2026-03-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2133"
  },
  {
    "amount": "3490.5",
    "category": "utilities",
    "currency": "INR",
    "date": "2026-03-05",
    "description": "Household utility payment",
    "event_id": "event_2077@2026-03-05",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2077"
  },
  {
    "amount": "2510",
    "category": "insurance",
    "currency": "INR",
    "date": "2026-03-06",
    "description": "Insurance policy payment",
    "event_id": "event_2078@2026-03-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2078"
  },
  {
    "amount": "2260.73",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-07",
    "description": "Household groceries",
    "event_id": "event_2100@2026-03-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2100"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-03-07",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-03-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "1200",
    "category": "streaming",
    "currency": "INR",
    "date": "2026-03-08",
    "description": "Family streaming plan",
    "event_id": "event_2080@2026-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2080"
  },
  {
    "amount": "355",
    "category": "cloud_storage",
    "currency": "INR",
    "date": "2026-03-11",
    "description": "Online backup subscription",
    "event_id": "event_2079@2026-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2079"
  },
  {
    "amount": "2680.78",
    "category": "shopping",
    "currency": "INR",
    "date": "2026-03-11",
    "description": "Monthly shopping spend",
    "event_id": "event_2081@2026-03-11",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2081"
  },
  {
    "amount": "1916.16",
    "category": "entertainment",
    "currency": "INR",
    "date": "2026-03-13",
    "description": "Local event tickets",
    "event_id": "event_2082@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2082"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-13",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-03-13",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "1760.99",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-14",
    "description": "Local taxi",
    "event_id": "event_2123@2026-03-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2123"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-03-14",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-03-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "61000",
    "category": "salary",
    "currency": "INR",
    "date": "2026-03-15",
    "description": "Payroll credit",
    "event_id": "event_2075@2026-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2075"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-03-21",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-03-21",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-23",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-03-23",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  },
  {
    "amount": "2113.95",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-27",
    "description": "Neighbourhood grocer",
    "event_id": "event_2098@2026-03-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2098"
  },
  {
    "amount": "2260.73",
    "category": "groceries",
    "currency": "INR",
    "date": "2026-03-27",
    "description": "Household groceries",
    "event_id": "event_2100@2026-03-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2100"
  },
  {
    "amount": "1893.38",
    "category": "dining",
    "currency": "INR",
    "date": "2026-03-28",
    "description": "Coffee shop",
    "event_id": "event_2155@2026-03-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2155"
  },
  {
    "amount": "1600.18",
    "category": "transport",
    "currency": "INR",
    "date": "2026-03-31",
    "description": "Metro and bus fares",
    "event_id": "event_2133@2026-03-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2133"
  },
  {
    "amount": "18600",
    "category": "rent",
    "currency": "INR",
    "date": "2026-04-01",
    "description": "Landlord standing order",
    "event_id": "event_2083@2026-04-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2083"
  },
  {
    "amount": "1750.91",
    "category": "transport",
    "currency": "INR",
    "date": "2026-04-02",
    "description": "Ride-hailing trip",
    "event_id": "event_2121@2026-04-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2121"
  }
]
```

## `request_25` / `user_25`

- Opening/minimum: `32063050` / `23379100`
- Expected safe amount: `1425000`; actual: `0`
- Expected earliest: ``; actual: ``
- Classified differences:
```json
{
  "amount_safe_to_pay": "recurrence/active-state/lifecycle upstream forecast attribution"
}
```
- Future flow and balance path:
```text
2024-03-06 flow=-2290659.42 balance=29772390.58
2024-03-07 flow=-904400 balance=28867990.58
2024-03-08 flow=-2618569.01 balance=26249421.57
2024-03-09 flow=-1675144.82 balance=24574276.75
2024-03-12 flow=-1296621.29 balance=23277655.46
2024-03-14 flow=-504697.37 balance=22772958.09
2024-03-15 flow=27804944.54 balance=50577902.63
2024-03-19 flow=-1101344.82 balance=49476557.81
2024-03-20 flow=-663001.49 balance=48813556.32
2024-03-27 flow=-1204804.45 balance=47608751.87
2024-03-29 flow=-1101344.82 balance=46507407.05
2024-03-31 flow=-721837.88 balance=45785569.17
2024-04-02 flow=-6954000 balance=38831569.17
2024-04-03 flow=-949118.03 balance=37882451.14
2024-04-04 flow=-695049.46 balance=37187401.68
2024-04-06 flow=-1341541.39 balance=35845860.29
2024-04-07 flow=-904400 balance=34941460.29
2024-04-08 flow=-3719913.83 balance=31221546.46
2024-04-09 flow=-573800 balance=30647746.46
2024-04-12 flow=-1296621.29 balance=29351125.17
2024-04-14 flow=-1167698.86 balance=28183426.31
2024-04-15 flow=28499994 balance=56683420.31
2024-04-18 flow=-1101344.82 balance=55582075.49
2024-04-24 flow=-1899853.91 balance=53682221.58
2024-04-28 flow=-1101344.82 balance=52580876.76
2024-04-30 flow=-721837.88 balance=51859038.88
2024-05-01 flow=-949118.03 balance=50909920.85
2024-05-02 flow=-6954000 balance=43955920.85
2024-05-06 flow=-1341541.39 balance=42614379.46
2024-05-07 flow=-904400 balance=41709979.46
2024-05-08 flow=-3719913.83 balance=37990065.63
2024-05-09 flow=-1236801.49 balance=36753264.14
2024-05-12 flow=-1296621.29 balance=35456642.85
2024-05-14 flow=-1199746.83 balance=34256896.02
2024-05-15 flow=28499994 balance=62756890.02
2024-05-18 flow=-1101344.82 balance=61655545.2
2024-05-22 flow=-1204804.45 balance=60450740.75
2024-05-28 flow=-1101344.82 balance=59349395.93
2024-05-29 flow=-949118.03 balance=58400277.9
2024-05-31 flow=-721837.88 balance=57678440.02
2024-06-02 flow=-6954000 balance=50724440.02
2024-06-03 flow=-1358050.95 balance=49366389.07
```
- Projected event attribution:
```json
[
  {
    "amount": "1341541.39",
    "category": "utilities",
    "currency": "IDR",
    "date": "2024-03-06",
    "description": "Household utility payment",
    "event_id": "event_2201@2024-03-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2201"
  },
  {
    "amount": "949118.03",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-03-06",
    "description": "Coffee shop",
    "event_id": "event_2283@2024-03-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2283"
  },
  {
    "amount": "904400",
    "category": "insurance",
    "currency": "IDR",
    "date": "2024-03-07",
    "description": "Insurance policy payment",
    "event_id": "event_2202@2024-03-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2202"
  },
  {
    "amount": "1369082.68",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-03-08",
    "description": "Household groceries",
    "event_id": "event_2223@2024-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2223"
  },
  {
    "amount": "1249486.33",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-03-08",
    "description": "Weekend food delivery",
    "event_id": "event_2270@2024-03-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2270"
  },
  {
    "amount": "573800",
    "category": "streaming",
    "currency": "IDR",
    "date": "2024-03-09",
    "description": "Video streaming plan",
    "event_id": "event_2204@2024-03-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2204"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-03-09",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-03-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "126350",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2024-03-12",
    "description": "Cloud storage plan",
    "event_id": "event_2203@2024-03-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2203"
  },
  {
    "amount": "1170271.29",
    "category": "shopping",
    "currency": "IDR",
    "date": "2024-03-12",
    "description": "Monthly shopping spend",
    "event_id": "event_2205@2024-03-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2205"
  },
  {
    "amount": "504697.37",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2024-03-14",
    "description": "Games and recreation",
    "event_id": "event_2206@2024-03-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2206"
  },
  {
    "amount": "695049.46",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-03-15",
    "description": "Parking and tolls",
    "event_id": "event_2247@2024-03-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2247"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-03-19",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-03-19",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "663001.49",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-03-20",
    "description": "Metro and bus fares",
    "event_id": "event_2259@2024-03-20",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2259"
  },
  {
    "amount": "1204804.45",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-03-27",
    "description": "Neighbourhood restaurant",
    "event_id": "event_2286@2024-03-27",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2286"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-03-29",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-03-29",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "721837.88",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-03-31",
    "description": "Rail pass",
    "event_id": "event_2248@2024-03-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2248"
  },
  {
    "amount": "6954000",
    "category": "rent",
    "currency": "IDR",
    "date": "2024-04-02",
    "description": "Monthly rent",
    "event_id": "event_2207@2024-04-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2207"
  },
  {
    "amount": "949118.03",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-04-03",
    "description": "Coffee shop",
    "event_id": "event_2283@2024-04-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2283"
  },
  {
    "amount": "695049.46",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-04-04",
    "description": "Parking and tolls",
    "event_id": "event_2247@2024-04-04",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2247"
  },
  {
    "amount": "1341541.39",
    "category": "utilities",
    "currency": "IDR",
    "date": "2024-04-06",
    "description": "Household utility payment",
    "event_id": "event_2201@2024-04-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2201"
  },
  {
    "amount": "904400",
    "category": "insurance",
    "currency": "IDR",
    "date": "2024-04-07",
    "description": "Insurance policy payment",
    "event_id": "event_2202@2024-04-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2202"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-04-08",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-04-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "1369082.68",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-04-08",
    "description": "Household groceries",
    "event_id": "event_2223@2024-04-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2223"
  },
  {
    "amount": "1249486.33",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-04-08",
    "description": "Weekend food delivery",
    "event_id": "event_2270@2024-04-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2270"
  },
  {
    "amount": "573800",
    "category": "streaming",
    "currency": "IDR",
    "date": "2024-04-09",
    "description": "Video streaming plan",
    "event_id": "event_2204@2024-04-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2204"
  },
  {
    "amount": "126350",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2024-04-12",
    "description": "Cloud storage plan",
    "event_id": "event_2203@2024-04-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2203"
  },
  {
    "amount": "1170271.29",
    "category": "shopping",
    "currency": "IDR",
    "date": "2024-04-12",
    "description": "Monthly shopping spend",
    "event_id": "event_2205@2024-04-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2205"
  },
  {
    "amount": "504697.37",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2024-04-14",
    "description": "Games and recreation",
    "event_id": "event_2206@2024-04-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2206"
  },
  {
    "amount": "663001.49",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-04-14",
    "description": "Metro and bus fares",
    "event_id": "event_2259@2024-04-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2259"
  },
  {
    "amount": "1800",
    "category": "salary",
    "currency": "USD",
    "date": "2024-04-15",
    "description": "International employer payroll",
    "event_id": "event_2199@2024-04-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2199"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-04-18",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-04-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "695049.46",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-04-24",
    "description": "Parking and tolls",
    "event_id": "event_2247@2024-04-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2247"
  },
  {
    "amount": "1204804.45",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-04-24",
    "description": "Neighbourhood restaurant",
    "event_id": "event_2286@2024-04-24",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2286"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-04-28",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-04-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "721837.88",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-04-30",
    "description": "Rail pass",
    "event_id": "event_2248@2024-04-30",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2248"
  },
  {
    "amount": "949118.03",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-05-01",
    "description": "Coffee shop",
    "event_id": "event_2283@2024-05-01",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2283"
  },
  {
    "amount": "6954000",
    "category": "rent",
    "currency": "IDR",
    "date": "2024-05-02",
    "description": "Monthly rent",
    "event_id": "event_2207@2024-05-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2207"
  },
  {
    "amount": "1341541.39",
    "category": "utilities",
    "currency": "IDR",
    "date": "2024-05-06",
    "description": "Household utility payment",
    "event_id": "event_2201@2024-05-06",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2201"
  },
  {
    "amount": "904400",
    "category": "insurance",
    "currency": "IDR",
    "date": "2024-05-07",
    "description": "Insurance policy payment",
    "event_id": "event_2202@2024-05-07",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2202"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-05-08",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "1369082.68",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-05-08",
    "description": "Household groceries",
    "event_id": "event_2223@2024-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2223"
  },
  {
    "amount": "1249486.33",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-05-08",
    "description": "Weekend food delivery",
    "event_id": "event_2270@2024-05-08",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2270"
  },
  {
    "amount": "573800",
    "category": "streaming",
    "currency": "IDR",
    "date": "2024-05-09",
    "description": "Video streaming plan",
    "event_id": "event_2204@2024-05-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2204"
  },
  {
    "amount": "663001.49",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-05-09",
    "description": "Metro and bus fares",
    "event_id": "event_2259@2024-05-09",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2259"
  },
  {
    "amount": "126350",
    "category": "cloud_storage",
    "currency": "IDR",
    "date": "2024-05-12",
    "description": "Cloud storage plan",
    "event_id": "event_2203@2024-05-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2203"
  },
  {
    "amount": "1170271.29",
    "category": "shopping",
    "currency": "IDR",
    "date": "2024-05-12",
    "description": "Monthly shopping spend",
    "event_id": "event_2205@2024-05-12",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2205"
  },
  {
    "amount": "504697.37",
    "category": "entertainment",
    "currency": "IDR",
    "date": "2024-05-14",
    "description": "Games and recreation",
    "event_id": "event_2206@2024-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2206"
  },
  {
    "amount": "695049.46",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-05-14",
    "description": "Parking and tolls",
    "event_id": "event_2247@2024-05-14",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2247"
  },
  {
    "amount": "1800",
    "category": "salary",
    "currency": "USD",
    "date": "2024-05-15",
    "description": "International employer payroll",
    "event_id": "event_2199@2024-05-15",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2199"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-05-18",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-05-18",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "1204804.45",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-05-22",
    "description": "Neighbourhood restaurant",
    "event_id": "event_2286@2024-05-22",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2286"
  },
  {
    "amount": "1101344.82",
    "category": "groceries",
    "currency": "IDR",
    "date": "2024-05-28",
    "description": "Neighbourhood grocer",
    "event_id": "event_2218@2024-05-28",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2218"
  },
  {
    "amount": "949118.03",
    "category": "dining",
    "currency": "IDR",
    "date": "2024-05-29",
    "description": "Coffee shop",
    "event_id": "event_2283@2024-05-29",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2283"
  },
  {
    "amount": "721837.88",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-05-31",
    "description": "Rail pass",
    "event_id": "event_2248@2024-05-31",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2248"
  },
  {
    "amount": "6954000",
    "category": "rent",
    "currency": "IDR",
    "date": "2024-06-02",
    "description": "Monthly rent",
    "event_id": "event_2207@2024-06-02",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2207"
  },
  {
    "amount": "695049.46",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-03",
    "description": "Parking and tolls",
    "event_id": "event_2247@2024-06-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2247"
  },
  {
    "amount": "663001.49",
    "category": "transport",
    "currency": "IDR",
    "date": "2024-06-03",
    "description": "Metro and bus fares",
    "event_id": "event_2259@2024-06-03",
    "provenance": "recurrence:max_last_3",
    "source_event_id": "event_2259"
  }
]
```
