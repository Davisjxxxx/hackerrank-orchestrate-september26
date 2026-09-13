# Mobile vertical slice evidence

`apps/mobile/App.tsx` is an Expo + React Native + TypeScript home shell with four first-class actions:

- Scan barcode
- Take photo
- Paste/share link
- Search item

The current buttons are an API-contract demonstration shell: they call the matching FastAPI intake route using text/reference values and render exact/ambiguous identity state. They do not yet invoke native camera, barcode, image-picker, share-sheet, or OCR APIs. Those capabilities remain explicit `ADAPTER_SEAM` work and must not be presented as working end-user capture until device-bound adapters are wired and tested.

The Python acceptance evidence is in `tests/test_api.py` and `tests/test_independent_redteam.py`: barcode/URL/reference-photo intake, deterministic evaluation replay, financial veto/fail-closed behavior, watch creation, subject isolation, and deletion. The Expo dependency tree resolves, `npm run typecheck` passes, `npx expo config --json` validates the app config, and the high-severity audit gate is clean. A native device/store build was not run in this lab; camera permissions, barcode capture, share-sheet, image retention/deletion, and simulator checks remain deferred.
