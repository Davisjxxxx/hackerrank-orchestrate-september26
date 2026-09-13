# Final recurrence top-five diagnosis

This is evaluation evidence only. No sample answer is used by runtime logic and
`code/main.py` remains the R0 control.

## Common result

All five ranked policies retained **3/25 exact rows**, **4/25 exact safe
amounts**, and **21/25 numeric mismatches**. The first policy reduced aggregate
absolute error to `5,203,249.78`, but this was a redistribution of non-exact
amounts, not a correction of a numeric residual. Policies 2 and 3 were
metrics-equivalent to R0; policies 4 and 5 increased aggregate error.

## Top-five policy effects

| Rank | Global difference from R0 | Safe-amount changes | Error improvements | Error regressions | Result |
|---:|---|---:|---:|---:|---|
| 1 | A0 chronology, fixed tolerance 4, debit/credit median | 16 | 7 | 9 | No exact or numeric gain |
| 2 | Credit median only (R0 debit max) | 0 | 0 | 0 | Equivalent to R0 |
| 3 | Credit median plus loose monthly range | 0 | 0 | 0 | Equivalent to R0 |
| 4 | A0, fixed tolerance 3, debit/credit median | 15 | 2 | 13 | Worse aggregate error |
| 5 | Same as 4 with loose monthly range | 15 | 2 | 13 | Worse aggregate error |

For rank 1, the improved requests were `request_04`, `request_08`,
`request_17`, `request_19`, `request_22`, `request_24`, and `request_25`.
The regressed requests were `request_02`, `request_03`, `request_05`,
`request_07`, `request_14`, `request_15`, `request_18`, `request_20`, and
`request_23`. No request reached an exact safe amount that
was not already exact under R0.

## Structural checks

- `178/25342` financial-event rows have different `event_date` and cash date;
  cash-date A1/A2 variants did not improve exact safe amounts and reduced
  earliest-date accuracy from `18/25` to `17/25` in the best comparable rows.
- Conservative lowercase/date/reference normalization produced **zero**
  multi-description debit groups. There is therefore no dataset-supported
  normalization collision to promote.
- Debit-only category shortfall completion was tested in the bounded search.
  It added unsupported-looking obligations broadly; the best shortfall policy
  had `3/25` exact rows, `3/25` exact safe amounts, `22` numeric mismatches,
  and degraded status/method/plan accuracy.

## One derived candidate

The permitted final derived candidate was:

`A1 + debit=max + credit=latest + fixed tolerance=4 + strict monthly range + 3 complete periods + latest period estimator + latest phase + debit-only shortfall`

It produced `2/25` exact rows, `3/25` exact safe amounts, `22` numeric
mismatches, absolute error `5,042,179.09`, status `13/25`, method `15/25`,
plan `15/25`, and earliest `13/25`. It was rejected.

## Conclusion

No defensible global chronology, amount, exact-description, or debit-category
completion policy beat R0 on exact correctness. No production policy was
promoted.
