# Cortex integration plan

`CortexGateReviewer` is a future implementation of the existing
`AdversarialReviewer` port. It is first-class governance infrastructure but
not a hard runtime dependency for tonight's local product integration.

## Contract

1. Product creates an immutable evidence envelope and request fingerprint.
2. Cortex receives the envelope plus referenced evidence, not mutable finance
   internals or credentials.
3. Cortex may challenge, verify evidence, generate counterexamples, abstain,
   and certify/promote through the governance interface.
4. Cortex may not change deterministic financial arithmetic, mutate the
   finance decision record, bypass certification, or bypass the final veto.
5. A missing, timed-out, malformed, or unauthenticated Cortex result is an
   abstention and blocks release when Cortex is configured as mandatory.

## Delivery sequence

- keep `LocalAdversarialReviewer` as deterministic CI baseline;
- add an authenticated client with request/response schema validation;
- bind each result to the exact decision ID, evidence hashes, and code version;
- run Cortex in a separate trust domain/process;
- compare local invariant results with Cortex findings;
- promote only after certification and final veto pass;
- retain red-team findings and reviewer disagreements for audit.

No Cortex credential or production endpoint is stored in this repository.
