from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import EvidenceMessage, FinancialEvent


@dataclass(frozen=True)
class MessageFacts:
    unavailable_event_ids: frozenset[str] = frozenset()
    terminated_event_ids: frozenset[str] = frozenset()
    internal_transfer_event_ids: frozenset[str] = frozenset()
    one_time_event_ids: frozenset[str] = frozenset()


def classify_message(message: EvidenceMessage, events: Iterable[FinancialEvent]) -> MessageFacts:
    """Classify factual financial evidence; message text is never executed."""
    text = f"{message.subject or ''} {message.sanitized_text or ''}".lower()
    related = next((e for e in events if e.id == message.related_event_id), None)
    unavailable = {related.id} if related and related.direction == "credit" and any(p in text for p in ("pending", "not withdrawable", "not credited", "awaiting approval", "not approved", "processing")) else set()
    terminated = {related.id} if related and related.direction == "credit" and any(p in text for p in ("contract ended", "employment ended", "no renewal", "income source ended", "off-season income not confirmed")) else set()
    one_time = {related.id} if related and related.direction == "credit" and any(p in text for p in ("one-time", "bonus", "commission", "arrears", "refund", "prize", "invoice payment", "reimbursement")) and "recurring" not in text else set()
    transfer_ids: set[str] = set()
    if any(p in text for p in ("internal transfer", "own accounts", "same account holder", "between my accounts")) and related:
        transfer_ids.add(related.id)
        for event in events:
            if event.id != related.id and event.amount == related.amount and abs((event.transaction_date - related.transaction_date).days) <= 2:
                transfer_ids.add(event.id)
    return MessageFacts(frozenset(unavailable), frozenset(terminated), frozenset(transfer_ids), frozenset(one_time))


def message_facts(session: Session, user_id: str, events: Iterable[FinancialEvent]) -> MessageFacts:
    rows = list(events)
    combined = MessageFacts()
    for message in session.scalars(select(EvidenceMessage).where(EvidenceMessage.user_id == user_id)).all():
        facts = classify_message(message, rows)
        combined = MessageFacts(combined.unavailable_event_ids | facts.unavailable_event_ids, combined.terminated_event_ids | facts.terminated_event_ids, combined.internal_transfer_event_ids | facts.internal_transfer_event_ids, combined.one_time_event_ids | facts.one_time_event_ids)
    return combined
