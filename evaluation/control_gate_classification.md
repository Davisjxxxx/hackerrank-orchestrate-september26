# Authority-first G1-G51 control classification

This matrix reclassifies the existing tests without weakening their
assertions.  A test is blocking only when its authority and applicability are
present.  `INVALID_OLD_POLICY` means the assertion encodes a universal
participant-derived semantic that must not control scored arithmetic; it is
retained as a regression diagnostic until replaced by an evidence-gated rule.

| Class | Tests | Authority/applicability reason |
|---|---|---|
| HARD_GATE | G1-G5, G7-G11, G15-G19, G21-G26, G30-G38, G39, G41-G50 | Untrusted-evidence safety, cash-state exclusion, actual lifecycle/conflict handling, deterministic Decimal/FX/date arithmetic, supplied payment-option constraints, profile permissions, and output-plan invariants. The relevant evidence is supplied by the organizer-facing schema or the applicable record. |
| CONDITIONAL_CONTROL | G6, G12-G14, G20, G29 | These controls require OCR grounding, exact duplicate/lifecycle evidence, an actual conflict, or an applicable flexibility/recurrence fact. Missing evidence is `NOT_APPLICABLE` or `UNRESOLVED`, not failure. |
| ADVISORY_DIAGNOSTIC | G40 | Explanations must remain deterministic, grounded, and consistent, but byte-level wording is not a financial-arithmetic authority. |
| INVALID_OLD_POLICY | G27-G28, G51 | Universal `max(last_3)`/few-occurrence recurrence and byte-exact sample prose are participant-derived policies, not organizer-authorized universal facts. Keep as diagnostics; do not use them to invent cash flows or block the authority-first core. |

## Internal control states

Every resolver control uses exactly `PASS`, `FAIL`, `NOT_APPLICABLE`, or
`UNRESOLVED`.  `FAIL` is emitted only for applicable evidence that violates a
rule.  The parallel resolver exposes `evidence_records` for ledger facts and
`control_results` for the current request; projected facts are labelled
`CONDITIONAL_INFERENCE` and cite their source event.

## Preserved assurance

Provenance, immutable source rows, deterministic replay, reason codes,
unsupported-evidence detection, unknown-state handling, evidence hashes,
adversarial fixtures, the Lane B seam, and the Cortex seam remain outside the
cash arithmetic unless their evidence-gated control is applicable.
