from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
import json
import os
from typing import Any, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from price_intel.connectors.base import ConnectorError, ConnectorNormalizationError, ConnectorRateLimited, ConnectorStatus, ConnectorUnavailable
from price_intel.intake import NormalizedProductInput
from price_intel.models import Condition, ObservationTrust, PriceObservation, ProductIdentity


class ShopSavvyAdapter:
    """Server-side ShopSavvy adapter. No key is ever sent to the client."""

    name = "shopsavvy"

    def __init__(self, api_key: str | None = None, *, base_url: str = "https://api.shopsavvy.com/v1", timeout_seconds: float = 10.0):
        self.api_key = api_key or os.getenv("SHOPSAVVY_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.status = ConnectorStatus(self.name, bool(self.api_key), "SHOPSAVVY_API_KEY", False, "Live validation requires an authorized key")

    def resolve_product(self, intake: NormalizedProductInput) -> Sequence[ProductIdentity]:
        params: dict[str, str] = {}
        if intake.gtin:
            params["barcode"] = intake.gtin
        elif intake.asin:
            params["asin"] = intake.asin
        elif intake.source_url:
            params["url"] = intake.source_url
        elif intake.query_text:
            params["q"] = intake.query_text
        else:
            return ()
        payload = self._get("products", params)
        if not isinstance(payload, Mapping):
            raise ConnectorNormalizationError("ShopSavvy product response must be an object")
        raw_products = payload.get("products")
        if raw_products is not None and not isinstance(raw_products, list):
            raise ConnectorNormalizationError("ShopSavvy products must be a list")
        raw_candidates: list[object] = []
        singular = payload.get("product")
        if singular is not None:
            if not isinstance(singular, Mapping):
                raise ConnectorNormalizationError("ShopSavvy product must be an object")
            raw_candidates.append(singular)
        raw_candidates.extend(raw_products or [])
        if not raw_candidates:
            return ()
        candidates: list[ProductIdentity] = []
        for raw_candidate in raw_candidates:
            if not isinstance(raw_candidate, Mapping):
                continue
            try:
                candidates.append(_shop_savvy_product_identity(raw_candidate))
            except ConnectorNormalizationError:
                continue
        if not candidates:
            raise ConnectorNormalizationError("ShopSavvy product candidates were malformed")
        return tuple(sorted(candidates, key=_product_sort_key))

    def current_offers(self, product: ProductIdentity) -> Sequence[PriceObservation]:
        return self._offers(product, history_days=None)

    def price_history(self, product: ProductIdentity, *, lookback_days: int) -> Sequence[PriceObservation]:
        return self._offers(product, history_days=lookback_days)

    def _offers(self, product: ProductIdentity, history_days: int | None) -> Sequence[PriceObservation]:
        if product.asin:
            params = {"asin": product.asin}
        elif product.gtin:
            params = {"barcode": product.gtin}
        else:
            return ()
        if history_days is not None:
            params["history_days"] = str(history_days)
        payload = self._get("offers", params)
        if not isinstance(payload, Mapping):
            raise ConnectorNormalizationError("ShopSavvy offer response must be an object")
        observations: list[PriceObservation] = []
        offers = payload.get("offers", [])
        if not isinstance(offers, list):
            raise ConnectorNormalizationError("ShopSavvy offers must be a list")
        for offer in offers:
            if not isinstance(offer, Mapping):
                continue
            observations.extend(_shop_savvy_offer_rows(offer, self.name))
        return tuple(observations)

    def _get(self, path: str, params: Mapping[str, str]) -> Mapping[str, Any]:
        if not self.api_key:
            raise ConnectorUnavailable("SHOPSAVVY_API_KEY is not configured")
        request = Request(
            f"{self.base_url}/{path}?{urlencode(params)}",
            headers={"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"},
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 429:
                raise ConnectorRateLimited("ShopSavvy rate limit reached") from exc
            raise ConnectorError(f"ShopSavvy request failed with HTTP {exc.code}") from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ConnectorError("ShopSavvy request failed") from exc


@dataclass(frozen=True)
class UnconfiguredProviderAdapter:
    name: str
    credential_env: str | tuple[str, ...]
    notes: str

    @property
    def status(self) -> ConnectorStatus:
        requirements = (self.credential_env,) if isinstance(self.credential_env, str) else self.credential_env
        configured = all(bool(os.getenv(name)) for name in requirements)
        display = "/".join(requirements)
        return ConnectorStatus(self.name, configured, display, False, self.notes)

    def resolve_product(self, intake: NormalizedProductInput) -> Sequence[ProductIdentity]:
        self._unavailable()

    def current_offers(self, product: ProductIdentity) -> Sequence[PriceObservation]:
        self._unavailable()

    def price_history(self, product: ProductIdentity, *, lookback_days: int) -> Sequence[PriceObservation]:
        self._unavailable()

    def _unavailable(self) -> None:
        raise ConnectorUnavailable(f"{self.name} adapter is not configured; set {self.credential_env} server-side")


def build_provider_adapters() -> tuple[object, ...]:
    return (
        ShopSavvyAdapter(),
        UnconfiguredProviderAdapter("keepa", "KEEPA_API_KEY", "Amazon history lane; token economics and license require account validation"),
        UnconfiguredProviderAdapter("ebay", ("EBAY_CLIENT_ID", "EBAY_CLIENT_SECRET"), "Browse API lane; production access is partner-gated"),
        UnconfiguredProviderAdapter("bestbuy", "BESTBUY_API_KEY", "Catalog and open-box lane"),
        UnconfiguredProviderAdapter("serpapi", "SERPAPI_API_KEY", "Paid Google Shopping discovery lane"),
        UnconfiguredProviderAdapter("slickdeals", "SLICKDEALS_TOKEN", "Authorized partner/deal-signal lane"),
    )


def _shop_savvy_offer_rows(offer: Mapping[str, Any], provider: str) -> list[PriceObservation]:
    if not isinstance(offer, Mapping):
        return []
    retailer = offer.get("retailer") or offer.get("seller")
    source_url = offer.get("url")
    condition = _condition(offer.get("condition"))
    rows = []
    history = offer.get("history") or []
    if not isinstance(history, list):
        return []
    if history:
        for point in history:
            if not isinstance(point, Mapping):
                continue
            try:
                rows.append(_row(point, provider, retailer, source_url, condition, offer=offer))
            except ConnectorNormalizationError:
                continue
    else:
        try:
            rows.append(_row(offer, provider, retailer, source_url, condition))
        except ConnectorNormalizationError:
            return []
    return rows


def _row(payload: Mapping[str, Any], provider: str, retailer: str | None, source_url: str | None, condition: Condition, *, offer: Mapping[str, Any] | None = None) -> PriceObservation:
    offer = offer or payload
    missing: list[str] = []
    timestamp = payload.get("timestamp") or payload.get("observed_at") or offer.get("timestamp") or offer.get("observed_at")
    if timestamp is None:
        observed_at = datetime(1970, 1, 1, tzinfo=timezone.utc)
        missing.append("timestamp")
    else:
        try:
            observed_at = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        except (TypeError, ValueError) as exc:
            raise ConnectorNormalizationError("ShopSavvy timestamp is invalid") from exc
        if observed_at.tzinfo is None or observed_at.utcoffset() is None:
            raise ConnectorNormalizationError("ShopSavvy timestamp must include a timezone")
    raw_price = payload.get("price") if payload.get("price") is not None else payload.get("current_price")
    if raw_price is None:
        raise ConnectorNormalizationError("ShopSavvy offer has no price")
    try:
        price = Decimal(str(raw_price))
    except Exception as exc:
        raise ConnectorNormalizationError("ShopSavvy price is invalid") from exc
    if not price.is_finite() or price < 0:
        raise ConnectorNormalizationError("ShopSavvy price must be finite and non-negative")
    raw_shipping = payload.get("shipping") if "shipping" in payload else offer.get("shipping")
    if raw_shipping is None:
        shipping = Decimal("0")
        missing.append("shipping")
    else:
        try:
            shipping = Decimal(str(raw_shipping))
        except Exception as exc:
            raise ConnectorNormalizationError("ShopSavvy shipping is invalid") from exc
        if not shipping.is_finite() or shipping < 0:
            raise ConnectorNormalizationError("ShopSavvy shipping must be finite and non-negative")
    raw_currency = payload.get("currency") or offer.get("currency")
    currency = str(raw_currency).strip().upper() if raw_currency else "UNK"
    if raw_currency and (len(currency) != 3 or not currency.isalpha()):
        raise ConnectorNormalizationError("ShopSavvy currency is invalid")
    if not raw_currency:
        missing.append("currency")
    raw_availability = payload.get("availability") if "availability" in payload else offer.get("availability")
    availability = _availability(raw_availability)
    available = availability is True
    if availability is None:
        missing.append("availability")
    if condition == Condition.UNKNOWN:
        missing.append("condition")
    metadata = {"normalization_status": "quarantined", "missing_fields": ",".join(sorted(set(missing)))} if missing else {}
    try:
        landed_price = price + shipping
        if not landed_price.is_finite():
            raise ConnectorNormalizationError("ShopSavvy landed price is invalid")
        return PriceObservation(
            provider=provider,
            retailer=str(retailer) if retailer else None,
            observed_at=observed_at,
            price=price,
            shipping=shipping,
            condition=condition,
            available=available and not missing,
            source_url=str(source_url) if source_url else None,
            currency=currency,
            provenance="recorded_from_shopsavvy_response",
            metadata=metadata,
            trust=ObservationTrust.QUARANTINED if missing else ObservationTrust.TRUSTED_PROVIDER,
        )
    except ConnectorNormalizationError:
        raise
    except (ArithmeticError, TypeError, ValueError) as exc:
        raise ConnectorNormalizationError("ShopSavvy offer fields failed domain validation") from exc


def _condition(value: Any) -> Condition:
    normalized = str(value or "unknown").lower().replace("-", "_")
    return {
        "new": Condition.NEW,
        "refurbished": Condition.REFURBISHED,
        "used": Condition.USED,
        "open_box": Condition.OPEN_BOX,
        "openbox": Condition.OPEN_BOX,
    }.get(normalized, Condition.UNKNOWN)


def _availability(value: Any) -> bool | None:
    if value is None:
        return None
    normalized = str(value).strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in {"in_stock", "instock", "available", "available_now", "yes", "true", "1", "on"}:
        return True
    if normalized in {"out_of_stock", "unavailable", "not_available", "sold_out", "false", "0", "off"}:
        return False
    return None


def _shop_savvy_product_identity(product: Mapping[str, Any]) -> ProductIdentity:
    identifiers = product.get("identifiers") or {}
    specifications = product.get("specifications") or {}
    if not isinstance(identifiers, Mapping):
        raise ConnectorNormalizationError("ShopSavvy identifiers must be an object")
    if not isinstance(specifications, Mapping):
        raise ConnectorNormalizationError("ShopSavvy specifications must be an object")
    gtin = identifiers.get("gtin") or identifiers.get("upc") or identifiers.get("ean") or identifiers.get("isbn")
    return ProductIdentity(
        title=str(product.get("name") or product.get("title") or "Unknown product"),
        brand=str(product["brand"]) if product.get("brand") is not None else None,
        model=str(product.get("model") or product.get("model_number")) if product.get("model") or product.get("model_number") else None,
        gtin=str(gtin) if gtin else None,
        mpn=str(product["mpn"]) if product.get("mpn") is not None else None,
        asin=str(identifiers.get("asin") or product.get("asin")) if identifiers.get("asin") or product.get("asin") else None,
        variant={str(key): str(value) for key, value in specifications.items()},
        source_provenance="shopsavvy",
    )


def _product_sort_key(product: ProductIdentity) -> tuple[str, ...]:
    return (
        product.gtin or "",
        product.asin or "",
        product.brand or "",
        product.model or "",
        product.mpn or "",
        product.title,
        repr(sorted(product.variant.items())),
    )
