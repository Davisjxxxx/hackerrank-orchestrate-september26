"""Run three deterministic, fixture-labelled product decision stories."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json

from price_intel.governance import GovernedDecisionService
from price_intel.models import FinancialCoverageState, FinancialSafetyResult, FinancialState, PriceObservation, ProductIdentity, PurchaseIntent
from price_intel.observation_store import InMemoryObservationStore
from price_intel.price_intelligence import PriceIntelligenceService


NOW = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)
PRODUCT = ProductIdentity("Example OLED TV 55-inch", brand="Example", model="OLED55-X1", gtin="036000291452")
CONTROLS = {
    "financial_input_validated": True, "canonicalization_completed": True,
    "lifecycle_resolution_completed": True, "dedup_completed": True,
    "fx_processing_completed": True, "recurrence_processing_completed": True,
    "pending_debits_checked": True, "pending_credits_excluded": True,
    "confirmed_income_checked": True, "simulation_completed": True,
    "protected_balance_verified": True, "candidate_plans_evaluated": True,
    "product_identity_verified": True, "current_market_check_status": True,
    "price_history_state_declared": True, "condition_handling_verified": True,
    "decision_explanation_grounded": True, "safe_amount_covers_current_price": True,
    "unsupported_income_used": False, "payment_plan_legal": True, "deadline_respected": True,
}


def observations(current: str) -> tuple[PriceObservation, ...]:
    history = tuple(PriceObservation("recorded_fixture", NOW - timedelta(days=(index + 1) * 20), Decimal(str(price)), retailer="Example Store", provenance="sanitized_fixture")
                    for index, price in enumerate((700, 720, 740, 760, 780, 800, 820, 840, 860, 880, 900, 920)))
    return history + (PriceObservation("recorded_fixture", NOW, Decimal(current), retailer="Example Store", provenance="sanitized_fixture"),)


def financial(state: FinancialState, *, safe: str, later: datetime | None = None) -> FinancialSafetyResult:
    return FinancialSafetyResult(financial_state=state, safe_amount_today=Decimal(safe), minimum_balance=Decimal("500"),
                                 earliest_safe_full_payment_date=later, financial_data_as_of=NOW,
                                 financial_coverage_state=FinancialCoverageState.FULL)


def main() -> None:
    service = GovernedDecisionService()
    stories = (
        ("Demo A — safe + good price", "705", financial(FinancialState.SAFE_NOW, safe="1000")),
        ("Demo B — safe + poor price", "920", financial(FinancialState.SAFE_NOW, safe="1000")),
        ("Demo C — great deal + financially unsafe", "705", financial(FinancialState.SAFE_LATER, safe="0", later=NOW + timedelta(days=14))),
    )
    for title, current, finance_result in stories:
        store = InMemoryObservationStore()
        store.append("prod_demo_oled", PRODUCT, observations(current), ingested_at=NOW)
        price = PriceIntelligenceService(store).evaluate("prod_demo_oled", PRODUCT, PurchaseIntent(PRODUCT), now=NOW)
        result = service.evaluate(request={"story": title, "source": "sanitized_fixture"}, product=PRODUCT,
                                  financial=finance_result, price=price, control_evidence=CONTROLS)
        print(json.dumps({"story": title, "fixture_data": True, "current_price": current,
                          "price_signal": price.price_signal, "financial_state": finance_result.financial_state.value,
                          "recommendation": result.envelope.candidate_recommendation.value,
                          "review": result.review.status.value, "certification": result.certification.status.value,
                          "release": result.release.status.value}, sort_keys=True))


if __name__ == "__main__":
    main()
