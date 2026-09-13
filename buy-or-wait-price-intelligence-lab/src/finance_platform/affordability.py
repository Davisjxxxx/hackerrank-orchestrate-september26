from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from typing import Any

from .canonical import CanonicalState, CanonicalStateService, cash_date
from .schemas import DecisionInput, DecisionOutput


class AffordabilityService:
    """Deterministic cash-flow decision service; it never reads files or calls models."""

    def __init__(self, state_service: CanonicalStateService | None = None):
        self.state_service = state_service or CanonicalStateService()

    def evaluate(self, state: CanonicalState, request: DecisionInput) -> DecisionOutput:
        amount = request.amount
        reserve = state.minimum_balance
        events = [e for e in state.events if e.status not in {"failed", "cancelled", "unrealized"} and e.direction != "transfer"]
        horizon = request.request_date + timedelta(days=90) if request.request_date else state.as_of + timedelta(days=90)
        base_trough, base_schedule = self._simulate(state, events, request.request_date or state.as_of, horizon, Decimal("0"))
        safe_now = max(Decimal("0"), min(amount, base_trough - reserve))
        safe_now = safe_now.quantize(Decimal("0.01"))
        if safe_now >= amount:
            return self._finalize(self._output(amount, safe_now, "affordable_now", "full_payment", request.request_date or state.as_of, base_trough, ["current available cash", f"reserve {reserve}"]), state)
        earliest = self._earliest(events, state, request, horizon, reserve)
        methods = set(self._profile_methods(state))
        if earliest and "full_payment" in methods and earliest <= (request.desired_completion_date or horizon):
            return self._finalize(self._output(amount, safe_now, "affordable_later", "wait", earliest, base_trough, [f"safe full payment date {earliest}", "pending credits excluded"]), state)
        if request.allows_partial_payment and "partial_payment" in methods and safe_now > 0 and safe_now < amount and earliest and earliest <= (request.desired_completion_date or horizon):
            plan = [{"date": request.request_date or state.as_of, "amount": safe_now}, {"date": earliest, "amount": amount - safe_now}]
            return self._finalize(self._output(amount, safe_now, "affordable_with_plan", "partial_payment", earliest, base_trough, ["two-payment plan", "pending debits reserved"], plan=plan), state)
        for option in request.payment_options:
            if option.get("type") == "installments" and "installments" in methods and self._option_safe(events, state, request, option, horizon, reserve):
                return self._finalize(self._output(amount, safe_now, "affordable_with_plan", "installments", earliest, base_trough, ["supplied payment option passed deterministic forecast"], plan=option.get("payments", [])), state)
        if "full_payment" in methods:
            return self._finalize(self._output(amount, safe_now, "not_affordable", "wait", None, base_trough, ["no safe full payment within forecast"]), state)
        return self._finalize(self._output(amount, safe_now, "not_affordable", "not_recommended", None, base_trough, ["no eligible safe method"]), state)

    @staticmethod
    def _finalize(result: DecisionOutput, state: CanonicalState) -> DecisionOutput:
        if state.freshness == "current": return result
        warning = "Financial data is incomplete; connect an account or complete a sync before relying on this recommendation." if state.freshness == "incomplete" else "Financial data is stale; refresh before relying on this recommendation."
        return result.model_copy(update={"confidence": "low" if state.freshness == "incomplete" else "medium", "warnings": [warning], "evidence_summary": [*result.evidence_summary, f"financial data as of {state.financial_data_as_of.isoformat() if state.financial_data_as_of else 'unknown'}"]})

    def _simulate(self, state: CanonicalState, events: list[Any], start: date, horizon: date, purchase: Decimal) -> tuple[Decimal, list[tuple[date, Decimal, str]]]:
        balance = Decimal(str(state.available_cash)) - purchase
        schedule: list[tuple[date, Decimal, str]] = [(start, balance, "purchase")]
        for event in events:
            d = cash_date(event)
            if d < start or d > horizon:
                if event.status == "pending" and event.direction == "debit" and d < start:
                    d = start
                else:
                    continue
            if event.direction == "credit" and event.status != "settled":
                continue
            balance += Decimal(str(event.amount)) if event.direction == "credit" else -Decimal(str(event.amount))
            schedule.append((d, balance, f"event:{event.id}"))
        for stream in state.streams:
            if stream.direction == "credit" and stream.confidence not in {"high", "confirmed"}:
                continue
            d = stream.next_expected_date
            count = 0
            while d and d <= horizon and count < 20:
                if d >= start:
                    balance += Decimal(str(stream.expected_amount)) if stream.direction == "credit" else -Decimal(str(stream.expected_amount))
                    schedule.append((d, balance, f"stream:{stream.id}"))
                if stream.cadence_type == "monthly":
                    from calendar import monthrange
                    month = d.month % 12 + 1; year = d.year + (1 if d.month == 12 else 0)
                    d = date(year, month, min(d.day, monthrange(year, month)[1]))
                else:
                    d += timedelta(days=stream.interval_days or 7)
                count += 1
        return (min((row[1] for row in schedule), default=balance), schedule)

    def _earliest(self, events: list[Any], state: CanonicalState, request: DecisionInput, horizon: date, reserve: Decimal) -> date | None:
        start = request.request_date or state.as_of
        for offset in range(91):
            day = start + timedelta(days=offset)
            trough, _ = self._simulate(state, events, day, horizon, request.amount)
            if trough >= reserve:
                return day
        return None

    @staticmethod
    def _profile_methods(state: CanonicalState) -> list[str]:
        from .db import FinancialProfile
        return getattr(state, "payment_methods", None) or ["full_payment", "wait", "partial_payment"]

    def _option_safe(self, events: list[Any], state: CanonicalState, request: DecisionInput, option: dict[str, Any], horizon: date, reserve: Decimal) -> bool:
        balance = Decimal(str(state.available_cash))
        for payment in option.get("payments", []):
            payment_date = payment.get("date")
            if isinstance(payment_date, str): payment_date = date.fromisoformat(payment_date)
            trough, _ = self._simulate(state, events, request.request_date or state.as_of, horizon, Decimal(str(payment.get("amount", "0"))))
            balance = min(balance, trough)
            if balance < reserve: return False
        return True

    @staticmethod
    def _output(amount: Decimal, safe: Decimal, status: str, method: str, earliest: date | None, trough: Decimal, evidence: list[str], *, plan: list[dict[str, Any]] | None = None) -> DecisionOutput:
        return DecisionOutput(amount_safe_to_pay_now=safe, status=status, recommended_method=method, earliest_safe_full_payment_date=earliest, payment_plan=plan or [], spending_changes=[], minimum_projected_balance=trough, confidence="high", warnings=[], evidence_summary=evidence, explanation=f"Available cash supports {safe} now while preserving the minimum reserve; projected trough is {trough}.")
