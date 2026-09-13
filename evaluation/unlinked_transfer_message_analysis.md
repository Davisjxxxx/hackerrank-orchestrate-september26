# Unlinked transfer message analysis

- Message: `message_13`
- Scope: user `user_18`, request `request_18`, source `bank`
- Sent at: `2026-07-01T09:30:00Z`
- `related_event_id`: blank
- Explicit amount: none
- Explicit date: none
- User financial-event rows: 75
- User linked-event rows: 0

## Decision

The message is contextual evidence that two existing bank-history rows represent an internal transfer, but it does not identify either row and provides no amount or date. No unambiguous matching pair exists in the supplied rows. It therefore creates no cash-flow event and does not borrow an amount from another transaction. The existing structured rows remain governed by their own status, direction, settlement date, and lifecycle data.

This is the conservative rule required by the participant statement and contract: a message may amend a quantified supplied fact when the target is unambiguous; this message does neither.

## Message text

There’s an update from Summit Bank on your recent account activity. The matching debit and credit came from a transfer between your two accounts. Both accounts are registered under the same account holder. Both entries will remain visible in your transaction history. Txn ref BAN-0013.
