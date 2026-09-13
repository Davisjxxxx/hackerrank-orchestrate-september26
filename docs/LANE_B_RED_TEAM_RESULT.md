# Lane B internal red-team result

## Target

- Checkpoint: `c3a6782ac05257af816406fb18f6087ccfe0b5e4`
- Scope: governance, finance seam, price truthfulness, API release behavior,
  demo credibility, and root test contamination.
- Out of scope: connected accounts, production auth/cloud, live Cortex,
  advanced forecasting, and new provider implementation.

## Findings and disposition

1. Root pytest collected both imported workspaces and failed with 28 collection
   errors. Fixed with root `conftest.py` collection ignores; root finance tests
   remain discoverable.
2. Final veto trusted a committee object's status and selected-candidate
   eligibility. Fixed by requiring `APPROVED` and membership in eligible
   candidates.
3. Missing certification/reviewer objects could raise instead of returning a
   blocked result. Fixed with explicit fail-closed handling.
4. Reviewers received mutable control/payment mappings. Fixed with immutable
   evidence snapshots, preventing control or payment-plan mutation before
   certification.
5. Governance output lacked an execution trace and unresolved attack markers
   were discarded. Fixed with `governance_trace` and explicit escalation of
   normalized attack markers.
6. A missing current price could release a watch fallback. Fixed by blocking
   governed release when current price evidence is absent.

No critical/high attack remains unresolved within Lane B scope. The local
reviewer honestly remains a normalized-evidence challenger; it does not claim
to independently reconstruct raw Lane A events.

The final focused governance/API hardening run collected **44 cases** and
passed **44/44**. The full canonical lab suite passed **125/125**, the retained
red-team workspace passed **49/49**, and root finance/evaluation collection
passed **9/9** after the contamination guard.
