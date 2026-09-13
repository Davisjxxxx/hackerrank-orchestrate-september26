# Recurrence identity inventory

Observed rows: 25342. No merchant, payee, account, provider, source-record, recurrence-marker, or explicit stream-ID column is supplied.

| Field | Meaning | Stability | Can distinguish obligations? | Classification |
|---|---|---|---|---|
| event_id | unique opaque row identifier | unique per observation | No; it distinguishes rows, not a recurring entity | structural row key, not stream identity |
| user_id | user partition | stable for a user's records | No by itself; all obligations for one user share it | structural partition |
| event_type | income/expense/subscription/debt/etc. | stable within an obligation class | Sometimes; separate types should not merge | structural |
| description | human-readable payee/obligation label | often rotates for groceries, transport, dining | Sometimes; useful merchant/obligation evidence but not a source ID | mostly descriptive |
| category | broad financial category | stable across many recurring observations | No; several obligations and rotating streams share it | structural semantic feature, insufficient alone |
| direction | debit/credit/non_cash | stable for a cash-flow stream | Yes; opposite directions must remain separate | structural |
| amount | observed monetary value | fixed for contractual bills; variable for ordinary spending | Supporting evidence only; never sole identity | measurement |
| currency | source currency | usually stable per user/obligation | Occasionally; helps prevent invalid cross-currency merges | structural/supporting |
| event_date | observed occurrence date | supports cadence and phase | Yes, through temporal sequence; not an identity by itself | structural temporal evidence |
| settlement_date | cash-effective date | may differ for pending/scheduled rows | No; controls cash timing and lifecycle precedence | lifecycle/cash timing |
| status | settled/pending/scheduled/failed/cancelled/unrealized | changes over a lifecycle | Yes for lifecycle collapse, not recurring identity | lifecycle |
| linked_event_id | optional lifecycle link | sparse; populated on linked rows only | Yes when present; no transfer link exists for the unlinked message case | structural lifecycle |
| flexibility | fixed/reducible/stoppable/etc. | stable for a stream in observed data | Yes as a guard against merging semantically different change policies | structural policy feature |
| minimum_allowed_amount | floor for reducible events | blank for most rows; stable where supplied | Supporting evidence for a change plan, not stream identity | policy metadata |

## Negative controls

The data contains concrete anti-overmerge cases:

- `user_01` has `event_84` (settled `Local taxi`, 2024-03-02, ZAR 339.29) and `event_102` (pending `Pending fuel authorization`, same occurrence date, settlement 2024-03-05, ZAR 567.60) in `transport`. Same category and date do not prove one stream; lifecycle/status and settlement remain separate.
- `user_10` has weekly `salary` credits whose descriptions rotate among `Delivery platform payout`, `Weekly app earnings`, `Task marketplace payout`, and `Driver platform payout`. Category-only recurrence would merge income streams without a supplied source identifier; the repeated weekly cadence is evidence of a family, not permission to invent a single employer/source.
- `user_23` contains a regular `Clinic payment` healthcare series and a separate pending `Pending pharmacy card charge` healthcare record. Same category does not make the pending charge a continuation of the clinic stream.
- `user_77` has `event_7185` (`Purchase awaiting refund`, debit) linked to `event_7186` (`Pending merchant refund`, credit). The lifecycle link and opposite directions dominate any category or amount similarity; these rows must not be treated as a recurring debit stream.
- `user_01` groceries include similarly sized but differently described observations such as `Neighbourhood grocer` (ZAR 925.62) and `Bulk pantry shop` (ZAR 915.12). Amount similarity supports a candidate cluster but cannot be its sole identity.

## Consequence

The strongest available identity is a tuple of user, direction, event type, category, flexibility, controlled description evidence, and a causal date sequence. `linked_event_id` is authoritative for lifecycle relationships when present, but it cannot repair the unlinked transfer message because that message supplies no corresponding event identifier or amount.
