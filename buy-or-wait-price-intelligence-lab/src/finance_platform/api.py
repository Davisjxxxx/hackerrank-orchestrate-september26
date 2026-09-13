from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from fastapi import Body, Depends, FastAPI, File, Header, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from .affordability import AffordabilityService
from .canonical import CanonicalStateService
from .db import DecisionRequest, DecisionResult, EvidenceMessage, FinancialEvent, FinancialProfile, SourceAccount, SourceConnection, User, engine, init_db, new_id
from .documents import DocumentService
from .ingestion import TransactionImportService
from .schemas import DecisionInput, ProfileInput
from .settings import settings
from .security import TokenCipher
from .connectors.gmail import GmailConnector
from .connectors.plaid import PlaidConnector


def _session():
    session = Session(bind=engine)
    try: yield session
    finally: session.close()


def _user(authorization: str | None, x_user_id: str | None) -> str:
    if authorization and authorization.lower().startswith("bearer user:"):
        value = authorization.split(":", 1)[1].strip()
    elif settings.environment == "development" and x_user_id:
        value = x_user_id.strip()
    else:
        raise HTTPException(status_code=401, detail="authenticated user required")
    if not value or len(value) > 80: raise HTTPException(status_code=401, detail="invalid user identity")
    return value


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(title="Buy or Wait Real-World Finance API", version="1.0.0")
    importer = TransactionImportService(); state = CanonicalStateService(); affordability = AffordabilityService(state); documents = DocumentService()

    @app.get("/health")
    def health() -> dict[str, str]: return {"status": "ok", "mode": settings.environment}

    @app.post("/v1/users")
    def create_user(user_id: str, session: Session = Depends(_session)) -> dict[str, str]:
        if session.get(User, user_id): raise HTTPException(409, "user already exists")
        session.add(User(id=user_id)); session.add(FinancialProfile(user_id=user_id)); session.commit()
        return {"user_id": user_id}

    @app.put("/v1/profile")
    def update_profile(payload: ProfileInput, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id); profile = session.get(FinancialProfile, user_id)
        if not profile: raise HTTPException(404, "user not found")
        for key, value in payload.model_dump().items(): setattr(profile, key, value)
        session.commit(); return payload.model_dump(mode="json")

    @app.post("/v1/imports/transactions/preview")
    async def preview_transactions(file: UploadFile = File(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        _user(authorization, x_user_id); content = await file.read()
        try: events = importer.preview(file.filename or "upload.csv", content)
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc
        return {"rows": len(events), "events": [event.model_dump(mode="json") for event in events]}

    @app.post("/v1/imports/transactions")
    async def import_transactions(file: UploadFile = File(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id); content = await file.read()
        try: events = importer.preview(file.filename or "upload.csv", content); return importer.commit(session, user_id=user_id, filename=file.filename or "upload.csv", content=content, events=events)
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc

    @app.post("/v1/documents")
    async def upload_document(file: UploadFile = File(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id)
        try: row = documents.store(session, user_id=user_id, filename=file.filename or "upload", content_type=file.content_type, content=await file.read())
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc
        return {"id": row.id, "filename": row.filename, "status": row.status, "confidence": row.extraction_confidence}

    @app.get("/v1/state")
    def get_state(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id)
        try: value = state.state(session, user_id, as_of=date.today())
        except ValueError as exc: raise HTTPException(404, str(exc)) from exc
        return {"user_id": user_id, "home_currency": value.home_currency, "available_cash": str(value.available_cash), "minimum_balance": str(value.minimum_balance), "pending_debits": [{"id": e.id, "amount": str(e.amount), "date": str(e.transaction_date)} for e in value.pending_debits], "pending_credits": [{"id": e.id, "amount": str(e.amount)} for e in value.pending_credits], "recurring_streams": [{"id": s.id, "direction": s.direction, "cadence": s.cadence_type, "amount": str(s.expected_amount), "confidence": s.confidence, "evidence": s.source_event_ids} for s in value.streams], "uncertain_facts": list(value.uncertain_facts)}

    @app.get("/v1/accounts")
    def accounts(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> list[dict[str, Any]]:
        user_id = _user(authorization, x_user_id)
        return [{"id": a.id, "name": a.name, "currency": a.currency, "available_balance": str(a.available_balance) if a.available_balance is not None else None, "current_balance": str(a.current_balance) if a.current_balance is not None else None} for a in session.scalars(select(SourceAccount).where(SourceAccount.user_id == user_id)).all()]

    @app.post("/v1/evidence/messages")
    def evidence_message(payload: dict[str, Any] = Body(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        import re
        user_id = _user(authorization, x_user_id); related = payload.get("related_event_id")
        if related and not session.scalar(select(FinancialEvent).where(FinancialEvent.id == related, FinancialEvent.user_id == user_id)): raise HTTPException(422, "related event is not owned by user")
        raw = str(payload.get("text", "")); sanitized = re.sub(r"<[^>]+>", " ", raw).strip()
        if not sanitized: raise HTTPException(422, "message text is required")
        received = payload.get("received_at")
        try: received_at = datetime.fromisoformat(str(received)) if received else datetime.now(timezone.utc)
        except ValueError as exc: raise HTTPException(422, "received_at must be ISO-8601") from exc
        if received_at.tzinfo is None: raise HTTPException(422, "received_at must include timezone")
        row = EvidenceMessage(user_id=user_id, provider_message_id=payload.get("provider_message_id"), sender=payload.get("sender"), received_at=received_at, subject=payload.get("subject"), sanitized_text=sanitized, thread_id=payload.get("thread_id"), related_event_id=related)
        session.add(row); session.commit(); return {"id": row.id, "stored_as": "untrusted_financial_evidence"}

    @app.post("/v1/decisions")
    def create_decision(payload: DecisionInput, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id); request_date = payload.request_date or date.today(); payload = payload.model_copy(update={"request_date": request_date})
        try:
            canonical = state.state(session, user_id, as_of=request_date); result = affordability.evaluate(canonical, payload)
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc
        req = DecisionRequest(user_id=user_id, amount=payload.amount, currency=payload.currency, description=payload.description, category=payload.category, request_date=request_date, desired_completion_date=payload.desired_completion_date, allows_partial_payment=payload.allows_partial_payment)
        session.add(req); session.flush(); row = DecisionResult(request_id=req.id, user_id=user_id, result=result.model_dump(mode="json")); session.add(row); session.commit()
        return {"decision_id": row.id, **result.model_dump(mode="json"), "evidence": {"pending_debits": len(canonical.pending_debits), "pending_credits_excluded": len(canonical.pending_credits), "recurring_streams": len(canonical.streams)}}

    @app.get("/v1/decisions/{decision_id}")
    def get_decision(decision_id: str, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id); row = session.scalar(select(DecisionResult).where(DecisionResult.id == decision_id, DecisionResult.user_id == user_id))
        if not row: raise HTTPException(404, "decision not found")
        return {"decision_id": row.id, **row.result}

    @app.get("/v1/connectors")
    def connectors() -> list[dict[str, str]]: return [{"provider": "plaid", "status": "sandbox-ready" if settings.plaid_client_id else "credentials-required"}, {"provider": "gmail", "status": "oauth-ready" if settings.gmail_client_id else "credentials-required"}, {"provider": "file_import", "status": "ready"}, {"provider": "documents", "status": "ready"}, {"provider": "fx", "status": "stored-rates-ready"}]

    @app.post("/v1/connectors/plaid/link/token/create")
    async def plaid_link_token(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        _user(authorization, x_user_id)
        try: return await PlaidConnector().connect()
        except RuntimeError as exc: raise HTTPException(503, str(exc)) from exc

    @app.post("/v1/connectors/plaid/public/token/exchange")
    async def plaid_exchange(payload: dict[str, str] = Body(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id)
        token = payload.get("public_token")
        if not token: raise HTTPException(422, "public_token is required")
        try:
            result = await PlaidConnector().exchange_public_token(token)
            if not settings.token_encryption_key: raise HTTPException(503, "FINANCE_TOKEN_ENCRYPTION_KEY is required before storing Plaid access tokens")
            with Session(bind=engine) as session:
                row = SourceConnection(user_id=user_id, provider="plaid", status="connected", external_item_id=result.get("item_id"), encrypted_access_token=TokenCipher(settings.token_encryption_key).encrypt(str(result["access_token"])), provider_metadata={"environment": settings.plaid_env})
                session.add(row); session.commit(); return {"connection_id": row.id, "item_id": row.external_item_id}
        except RuntimeError as exc: raise HTTPException(503, str(exc)) from exc

    @app.post("/v1/connections/{connection_id}/refresh")
    async def refresh_connection(connection_id: str, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, Any]:
        user_id = _user(authorization, x_user_id); row = session.scalar(select(SourceConnection).where(SourceConnection.id == connection_id, SourceConnection.user_id == user_id))
        if not row: raise HTTPException(404, "connection not found")
        if row.provider != "plaid" or not row.encrypted_access_token or not settings.token_encryption_key: raise HTTPException(503, "connection refresh is not configured")
        result = await PlaidConnector().refresh(access_token=TokenCipher(settings.token_encryption_key).decrypt(row.encrypted_access_token), cursor=None)
        row.last_successful_sync = datetime.now(timezone.utc); session.commit()
        return {"provider": result.provider, "fetched": result.fetched, "inserted": result.inserted, "updated": result.updated, "duplicates": result.duplicates, "cursor": result.cursor}

    @app.delete("/v1/connections/{connection_id}")
    def disconnect_connection(connection_id: str, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, bool]:
        user_id = _user(authorization, x_user_id); row = session.scalar(select(SourceConnection).where(SourceConnection.id == connection_id, SourceConnection.user_id == user_id))
        if not row: raise HTTPException(404, "connection not found")
        row.status = "revoked"; row.encrypted_access_token = None; session.commit(); return {"disconnected": True}

    @app.post("/v1/connectors/gmail/connect")
    async def gmail_connect(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        _user(authorization, x_user_id)
        try: return await GmailConnector().connect()
        except RuntimeError as exc: raise HTTPException(503, str(exc)) from exc

    @app.post("/v1/connectors/gmail/sync")
    async def gmail_sync(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, Any]:
        _user(authorization, x_user_id)
        try: return (await GmailConnector().sync()).__dict__
        except RuntimeError as exc: raise HTTPException(503, str(exc)) from exc

    @app.delete("/v1/connectors/gmail/disconnect")
    async def gmail_disconnect(authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None)) -> dict[str, bool]:
        _user(authorization, x_user_id); await GmailConnector().disconnect(); return {"disconnected": True}

    @app.post("/v1/review/events/{event_id}")
    def review_event(event_id: str, payload: dict[str, Any] = Body(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, str]:
        user_id = _user(authorization, x_user_id); event = session.scalar(select(FinancialEvent).where(FinancialEvent.id == event_id, FinancialEvent.user_id == user_id))
        if not event: raise HTTPException(404, "event not found")
        if payload.get("category") is not None: event.category = str(payload["category"])
        if payload.get("flexibility") in {"essential", "flexible", "unknown"}: event.flexibility = payload["flexibility"]
        if payload.get("recurrence") == "one_time": event.recurrence_eligible = False
        if payload.get("recurrence") == "recurring": event.recurrence_eligible = True
        session.commit(); return {"event_id": event.id, "status": "review_applied"}

    @app.post("/v1/review/events/{event_id}/transfer")
    def review_transfer(event_id: str, payload: dict[str, str] = Body(...), authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, str]:
        user_id = _user(authorization, x_user_id); counterpart = payload.get("counterpart_event_id"); evidence = payload.get("evidence_id", "user_review")
        if not counterpart: raise HTTPException(422, "counterpart_event_id is required")
        try: CanonicalStateService().mark_internal_transfer(session, user_id, event_id, counterpart, evidence_id=evidence)
        except ValueError as exc: raise HTTPException(422, str(exc)) from exc
        return {"status": "internal_transfer_marked", "debit_event_id": event_id, "credit_event_id": counterpart}

    @app.post("/v1/review/streams/{stream_id}/end")
    def end_stream(stream_id: str, authorization: str | None = Header(default=None), x_user_id: str | None = Header(default=None), session: Session = Depends(_session)) -> dict[str, str]:
        from .db import RecurringStream
        user_id = _user(authorization, x_user_id); stream = session.scalar(select(RecurringStream).where(RecurringStream.id == stream_id, RecurringStream.user_id == user_id))
        if not stream: raise HTTPException(404, "stream not found")
        stream.status = "ended"; session.commit(); return {"stream_id": stream.id, "status": stream.status}

    return app
