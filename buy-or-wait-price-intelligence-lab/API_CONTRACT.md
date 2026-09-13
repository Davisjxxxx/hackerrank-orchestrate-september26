# API contract 0.2.1

The service is created by `price_intel.api.create_app()`. FastAPI generates the machine-readable contract at `GET /openapi.json` and Swagger UI at `GET /docs`.

Money is serialized as decimal strings. Provider credentials, raw secrets, and private financial credentials are never response fields.

## Intake

`POST /v1/intake/barcode`

```json
{"barcode":"036000291452","observed_price":"899.99","observed_shipping":"0","currency":"USD","retailer_hint":"Store A"}
```

`POST /v1/intake/url` accepts `product_url`; `POST /v1/intake/photo` accepts `image_ref` plus optional bounded `ocr_evidence`; `POST /v1/intake/search` accepts `query_text`.

All intake responses include `state`, `reason_codes`, `normalized_input`, and ranked candidates. Exact matches also include `product_id` and `product`. Ambiguous or unresolved inputs do not get silently promoted to a product.

## Evaluation and evidence

`POST /v1/products/{product_id}/evaluate` accepts urgency, wait window, accepted conditions, Decimal savings thresholds, and an explicit lab fixture request routed through the server-side `FinancialSafetyProvider` seam. An omitted financial state returns `422`; unknown/stale/contradictory or future-dated SAFE_NOW evidence cannot produce a buying decision. Financial contradiction checks use `financial_data_as_of`, then the explicit evaluation `as_of`, never ambient wall-clock time. The production financial engine must replace the fixture provider before deployment. The response includes an opaque deterministic `decision_id`, `combined_decision`, `financial_state`, price decision, reason codes, and structured evidence.

`GET /v1/products/{product_id}/prices` and `/history` return normalized observations. `condition` can filter the response.

## Watches and decisions

- `POST /v1/watches` creates a decision-aware watch with `product_id`, target price, maximum wait date, accepted conditions, source/retailer restrictions, original decision, urgency, and opaque notification target reference.
- Watch targets must be finite, non-negative Decimal values. `accepted_conditions` must contain at least one supported purchasable condition; empty, unknown, NaN, and infinite values return `422` at the API boundary and are revalidated by the domain service.
- `GET /v1/watches` is scoped by an authenticated subject. The canonical fixture credential is `Authorization: Bearer fixture:<subject>`; `X-User-Id` is retained only for supplied legacy tests.
- `DELETE /v1/watches/{watch_id}` only deletes a watch owned by the requesting user.
- `GET /v1/decisions/{decision_id}` requires an authenticated subject that owns the decision; cross-subject and unauthenticated reads return `404`/`401`.

## Error behavior

- Invalid barcode, URL, currency, or photo reference: `422`.
- Unknown product, decision, or user-owned watch: `404`.
- Ambiguous identity: `200` with `state=needs_confirmation`, not a guessed product.
- Provider outage/rate limit is isolated in connector exceptions; fixture-backed API operation remains available.
- Captured offers are private observations. They are not shared history and are only included when evaluating for the authenticated subject that captured them.
