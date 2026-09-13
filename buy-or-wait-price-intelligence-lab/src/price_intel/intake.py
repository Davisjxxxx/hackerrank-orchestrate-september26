from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Mapping
from datetime import datetime
from urllib.parse import urlparse, urlunparse
import re


class ProductIntakeMode(StrEnum):
    BARCODE = "barcode"
    CAMERA_PHOTO = "camera_photo"
    IMAGE_UPLOAD = "image_upload"
    PRODUCT_URL = "product_url"
    TEXT_SEARCH = "text_search"
    MANUAL = "manual"


@dataclass(frozen=True)
class ProductIntakeRequest:
    mode: ProductIntakeMode
    barcode: str | None = None
    product_url: str | None = None
    query_text: str | None = None
    image_ref: str | None = None
    retailer_hint: str | None = None
    observed_price: Decimal | None = None
    observed_shipping: Decimal = Decimal("0")
    observed_at: datetime | None = None
    currency: str | None = None
    provenance: str | None = None
    ocr_evidence: Mapping[str, str] = field(default_factory=dict)
    user_confirmed: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedProductInput:
    mode: ProductIntakeMode
    gtin: str | None = None
    gtin14: str | None = None
    asin: str | None = None
    source_url: str | None = None
    source_host: str | None = None
    query_text: str | None = None
    image_ref: str | None = None
    retailer_hint: str | None = None
    observed_price: Decimal | None = None
    observed_shipping: Decimal = Decimal("0")
    observed_at: datetime | None = None
    currency: str | None = None
    provenance: str | None = None
    ocr_evidence: Mapping[str, str] = field(default_factory=dict)
    user_confirmed: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)


class ProductIntakeError(ValueError):
    pass


def normalize_intake(request: ProductIntakeRequest) -> NormalizedProductInput:
    currency = request.currency.upper().strip() if request.currency else None
    if currency is not None and (len(currency) != 3 or not currency.isalpha()):
        raise ProductIntakeError("currency must be a 3-letter ISO-style code")

    observed_price = _money(request.observed_price, "observed_price") if request.observed_price is not None else None
    observed_shipping = _money(request.observed_shipping, "observed_shipping")
    if request.observed_at is not None and request.observed_at.tzinfo is None:
        raise ProductIntakeError("observed_at must include a timezone")

    metadata = _safe_evidence_map(request.metadata)
    ocr_evidence = _safe_evidence_map(request.ocr_evidence)

    if request.mode == ProductIntakeMode.BARCODE:
        if not request.barcode:
            raise ProductIntakeError("barcode mode requires barcode")
        barcode = request.barcode.strip()
        if barcode.lower().startswith(("http://", "https://")):
            source_url, host, asin = normalize_product_url(barcode)
            return NormalizedProductInput(
                mode=request.mode,
                asin=asin,
                source_url=source_url,
                source_host=host,
                retailer_hint=request.retailer_hint,
                observed_price=observed_price,
                observed_shipping=observed_shipping,
                observed_at=request.observed_at,
                currency=currency,
                provenance=request.provenance,
                ocr_evidence=ocr_evidence,
                user_confirmed=request.user_confirmed,
                metadata=metadata,
            )
        gtin = normalize_identifier(barcode)
        return NormalizedProductInput(
            mode=request.mode,
            gtin=gtin,
            gtin14=gtin.zfill(14),
            retailer_hint=request.retailer_hint,
            observed_price=observed_price,
            observed_shipping=observed_shipping,
            observed_at=request.observed_at,
            currency=currency,
            provenance=request.provenance,
            ocr_evidence=ocr_evidence,
            user_confirmed=request.user_confirmed,
            metadata=metadata,
        )

    if request.mode == ProductIntakeMode.PRODUCT_URL:
        if not request.product_url:
            raise ProductIntakeError("product_url mode requires product_url")
        source_url, host, asin = normalize_product_url(request.product_url)
        return NormalizedProductInput(
            mode=request.mode,
            asin=asin,
            source_url=source_url,
            source_host=host,
            retailer_hint=request.retailer_hint,
            observed_price=observed_price,
            observed_shipping=observed_shipping,
            observed_at=request.observed_at,
            currency=currency,
            provenance=request.provenance,
            ocr_evidence=ocr_evidence,
            user_confirmed=request.user_confirmed,
            metadata=metadata,
        )

    if request.mode == ProductIntakeMode.TEXT_SEARCH:
        query = (request.query_text or "").strip()
        if len(query) < 2:
            raise ProductIntakeError("text_search mode requires a non-empty query")
        return NormalizedProductInput(
            mode=request.mode,
            query_text=" ".join(query.split()),
            retailer_hint=request.retailer_hint,
            observed_price=observed_price,
            observed_shipping=observed_shipping,
            observed_at=request.observed_at,
            currency=currency,
            provenance=request.provenance,
            metadata=metadata,
        )

    if request.mode in {ProductIntakeMode.CAMERA_PHOTO, ProductIntakeMode.IMAGE_UPLOAD}:
        image_ref = (request.image_ref or "").strip()
        if not image_ref:
            raise ProductIntakeError(f"{request.mode.value} mode requires image_ref")
        if len(image_ref) > 4096:
            raise ProductIntakeError("image_ref is too long")
        return NormalizedProductInput(
            mode=request.mode,
            image_ref=image_ref,
            query_text=" ".join((request.query_text or "").split()) or None,
            retailer_hint=request.retailer_hint,
            observed_price=observed_price,
            observed_shipping=observed_shipping,
            observed_at=request.observed_at,
            currency=currency,
            provenance=request.provenance,
            ocr_evidence=ocr_evidence,
            user_confirmed=request.user_confirmed,
            metadata=metadata,
        )

    if request.mode == ProductIntakeMode.MANUAL:
        query = " ".join((request.query_text or "").split())
        if not query and not request.metadata:
            raise ProductIntakeError("manual mode requires query_text or metadata")
        return NormalizedProductInput(
            mode=request.mode,
            query_text=query or None,
            retailer_hint=request.retailer_hint,
            observed_price=observed_price,
            observed_shipping=observed_shipping,
            observed_at=request.observed_at,
            currency=currency,
            provenance=request.provenance,
            ocr_evidence=ocr_evidence,
            user_confirmed=request.user_confirmed,
            metadata=metadata,
        )

    raise ProductIntakeError(f"unsupported intake mode: {request.mode}")


def normalize_identifier(value: str) -> str:
    compact = re.sub(r"[\s-]", "", value).upper()
    if re.fullmatch(r"[0-9]{9}[0-9X]", compact):
        return normalize_isbn(compact)
    return normalize_gtin(compact)


def normalize_gtin(value: str) -> str:
    digits = re.sub(r"[\s-]", "", value)
    if not digits.isdigit():
        raise ProductIntakeError("barcode must contain only digits, spaces, or hyphens")
    if len(digits) not in {8, 12, 13, 14}:
        raise ProductIntakeError("supported GTIN lengths are 8, 12, 13, and 14 digits")
    if not _valid_gtin_check_digit(digits):
        raise ProductIntakeError("invalid GTIN check digit")
    return digits


def normalize_isbn(value: str) -> str:
    compact = re.sub(r"[\s-]", "", value).upper()
    if not re.fullmatch(r"(?:[0-9]{9}[0-9X]|97[89][0-9]{10})", compact):
        raise ProductIntakeError("ISBN must be ISBN-10 or ISBN-13")
    if len(compact) == 10:
        total = sum((10 - index) * (10 if char == "X" else int(char)) for index, char in enumerate(compact))
        if total % 11 != 0:
            raise ProductIntakeError("invalid ISBN check digit")
        compact = _isbn10_to_isbn13(compact)
    if not _valid_gtin_check_digit(compact):
        raise ProductIntakeError("invalid ISBN check digit")
    return compact


def _isbn10_to_isbn13(value: str) -> str:
    body = "978" + value[:9]
    total = sum(int(char) * (1 if index % 2 == 0 else 3) for index, char in enumerate(body))
    return body + str((10 - total % 10) % 10)


def normalize_product_url(value: str) -> tuple[str, str, str | None]:
    candidate = value.strip()
    if any(ord(char) < 32 for char in candidate):
        raise ProductIntakeError("product_url contains control characters")
    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ProductIntakeError("product_url must be an absolute http(s) URL")
    if parsed.username or parsed.password:
        raise ProductIntakeError("product_url must not contain embedded credentials")
    try:
        parsed.port
    except ValueError as exc:
        raise ProductIntakeError("product_url has an invalid port") from exc
    host = (parsed.hostname or "").lower().removeprefix("www.")
    if not host:
        raise ProductIntakeError("product_url must include a hostname")
    asin = _extract_amazon_asin(host, parsed.path)
    canonical = urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, parsed.params, parsed.query, ""))
    return canonical, host, asin


def _extract_amazon_asin(host: str, path: str) -> str | None:
    amazon_domains = {
        "amazon.com", "amazon.ca", "amazon.co.uk", "amazon.de", "amazon.fr",
        "amazon.it", "amazon.es", "amazon.co.jp", "amazon.in", "amazon.com.au",
        "amazon.com.mx", "amazon.nl", "amazon.sg", "amazon.se", "amazon.pl",
        "amazon.be", "amazon.ie", "amazon.ae", "amazon.sa", "amazon.com.tr",
    }
    if not any(host == domain or host.endswith(f".{domain}") for domain in amazon_domains):
        return None
    match = re.search(r"/(?:dp|gp/product|gp/aw/d)/([A-Z0-9]{10})(?:[/?]|$)", path, re.IGNORECASE)
    return match.group(1).upper() if match else None


def _valid_gtin_check_digit(digits: str) -> bool:
    body = digits[:-1]
    expected = int(digits[-1])
    total = 0
    for index, char in enumerate(reversed(body)):
        total += int(char) * (3 if index % 2 == 0 else 1)
    check = (10 - (total % 10)) % 10
    return check == expected


def _safe_evidence_map(values: Mapping[str, str]) -> Mapping[str, str]:
    """Keep untrusted OCR/metadata as bounded evidence, never executable input."""

    safe: dict[str, str] = {}
    for key, value in values.items():
        safe_key = str(key)[:80]
        safe_value = " ".join(str(value).split())[:512]
        if safe_key and safe_value:
            safe[safe_key] = safe_value
    return safe


def _money(value: object, field_name: str) -> Decimal:
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ProductIntakeError(f"{field_name} must be a finite Decimal") from exc
    if not result.is_finite():
        raise ProductIntakeError(f"{field_name} must be finite")
    if result < 0:
        raise ProductIntakeError(f"{field_name} cannot be negative")
    return result
