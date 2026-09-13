# Dependency and license review

Review scope: release candidate 0.2.1, 2026-09-12.

## Python runtime

`pyproject.toml` declares FastAPI and Uvicorn runtime dependencies, with Pytest and HTTPX in the development extra. The isolated `.venv` install reports `pip check` clean and the full suite passes. The global workstation environment has unrelated package conflicts and is not used as release evidence.

FastAPI and Pydantic are MIT-licensed projects; Uvicorn is BSD-3-Clause; Pytest is MIT; HTTPX is BSD-3-Clause. Verify the exact transitive license set from the lock/export produced by the deployment build before distributing a binary/container.

## Mobile runtime

`apps/mobile/package.json` declares Expo SDK 57, React Native 0.86.3, React, Expo camera/image/linking packages, and TypeScript. The lockfile resolves cleanly, `npm ls` reports a valid tree, `npm run typecheck` passes, and `npm audit --omit=dev --audit-level=high` reports 0 vulnerabilities. The `uuid` override removes a transitive advisory in Expo's config tooling; verify it again when the Expo SDK changes. A native device/store build has not been run in this lab.

## Reuse and attribution

No third-party source code was copied into this lab. `shopsavvy/shopsavvy-mcp-server` was used only as an architectural reference and is documented as MIT-licensed; `aymanggv/barcode-price-comparison-app` and other projects were reviewed only for flow ideas. No provider SDK is bundled and no scraping implementation was added.

## Release condition

The current lab has no committed credentials and the tracked-file secret scan is clean. A future release must attach a dependency lockfile/SBOM, license report, vulnerability scan, and mobile lockfile before production publication.
