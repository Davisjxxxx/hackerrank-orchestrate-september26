from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("FINANCE_DATABASE_URL", "sqlite:///./buy_or_wait_real_world.db")
    environment: str = os.getenv("ENVIRONMENT", "development")
    document_root: Path = Path(os.getenv("FINANCE_DOCUMENT_ROOT", "./var/documents"))
    max_upload_bytes: int = int(os.getenv("FINANCE_MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
    plaid_client_id: str | None = os.getenv("PLAID_CLIENT_ID")
    plaid_secret: str | None = os.getenv("PLAID_SECRET")
    plaid_env: str = os.getenv("PLAID_ENV", "sandbox")
    gmail_client_id: str | None = os.getenv("GMAIL_CLIENT_ID")
    gmail_client_secret: str | None = os.getenv("GMAIL_CLIENT_SECRET")
    token_encryption_key: str | None = os.getenv("FINANCE_TOKEN_ENCRYPTION_KEY")
    fx_base_url: str = os.getenv("FX_BASE_URL", "https://api.frankfurter.app")


settings = Settings()
