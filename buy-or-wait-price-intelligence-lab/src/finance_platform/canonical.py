from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import FinancialEvent, FinancialProfile, RecurringStream
from .recurrence import RecurringStreamDetector, cash_date
from .evidence import message_facts


@dataclass(frozen=True)
class CanonicalState:
    user_id: str
    as_of: date
    home_currency: str
    available_cash: Decimal
    minimum_balance: Decimal
    payment_methods: tuple[str, ...]
    events: tuple[FinancialEvent, ...]
    streams: tuple[RecurringStream, ...]
    pending_debits: tuple[FinancialEvent, ...]
    pending_credits: tuple[FinancialEvent, ...]
    uncertain_facts: tuple[str, ...]


def spendable_credit(event: FinancialEvent) -> bool:
    return event.direction == "credit" and event.status in {"settled"}


def pending_debit_is_obligation(event: FinancialEvent) -> bool:
    return event.direction == "debit" and event.status == "pending"


class CanonicalStateService:
    def __init__(self, detector: RecurringStreamDetector | None = None):
        self.detector = detector or RecurringStreamDetector()

    def state(self, session: Session, user_id: str, *, as_of: date) -> CanonicalState:
        profile = session.get(FinancialProfile, user_id)
        if profile is None:
            raise ValueError("financial profile is required")
        events = tuple(session.scalars(select(FinancialEvent).where(FinancialEvent.user_id == user_id)).all())
        facts = message_facts(session, user_id, events)
        streams = tuple(self.detector.detect(events, as_of=as_of, excluded_event_ids=set(facts.unavailable_event_ids | facts.terminated_event_ids | facts.one_time_event_ids | facts.internal_transfer_event_ids)))
        # Keep the derived stream ledger queryable while preserving its source
        # event IDs. Existing user-ended streams are not reactivated.
        ended = {row.identity_key for row in session.scalars(select(RecurringStream).where(RecurringStream.user_id == user_id, RecurringStream.status == "ended")).all()}
        persisted: list[RecurringStream] = []
        for stream in streams:
            if stream.identity_key in ended:
                continue
            current = session.scalar(select(RecurringStream).where(RecurringStream.user_id == user_id, RecurringStream.identity_key == stream.identity_key))
            if current is None:
                session.add(stream); persisted.append(stream)
            else:
                for field in ("direction", "event_type", "category", "cadence_type", "interval_days", "expected_amount", "currency", "next_expected_date", "confidence", "reason", "source_event_ids"):
                    setattr(current, field, getattr(stream, field))
                persisted.append(current)
        session.flush()
        pending_debits = tuple(e for e in events if pending_debit_is_obligation(e))
        pending_credits = tuple(e for e in events if e.direction == "credit" and e.status == "pending")
        uncertain = tuple(f"event:{e.id}:status={e.status}" for e in events if e.status in {"pending", "scheduled"} and e.direction == "credit")
        return CanonicalState(user_id, as_of, profile.home_currency, Decimal(str(profile.current_available_cash)), Decimal(str(profile.minimum_balance_to_keep + profile.emergency_buffer)), tuple(profile.payment_methods or ("full_payment", "wait")), events, tuple(persisted), pending_debits, pending_credits, uncertain)

    def mark_internal_transfer(self, session: Session, user_id: str, debit_id: str, credit_id: str, *, evidence_id: str) -> None:
        debit = session.get(FinancialEvent, debit_id)
        credit = session.get(FinancialEvent, credit_id)
        if not debit or not credit or debit.user_id != user_id or credit.user_id != user_id or debit.direction != "debit" or credit.direction != "credit":
            raise ValueError("events must be same-user debit/credit pair")
        if debit.amount != credit.amount or abs((debit.transaction_date - credit.transaction_date).days) > 2:
            raise ValueError("transfer pair requires matching amount and nearby dates")
        debit.direction = credit.direction = "transfer"
        debit.event_type = credit.event_type = "transfer"
        debit.recurrence_eligible = credit.recurrence_eligible = False
        debit.provider_metadata = {**(debit.provider_metadata or {}), "internal_transfer_evidence": evidence_id}
        credit.provider_metadata = {**(credit.provider_metadata or {}), "internal_transfer_evidence": evidence_id}
