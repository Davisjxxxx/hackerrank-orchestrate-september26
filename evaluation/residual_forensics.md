# Residual forensic ledger

Generated from current R0 at `days_0_through_89`. `delta = predicted safe - expected safe`; positive means production grants too much capacity.

- Numeric residual rows: 21/25
- Event-level attribution rows: 737

## Algebraic families

| Family | Requests | Count | Absolute safe error | Interpretation |
|---|---|---:|---:|---|
| missing debit / extra credit / delayed debit | request_02, request_03, request_04, request_05, request_06, request_07, request_08, request_10, request_11, request_13, request_14, request_15, request_17, request_18, request_19, request_20, request_21, request_22, request_23 | 19 | 5504734.08 | actual forecast is too optimistic |
| extra debit / missing credit / early debit | request_24, request_25 | 2 | 1425862.64 | actual forecast is too pessimistic or early |

## Interpretation

The algebra identifies the trough difference but does not by itself identify a unique event correction. Positive rows require additional debit pressure, removal of credit, or earlier debit timing; negative rows require the inverse. Event-level candidates are in `residual_cashflow_items.csv`; no expected values are used by production.
