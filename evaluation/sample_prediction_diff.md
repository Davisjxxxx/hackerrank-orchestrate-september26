# Solved-sample prediction diff

Command: `python3 code/main.py --samples` followed by an in-memory comparison
with `dataset/sample_requests.csv`. The reference mode does not overwrite the
root target output.

| Metric | Result |
|---|---:|
| Rows | 25 |
| Full-row exact | 3/25 |
| Amount-safe exact | 4/25 |
| Numeric amount mismatches | 21 |
| Absolute safe-amount error | 6,930,596.72 |

Numeric differences (`expected -> actual`) were:

| Request | Expected | Actual | Delta |
|---|---:|---:|---:|
| request_02 | 17,229,139.20 | 18,479,330.16 | +1,250,190.96 |
| request_03 | 873,000 | 1,050,071.39 | +177,071.39 |
| request_04 | 8,401,800 | 11,584,778.17 | +3,182,978.17 |
| request_05 | 737 | 7,006.21 | +6,269.21 |
| request_06 | 603.30 | 620.40 | +17.10 |
| request_07 | 87,170.56 | 98,080.53 | +10,909.97 |
| request_08 | 284.57 | 383.59 | +99.02 |
| request_10 | 12,700 | 266,700 | +254,000 |
| request_11 | 12,510,645 | 13,110,000 | +599,355 |
| request_13 | 433.40 | 941.60 | +508.20 |
| request_14 | 597.74 | 613.64 | +15.90 |
| request_15 | 83.05 | 225.66 | +142.61 |
| request_17 | 243,849.58 | 248,325.96 | +4,476.38 |
| request_18 | 462 | 662.19 | +200.19 |
| request_19 | 28,820 | 37,555.87 | +8,735.87 |
| request_20 | 5,400 | 14,941.75 | +9,541.75 |
| request_21 | 1,543.35 | 1,574.40 | +31.05 |
| request_22 | 475.46 | 514.86 | +39.40 |
| request_23 | 9,152 | 9,303.91 | +151.91 |
| request_24 | 13,420 | 12,557.36 | -862.64 |
| request_25 | 1,425,000 | 0 | -1,425,000 |

Non-numeric differing fields are recurrence-derived downstream fields or
explanation text; the complete field list is emitted by the comparison
command and remains unchanged from the frozen R0 benchmark.
