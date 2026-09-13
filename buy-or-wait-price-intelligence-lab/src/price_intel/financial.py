from __future__ import annotations

from typing import Any, Protocol

from .models import FinancialCoverageState, FinancialSafetyResult, FinancialState, ProductIdentity


class FinancialEvidenceUnavailable(RuntimeError):
    pass


class FinancialSafetyProvider(Protocol):
    """Server-side seam for the authoritative financial engine."""

    def evaluate(self, *, subject_id: str, product: ProductIdentity, request: Any) -> FinancialSafetyResult: ...


class FixtureFinancialSafetyProvider:
    """Explicit lab-only provider used until the financial engine is injected."""

    def evaluate(self, *, subject_id: str, product: ProductIdentity, request: Any) -> FinancialSafetyResult:
        state = request.financial_state
        if state is None:
            raise FinancialEvidenceUnavailable("authoritative financial result is required")
        coverage = request.financial_coverage_state
        # Public request fields are only a lab fixture input. SAFE_NOW remains
        # non-authoritative unless the fixture explicitly carries FULL
        # coverage; the production provider must supply the real result.
        return FinancialSafetyResult(
            financial_state=state,
            safe_amount_today=request.safe_amount_today,
            earliest_safe_full_payment_date=request.earliest_safe_full_payment_date,
            minimum_balance=request.minimum_balance,
            recommended_payment_method=request.recommended_payment_method,
            payment_plan=request.payment_plan,
            financial_reason_codes=tuple(request.financial_reason_codes),
            financial_data_as_of=request.financial_data_as_of,
            financial_coverage_state=coverage,
        )
