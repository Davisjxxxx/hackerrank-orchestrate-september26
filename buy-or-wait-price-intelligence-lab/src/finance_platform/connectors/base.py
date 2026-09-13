from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Protocol


@dataclass(frozen=True)
class ConnectorHealth:
    provider: str
    status: str
    last_successful_sync: datetime | None = None
    detail: str | None = None


@dataclass(frozen=True)
class ConnectorSyncResult:
    provider: str
    fetched: int = 0
    inserted: int = 0
    updated: int = 0
    duplicates: int = 0
    review_required: int = 0
    cursor: str | None = None
    errors: tuple[str, ...] = ()
    records: tuple[dict[str, Any], ...] = ()


class FinancialConnector(Protocol):
    async def connect(self, **kwargs: Any) -> dict[str, Any]: ...
    async def disconnect(self, **kwargs: Any) -> None: ...
    async def sync(self, **kwargs: Any) -> ConnectorSyncResult: ...
    async def refresh(self, **kwargs: Any) -> ConnectorSyncResult: ...
    async def health(self, **kwargs: Any) -> ConnectorHealth: ...
