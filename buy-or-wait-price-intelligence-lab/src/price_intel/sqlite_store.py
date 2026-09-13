"""Durable first-party price history storage.

The lab's in-memory store remains the default for isolated tests and API
fixtures.  This module is the production-shaped persistence port for the
integration lane: it uses only the standard library, preserves provenance,
keeps user captures tenant-private, and makes duplicate ingestion idempotent.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import json
import sqlite3
from threading import RLock
from typing import Iterable, Sequence

from .models import Condition, ObservationTrust, PriceObservation, ProductIdentity
from .observation_store import CanonicalPriceObservation, ObservationStore
from .statistics import percentile


class SQLitePriceHistoryStore(ObservationStore):
    """SQLite-backed observation store behind the existing ``ObservationStore`` port."""

    def __init__(self, path: str = ":memory:", *, freshness_window_days: int = 7):
        self.path = path
        self.freshness_window_days = freshness_window_days
        self._lock = RLock()
        self._connection = sqlite3.connect(path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._initialize()

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    def _initialize(self) -> None:
        with self._connection:
            self._connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    canonical_title TEXT NOT NULL,
                    brand TEXT,
                    model TEXT,
                    gtin TEXT,
                    category TEXT,
                    normalized_attributes TEXT NOT NULL,
                    identity_confidence TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS price_observations (
                    observation_id TEXT PRIMARY KEY,
                    product_id TEXT NOT NULL,
                    user_id TEXT NOT NULL DEFAULT '',
                    provider TEXT NOT NULL,
                    seller TEXT,
                    retailer TEXT,
                    seller_item_id TEXT,
                    source_url TEXT,
                    condition TEXT NOT NULL,
                    item_price TEXT NOT NULL,
                    shipping_price TEXT NOT NULL,
                    effective_total_price TEXT NOT NULL,
                    currency TEXT NOT NULL,
                    availability INTEGER NOT NULL,
                    observed_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    provenance TEXT,
                    freshness TEXT NOT NULL,
                    captured INTEGER NOT NULL,
                    trust TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    ingested_at TEXT NOT NULL,
                    UNIQUE(product_id, user_id, provider, retailer, seller_item_id,
                           source_url, condition, item_price, shipping_price, currency,
                           observed_at)
                );
                CREATE INDEX IF NOT EXISTS idx_price_observations_product_time
                    ON price_observations(product_id, user_id, observed_at DESC);
                """
            )

    def record_product(self, product_id: str, product: ProductIdentity, *, category: str | None = None,
                       created_at: datetime | None = None) -> None:
        created_at = _aware(created_at or datetime.now(timezone.utc))
        payload = json.dumps(dict(sorted(product.variant.items())), sort_keys=True)
        with self._lock, self._connection:
            self._connection.execute(
                """
                INSERT INTO products(product_id, canonical_title, brand, model, gtin,
                    category, normalized_attributes, identity_confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(product_id) DO UPDATE SET
                    canonical_title=excluded.canonical_title,
                    brand=excluded.brand,
                    model=excluded.model,
                    gtin=excluded.gtin,
                    category=COALESCE(excluded.category, products.category),
                    normalized_attributes=excluded.normalized_attributes,
                    identity_confidence=excluded.identity_confidence
                """,
                (product_id, product.title, product.brand, product.model, product.gtin,
                 category, payload, str(product.identity_confidence), created_at.isoformat()),
            )

    def append(self, product_id: str, product: ProductIdentity,
               observations: Iterable[PriceObservation], *, ingested_at: datetime | None = None,
               user_id: str | None = None) -> Sequence[CanonicalPriceObservation]:
        ingested_at = _aware(ingested_at or datetime.now(timezone.utc))
        self.record_product(product_id, product, created_at=ingested_at)
        stored: list[CanonicalPriceObservation] = []
        for observation in observations:
            normalized = _with_freshness(observation, ingested_at, self.freshness_window_days)
            if normalized.trust == ObservationTrust.QUARANTINED:
                continue
            if normalized.trust == ObservationTrust.USER_PRIVATE and not user_id:
                continue
            owner = user_id if normalized.trust == ObservationTrust.USER_PRIVATE else ""
            observation_id = _observation_id(product_id, owner, normalized)
            metadata = dict(normalized.metadata)
            seller_item_id = metadata.get("seller_item_id")
            row = (
                observation_id, product_id, owner, normalized.provider, normalized.seller,
                normalized.retailer, seller_item_id, normalized.source_url,
                normalized.condition.value, str(normalized.price), str(normalized.shipping),
                str(normalized.landed_price), normalized.currency, int(normalized.available),
                _aware(normalized.observed_at).isoformat(), normalized.provider,
                str(normalized.product_match_confidence), normalized.provenance,
                normalized.freshness, int(normalized.captured), normalized.trust.value,
                json.dumps(metadata, sort_keys=True), ingested_at.isoformat(),
            )
            with self._lock, self._connection:
                self._connection.execute(
                    """
                    INSERT OR IGNORE INTO price_observations(
                        observation_id, product_id, user_id, provider, seller, retailer,
                        seller_item_id, source_url, condition, item_price, shipping_price,
                        effective_total_price, currency, availability, observed_at, source,
                        confidence, provenance, freshness, captured, trust, metadata_json,
                        ingested_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row,
                )
            record = self._get_by_id(observation_id)
            if record is not None:
                stored.append(record)
        return tuple(stored)

    def record_observation(self, product_id: str, product: ProductIdentity,
                           observation: PriceObservation, *, user_id: str | None = None,
                           ingested_at: datetime | None = None) -> CanonicalPriceObservation | None:
        return next(iter(self.append(product_id, product, (observation,), user_id=user_id,
                                     ingested_at=ingested_at)), None)

    def list(self, product_id: str, *, user_id: str | None = None) -> Sequence[CanonicalPriceObservation]:
        owners = [""] + ([user_id] if user_id else [])
        placeholders = ",".join("?" for _ in owners)
        with self._lock:
            rows = self._connection.execute(
                f"SELECT * FROM price_observations WHERE product_id = ? AND user_id IN ({placeholders}) "
                "ORDER BY observed_at, observation_id",
                (product_id, *owners),
            ).fetchall()
        return tuple(self._record_from_row(row) for row in rows)

    def observations(self, product_id: str, *, user_id: str | None = None) -> tuple[PriceObservation, ...]:
        return tuple(row.observation for row in self.list(product_id, user_id=user_id))

    def get_history(self, product_id: str, *, user_id: str | None = None,
                    condition: Condition | None = None) -> tuple[CanonicalPriceObservation, ...]:
        records = self.list(product_id, user_id=user_id)
        if condition is None:
            return tuple(records)
        return tuple(row for row in records if row.observation.condition == condition)

    def get_recent_observations(self, product_id: str, *, days: int = 30,
                                user_id: str | None = None,
                                now: datetime | None = None) -> tuple[CanonicalPriceObservation, ...]:
        now = _aware(now or datetime.now(timezone.utc))
        cutoff = now - timedelta(days=days)
        return tuple(row for row in self.list(product_id, user_id=user_id)
                     if cutoff <= _aware(row.observation.observed_at) <= now)

    def get_statistics(self, product_id: str, *, user_id: str | None = None,
                       condition: Condition = Condition.NEW) -> dict[str, object]:
        values = [row.landed_price for row in self.get_history(product_id, user_id=user_id, condition=condition)
                  if row.observation.available and row.observation.freshness != "invalid"]
        if not values:
            return {"status": "INSUFFICIENT", "count": 0, "low": None, "high": None,
                    "average": None, "median": None, "currency": None}
        return {
            "status": "SUFFICIENT" if len(values) >= 10 else "INSUFFICIENT",
            "count": len(values), "low": str(min(values)), "high": str(max(values)),
            "average": str(sum(values, Decimal("0")) / Decimal(len(values))),
            "median": str(percentile(values, Decimal("0.5"))),
            "currency": self.get_history(product_id, user_id=user_id, condition=condition)[0].observation.currency,
        }

    def get_low(self, product_id: str, **kwargs: object) -> Decimal | None:
        value = self.get_statistics(product_id, **kwargs).get("low")
        return Decimal(value) if value is not None else None

    def get_high(self, product_id: str, **kwargs: object) -> Decimal | None:
        value = self.get_statistics(product_id, **kwargs).get("high")
        return Decimal(value) if value is not None else None

    def get_average(self, product_id: str, **kwargs: object) -> Decimal | None:
        value = self.get_statistics(product_id, **kwargs).get("average")
        return Decimal(value) if value is not None else None

    def get_price_signal(self, product_id: str, *, current_price: Decimal | None = None,
                         user_id: str | None = None, condition: Condition = Condition.NEW) -> str:
        stats = self.get_statistics(product_id, user_id=user_id, condition=condition)
        if stats["status"] != "SUFFICIENT" or current_price is None:
            return "UNKNOWN"
        target = Decimal(str(stats["median"]))
        low = Decimal(str(stats["low"]))
        if current_price <= low * Decimal("1.03"):
            return "STRONG_BUY"
        if current_price <= target * Decimal("0.90"):
            return "BUY"
        if current_price >= target * Decimal("1.10"):
            return "STRONG_WAIT"
        if current_price > target:
            return "WAIT"
        return "NEUTRAL"

    def _get_by_id(self, observation_id: str) -> CanonicalPriceObservation | None:
        with self._lock:
            row = self._connection.execute(
                "SELECT * FROM price_observations WHERE observation_id = ?", (observation_id,)
            ).fetchone()
        return self._record_from_row(row) if row else None

    def _record_from_row(self, row: sqlite3.Row) -> CanonicalPriceObservation:
        product = self._product_from_row(row["product_id"])
        observation = PriceObservation(
            provider=row["provider"], observed_at=datetime.fromisoformat(row["observed_at"]),
            price=Decimal(row["item_price"]), shipping=Decimal(row["shipping_price"]),
            condition=Condition(row["condition"]), available=bool(row["availability"]),
            seller=row["seller"], retailer=row["retailer"], source_url=row["source_url"],
            product_match_confidence=Decimal(row["confidence"]), currency=row["currency"],
            captured=bool(row["captured"]), provenance=row["provenance"],
            freshness=row["freshness"], trust=ObservationTrust(row["trust"]),
            metadata=json.loads(row["metadata_json"]),
        )
        return CanonicalPriceObservation(row["product_id"], product, observation,
                                         datetime.fromisoformat(row["ingested_at"]))

    def _product_from_row(self, product_id: str) -> ProductIdentity:
        with self._lock:
            row = self._connection.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
        if row is None:
            raise KeyError(f"unknown product_id: {product_id}")
        return ProductIdentity(title=row["canonical_title"], brand=row["brand"], model=row["model"],
                               gtin=row["gtin"], variant=json.loads(row["normalized_attributes"]),
                               identity_confidence=Decimal(row["identity_confidence"]),
                               source_provenance="sqlite_first_party")


def _observation_id(product_id: str, user_id: str, observation: PriceObservation) -> str:
    payload = {
        "product_id": product_id, "user_id": user_id, "provider": observation.provider,
        "retailer": observation.retailer, "seller_item_id": observation.metadata.get("seller_item_id"),
        "source_url": observation.source_url, "condition": observation.condition.value,
        "item_price": str(observation.price), "shipping_price": str(observation.shipping),
        "currency": observation.currency, "observed_at": _aware(observation.observed_at).isoformat(),
    }
    return "obs_" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:24]


def _with_freshness(observation: PriceObservation, ingested_at: datetime, window: int) -> PriceObservation:
    if observation.freshness != "unknown":
        return observation
    age = max(0, (_aware(ingested_at) - _aware(observation.observed_at)).days)
    return PriceObservation(provider=observation.provider, observed_at=observation.observed_at,
        price=observation.price, shipping=observation.shipping, condition=observation.condition,
        available=observation.available, seller=observation.seller, retailer=observation.retailer,
        source_url=observation.source_url, product_match_confidence=observation.product_match_confidence,
        deal_signal=observation.deal_signal, metadata=observation.metadata, currency=observation.currency,
        captured=observation.captured, provenance=observation.provenance,
        freshness="fresh" if age <= window else "stale", trust=observation.trust)


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamps must include a timezone")
    return value
