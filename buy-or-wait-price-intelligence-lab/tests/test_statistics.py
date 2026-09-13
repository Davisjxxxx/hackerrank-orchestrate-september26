from decimal import Decimal
from price_intel.statistics import empirical_percentile_rank, percentile


def test_percentile_is_deterministic_decimal_math():
    values = [Decimal("10"), Decimal("20"), Decimal("30"), Decimal("40")]
    assert percentile(values, Decimal("0.5")) == Decimal("25.0")
    assert empirical_percentile_rank(values, Decimal("20")) == Decimal("50.0")
