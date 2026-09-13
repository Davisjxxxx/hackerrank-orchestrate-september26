# ADR-001: deployable app boundary

Status: accepted for the 0.2.1 release candidate

## Decision

Use an Expo + React Native + TypeScript client over a FastAPI/Pydantic service boundary. Keep intake normalization, product identity resolution, connector normalization, Decimal price policy, financial composition, and watch policy in the Python package.

```text
Expo client -> FastAPI intake/evaluation API -> resolver -> canonical product
                                      -> provider adapters -> observations
                                      -> price engine -> financial result -> decision
                                      -> watch repository/scheduler/notification ports
```

The engine imports no React Native, Expo, FastAPI, database, camera, OCR, shopping-provider, or notification package.

## Consequences

- The client can later use `expo-camera`, `expo-image-picker`, and share/deep-link handling without moving decision logic into JavaScript.
- Provider keys remain server-side. The client receives normalized offers and evidence only.
- The lab uses an in-memory repository and recorded fixtures. PostgreSQL, object storage, a queue, authentication, and push delivery are explicit adapter work for integration.
- The photo route accepts a durable `image_ref` and bounded OCR evidence. A vision adapter can be added without allowing image text to execute instructions or alter the financial result.

## Integration choices

- Barcode/camera: `expo-camera` adapter in the client; API accepts the normalized barcode or photo reference.
- Upload: `expo-image-picker` produces a short-lived server reference. Default policy is delete-after-resolution unless a user saves a watch.
- Share sheet: `expo-linking`/platform share extension forwards a URL to `/v1/intake/url`.
- API: FastAPI exposes generated OpenAPI at `/openapi.json` and interactive docs at `/docs`.
- Persistence: `WatchRepository` and product/decision stores are ports. Production direction is PostgreSQL plus a scheduler/queue.
- Notifications: `NotificationGateway` is a port; notification targets are opaque references, never financial payloads.
- Authentication: integrate user authentication before multi-user production. Until then, the API test seam uses `X-User-Id`; it is not a production auth mechanism.
- Deployment: containerized FastAPI behind TLS with secrets injected as environment/secret-manager values; Expo EAS is the client release direction.

## Rejected alternatives

- Rewriting the decision core in TypeScript would duplicate Decimal policy and weaken parity with the financial engine.
- Calling providers directly from mobile would expose credentials and make provider outages part of the client contract.
- A database dependency in the engine would prevent deterministic replay and fixture-only CI.
