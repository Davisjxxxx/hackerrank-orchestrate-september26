from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence

from price_intel.intake import NormalizedProductInput
from price_intel.models import PriceObservation, ProductIdentity


class ConnectorError(RuntimeError):
    """Provider failures are isolated from the deterministic engine."""


class ConnectorUnavailable(ConnectorError):
    pass


class ConnectorRateLimited(ConnectorError):
    pass


class ConnectorNormalizationError(ConnectorError):
    """Provider payload was malformed or incomplete for safe ingestion."""
    pass


@dataclass(frozen=True)
class ConnectorStatus:
    name: str
    configured: bool
    credential_env: str | None
    live_validated: bool = False
    notes: str = ""


class ProviderAdapter(Protocol):
    name: str
    status: ConnectorStatus

    def resolve_product(self, intake: NormalizedProductInput) -> Sequence[ProductIdentity]: ...

    def current_offers(self, product: ProductIdentity) -> Sequence[PriceObservation]: ...

    def price_history(self, product: ProductIdentity, *, lookback_days: int) -> Sequence[PriceObservation]: ...


class ProductResolutionConnector(Protocol):
    name: str

    def resolve_product(self, intake: NormalizedProductInput) -> Sequence[ProductIdentity]: ...


class CurrentOfferConnector(Protocol):
    name: str

    def current_offers(self, product: ProductIdentity) -> Sequence[PriceObservation]: ...


class PriceHistoryConnector(Protocol):
    name: str

    def price_history(self, product: ProductIdentity, *, lookback_days: int) -> Sequence[PriceObservation]: ...


class DealFeedConnector(Protocol):
    name: str

    def historical_deals(self, product: ProductIdentity, *, lookback_days: int) -> Sequence[PriceObservation]: ...


# Product-integration vocabulary. These aliases are deliberately small ports
# so providers can be replaced without coupling the decision engine to SDKs.
class ProductResolver(ProductResolutionConnector, Protocol):
    pass


class CurrentOfferProvider(CurrentOfferConnector, Protocol):
    pass


class PriceHistoryProvider(PriceHistoryConnector, Protocol):
    pass


class UsedOfferProvider(CurrentOfferConnector, Protocol):
    pass


class PriceWatchProvider(Protocol):
    def create_watch(self, *args: Any, **kwargs: Any) -> Any: ...

    def evaluate_watch(self, *args: Any, **kwargs: Any) -> Any: ...
