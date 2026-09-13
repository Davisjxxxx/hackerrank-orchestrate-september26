from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from .base import ConnectorHealth, ConnectorSyncResult
from ..settings import settings


class PlaidConnector:
    """Read-only Plaid Transactions/Accounts/Balance adapter.

    Tokens are accepted only by the service boundary and are never returned to
    callers. The production repository stores only an encrypted token.
    """
    provider = "plaid"

    def __init__(self, *, client_id: str | None = None, secret: str | None = None, environment: str | None = None):
        self.client_id = client_id or settings.plaid_client_id
        self.secret = secret or settings.plaid_secret
        self.environment = environment or settings.plaid_env
        self.base_url = {"sandbox": "https://sandbox.plaid.com", "production": "https://production.plaid.com", "development": "https://development.plaid.com"}.get(self.environment, "https://sandbox.plaid.com")

    def _require_config(self) -> None:
        if not self.client_id or not self.secret:
            raise RuntimeError("Plaid is not configured; set PLAID_CLIENT_ID and PLAID_SECRET")

    async def connect(self, *, products: list[str] | None = None, country_codes: list[str] | None = None, language: str = "en", **_: Any) -> dict[str, Any]:
        self._require_config()
        payload = {"client_id": self.client_id, "secret": self.secret, "user": {"client_user_id": "server-user"}, "client_name": "Buy or Wait", "products": products or ["transactions"], "country_codes": country_codes or ["US"], "language": language}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(f"{self.base_url}/link/token/create", json=payload)
            response.raise_for_status()
            return {"link_token": response.json().get("link_token"), "environment": self.environment}

    async def exchange_public_token(self, public_token: str) -> dict[str, Any]:
        self._require_config()
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(f"{self.base_url}/item/public_token/exchange", json={"client_id": self.client_id, "secret": self.secret, "public_token": public_token})
            response.raise_for_status()
            data = response.json()
            return {"access_token": data.get("access_token"), "item_id": data.get("item_id")}

    async def sync(self, *, access_token: str, cursor: str | None = None, **_: Any) -> ConnectorSyncResult:
        self._require_config()
        payload = {"client_id": self.client_id, "secret": self.secret, "access_token": access_token, "cursor": cursor}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.base_url}/transactions/sync", json={k: v for k, v in payload.items() if v is not None})
            response.raise_for_status()
            data = response.json()
        added = tuple(data.get("added", ()))
        modified = tuple(data.get("modified", ()))
        return ConnectorSyncResult(provider=self.provider, fetched=len(added) + len(modified), updated=len(modified), cursor=data.get("next_cursor"), records=added + modified)

    async def refresh(self, **kwargs: Any) -> ConnectorSyncResult:
        return await self.sync(**kwargs)

    async def disconnect(self, **_: Any) -> None:
        return None

    async def health(self, **_: Any) -> ConnectorHealth:
        configured = bool(self.client_id and self.secret)
        return ConnectorHealth(self.provider, "configured" if configured else "unconfigured", detail=self.environment)
