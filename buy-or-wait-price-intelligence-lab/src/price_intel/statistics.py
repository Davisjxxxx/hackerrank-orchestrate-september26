from __future__ import annotations

from decimal import Decimal
from typing import Sequence


def percentile(values: Sequence[Decimal], q: Decimal) -> Decimal:
    if not values:
        raise ValueError("values must not be empty")
    if q < 0 or q > 1:
        raise ValueError("q must be within [0, 1]")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = q * Decimal(len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - Decimal(lower)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def empirical_percentile_rank(values: Sequence[Decimal], x: Decimal) -> Decimal:
    if not values:
        raise ValueError("values must not be empty")
    at_or_below = sum(1 for value in values if value <= x)
    return (Decimal(at_or_below) / Decimal(len(values))) * Decimal("100")


def winsorize(values: Sequence[Decimal], lower_q: Decimal = Decimal("0.05"), upper_q: Decimal = Decimal("0.95")) -> list[Decimal]:
    """Clamp extreme observations without changing the sample size."""

    if not values:
        return []
    if not (Decimal("0") <= lower_q <= upper_q <= Decimal("1")):
        raise ValueError("winsorization quantiles must be within [0, 1]")
    lower = percentile(values, lower_q)
    upper = percentile(values, upper_q)
    return [min(upper, max(lower, value)) for value in values]


def distinct_source_count(providers: Sequence[str], retailers: Sequence[str | None]) -> int:
    """Count independent source/retailer pairs, not repeated aggregator rows."""

    pairs = {(provider, retailer or "") for provider, retailer in zip(providers, retailers)}
    return len(pairs)
