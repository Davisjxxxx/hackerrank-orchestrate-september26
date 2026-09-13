# Parallel authority-first finance core

The implementation is in `code/authority_core/` and is evaluation-only in
this checkpoint.  The current `code/main.py` remains the R0 benchmark.

```text
RAW DATA
    -> schema/evidence validation
    -> control applicability
    -> authoritative fact resolution
    -> evidence-gated recurrence
    -> 90-day ledger
    -> safe-to-pay
    -> supplied-plan enumeration
    -> deterministic validation
```

The resolver excludes failed, cancelled, unrealized, and non-cash records;
does not count pending credits; keeps applicable debit obligations; removes
only exact duplicate representations; retains actual linked rows unless the
records themselves establish a lifecycle replacement; converts using the
settlement-date fixed rate; and preserves explicit future rows.

Recurrence is bounded to three candidates:

* R1: strong individual tracks, with monthly phase or repeated fixed-gap
  evidence; description is not authoritative identity.
* R2: aggregate compatible dimensions by supported period, using a bounded
  recent-period estimator.
* R3: R1 plus aggregate fallback only where no strong individual track is
  established.

Inferred events carry `CONDITIONAL_INFERENCE` authority, source event IDs,
inference provenance, and applicability state.  An unsupported stream is
diagnosed as unresolved and does not create a ledger event.  A terminal
employer message disables only salary continuation; it does not erase
unrelated supported expense recurrence.  A future salary continues only when
an explicit confirmed/scheduled salary is monthly-phase-compatible with a
historical salary; the continuation is bounded to the 90-day window and is
suppressed on the explicit settlement date.

No production wiring was changed because no candidate passed the promotion
criteria in this run.
