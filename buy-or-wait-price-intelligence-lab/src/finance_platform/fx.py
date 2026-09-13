from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Protocol
import httpx

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import ExchangeRate


class FXProvider(Protocol):
    def get_rate(self, base: str, quote: str, rate_date: date) -> Decimal: ...


class StoredFXProvider:
    def __init__(self, session: Session): self.session = session

    def get_rate(self, base: str, quote: str, rate_date: date) -> Decimal:
        base, quote = base.upper(), quote.upper()
        if base == quote: return Decimal("1")
        row = self.session.scalar(select(ExchangeRate).where(ExchangeRate.base_currency == base, ExchangeRate.quote_currency == quote, ExchangeRate.rate_date == rate_date))
        if row: return Decimal(str(row.rate))
        inverse = self.session.scalar(select(ExchangeRate).where(ExchangeRate.base_currency == quote, ExchangeRate.quote_currency == base, ExchangeRate.rate_date == rate_date))
        if inverse and inverse.rate: return Decimal("1") / Decimal(str(inverse.rate))
        raise LookupError(f"no stored FX rate for {base}/{quote} on {rate_date}")


class FrankfurterFXProvider:
    """Small explicit network adapter; callers should persist returned rates."""
    def __init__(self, base_url: str = "https://api.frankfurter.app"):
        self.base_url = base_url.rstrip("/")
        self._cache: dict[tuple[str, str, date], Decimal] = {}

    def get_rate(self, base: str, quote: str, rate_date: date) -> Decimal:
        base, quote = base.upper(), quote.upper()
        if base == quote: return Decimal("1")
        key = (base, quote, rate_date)
        if key in self._cache: return self._cache[key]
        endpoint = f"{self.base_url}/{rate_date.isoformat()}"
        response = httpx.get(endpoint, params={"from": base, "to": quote}, timeout=10)
        response.raise_for_status(); value = Decimal(str(response.json()["rates"][quote]))
        if not value.is_finite() or value <= 0: raise LookupError("FX provider returned invalid rate")
        self._cache[key] = value
        return value
