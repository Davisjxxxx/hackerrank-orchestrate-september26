# Conflict-chain inventory

Generated from participant-visible `dataset/` only. No dataset file was modified.

## Structural counts

- Financial events: 25342
- Populated `linked_event_id`: 58
- Missing link targets: 0
- Maximum link-chain length: 1
- Link cycles: 0
- Exact duplicate groups excluding `event_id`: 0
- Messages with `related_event_id`: 39; missing targets: 0
- Image links: 16; missing targets: 0

## Link status transitions

| Child status | Linked record status | Count |
|---|---|---:|
| `pending` | `settled` | 14 |
| `scheduled` | `failed` | 7 |
| `settled` | `cancelled` | 8 |
| `settled` | `settled` | 19 |
| `unrealized` | `settled` | 10 |

## Link event-type transitions

| Child type | Linked type | Count |
|---|---|---:|
| `debt_payment` | `debt_payment` | 7 |
| `expense` | `expense` | 14 |
| `investment_sale` | `investment_purchase` | 5 |
| `investment_valuation` | `investment_purchase` | 10 |
| `refund` | `expense` | 22 |

## Contract precedence mapping

| Precedence | Dataset discriminator | Deterministic treatment |
|---|---|---|
| cancellation / settlement / amendment | `status`, `settlement_date`, explicit message text, `related_event_id` | Exclude failed/cancelled/unrealized/non-cash; retain settled/scheduled cash; apply grounded pre-request payroll amendments. |
| newer same-source record | no source/provider/account ID exists; message `source_type` is not a transaction source key | Not implementable as a universal source comparison. No supplied field proves same source for unlinked rows. |
| settled over estimate/forecast | `status` and projected-vs-explicit representation | Settled rows are retained as history; scheduled rows are future obligations; projected rows are only generated from history. |
| financially safer unresolved interpretation | only if records actually conflict | Not used as a blanket default. Missing identity is not treated as a conflict. |

## Findings

- The links are not generic duplicate links: refunds, investment valuation, investment sales, and debt-payment retries have different event types. Collapsing every link would delete legitimate cash facts.
- `settled -> cancelled` and `scheduled -> failed` chains are observable. The current status filter excludes the invalid terminal record while preserving a valid successor/retry where present.
- There are no exact duplicate groups in the raw event table. The current canonical exact-duplicate guard is therefore inactive on this dataset.
- Message linkage is complete for populated `related_event_id`; messages tied to pending/unrealized/failed records remain evidence, not cash by themselves.
- The unavailable discriminator is specifically same-source identity for unlinked competing records. The dataset provides no source/account/merchant/recurrence ID, so selecting among multiple compatible recurrence partitions would require a participant assumption.
