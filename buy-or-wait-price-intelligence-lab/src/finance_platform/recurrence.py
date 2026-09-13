from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
import re
from typing import Iterable

from .db import FinancialEvent, RecurringStream

ONE_TIME_TYPES = {"bonus", "commission", "refund", "prize", "lottery", "arrears", "reimbursement", "invoice_payment", "asset_sale"}
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2, "confirmed": 3}


def normalized_descriptor(event: FinancialEvent) -> str:
    text = (event.merchant or event.description or "").lower().strip()
    text = re.sub(r"\b(?:19|20)\d{2}[-/]\d{1,2}[-/]\d{1,2}\b", " ", text)
    text = re.sub(r"\b(?:ref|reference|invoice|order|txn|transaction)[-_ ]?[a-z0-9]+\b", " ", text)
    text = re.sub(r"\b\d{4,}\b", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def is_one_time(event: FinancialEvent) -> bool:
    if event.event_type in ONE_TIME_TYPES:
        return True
    text = normalized_descriptor(event)
    return any(token in text.split() for token in ("bonus", "prize", "refund", "arrears", "reimbursement"))


def cash_date(event: FinancialEvent) -> date:
    return event.settlement_date or event.transaction_date


class RecurringStreamDetector:
    """Deterministic, provenance-first detector over canonical events."""

    def detect(self, events: Iterable[FinancialEvent], *, as_of: date, excluded_event_ids: set[str] | None = None) -> list[RecurringStream]:
        excluded_event_ids = excluded_event_ids or set()
        eligible = [e for e in events if e.id not in excluded_event_ids and e.status == "settled" and e.recurrence_eligible and not is_one_time(e) and e.direction in {"credit", "debit"} and cash_date(e) <= as_of]
        groups: dict[tuple[str, str, str, str, str], list[FinancialEvent]] = defaultdict(list)
        for event in eligible:
            key = (event.user_id, event.direction, event.event_type, event.category or "uncategorized", normalized_descriptor(event))
            groups[key].append(event)
        streams: list[RecurringStream] = []
        for key, rows in groups.items():
            rows.sort(key=cash_date)
            if len(rows) < 3:
                continue
            gaps = [(cash_date(b) - cash_date(a)).days for a, b in zip(rows, rows[1:])]
            cadence, interval = self._cadence(gaps)
            if cadence == "unknown":
                continue
            amounts = [Decimal(str(row.amount)) for row in rows[-3:]]
            expected = self._median(amounts) if key[1] == "credit" else max(amounts)
            next_date = self._next_date(cash_date(rows[-1]), cadence, interval)
            confidence = "high" if len(rows) >= 4 and max(gaps) - min(gaps) <= 5 else "medium"
            streams.append(RecurringStream(
                user_id=key[0], direction=key[1], event_type=key[2], category=None if key[3] == "uncategorized" else key[3],
                identity_key="|".join(key), cadence_type=cadence, interval_days=interval,
                expected_amount=expected, currency=rows[-1].currency, next_expected_date=next_date,
                confidence=confidence, reason=f"{len(rows)} settled observations; gaps={gaps}; descriptor={key[4]}",
                source_event_ids=[row.id for row in rows],
            ))
        return streams

    @staticmethod
    def _cadence(gaps: list[int]) -> tuple[str, int | None]:
        if not gaps:
            return "unknown", None
        median = sorted(gaps)[len(gaps) // 2]
        if 6 <= median <= 8 and all(abs(g - median) <= 2 for g in gaps):
            return "weekly", 7
        if 13 <= median <= 15 and all(abs(g - median) <= 3 for g in gaps):
            return "biweekly", 14
        if 27 <= median <= 32 and all(abs(g - median) <= 4 for g in gaps):
            return "monthly", None
        if all(abs(g - median) <= 3 for g in gaps):
            return "fixed_days", median
        return "unknown", None

    @staticmethod
    def _next_date(last: date, cadence: str, interval: int | None) -> date:
        if cadence == "monthly":
            month = last.month % 12 + 1
            year = last.year + (1 if last.month == 12 else 0)
            import calendar
            return date(year, month, min(last.day, calendar.monthrange(year, month)[1]))
        return last + timedelta(days=interval or 7)

    @staticmethod
    def _median(values: list[Decimal]) -> Decimal:
        ordered = sorted(values)
        return ordered[len(ordered) // 2]
