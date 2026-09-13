from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from price_intel.connectors.base import ConnectorStatus
from price_intel.intake import NormalizedProductInput
from price_intel.models import PriceObservation, ProductIdentity


@dataclass(frozen=True)
class RecordedCatalogConnector:
    """Sanitized deterministic provider fixture used by CI and local demos."""

    name: str
    products: Mapping[str, ProductIdentity]
    offers: Mapping[str, Sequence[PriceObservation]]
    status: ConnectorStatus = ConnectorStatus("recorded_fixture", True, None, True, "Sanitized CI data")

    def resolve_product(self, intake: NormalizedProductInput) -> Sequence[ProductIdentity]:
        matches = []
        for product in self.products.values():
            if intake.gtin and product.gtin and intake.gtin.zfill(14) == product.gtin.zfill(14):
                matches.append(product)
            elif intake.asin and product.asin and intake.asin.upper() == product.asin.upper():
                matches.append(product)
            elif intake.query_text and intake.query_text.lower() in product.title.lower():
                matches.append(product)
        return tuple(matches)

    def current_offers(self, product: ProductIdentity) -> Sequence[PriceObservation]:
        return tuple(self.offers.get(_product_key(product), ()))

    def price_history(self, product: ProductIdentity, *, lookback_days: int) -> Sequence[PriceObservation]:
        return tuple(self.offers.get(_product_key(product), ()))


def _product_key(product: ProductIdentity) -> str:
    return product.gtin or product.asin or product.mpn or product.title
