# Round 2 remediation debug report

## Symptom

The second independent suite reproduced 12 failures against commit `29b754bd54c16f307b4ed56d938cbc630b3d9107`.

## Root cause

The deterministic engine used first-seen observation deduplication without currency or quality precedence, mixed-currency detection counted rows rather than distinct currencies, and the core did not enforce quarantine trust. ShopSavvy normalization used permissive availability handling and assumed nested provider mappings. Financial contradiction logic used ambient wall-clock time. Watch target and condition validation was incomplete at the API and domain boundaries.

## Fix

- Added currency-aware observation identity and deterministic quality selection.
- Added explicit mixed-currency ambiguity handling and engine-level quarantine filtering.
- Added explicit provider availability normalization, nested response validation, connector error translation, and bounded candidate preservation.
- Anchored financial contradiction checks to financial/evaluation evidence time and rejected future-dated payloads for SAFE_NOW composition.
- Added shared finite-money validation and API/domain watch condition validation.
- Corrected recurrence estimates to use intervals between distinct deal episodes and require two episodes for recurrence evidence.

## Evidence

- Round 2 independent regressions: 12 passed.
- Round 1 independent regressions: 19 passed.
- Full project suite: verified after remediation.
- Mobile, Expo, dependency, OpenAPI, secret-scan, and archive hygiene gates are rerun before packaging.

## Status

DONE — ready for a third independent red-team review after the local remediation commit and cache-free handoff archive are produced.
