"""Protected finance-core integration port.

The product lane depends on this protocol only.  The committed HackerRank
engine can be wrapped behind it later; no product module imports or changes
``code/main.py`` or the scored output contract.
"""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from .models import FinancialSafetyResult, ProductIdentity


class FinancialDecisionProvider(Protocol):
    """Authoritative finance service boundary consumed by product decisions."""

    def evaluate(self, request: Mapping[str, Any], *, product: ProductIdentity,
                 subject_id: str | None = None) -> FinancialSafetyResult: ...


class CommittedFinanceCheckpointAdapter:
    """Adapter placeholder for the committed deterministic checkpoint.

    A callable is injected by an integration test or the later finance-lane
    convergence.  The adapter intentionally fails closed when no callable is
    supplied, so installation cannot be mistaken for live integration.
    """

    def __init__(self, evaluator=None):
        self.evaluator = evaluator

    def evaluate(self, request: Mapping[str, Any], *, product: ProductIdentity,
                 subject_id: str | None = None) -> FinancialSafetyResult:
        if self.evaluator is None:
            raise RuntimeError("committed finance checkpoint adapter is not wired")
        result = self.evaluator(request, product=product, subject_id=subject_id)
        if not isinstance(result, FinancialSafetyResult):
            raise TypeError("finance adapter must return FinancialSafetyResult")
        return result
