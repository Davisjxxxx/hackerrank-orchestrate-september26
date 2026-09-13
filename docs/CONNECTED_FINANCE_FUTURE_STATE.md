# Connected finance future state

Connected accounts are future adapters, not tonight's blocker. Every source
must normalize into the same canonical finance model consumed by the protected
`FinancialDecisionProvider` boundary.

```text
FinancialSourceAdapter
├── CSVFinancialSourceAdapter
├── BankAccountAdapter
├── CreditCardAdapter
├── LoanAdapter
├── BrokerageAdapter
└── FutureConnectorAdapter
```

The CSV adapter is the current challenge-facing source. Bank, card, loan, and
brokerage adapters must be read-only, consent-scoped, tenant-isolated, and
explicit about pending, settled, cancelled, unrealized, and future states.
They must not expose credentials to product or model layers. A connector
failure produces incomplete evidence and a blocked/confirmation result; it
does not invent income or available cash.

Future work includes encrypted durable storage, token vaulting, consent and
revocation, provider webhooks, reconciliation, rate limits, audit trails,
transactional snapshots, and independently verified as-of timestamps. No
production account action, transfer, payment, or migration is performed by
this lane.
