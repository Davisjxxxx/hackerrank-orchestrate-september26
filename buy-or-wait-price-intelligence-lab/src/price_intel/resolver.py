from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import re
from typing import Iterable, Sequence

from .intake import NormalizedProductInput
from .models import ProductIdentity


class IdentityResolutionState(StrEnum):
    EXACT = "exact"
    NEEDS_CONFIRMATION = "needs_confirmation"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class IdentityCandidate:
    product: ProductIdentity
    score: int
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class IdentityResolution:
    state: IdentityResolutionState
    product: ProductIdentity | None
    candidates: tuple[IdentityCandidate, ...]
    reason_codes: tuple[str, ...]


def canonical_product_id(product: ProductIdentity) -> str:
    # Enrichment must not fragment a strong identity. Variant attributes are
    # part of the key only when no stronger stable identifier exists.
    if product.gtin:
        key = f"gtin:{re.sub(r'[^0-9]', '', product.gtin).zfill(14)}"
    elif product.asin:
        key = f"asin:{product.asin.upper()}"
    elif product.mpn and product.brand:
        key = f"brand_mpn:{_normalize_token(product.brand)}:{_normalize_token(product.mpn)}"
    elif product.brand and product.model:
        variant = ";".join(f"{key}={_normalize_token(value)}" for key, value in sorted(product.variant.items()))
        key = f"brand_model:{_normalize_token(product.brand)}:{_normalize_token(product.model)}:{variant}"
    else:
        variant = ";".join(f"{key}={_normalize_token(value)}" for key, value in sorted(product.variant.items()))
        key = f"title:{_normalize_title(product.title)}:{variant}"
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return f"prod_{digest[:16]}"


class ProductIdentityResolver:
    """Deterministic resolver with an explicit ambiguity gate."""

    def resolve(self, intake: NormalizedProductInput, candidates: Iterable[ProductIdentity]) -> IdentityResolution:
        ranked = sorted(
            (self._score(intake, candidate) for candidate in candidates),
            key=lambda candidate: (-candidate.score, _candidate_key(candidate.product)),
        )
        if not ranked or ranked[0].score <= 0:
            return IdentityResolution(IdentityResolutionState.UNRESOLVED, None, tuple(ranked), ("NO_IDENTITY_MATCH",))

        top = ranked[0]
        has_strong_identifier = top.score >= 100
        strong_candidates = [candidate for candidate in ranked if candidate.score >= 95]
        conflicting_strong = [candidate for candidate in strong_candidates if self._materially_different(top.product, candidate.product)]
        materially_different = [candidate for candidate in ranked if self._materially_different(top.product, candidate.product)]
        if conflicting_strong or (not has_strong_identifier and len(materially_different) > 1) or (not has_strong_identifier and top.score < 80):
            return IdentityResolution(
                IdentityResolutionState.NEEDS_CONFIRMATION,
                None,
                tuple(ranked[:5]),
                ("AMBIGUOUS_PRODUCT_IDENTITY", "VARIANT_CONFIRMATION_REQUIRED"),
            )

        confidence = min(1, top.score / 100)
        product = ProductIdentity(
            title=top.product.title,
            brand=top.product.brand,
            model=top.product.model,
            gtin=top.product.gtin,
            mpn=top.product.mpn,
            asin=top.product.asin,
            variant=top.product.variant,
            identity_confidence=top.product.identity_confidence if top.product.identity_confidence < 1 else _decimal(confidence),
            identity_evidence=top.evidence or top.product.identity_evidence,
            source_provenance=top.product.source_provenance,
        )
        return IdentityResolution(IdentityResolutionState.EXACT, product, tuple(ranked[:5]), ("IDENTITY_RESOLVED",))

    def _score(self, intake: NormalizedProductInput, product: ProductIdentity) -> IdentityCandidate:
        evidence: list[str] = []
        score = 0
        if intake.gtin and product.gtin and intake.gtin.zfill(14) == product.gtin.zfill(14):
            score += 100
            evidence.append("EXACT_GTIN")
        if intake.asin and product.asin and intake.asin.upper() == product.asin.upper():
            score += 95
            evidence.append("EXACT_ASIN")
        if intake.query_text:
            query = _normalize_title(intake.query_text)
            title = _normalize_title(product.title)
            if query == title:
                score += 70
                evidence.append("EXACT_NORMALIZED_TITLE")
            elif query and (query in title or title in query):
                score += 45
                evidence.append("TITLE_CONTAINS_QUERY")
            else:
                query_tokens = set(query.split())
                title_tokens = set(title.split())
                overlap = len(query_tokens & title_tokens) / max(len(query_tokens), 1)
                if overlap >= 0.6:
                    score += 35
                    evidence.append("FUZZY_TITLE")
        if intake.ocr_evidence:
            mpn = intake.ocr_evidence.get("mpn") or intake.ocr_evidence.get("model")
            if mpn and product.mpn and _normalize_token(mpn) == _normalize_token(product.mpn):
                score += 80
                evidence.append("OCR_MPN_MATCH")
            brand = intake.ocr_evidence.get("brand")
            if brand and product.brand and _normalize_token(brand) == _normalize_token(product.brand):
                score += 20
                evidence.append("OCR_BRAND_MATCH")
        if intake.source_host and product.source_provenance and intake.source_host in product.source_provenance:
            score += 10
            evidence.append("SOURCE_HOST_MATCH")
        if intake.user_confirmed:
            score += 20
            evidence.append("USER_CONFIRMED")
        return IdentityCandidate(product, score, tuple(evidence))

    @staticmethod
    def _materially_different(left: ProductIdentity, right: ProductIdentity) -> bool:
        if left.gtin and right.gtin and left.gtin.zfill(14) != right.gtin.zfill(14):
            return True
        for key in {"capacity", "storage", "size", "pack_count", "bundle", "edition", "generation", "year", "condition", "carrier", "region"}:
            if left.variant.get(key, "").lower() != right.variant.get(key, "").lower():
                return True
        if left.model and right.model and _normalize_token(left.model) != _normalize_token(right.model):
            return True
        if left.mpn and right.mpn and _normalize_token(left.mpn) != _normalize_token(right.mpn):
            return True
        if left.brand and right.brand and _normalize_token(left.brand) != _normalize_token(right.brand):
            return True
        return False


class FixtureProductResolver(ProductIdentityResolver):
    def __init__(self, products: Sequence[ProductIdentity]):
        self.products = tuple(products)

    def resolve_product(self, intake: NormalizedProductInput) -> IdentityResolution:
        return self.resolve(intake, self.products)


def _normalize_title(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.lower()).split())


def _normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _candidate_key(product: ProductIdentity) -> tuple[str, ...]:
    return (
        product.gtin or "",
        product.asin or "",
        product.mpn or "",
        product.brand or "",
        product.model or "",
        _normalize_title(product.title),
        repr(sorted(product.variant.items())),
    )


def _decimal(value: float):
    from decimal import Decimal

    return Decimal(str(value)).quantize(Decimal("0.01"))
