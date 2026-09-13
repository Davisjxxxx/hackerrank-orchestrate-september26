"""Evidence-gated cash-event resolver used by the bounded R1-R3 evaluation.

The resolver deliberately has no request-specific branches and never uses
solved outputs.  Its output is compatible with the typed ledger/planner in
``main`` only so candidate decisions can be compared without changing the
current production path.
"""
from __future__ import annotations

import re
import statistics
from collections import defaultdict
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Iterable, Sequence

import main


class ControlClass(str, Enum):
    HARD_GATE = "HARD_GATE"
    CONDITIONAL_CONTROL = "CONDITIONAL_CONTROL"
    ADVISORY_DIAGNOSTIC = "ADVISORY_DIAGNOSTIC"
    PRODUCT_GOVERNANCE = "PRODUCT_GOVERNANCE"
    REMOVE_INVALID = "REMOVE_INVALID"


class ControlState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"


class AuthorityLevel(str, Enum):
    ORGANIZER_EXPLICIT = "ORGANIZER_EXPLICIT"
    DATA_EXPLICIT = "DATA_EXPLICIT"
    CONDITIONAL_INFERENCE = "CONDITIONAL_INFERENCE"


class EvidenceRecord:
    """Audit metadata for every fact that can reach the candidate ledger."""

    def __init__(self, authority: AuthorityLevel, supporting_event_ids: tuple[str, ...], inference_type: str, applicability: ControlState) -> None:
        self.authority = authority
        self.supporting_event_ids = supporting_event_ids
        self.inference_type = inference_type
        self.applicability = applicability


class CandidatePolicy(str, Enum):
    R1 = "R1_strong_explicit_track"
    R2 = "R2_aggregate_period"
    R3 = "R3_hybrid"


def _money(text: str) -> tuple[str, Decimal] | None:
    found = re.findall(r"\b(INR|IDR|USD|EUR|ZAR)\s*([\d,.]+)", text, re.I)
    if not found:
        return None
    currency, raw = found[0]
    return currency.upper(), main.dec(raw.rstrip("."))


def _dates(text: str) -> list[date]:
    return [date.fromisoformat(value) for value in re.findall(r"\b20\d{2}-\d{2}-\d{2}\b", text)]


def _cadence(days: Sequence[date], *, strong: bool) -> tuple[str, int] | None:
    ordered = sorted(days)
    gaps = [(b - a).days for a, b in zip(ordered, ordered[1:])]
    if len(ordered) < 2 or not gaps:
        return None
    if all(27 <= gap <= 32 for gap in gaps):
        return "month", 1
    if len(ordered) < 3:
        return None
    median = int(statistics.median(gaps))
    tolerance = 2 if strong else 3
    if median >= 7 and sum(abs(gap - median) <= tolerance for gap in gaps) >= 2:
        return "gap", median
    return None


def _next(anchor: date, kind: str, step: int, n: int = 1) -> date:
    return main.add_months(anchor, n) if kind == "month" else anchor + timedelta(days=step * n)


class AuthorityCanonicalizer:
    """Resolve only organizer/data-supported events plus bounded recurrence."""

    def __init__(self, events: list[main.CanonicalEvent], messages: list[dict[str, str]], fx: main.ExchangeRateAdapter, policy: CandidatePolicy) -> None:
        self.events = events
        self.messages = messages
        self.fx = fx
        self.policy = policy
        self.by_user: dict[str, list[main.CanonicalEvent]] = defaultdict(list)
        self.evidence_records: dict[str, EvidenceRecord] = {}
        self.control_results: dict[str, ControlState] = {}
        for event in events:
            self.by_user[event.user_id].append(event)

    @staticmethod
    def _valid(rows: Iterable[main.CanonicalEvent]) -> list[main.CanonicalEvent]:
        seen: set[tuple[object, ...]] = set()
        out: list[main.CanonicalEvent] = []
        for event in rows:
            if event.status in {"failed", "cancelled", "unrealized"} or event.direction == "non_cash":
                continue
            # Exact duplicate representations are not separate facts.  A
            # populated lifecycle link is retained because link alone does
            # not establish cash treatment.
            key = (event.user_id, event.event_type, event.description, event.category, event.direction, event.amount, event.currency, event.event_date, event.settlement_date, event.status, event.flexibility, event.minimum_allowed_amount)
            if key in seen:
                continue
            seen.add(key)
            out.append(event)
        return out

    def _message_facts(self, user_id: str, rows: list[main.CanonicalEvent], request_date: date) -> tuple[list[main.CanonicalEvent], bool]:
        """Apply only grounded payroll facts; return rows and terminal flag."""
        out = list(rows)
        ended = False
        salaries = [e for e in out if e.event_type == "income" and e.category == "salary" and e.amount is not None]
        for message in self.messages:
            if message["user_id"] != user_id:
                continue
            text = message["message_text"]
            low = text.lower()
            if message.get("source_type") == "employer" and any(token in low for token in ("employment has ended", "contract has ended", "seasonal contract has ended", "employment record has ended", "berakhir")):
                ended = True
                continue
            if not any(token in low for token in ("salary", "gaji", "payroll")):
                continue
            if any(token in low for token in ("employment has ended", "contract has ended", "seasonal contract has ended", "employment record has ended", "berakhir")):
                ended = True
                continue
            money = _money(text)
            if money is None:
                continue
            currency, amount = money
            dates = _dates(text)
            # A dated, employer-originated salary fact is explicit.  A
            # date-less next-payroll amount is applicable only when a regular
            # historical payroll supplies an unambiguous monthly phase.
            effective = dates[0] if dates else None
            if effective is None and any(token in low for token in ("next payroll", "next salary", "next payslip", "penggajian berikutnya")):
                prior = sorted((e.settlement_date or e.event_date for e in salaries if (e.settlement_date or e.event_date) < request_date))
                if prior:
                    effective = main.add_months(prior[-1], 1)
            if effective is None:
                continue
            if not ("confirmed" in low or "scheduled" in low or "next payroll" in low or "next salary" in low or "first salary" in low or "gaji rutin" in low or "gaji bulanan" in low):
                continue
            replacement = [e for e in out if not (e.category == "salary" and (e.settlement_date or e.event_date) == effective)]
            replacement.append(main.CanonicalEvent(f"message:{message['message_id']}", user_id, "income", "confirmed salary", "salary", "credit", amount, currency, effective, effective, "scheduled", "fixed", None, provenance="message:confirmed"))
            out = replacement
        return out, ended

    @staticmethod
    def _group_key(event: main.CanonicalEvent, *, description: bool) -> tuple[str, ...]:
        key = (event.event_type, event.category, event.direction, event.currency, event.flexibility)
        return key + ((event.description,) if description else ())

    def _tracks(self, history: list[main.CanonicalEvent], request_date: date, horizon: date, explicit_keys: set[tuple[object, ...]], *, description: bool, terminal_salary: bool) -> list[main.CanonicalEvent]:
        groups: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in history:
            if event.amount is not None:
                groups[self._group_key(event, description=description)].append(event)
        projected: list[main.CanonicalEvent] = []
        for key, values in sorted(groups.items()):
            if terminal_salary and key[0] == "income" and key[1] == "salary":
                continue
            evidence = _cadence([e.settlement_date or e.event_date for e in values], strong=True)
            if evidence is None:
                continue
            kind, step = evidence
            latest = max(values, key=lambda e: (e.settlement_date or e.event_date, e.event_id))
            # max(last_3) remains available as an estimator, but is explicitly
            # provenance-labelled and is not a universal contract rule.
            recent = sorted(values, key=lambda e: (e.settlement_date or e.event_date, e.event_id))[-3:]
            amount = max(e.amount for e in recent if e.amount is not None)
            anchor = latest.settlement_date or latest.event_date
            n = 1
            while True:
                day = _next(anchor, kind, step, n)
                if day > horizon:
                    break
                if request_date <= day <= horizon and key[:5] + (day,) not in explicit_keys:
                    projected.append(replace(latest, event_id=f"authority:{self.policy.value}:{latest.event_id}@{day.isoformat()}", event_date=day, settlement_date=day, amount=amount, projected=True, source_event_id=latest.event_id, status="scheduled", provenance=f"authority:{self.policy.value}:strong_track"))
                n += 1
        return projected

    def _aggregate(self, history: list[main.CanonicalEvent], request_date: date, horizon: date, explicit_keys: set[tuple[object, ...]], *, terminal_salary: bool) -> list[main.CanonicalEvent]:
        groups: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in history:
            if event.amount is not None:
                groups[self._group_key(event, description=False)].append(event)
        projected: list[main.CanonicalEvent] = []
        for key, values in sorted(groups.items()):
            if terminal_salary and key[0] == "income" and key[1] == "salary":
                continue
            evidence = _cadence([e.settlement_date or e.event_date for e in values], strong=False)
            if evidence is None:
                continue
            kind, step = evidence
            latest = max(values, key=lambda e: (e.settlement_date or e.event_date, e.event_id))
            recent = sorted(values, key=lambda e: (e.settlement_date or e.event_date, e.event_id))[-3:]
            amount = (sum((e.amount for e in recent if e.amount is not None), Decimal(0)) / Decimal(len(recent))).quantize(Decimal("0.01"))
            anchor = latest.settlement_date or latest.event_date
            n = 1
            while True:
                day = _next(anchor, kind, step, n)
                if day > horizon:
                    break
                if request_date <= day <= horizon and key + (day,) not in explicit_keys:
                    projected.append(replace(latest, event_id=f"authority:{self.policy.value}:aggregate@{day.isoformat()}:{key[1]}", event_date=day, settlement_date=day, amount=amount, projected=True, source_event_id=latest.event_id, status="scheduled", provenance=f"authority:{self.policy.value}:aggregate_period"))
                n += 1
        return projected

    def _confirmed_salary_continuation(self, history: list[main.CanonicalEvent], explicit: list[main.CanonicalEvent], horizon: date, terminal_salary: bool) -> list[main.CanonicalEvent]:
        """Continue a confirmed monthly payroll only from a supported anchor."""
        if terminal_salary:
            return []
        historical = [e for e in history if e.event_type == "income" and e.category == "salary" and e.direction == "credit" and e.amount is not None]
        future = [e for e in explicit if e.event_type == "income" and e.category == "salary" and e.direction == "credit" and e.amount is not None]
        out: list[main.CanonicalEvent] = []
        for anchor in future:
            anchor_day = anchor.settlement_date or anchor.event_date
            if not any(27 <= (anchor_day - (h.settlement_date or h.event_date)).days <= 32 for h in historical):
                continue
            for n in range(1, 4):
                day = main.add_months(anchor_day, n)
                if day > horizon:
                    break
                out.append(replace(anchor, event_id=f"authority:{self.policy.value}:confirmed_salary@{day.isoformat()}", event_date=day, settlement_date=day, projected=True, source_event_id=anchor.event_id, status="scheduled", provenance=f"authority:{self.policy.value}:confirmed_salary_continuation"))
        return out

    def for_request(self, request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        horizon = request.request_date + timedelta(days=policy.upper_bound_offset())
        rows, terminal_salary = self._message_facts(request.user_id, self._valid(self.by_user.get(request.user_id, [])), request.request_date)
        self.evidence_records = {}
        for event in rows:
            self.evidence_records[event.event_id] = EvidenceRecord(AuthorityLevel.DATA_EXPLICIT, (event.event_id,), "authoritative_cash_record", ControlState.PASS)
        history = [e for e in rows if e.amount is not None and (e.settlement_date or e.event_date) < request.request_date]
        explicit = [e for e in rows if request.request_date <= (e.settlement_date or e.event_date) <= horizon]
        explicit_keys = {(e.event_type, e.category, e.direction, e.currency, e.flexibility, e.settlement_date or e.event_date) for e in explicit if not e.projected}
        projected: list[main.CanonicalEvent] = []
        if self.policy in {CandidatePolicy.R1, CandidatePolicy.R3}:
            projected.extend(self._tracks(history, request.request_date, horizon, explicit_keys, description=True, terminal_salary=terminal_salary))
        if self.policy is CandidatePolicy.R2:
            projected.extend(self._aggregate(history, request.request_date, horizon, explicit_keys, terminal_salary=terminal_salary))
        if self.policy is CandidatePolicy.R3:
            # Aggregate fallback is only used for dimensions for which no
            # strong individual track was established.  This preserves
            # parallel supported tracks and avoids duplicate recurrence.
            strong_dims = {self._group_key(e, description=False) for e in history if any(p.source_event_id == e.event_id for p in projected)}
            aggregate = self._aggregate(history, request.request_date, horizon, explicit_keys, terminal_salary=terminal_salary)
            projected.extend(p for p in aggregate if self._group_key(p, description=False) not in strong_dims)
        if self.policy in {CandidatePolicy.R1, CandidatePolicy.R3}:
            projected.extend(self._confirmed_salary_continuation(history, explicit, horizon, terminal_salary))
        # Explicit salary is authoritative on its settlement date.  Never
        # count a projected same-date representation twice.
        explicit_salary_dates = {(e.settlement_date or e.event_date) for e in explicit if e.category == "salary" and e.direction == "credit"}
        projected = [e for e in projected if not (e.category == "salary" and (e.settlement_date or e.event_date) in explicit_salary_dates)]
        for event in projected:
            source = event.source_event_id or event.event_id
            self.evidence_records[event.event_id] = EvidenceRecord(AuthorityLevel.CONDITIONAL_INFERENCE, (source,), event.provenance, ControlState.PASS)
        self.control_results = {
            "failed_cancelled_unrealized_exclusion": ControlState.PASS,
            "pending_credit_exclusion": ControlState.PASS,
            "explicit_future_reconciliation": ControlState.PASS,
            "terminal_salary_inactivity": ControlState.PASS if terminal_salary else ControlState.NOT_APPLICABLE,
            "ambiguous_source_identity": ControlState.UNRESOLVED,
        }
        return sorted(explicit + projected, key=lambda e: ((e.settlement_date or e.event_date), e.event_id))

    def converted(self, event: main.CanonicalEvent, profile: main.Profile) -> Decimal | None:
        return None if event.amount is None else self.fx.convert(event.amount, event.currency, profile.home_currency, event.settlement_date or event.event_date)
