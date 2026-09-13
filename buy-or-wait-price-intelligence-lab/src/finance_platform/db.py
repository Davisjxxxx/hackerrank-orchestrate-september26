from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any
import uuid

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text, UniqueConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

from .settings import settings


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(80), primary_key=True)
    email: Mapped[str | None] = mapped_column(String(320))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    profile: Mapped["FinancialProfile | None"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")


class FinancialProfile(Base):
    __tablename__ = "financial_profiles"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    home_currency: Mapped[str] = mapped_column(String(3), default="USD")
    current_available_cash: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    minimum_balance_to_keep: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    emergency_buffer: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    income_confidence_preference: Mapped[str] = mapped_column(String(20), default="conservative")
    protected_categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    flexible_categories: Mapped[list[str]] = mapped_column(JSON, default=list)
    payment_methods: Mapped[list[str]] = mapped_column(JSON, default=lambda: ["full_payment", "wait"])
    max_installment_months: Mapped[int | None] = mapped_column(Integer)
    forecast_horizon_days: Mapped[int] = mapped_column(Integer, default=90)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    user: Mapped[User] = relationship(back_populates="profile")


class SourceConnection(Base):
    __tablename__ = "source_connections"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("conn"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(30), default="connected")
    external_item_id: Mapped[str | None] = mapped_column(String(200))
    encrypted_access_token: Mapped[str | None] = mapped_column(Text)
    provider_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    last_successful_sync: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class SourceAccount(Base):
    __tablename__ = "source_accounts"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("acct"))
    connection_id: Mapped[str] = mapped_column(ForeignKey("source_connections.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    external_id: Mapped[str] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(200), default="Account")
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    available_balance: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    current_balance: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    __table_args__ = (UniqueConstraint("connection_id", "external_id", name="uq_source_account_external"),)


class ConnectorSyncRun(Base):
    __tablename__ = "connector_sync_runs"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("sync"))
    connection_id: Mapped[str] = mapped_column(ForeignKey("source_connections.id", ondelete="CASCADE"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(30), default="running")
    fetched: Mapped[int] = mapped_column(Integer, default=0)
    inserted: Mapped[int] = mapped_column(Integer, default=0)
    updated: Mapped[int] = mapped_column(Integer, default=0)
    duplicates: Mapped[int] = mapped_column(Integer, default=0)
    review_required: Mapped[int] = mapped_column(Integer, default=0)
    cursor: Mapped[str | None] = mapped_column(Text)
    error_summary: Mapped[str | None] = mapped_column(Text)


class ConnectorCursor(Base):
    __tablename__ = "connector_cursors"
    connection_id: Mapped[str] = mapped_column(ForeignKey("source_connections.id", ondelete="CASCADE"), primary_key=True)
    cursor: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class RawIngestionRecord(Base):
    __tablename__ = "raw_ingestion_records"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("raw"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    provider: Mapped[str] = mapped_column(String(40))
    connection_id: Mapped[str | None] = mapped_column(String(80), index=True)
    external_id: Mapped[str] = mapped_column(String(250))
    payload_hash: Mapped[str] = mapped_column(String(64), index=True)
    provider_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    schema_version: Mapped[str] = mapped_column(String(30), default="1")
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("provider", "connection_id", "external_id", "payload_hash", name="uq_raw_payload"),)


class FinancialEvent(Base):
    __tablename__ = "financial_events"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("evt"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    account_id: Mapped[str | None] = mapped_column(String(80), index=True)
    source: Mapped[str] = mapped_column(String(40))
    external_id: Mapped[str | None] = mapped_column(String(250), index=True)
    event_type: Mapped[str] = mapped_column(String(40), default="other")
    direction: Mapped[str] = mapped_column(String(10))
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    currency: Mapped[str] = mapped_column(String(3))
    transaction_date: Mapped[date] = mapped_column(Date)
    authorized_date: Mapped[date | None] = mapped_column(Date)
    settlement_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="settled")
    merchant: Mapped[str | None] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str | None] = mapped_column(String(120))
    pending_transaction_id: Mapped[str | None] = mapped_column(String(250))
    linked_event_id: Mapped[str | None] = mapped_column(String(80))
    confidence: Mapped[str] = mapped_column(String(20), default="high")
    recurrence_eligible: Mapped[bool] = mapped_column(Boolean, default=True)
    flexibility: Mapped[str] = mapped_column(String(20), default="unknown")
    minimum_allowed_amount: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    provider_metadata: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EvidenceMessage(Base):
    __tablename__ = "evidence_messages"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("msg"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    provider_message_id: Mapped[str | None] = mapped_column(String(250))
    sender: Mapped[str | None] = mapped_column(String(320))
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    subject: Mapped[str | None] = mapped_column(String(500))
    sanitized_text: Mapped[str] = mapped_column(Text)
    thread_id: Mapped[str | None] = mapped_column(String(250))
    related_event_id: Mapped[str | None] = mapped_column(String(80))
    factual_classification: Mapped[str | None] = mapped_column(String(80))
    confidence: Mapped[str] = mapped_column(String(20), default="low")


class EvidenceDocument(Base):
    __tablename__ = "evidence_documents"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("doc"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(120))
    sha256: Mapped[str] = mapped_column(String(64))
    storage_ref: Mapped[str] = mapped_column(Text)
    extracted_text: Mapped[str | None] = mapped_column(Text)
    extraction_confidence: Mapped[str] = mapped_column(String(20), default="low")
    status: Mapped[str] = mapped_column(String(30), default="needs_review")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EvidenceImage(Base):
    __tablename__ = "evidence_images"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("img"))
    document_id: Mapped[str] = mapped_column(ForeignKey("evidence_documents.id", ondelete="CASCADE"))
    page_or_region: Mapped[str | None] = mapped_column(String(120))
    ocr_text: Mapped[str | None] = mapped_column(Text)
    ocr_confidence: Mapped[str] = mapped_column(String(20), default="low")


class EvidenceFact(Base):
    __tablename__ = "evidence_facts"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("fact"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    fact_type: Mapped[str] = mapped_column(String(80))
    fact_value: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    confidence: Mapped[str] = mapped_column(String(20), default="low")
    source_kind: Mapped[str] = mapped_column(String(40))
    source_id: Mapped[str] = mapped_column(String(80))


class EventEvidenceLink(Base):
    __tablename__ = "event_evidence_links"
    event_id: Mapped[str] = mapped_column(ForeignKey("financial_events.id", ondelete="CASCADE"), primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    evidence_kind: Mapped[str] = mapped_column(String(40))


class RecurringStream(Base):
    __tablename__ = "recurring_streams"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("stream"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    direction: Mapped[str] = mapped_column(String(10))
    event_type: Mapped[str] = mapped_column(String(40))
    category: Mapped[str | None] = mapped_column(String(120))
    identity_key: Mapped[str] = mapped_column(String(250))
    cadence_type: Mapped[str] = mapped_column(String(30))
    interval_days: Mapped[int | None] = mapped_column(Integer)
    expected_amount: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    currency: Mapped[str] = mapped_column(String(3))
    next_expected_date: Mapped[date | None] = mapped_column(Date)
    confidence: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="active")
    reason: Mapped[str] = mapped_column(Text, default="")
    source_event_ids: Mapped[list[str]] = mapped_column(JSON, default=list)


class RecurringStreamOccurrence(Base):
    __tablename__ = "recurring_stream_occurrences"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("occ"))
    stream_id: Mapped[str] = mapped_column(ForeignKey("recurring_streams.id", ondelete="CASCADE"), index=True)
    event_id: Mapped[str | None] = mapped_column(String(80))
    occurrence_date: Mapped[date] = mapped_column(Date)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    status: Mapped[str] = mapped_column(String(20), default="projected")


class DecisionRequest(Base):
    __tablename__ = "decision_requests"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("req"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    currency: Mapped[str] = mapped_column(String(3))
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(120))
    request_date: Mapped[date] = mapped_column(Date)
    desired_completion_date: Mapped[date | None] = mapped_column(Date)
    allows_partial_payment: Mapped[bool] = mapped_column(Boolean, default=True)


class DecisionResult(Base):
    __tablename__ = "decision_results"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("decision"))
    request_id: Mapped[str] = mapped_column(ForeignKey("decision_requests.id", ondelete="CASCADE"), unique=True)
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    result: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DecisionEvidence(Base):
    __tablename__ = "decision_evidence"
    decision_id: Mapped[str] = mapped_column(ForeignKey("decision_results.id", ondelete="CASCADE"), primary_key=True)
    evidence_kind: Mapped[str] = mapped_column(String(40), primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    summary: Mapped[str] = mapped_column(Text)


class PaymentOption(Base):
    __tablename__ = "payment_options"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("pay"))
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    provider: Mapped[str] = mapped_column(String(100))
    option_type: Mapped[str] = mapped_column(String(30))
    total_payable: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    installment_amount: Mapped[Decimal | None] = mapped_column(Numeric(20, 8))
    number_of_payments: Mapped[int | None] = mapped_column(Integer)
    first_payment_date: Mapped[date | None] = mapped_column(Date)
    interval_days: Mapped[int | None] = mapped_column(Integer)
    fees: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=Decimal("0"))
    apr: Mapped[Decimal | None] = mapped_column(Numeric(10, 5))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    provenance: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id: Mapped[str] = mapped_column(String(80), primary_key=True, default=lambda: new_id("fx"))
    base_currency: Mapped[str] = mapped_column(String(3))
    quote_currency: Mapped[str] = mapped_column(String(3))
    rate_date: Mapped[date] = mapped_column(Date)
    rate: Mapped[Decimal] = mapped_column(Numeric(20, 12))
    provider: Mapped[str] = mapped_column(String(80))
    source_ref: Mapped[str | None] = mapped_column(String(250))
    __table_args__ = (UniqueConstraint("base_currency", "quote_currency", "rate_date", name="uq_fx_date_pair"),)


engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db(bind_engine=None) -> None:
    (bind_engine or engine).dispose() if bind_engine is not None else None
    Base.metadata.create_all(bind=bind_engine or engine)
