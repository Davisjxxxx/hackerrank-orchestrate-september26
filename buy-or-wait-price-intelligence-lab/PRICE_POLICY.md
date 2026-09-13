# Deterministic price policy

The price engine uses `Decimal` for every monetary operation.

1. Ignore unavailable, stale current, below-threshold-match-confidence, and non-accepted-condition observations.
2. Deduplicate repeated aggregator rows by provider, retailer, day, landed price, condition, source URL, and currency. When rows share that identity, choose the surviving observation deterministically by trust, monetary validity, availability, freshness, match confidence, recency, and stable provenance rather than insertion order.
3. Choose the lowest fresh new offer as the new-condition anchor when one exists. Never mix new/open-box/refurbished/used histories.
4. Use distinct currency values to detect mixed currency. A unique dominant currency can be evaluated with `MIXED_CURRENCY_IGNORED` evidence and no FX conversion. A tied mixed-currency set has no authoritative home-currency/FX policy and returns `INSUFFICIENT_DATA` with `MIXED_CURRENCY_AMBIGUOUS`; raw numeric prices are never compared across currencies.
5. Require minimum count and span before applying a target. Sparse history returns `SET_PRICE_WATCH` unless urgency is immediate.
6. Report the lowest observed price in the covered dataset, median, and p25 for context. Estimate the target from the 5th/95th-percentile winsorized distribution's p25 so one anomalous low does not become an automatic target. Do not label the minimum an all-time market low without external coverage.
7. Count unique deal dates and cluster dates within the configured episode gap. Repeated observations from one sale do not create fake episodes. Recurrence wait is estimated only when at least two distinct episodes exist, using the interval between episodes rather than dividing the covered span by the number of episodes.
8. Compare landed price (`item + shipping`), source freshness, distinct source/retailer count, history coverage, condition, identity confidence, and episode count in evidence.
9. Historical low is context. A low rank/near-low price, material savings, recurring episodes inside the wait window, urgency, or a watch state determines the timing recommendation.
10. Financial composition runs after price intelligence. `NOT_AFFORDABLE` maps to `NOT_RECOMMENDED`, `SAFE_LATER` maps to `FINANCIALLY_WAIT`, and `SAFE_WITH_PLAN` remains conservative and maps to `FINANCIALLY_WAIT` until installment semantics are proven. SAFE_NOW contradiction checks use `financial_data_as_of`, then explicit evaluation `as_of`; future-dated, missing-time, stale, partial, or contradictory evidence cannot authorize a buy.

This is a deterministic policy, not a claim of predictive accuracy. Seasonality, retailer-specific priors, coupon/member-only semantics, and tax are evidence fields or future adapter work until their provenance is authorized and sufficient.
