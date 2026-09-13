# Phase-aware recurrence comparison

The phase-aware experiment is compared directly with the current production checkpoint against all 25 solved rows. It is not promoted automatically.

| Policy | Exact rows | Differing fields | Improved requests | Regressed requests | False-merge proxy | False-split proxy |
|---|---:|---:|---|---|---:|---:|
| Current production | 3/25 | 67 | n/a | n/a | n/a | n/a |
| phase_aware_temporal_partition | 2/25 | 81 | none | request_01 | 1 | 0 |

## Changed projected streams

- `request_01`: current=40 projected rows, phase-aware=48 projected rows; added=31, removed=23
- `request_02`: current=33 projected rows, phase-aware=42 projected rows; added=19, removed=10
- `request_03`: current=49 projected rows, phase-aware=35 projected rows; added=16, removed=30
- `request_04`: current=47 projected rows, phase-aware=53 projected rows; added=31, removed=25
- `request_05`: current=24 projected rows, phase-aware=40 projected rows; added=19, removed=3
- `request_06`: current=53 projected rows, phase-aware=64 projected rows; added=40, removed=29
- `request_07`: current=27 projected rows, phase-aware=28 projected rows; added=14, removed=13
- `request_08`: current=28 projected rows, phase-aware=54 projected rows; added=32, removed=6
- `request_09`: current=36 projected rows, phase-aware=37 projected rows; added=17, removed=16
- `request_10`: current=38 projected rows, phase-aware=61 projected rows; added=43, removed=20
- `request_11`: current=50 projected rows, phase-aware=46 projected rows; added=17, removed=21
- `request_12`: current=35 projected rows, phase-aware=35 projected rows; added=15, removed=15
- `request_13`: current=39 projected rows, phase-aware=54 projected rows; added=31, removed=16
- `request_14`: current=51 projected rows, phase-aware=38 projected rows; added=12, removed=25
- `request_15`: current=56 projected rows, phase-aware=51 projected rows; added=33, removed=38
- `request_16`: current=24 projected rows, phase-aware=50 projected rows; added=32, removed=6
- `request_17`: current=57 projected rows, phase-aware=52 projected rows; added=25, removed=30
- `request_18`: current=26 projected rows, phase-aware=39 projected rows; added=21, removed=8
- `request_19`: current=43 projected rows, phase-aware=43 projected rows; added=19, removed=19
- `request_20`: current=45 projected rows, phase-aware=45 projected rows; added=20, removed=20
- `request_21`: current=33 projected rows, phase-aware=34 projected rows; added=9, removed=8
- `request_22`: current=36 projected rows, phase-aware=52 projected rows; added=30, removed=14
- `request_23`: current=31 projected rows, phase-aware=43 projected rows; added=18, removed=6
- `request_24`: current=27 projected rows, phase-aware=63 projected rows; added=39, removed=3
- `request_25`: current=37 projected rows, phase-aware=64 projected rows; added=40, removed=13

The phase-aware policy is rejected for production promotion because it loses one current exact row, gains no exact rows, and remains byte-incompatible with the solved samples.
