# Buy or Wait? mobile vertical-slice shell

This Expo + React Native + TypeScript shell exposes the four first-class intake actions and sends them to the typed FastAPI boundary. Camera/barcode/image-picker permissions and share-sheet integration are intentionally adapter work: the home flow keeps the client independent from provider credentials and the deterministic decision engine.

Run from `apps/mobile/` after installing Node dependencies:

```bash
npm install
npm run start
```

Set `EXPO_PUBLIC_API_BASE` for a device/simulator that cannot reach `localhost`. Provider credentials remain server-side.
