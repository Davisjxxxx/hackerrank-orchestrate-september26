from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AccessClass(StrEnum):
    OFFICIAL_API = "official_api"
    PARTNER_TOKEN = "partner_token"
    LIMITED_RELEASE = "limited_release"
    DEFERRED = "deferred"


@dataclass(frozen=True)
class ConnectorCandidate:
    name: str
    capability: str
    access: AccessClass
    credential_env: str | None
    v1_priority: int
    notes: str
    cost_notes: str = "Not yet validated"
    historical_role: str = "bootstrap_or_validation"
    mandatory_for_v1: bool = False


CONNECTOR_CATALOG = (
    ConnectorCandidate(
        "ShopSavvy Data API",
        "Barcode/ASIN/URL/model lookup, multi-retailer offers, historical prices, deals, scheduled monitoring",
        AccessClass.OFFICIAL_API,
        "SHOPSAVVY_API_KEY",
        0,
        "Authorized bootstrap/current-offer candidate; keep Buy or Wait decision logic provider-independent and retain first-party history.",
        "Paid credits; cache current/history responses and measure incremental decision value per evaluation/watch refresh.",
        "authorized_bootstrap_and_current_offers",
        False,
    ),
    ConnectorCandidate(
        "Keepa",
        "Amazon product lookup, complete price history, deals, tracking",
        AccessClass.OFFICIAL_API,
        "KEEPA_API_KEY",
        10,
        "Optional Amazon-specific historical validation/backfill only; not required for V1, CI, or watch refreshes.",
        "Token-metered/quota-dependent; use only when Amazon-specific validation materially improves a decision.",
        "optional_amazon_backfill",
        False,
    ),
    ConnectorCandidate(
        "eBay Browse API",
        "Current listings, GTIN/product/category/image search",
        AccessClass.OFFICIAL_API,
        "EBAY_CLIENT_ID/EBAY_CLIENT_SECRET",
        2,
        "Use for current new/used/refurbished market offers.",
        "Evaluate request economics and partner access; persist authorized observations for reuse.",
        "current_offer_and_condition_signal",
        False,
    ),
    ConnectorCandidate(
        "Best Buy APIs",
        "Current product/pricing catalog and open-box buying options",
        AccessClass.OFFICIAL_API,
        "BESTBUY_API_KEY",
        3,
        "Useful for electronics and open-box alternatives.",
        "Catalog/current pricing and open-box calls are cached as first-party observations where terms allow.",
        "current_offer_and_open_box_signal",
        False,
    ),
    ConnectorCandidate(
        "SerpApi Google Shopping",
        "Cross-retailer current shopping results",
        AccessClass.OFFICIAL_API,
        "SERPAPI_API_KEY",
        4,
        "Paid broad-market discovery adapter.",
        "Use only when additional retailer coverage changes the decision enough to justify per-search cost.",
        "current_discovery_only",
        False,
    ),
    ConnectorCandidate(
        "Slickdeals",
        "Deal/coupon feeds, community signals, merchant/category filters",
        AccessClass.PARTNER_TOKEN,
        "SLICKDEALS_TOKEN",
        5,
        "Partner API; request token from Slickdeals.",
        "Authorized deal signal only; no scraping.",
        "deal_signal_only",
        False,
    ),
    ConnectorCandidate(
        "eBay Marketplace Insights",
        "Historical sold-item data",
        AccessClass.LIMITED_RELEASE,
        None,
        6,
        "Limited release; do not make V1 depend on access.",
    ),
    ConnectorCandidate(
        "Brad's Deals",
        "Editorial deal signal",
        AccessClass.DEFERRED,
        None,
        90,
        "No public developer API identified; pursue partnership before automation.",
    ),
    ConnectorCandidate(
        "Facebook Marketplace",
        "Local resale listings",
        AccessClass.DEFERRED,
        None,
        99,
        "No stable sanctioned public consumer-search API identified for V1.",
    ),
)
