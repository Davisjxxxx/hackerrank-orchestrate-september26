# Buy or Wait? unified system architecture

```text
INPUT
│
├── URL
├── Search
├── Barcode
├── Photo / Screenshot
└── Financial Input
        │
        ▼
PRODUCT IDENTITY
        │
        ├───────────────────────┐
        ▼                       ▼
PRICE INTELLIGENCE        FINANCIAL INTELLIGENCE
        │                       │
Current offers             Canonical state
Internal history           90-day safety
Used/refurb                Safe-to-pay
Price signal               Payment options
        │                       │
        └────────────┬──────────┘
                     ▼
             DECISION SYNTHESIS
                     │
                     ▼
            ADVERSARIAL REVIEW
                     │
                     ▼
            CERTIFICATION GATE
                     │
                     ▼
             DECISION COMMITTEE
                     │
                     ▼
          DETERMINISTIC SAFETY VETO
                     │
                     ▼
           CERTIFIED RECOMMENDATION
```

The canonical shell remains the lab FastAPI/mobile product. Intake resolves a
stable product identity before current offers or history are evaluated. Every
eligible provider observation is normalized, provenance-labelled, and written
to the first-party history port. User captures remain tenant-private until an
explicit corroboration policy promotes them.

The finance side is an external deterministic subsystem from this lane's
perspective. `FinancialDecisionProvider.evaluate()` returns a typed
`FinancialSafetyResult`; the product never calls `code/main.py` directly and
never rewrites `safe_amount_today`, projected balances, payment plans, or
finance status. `CommittedFinanceCheckpointAdapter` is an explicit seam that
fails closed until the finance lane supplies a callable adapter.

`PriceIntelligenceService` converts the existing pure Decimal engine into a
machine-readable record. `GovernedDecisionService` creates the evidence
envelope, asks a distinct reviewer to challenge it, certifies mandatory
operations, selects among valid candidates, and applies a final deterministic
veto. The current API exposes this via
`POST /v1/products/{product_id}/governed-evaluate`; its default mode is
fixture-backed and is not a claim of production provider activation.

Canonical product states are `BUY_NOW`, `HOLD_FOR_BETTER_PRICE`,
`SET_PRICE_WATCH`, `CONSIDER_USED_OR_REFURBISHED`, `FINANCIALLY_WAIT`,
`NOT_RECOMMENDED`, and `NEEDS_CONFIRMATION`. Finance is evaluated first for
eligibility: a price signal can choose timing only after financial safety and
protected balance rules pass. Sparse or unavailable history produces
`UNKNOWN`/`INSUFFICIENT`, never an invented trend.

Deterministic eligibility is:

| State | Eligibility |
|---|---|
| `BUY_NOW` | full finance evidence, safe-now balance, verified identity, and strong/buy price signal |
| `HOLD_FOR_BETTER_PRICE` | safe now, sufficient history, and material recurring savings are evidenced |
| `SET_PRICE_WATCH` | safe now but timing is uncertain, weak, or history is insufficient |
| `CONSIDER_USED_OR_REFURBISHED` | safe now and a distinct, trustworthy alternative condition is materially cheaper |
| `FINANCIALLY_WAIT` | safe capacity is later or requires a conservative plan; price cannot override |
| `NOT_RECOMMENDED` | no safe payment date or deterministic finance veto |
| `NEEDS_CONFIRMATION` | incomplete identity, finance coverage, or mandatory evidence |

The API default remains the imported compatibility surface. No second UI or
second runtime API is introduced. SQLite is available behind the same
observation port for the next deployment step.
