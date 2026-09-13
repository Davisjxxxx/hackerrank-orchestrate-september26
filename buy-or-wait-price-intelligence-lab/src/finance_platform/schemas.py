from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    home_currency: str = Field(default="USD", min_length=3, max_length=3)
    current_available_cash: Decimal = Field(default=Decimal("0"), ge=0)
    minimum_balance_to_keep: Decimal = Field(default=Decimal("0"), ge=0)
    emergency_buffer: Decimal = Field(default=Decimal("0"), ge=0)
    income_confidence_preference: Literal["conservative", "balanced"] = "conservative"
    protected_categories: list[str] = Field(default_factory=list)
    flexible_categories: list[str] = Field(default_factory=list)
    payment_methods: list[str] = Field(default_factory=lambda: ["full_payment", "wait"])
    max_installment_months: int | None = Field(default=None, ge=1, le=60)
    forecast_horizon_days: int = Field(default=90, ge=1, le=365)
    timezone: str = "UTC"

    @field_validator("home_currency")
    @classmethod
    def currency_upper(cls, value: str) -> str:
        return value.upper()


class EventInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_type: str = "other"
    direction: Literal["credit", "debit", "transfer"]
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    transaction_date: date
    authorized_date: date | None = None
    settlement_date: date | None = None
    status: Literal["settled", "pending", "scheduled", "failed", "cancelled", "unrealized"] = "settled"
    merchant: str | None = None
    description: str = ""
    category: str | None = None
    external_id: str | None = None
    pending_transaction_id: str | None = None
    linked_event_id: str | None = None
    confidence: Literal["confirmed", "high", "medium", "low"] = "high"
    recurrence_eligible: bool = True
    flexibility: Literal["essential", "flexible", "unknown"] = "unknown"
    minimum_allowed_amount: Decimal | None = Field(default=None, ge=0)
    provider_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class DecisionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    description: str = Field(min_length=1, max_length=500)
    category: str | None = None
    request_date: date | None = None
    desired_completion_date: date | None = None
    allows_partial_payment: bool = True
    payment_options: list[dict[str, Any]] = Field(default_factory=list)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class DecisionOutput(BaseModel):
    amount_safe_to_pay_now: Decimal
    status: Literal["affordable_now", "affordable_with_plan", "affordable_later", "not_affordable"]
    recommended_method: Literal["full_payment", "partial_payment", "installments", "wait", "not_recommended"]
    earliest_safe_full_payment_date: date | None
    payment_plan: list[dict[str, Any]] = Field(default_factory=list)
    spending_changes: list[dict[str, Any]] = Field(default_factory=list)
    minimum_projected_balance: Decimal
    confidence: Literal["high", "medium", "low"]
    warnings: list[str] = Field(default_factory=list)
    evidence_summary: list[str] = Field(default_factory=list)
    explanation: str
