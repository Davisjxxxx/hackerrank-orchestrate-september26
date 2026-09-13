# Governance independence model

## Separate responsibilities

Decision synthesis proposes candidates from two independent records. The
adversarial reviewer attempts to falsify the evidence envelope. The
certification gate checks that mandatory operations occurred and have evidence.
The committee ranks only candidates that already satisfy deterministic finance
eligibility. The final veto is pure deterministic release logic.

Calling the same model twice would not establish independence. The local
reviewer instead has a different objective and schema, reads the envelope as a
trust-partitioned artifact, and runs invariant and counterexample checks for
duplicate income, unsupported income, liabilities, pending credits/debits,
recurrence, identity/variant mismatch, seller/condition disagreement, sparse
history, outliers, source inconsistency, and prompt injection. Evidence order
and candidate selection are not used to modify financial arithmetic.

## Diversity controls

- separate synthesis, challenge, certification, and committee interfaces;
- typed immutable `FinancialSafetyResult` and immutable evidence envelope;
- explicit control-evidence map with fail-closed missing keys;
- deterministic counterexample modules and arithmetic invariants;
- evidence hashes and observation references for replay;
- candidate-only committee decisions, never dollar-amount voting;
- future `CortexGateReviewer` and alternate-model/provider adapter seams;
- untrusted request text is retained as untrusted evidence and scanned for
  injection; it is never merged into trusted state.

## Correlated-failure risks

The local reviewer and synthesizer still share the same Python process and
domain models. A common model/schema defect, a poisoned upstream provider, or a
wrong product identity can therefore evade both. A future release should use a
separate process/provider, independently generated invariants, replayed
evidence with reordered inputs, and authenticated finance-result signatures.
The certification gate is intentionally not a second opinion on the
recommendation; it verifies operations and evidence, so it provides different
rather than redundant coverage.

## Fail-closed contract

Missing evidence yields `CERTIFICATION_FAILED`; critical challenges yield
`ABSTAIN`/blocked release; committee status cannot turn an unsafe finance state
into a buy candidate; and the final veto is not overridable by a model,
reviewer, or committee.
