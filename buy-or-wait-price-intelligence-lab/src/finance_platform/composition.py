from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from price_intel.engine import PriceIntelligenceEngine
from price_intel.models import PriceObservation, ProductIdentity, PurchaseIntent, Urgency
from price_intel.observation_store import InMemoryObservationStore
from price_intel.price_intelligence import PriceIntelligenceService
from price_intel.resolver import canonical_product_id

from .affordability import AffordabilityService
from .canonical import CanonicalStateService
from .schemas import DecisionInput


class BuyOrWaitService:
    """Composition only: price and finance engines stay independent."""

    def __init__(self, state_service: CanonicalStateService | None = None, affordability: AffordabilityService | None = None):
        self.state_service = state_service or CanonicalStateService()
        self.affordability = affordability or AffordabilityService(self.state_service)

    def evaluate_purchase(self, session: Session, *, user_id: str, purchase: DecisionInput, price_context: dict[str, Any] | None = None) -> dict[str, Any]:
        price_context = price_context or {}
        request_date = purchase.request_date
        if request_date is None: raise ValueError("purchase request_date is required")
        financial_state = self.state_service.state(session, user_id, as_of=request_date)
        affordability = self.affordability.evaluate(financial_state, purchase)
        price = self._price(purchase, price_context)
        financial_confidence = affordability.confidence
        decision, action = self._compose(affordability.status, price["verdict"], affordability.recommended_method, affordability.earliest_safe_full_payment_date)
        overall = "low" if "low" in {financial_confidence, price["confidence"]} else ("medium" if "medium" in {financial_confidence, price["confidence"]} else "high")
        warnings = [*affordability.warnings]
        if price["verdict"] == "unknown": warnings.append("Price history is incomplete; price timing is uncertain.")
        return {"decision": decision, "recommended_action": action, "price_verdict": price["verdict"], "affordability_verdict": affordability.status, "safe_to_pay_now": str(affordability.amount_safe_to_pay_now), "current_price": str(purchase.amount), "reference_price": price["reference_price"], "estimated_savings_if_waiting": price["estimated_savings"], "earliest_financially_safe_date": affordability.earliest_safe_full_payment_date.isoformat() if affordability.earliest_safe_full_payment_date else None, "payment_plan": affordability.payment_plan, "minimum_projected_balance": str(affordability.minimum_projected_balance), "price_confidence": price["confidence"], "financial_confidence": financial_confidence, "overall_confidence": overall, "warnings": warnings, "evidence_summary": [*affordability.evidence_summary, *price["evidence"]], "explanation": self._explanation(decision, purchase.amount, affordability, price), "financial_state_as_of": financial_state.financial_data_as_of.isoformat() if financial_state.financial_data_as_of else None, "financial_freshness": financial_state.freshness, "price_intelligence": price["record"]}

    def _price(self, purchase: DecisionInput, context: dict[str, Any]) -> dict[str, Any]:
        now = datetime.combine(purchase.request_date, datetime.min.time(), tzinfo=timezone.utc)
        product = ProductIdentity(title=purchase.description, source_provenance="user_purchase_input")
        store = InMemoryObservationStore(); service = PriceIntelligenceService(store, PriceIntelligenceEngine()); product_id = canonical_product_id(product)
        observations = [PriceObservation(provider="user_input", observed_at=now, price=purchase.amount, currency=purchase.currency, provenance="user_purchase_input")]
        for index, raw in enumerate(context.get("historical_prices", [])):
            value = Decimal(str(raw)); observations.append(PriceObservation(provider="user_reference", observed_at=now - timedelta(days=30 * (index + 1)), price=value, currency=purchase.currency, provenance="user_supplied_reference_history"))
        store.append(product_id, product, observations, ingested_at=now, user_id="composition")
        record = service.evaluate(product_id, product, PurchaseIntent(product=product, urgency=Urgency.FLEXIBLE, max_wait_days=90), now=now, user_id="composition")
        signal = record.price_signal
        # Sparse history is uncertainty, not evidence that the current price
        # is high. Only an adequate covered history can produce a directional
        # price verdict.
        if record.price_history_status != "SUFFICIENT":
            verdict = "unknown"
        else:
            verdict = "attractive" if signal in {"STRONG_BUY", "BUY"} else ("high" if signal in {"WAIT", "STRONG_WAIT"} else ("neutral" if signal == "NEUTRAL" else "unknown"))
        reference = str(record.historical_average) if record.historical_average is not None else None
        savings = str(max(Decimal("0"), Decimal(reference) - purchase.amount)) if reference else None
        confidence = "high" if record.confidence >= Decimal("0.75") else ("medium" if record.confidence >= Decimal("0.45") else "low")
        return {"verdict": verdict, "reference_price": reference, "estimated_savings": savings, "confidence": confidence, "record": record.to_dict(), "evidence": [f"price signal {signal}", f"price observations {record.observation_count}"]}

    @staticmethod
    def _compose(financial: str, price: str, method: str, earliest: Any) -> tuple[str, str]:
        if financial == "not_affordable": return (("WAIT_FOR_CASH_FLOW", "wait for cash flow") if earliest else ("DO_NOT_BUY", "do not buy"))
        if financial == "affordable_with_plan": return ("USE_PAYMENT_PLAN", "use the verified payment plan")
        if financial == "affordable_later": return ("WAIT_FOR_CASH_FLOW", "wait for cash flow")
        if price == "attractive": return ("BUY_NOW", "buy now")
        if price == "high": return ("WAIT_FOR_PRICE", "wait for a better price")
        return ("INSUFFICIENT_DATA", "confirm more price evidence")

    @staticmethod
    def _explanation(decision: str, amount: Decimal, affordability: Any, price: dict[str, Any]) -> str:
        price_text = f"Price evidence is {price['verdict']}" if price["verdict"] != "unknown" else "Price history is incomplete"
        return f"{decision}: the purchase is {amount} in the requested currency. {price_text}; financial forecast keeps a minimum projected balance of {affordability.minimum_projected_balance} and supports {affordability.amount_safe_to_pay_now} now."
