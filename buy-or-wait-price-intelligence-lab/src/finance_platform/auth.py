from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
from typing import Protocol

import jwt


class AuthenticationError(ValueError):
    pass


@dataclass(frozen=True)
class CurrentUser:
    user_id: str
    method: str


class CurrentUserProvider(Protocol):
    def authenticate(self, *, authorization: str | None, legacy_user_id: str | None = None) -> CurrentUser: ...


def _valid_user(value: str) -> bool:
    return bool(value) and len(value) <= 80 and all(c.isalnum() or c in "._:-" for c in value)


class DevelopmentUserProvider:
    def authenticate(self, *, authorization: str | None, legacy_user_id: str | None = None) -> CurrentUser:
        if authorization and authorization.lower().startswith("bearer user:"):
            value = authorization.split(":", 1)[1].strip()
            if _valid_user(value): return CurrentUser(value, "development_bearer")
        if legacy_user_id and _valid_user(legacy_user_id):
            return CurrentUser(legacy_user_id, "development_header")
        raise AuthenticationError("development user identity required")


class OIDCJWTUserProvider:
    """Production auth seam using a configured JWT public key and claims."""
    def __init__(self, public_key: str, *, issuer: str | None = None, audience: str | None = None):
        self.public_key, self.issuer, self.audience = public_key, issuer, audience

    def authenticate(self, *, authorization: str | None, legacy_user_id: str | None = None) -> CurrentUser:
        if not authorization or not authorization.lower().startswith("bearer "):
            raise AuthenticationError("Bearer JWT required")
        token = authorization.split(" ", 1)[1]
        options = {"algorithms": ["RS256", "ES256"]}
        kwargs = {"issuer": self.issuer} if self.issuer else {}
        if self.audience: kwargs["audience"] = self.audience
        try: claims = jwt.decode(token, self.public_key, **options, **kwargs)
        except jwt.PyJWTError as exc: raise AuthenticationError("invalid authentication token") from exc
        user_id = str(claims.get("sub") or claims.get("user_id") or "")
        if not _valid_user(user_id): raise AuthenticationError("token has no valid subject")
        return CurrentUser(user_id, "oidc_jwt")


def build_user_provider(environment: str) -> CurrentUserProvider:
    if environment in {"production", "staging"}:
        key = os.getenv("FINANCE_JWT_PUBLIC_KEY")
        if not key: raise RuntimeError("FINANCE_JWT_PUBLIC_KEY is required outside development")
        return OIDCJWTUserProvider(key, issuer=os.getenv("FINANCE_JWT_ISSUER"), audience=os.getenv("FINANCE_JWT_AUDIENCE"))
    return DevelopmentUserProvider()
