# Proprietary price-data moat

## Built now

- stable product identity and condition-aware observation model;
- provenance-preserving first-party observation persistence;
- deterministic duplicate suppression with private user-capture partition;
- SQLite persistence port plus in-memory fixture store;
- low/high/average/median/percentile statistics;
- price trend and signal with explicit `SUFFICIENT`, `INSUFFICIENT`, and
  `UNAVAILABLE` states;
- current-offer ingestion path that can capture every legitimate normalized
  observation;
- watch evaluation that feeds eligible observations back into history.

Keepa required: NO. Optional external history providers can corroborate or
backfill later, but the product's canonical history is first-party and does
not depend on Keepa.

## Growth path

```text
current observations
→ longitudinal product histories
→ category histories
→ seasonality
→ sale frequency
→ launch/replacement effects
→ price forecasting
→ personalized purchase timing
```

Near-term ingestion should add authorized retailer/marketplace feeds, explicit
rate limits, seller and variant reconciliation, freshness policies, and
scheduled watch refreshes. Later layers can learn category priors, replacement
cycles, forecast intervals, and personalized urgency while preserving the
original observation provenance and uncertainty.

## Integrity rules

Invalid or unresolved offers are not authoritative observations. New, used,
refurbished, open-box, and unknown conditions stay separate. A user capture is
private evidence unless corroborated. Sparse data remains sparse; the system
does not fabricate historical prices or trends.
