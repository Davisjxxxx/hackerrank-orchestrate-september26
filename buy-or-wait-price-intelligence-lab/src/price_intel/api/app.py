from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..demo import DEMO_NOW, DEMO_PRODUCT, demo_observations
from ..engine import PriceIntelligenceEngine
from ..auth import AuthenticationError, AuthenticatedSubject, Authenticator, FixtureAuthenticator
from ..financial import FinancialEvidenceUnavailable, FinancialSafetyProvider, FixtureFinancialSafetyProvider
from ..intake import ProductIntakeError, ProductIntakeMode, ProductIntakeRequest, normalize_intake
from ..models import (
    Condition,
    FinancialCoverageState,
    FinancialSafetyResult,
    FinancialState,
    ObservationTrust,
    PriceObservation,
    ProductIdentity,
    PurchaseIntent,
    Urgency,
    validate_non_negative_money,
)
from ..resolver import FixtureProductResolver, IdentityResolutionState, canonical_product_id
from ..watch import InMemoryWatchRepository, WatchService
from ..connectors.live import build_provider_adapters
from ..observation_store import InMemoryObservationStore
from ..price_intelligence import PriceIntelligenceService
from ..governance import GovernedDecisionService, MANDATORY_EVIDENCE


class IntakePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    barcode: str | None = None
    product_url: str | None = None
    query_text: str | None = None
    image_ref: str | None = None
    retailer_hint: str | None = None
    observed_price: Decimal | None = Field(default=None, ge=0)
    observed_shipping: Decimal = Field(default=Decimal("0"), ge=0)
    observed_at: datetime | None = None
    currency: str | None = None
    provenance: str | None = None
    ocr_evidence: dict[str, str] = Field(default_factory=dict)
    user_confirmed: bool = False
    metadata: dict[str, str] = Field(default_factory=dict)


class EvaluatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    urgency: Urgency = Urgency.FLEXIBLE
    max_wait_days: int = Field(default=60, ge=0, le=3650)
    accepted_conditions: list[Condition] = Field(default_factory=lambda: [Condition.NEW])
    minimum_savings_dollars: Decimal = Field(default=Decimal("25"), ge=0)
    minimum_savings_fraction: Decimal = Field(default=Decimal("0.08"), ge=0, le=1)
    financial_state: FinancialState | None = None
    safe_amount_today: Decimal | None = Field(default=None, ge=0)
    earliest_safe_full_payment_date: datetime | None = None
    minimum_balance: Decimal | None = Field(default=None, ge=0)
    recommended_payment_method: str | None = None
    payment_plan: dict[str, Any] = Field(default_factory=dict)
    financial_reason_codes: list[str] = Field(default_factory=list)
    financial_data_as_of: datetime | None = None
    financial_coverage_state: FinancialCoverageState = FinancialCoverageState.UNKNOWN
    as_of: datetime | None = None

    @field_validator("as_of", "earliest_safe_full_payment_date", "financial_data_as_of")
    @classmethod
    def timezone_required(cls, value: datetime | None) -> datetime | None:
        if value is not None and (value.tzinfo is None or value.utcoffset() is None):
            raise ValueError("timestamp must include a timezone")
        return value


class WatchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_price: Decimal = Field(ge=0)
    product_id: str | None = None
    max_wait_date: date
    accepted_conditions: list[Condition] = Field(default_factory=lambda: [Condition.NEW])
    retailer_restrictions: list[str] = Field(default_factory=list)
    source_restrictions: list[str] = Field(default_factory=list)
    original_decision: str = "set_price_watch"
    urgency: Urgency = Urgency.FLEXIBLE
    notification_target_ref: str | None = None

    @field_validator("target_price", mode="before")
    @classmethod
    def finite_target_price(cls, value: object) -> Decimal:
        return validate_non_negative_money(value, "target_price")

    @field_validator("accepted_conditions")
    @classmethod
    def valid_accepted_conditions(cls, value: list[Condition]) -> list[Condition]:
        if not value or any(condition == Condition.UNKNOWN for condition in value):
            raise ValueError("accepted_conditions must contain at least one purchasable condition")
        return value


class AppState:
    def __init__(self, *, authenticator: Authenticator | None = None, financial_provider: FinancialSafetyProvider | None = None):
        self.engine = PriceIntelligenceEngine()
        self.authenticator = authenticator or FixtureAuthenticator()
        self.financial_provider = financial_provider or FixtureFinancialSafetyProvider()
        self.products: dict[str, ProductIdentity] = {}
        self.observation_store = InMemoryObservationStore()
        self.decisions: dict[str, dict[str, Any]] = {}
        self.resolver = FixtureProductResolver((DEMO_PRODUCT,))
        self.watch_service = WatchService(InMemoryWatchRepository(), observation_store=self.observation_store)
        self.governance_service = GovernedDecisionService()
        self.governance_control_evidence = {key: True for key in MANDATORY_EVIDENCE}
        self.governance_control_evidence.update({"unsupported_income_used": False, "payment_plan_legal": True, "deadline_respected": True})
        product_id = canonical_product_id(DEMO_PRODUCT)
        self.products[product_id] = DEMO_PRODUCT
        self.observation_store.append(product_id, DEMO_PRODUCT, demo_observations(), ingested_at=DEMO_NOW)


def create_app(state: AppState | None = None) -> FastAPI:
    state = state or AppState()
    app = FastAPI(
        title="Buy or Wait? Purchase Decision API",
        version="0.2.1-rc1",
        description="Provider-independent product intake, price intelligence, financial veto, and decision-aware watches.",
    )
    app.state.domain = state

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "mode": "fixture-backed"}

    @app.get("/v1/connectors")
    def connector_status() -> list[dict[str, Any]]:
        return [_jsonable(adapter.status) for adapter in build_provider_adapters()]

    def _subject(*, authorization: str | None = None, x_user_id: str | None = None, required: bool = False) -> AuthenticatedSubject | None:
        headers: dict[str, str] = {}
        if authorization:
            headers["authorization"] = authorization
        if x_user_id:
            headers["x-user-id"] = x_user_id
        try:
            return state.authenticator.authenticate(headers, required=required)
        except AuthenticationError as exc:
            raise HTTPException(status_code=401, detail="authentication required") from exc

    def intake(mode: ProductIntakeMode, payload: IntakePayload, *, subject: AuthenticatedSubject | None) -> dict[str, Any]:
        try:
            normalized = normalize_intake(
                ProductIntakeRequest(
                    mode=mode,
                    barcode=payload.barcode,
                    product_url=payload.product_url,
                    query_text=payload.query_text,
                    image_ref=payload.image_ref,
                    retailer_hint=payload.retailer_hint,
                    observed_price=payload.observed_price,
                    observed_shipping=payload.observed_shipping,
                    observed_at=payload.observed_at,
                    currency=payload.currency,
                    provenance=payload.provenance,
                    ocr_evidence=payload.ocr_evidence,
                    user_confirmed=payload.user_confirmed,
                    metadata=payload.metadata,
                )
            )
        except ProductIntakeError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        resolution = state.resolver.resolve_product(normalized)
        response: dict[str, Any] = {
            "state": resolution.state.value,
            "reason_codes": list(resolution.reason_codes),
            "normalized_input": _jsonable(normalized),
            "candidates": [_jsonable(candidate) for candidate in resolution.candidates],
        }
        if resolution.state != IdentityResolutionState.EXACT or resolution.product is None:
            return response
        product_id = canonical_product_id(resolution.product)
        state.products[product_id] = resolution.product
        observations = list(state.observation_store.observations(product_id))
        if normalized.observed_price is not None:
            observations.append(
                PriceObservation(
                    provider="user_captured",
                    retailer=normalized.retailer_hint,
                    observed_at=normalized.observed_at or datetime.now(timezone.utc),
                    price=normalized.observed_price,
                    shipping=normalized.observed_shipping,
                    currency=normalized.currency or "USD",
                    captured=True,
                    provenance=normalized.provenance or "user_capture",
                    metadata=normalized.metadata,
                    trust=ObservationTrust.USER_PRIVATE,
                )
            )
            state.observation_store.append(
                product_id,
                resolution.product,
                observations[-1:],
                ingested_at=normalized.observed_at or datetime.now(timezone.utc),
                user_id=subject.subject_id if subject else None,
            )
        response.update({"product_id": product_id, "product": _jsonable(resolution.product)})
        return response

    @app.post("/v1/intake/barcode")
    def barcode(payload: IntakePayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        return intake(ProductIntakeMode.BARCODE, payload, subject=_subject(authorization=authorization, x_user_id=x_user_id))

    @app.post("/v1/intake/url")
    def url(payload: IntakePayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        return intake(ProductIntakeMode.PRODUCT_URL, payload, subject=_subject(authorization=authorization, x_user_id=x_user_id))

    @app.post("/v1/intake/photo")
    def photo(payload: IntakePayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        return intake(ProductIntakeMode.CAMERA_PHOTO, payload, subject=_subject(authorization=authorization, x_user_id=x_user_id))

    @app.post("/v1/intake/search")
    def search(payload: IntakePayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        return intake(ProductIntakeMode.TEXT_SEARCH, payload, subject=_subject(authorization=authorization, x_user_id=x_user_id))

    @app.post("/v1/products/{product_id}/evaluate")
    def evaluate(product_id: str, payload: EvaluatePayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        product = state.products.get(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="product not found")
        subject = _subject(authorization=authorization, x_user_id=x_user_id)
        as_of = payload.as_of or datetime.now(timezone.utc)
        intent = PurchaseIntent(
            product=product,
            urgency=payload.urgency,
            max_wait_days=payload.max_wait_days,
            accepted_conditions=frozenset(payload.accepted_conditions),
            minimum_savings_dollars=payload.minimum_savings_dollars,
            minimum_savings_fraction=payload.minimum_savings_fraction,
        )
        price_decision = state.engine.evaluate(intent, state.observation_store.observations(product_id, user_id=subject.subject_id if subject else None), now=as_of)
        try:
            financial = state.financial_provider.evaluate(subject_id=subject.subject_id if subject else "anonymous", product=product, request=payload)
        except FinancialEvidenceUnavailable as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        combined = state.engine.combine(financial, price_decision, as_of=as_of)
        owner_id = subject.subject_id if subject else "anonymous"
        decision_id = _decision_id(product_id, payload, as_of, owner_id)
        response = {
            "decision_id": decision_id,
            "product_id": product_id,
            "combined_decision": combined.decision.value,
            "financial_state": combined.financial_state.value,
            "reason_codes": list(combined.reason_codes) + list(price_decision.reason_codes),
            "price_decision": _jsonable(price_decision),
            "financial_result": _jsonable(financial),
            "evidence": {"canonical_product": _jsonable(product), **dict(price_decision.evidence)},
        }
        state.decisions[decision_id] = {"owner_id": owner_id, "response": response}
        return response

    @app.post("/v1/products/{product_id}/governed-evaluate")
    def governed_evaluate(product_id: str, payload: EvaluatePayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        """Return the product-level synthesis and all fail-closed governance stages.

        The default AppState is explicitly fixture-backed. Production callers
        must inject the authoritative financial provider and its evidence map;
        this endpoint never accepts client-supplied dollar arithmetic.
        """
        product = state.products.get(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="product not found")
        subject = _subject(authorization=authorization, x_user_id=x_user_id)
        as_of = payload.as_of or DEMO_NOW
        intent = PurchaseIntent(
            product=product, urgency=payload.urgency, max_wait_days=payload.max_wait_days,
            accepted_conditions=frozenset(payload.accepted_conditions),
            minimum_savings_dollars=payload.minimum_savings_dollars,
            minimum_savings_fraction=payload.minimum_savings_fraction,
        )
        price = PriceIntelligenceService(state.observation_store, state.engine).evaluate(
            product_id, product, intent, now=as_of, user_id=subject.subject_id if subject else None,
        )
        try:
            financial = state.financial_provider.evaluate(subject_id=subject.subject_id if subject else "anonymous", product=product, request=payload)
        except FinancialEvidenceUnavailable as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        controls = dict(state.governance_control_evidence)
        controls["safe_amount_covers_current_price"] = bool(
            financial.safe_amount_today is not None and price.current_best_price is not None
            and financial.safe_amount_today >= price.current_best_price
        )
        governed = state.governance_service.evaluate(
            request={"payload": _jsonable(payload), "as_of": as_of.isoformat(), "source": "fixture_api"},
            product=product, financial=financial, price=price, control_evidence=controls,
        )
        decision_id = governed.envelope.decision_id
        response = {"decision_id": decision_id, "product_id": product_id,
                    "recommendation": governed.envelope.candidate_recommendation.value,
                    "financial_state": financial.financial_state.value,
                    "price_intelligence": price.to_dict(), "governance": governed.to_dict(),
                    "mode": "fixture-backed"}
        state.decisions[decision_id] = {"owner_id": subject.subject_id if subject else "anonymous", "response": response}
        return response

    @app.get("/v1/products/{product_id}/prices")
    def prices(product_id: str, condition: Condition | None = Query(default=None), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> list[dict[str, Any]]:
        if product_id not in state.products:
            raise HTTPException(status_code=404, detail="product not found")
        subject = _subject(authorization=authorization, x_user_id=x_user_id)
        rows = state.observation_store.observations(product_id, user_id=subject.subject_id if subject else None)
        return [_jsonable(row) for row in rows if condition is None or row.condition == condition]

    @app.get("/v1/products/{product_id}/history")
    def history(product_id: str, condition: Condition | None = Query(default=None), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> list[dict[str, Any]]:
        return prices(product_id, condition, authorization, x_user_id)

    @app.post("/v1/watches")
    def create_watch(payload: WatchPayload, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        subject = _subject(authorization=authorization, x_user_id=x_user_id, required=True)
        product_id = payload.product_id or (payload.original_decision.split(":", 1)[-1] if payload.original_decision.startswith("product:") else None)
        if not product_id or product_id not in state.products:
            raise HTTPException(status_code=404, detail="product not found")
        product = state.products[product_id]
        try:
            watch = state.watch_service.create(
                user_id=subject.subject_id,
                product_id=product_id,
                product_title=product.title,
                target_price=payload.target_price,
                max_wait_date=payload.max_wait_date,
                accepted_conditions=frozenset(payload.accepted_conditions),
                retailer_restrictions=frozenset(payload.retailer_restrictions),
                source_restrictions=frozenset(payload.source_restrictions),
                original_decision=payload.original_decision,
                urgency=payload.urgency,
                notification_target_ref=payload.notification_target_ref,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        return _jsonable(watch)

    @app.get("/v1/watches")
    def list_watches(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> list[dict[str, Any]]:
        subject = _subject(authorization=authorization, x_user_id=x_user_id, required=True)
        return [_jsonable(watch) for watch in state.watch_service.repository.list(subject.subject_id)]

    @app.delete("/v1/watches/{watch_id}")
    def delete_watch(watch_id: str, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, bool]:
        subject = _subject(authorization=authorization, x_user_id=x_user_id, required=True)
        deleted = state.watch_service.repository.delete(subject.subject_id, watch_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="watch not found")
        return {"deleted": True}

    @app.get("/v1/decisions/{decision_id}")
    def get_decision(decision_id: str, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        subject = _subject(authorization=authorization, x_user_id=x_user_id, required=True)
        record = state.decisions.get(decision_id)
        if record is None or record["owner_id"] != subject.subject_id:
            raise HTTPException(status_code=404, detail="decision not found")
        return record["response"]

    return app


def _decision_id(product_id: str, payload: EvaluatePayload, as_of: datetime, owner_id: str = "anonymous") -> str:
    raw = json.dumps({"product_id": product_id, "payload": _jsonable(payload), "as_of": as_of.isoformat(), "owner_id": owner_id}, sort_keys=True)
    return "dec_" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _jsonable(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _jsonable(value.model_dump(mode="python"))
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, str):
        return value
    if hasattr(value, "value") and isinstance(value.value, str):
        return value.value
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(item) for item in value]
    return value
