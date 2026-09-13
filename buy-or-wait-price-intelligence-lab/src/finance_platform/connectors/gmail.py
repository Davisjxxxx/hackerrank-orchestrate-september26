from __future__ import annotations

from typing import Any

from .base import ConnectorHealth, ConnectorSyncResult
from ..settings import settings


class GmailConnector:
    provider = "gmail"
    scopes = ("https://www.googleapis.com/auth/gmail.readonly",)

    async def connect(self, **_: Any) -> dict[str, Any]:
        if not settings.gmail_client_id or not settings.gmail_client_secret:
            raise RuntimeError("Gmail OAuth is not configured; set GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET")
        return {"status": "oauth_ready", "scopes": list(self.scopes)}

    async def disconnect(self, **_: Any) -> None:
        return None

    async def sync(self, **_: Any) -> ConnectorSyncResult:
        if not settings.gmail_client_id:
            raise RuntimeError("Gmail OAuth credentials are required")
        # Provider transport is isolated here; message classification is a
        # separate untrusted-evidence pipeline and never executes message text.
        return ConnectorSyncResult(provider=self.provider)

    async def refresh(self, **kwargs: Any) -> ConnectorSyncResult:
        return await self.sync(**kwargs)

    async def health(self, **_: Any) -> ConnectorHealth:
        return ConnectorHealth(self.provider, "configured" if settings.gmail_client_id and settings.gmail_client_secret else "unconfigured", detail="readonly OAuth")
