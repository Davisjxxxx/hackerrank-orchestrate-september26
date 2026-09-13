from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol


@dataclass(frozen=True)
class AuthenticatedSubject:
    subject_id: str
    auth_method: str


class AuthenticationError(ValueError):
    pass


class Authenticator(Protocol):
    def authenticate(self, headers: Mapping[str, str], *, required: bool = True) -> AuthenticatedSubject | None: ...


class FixtureAuthenticator:
    """Local-test authentication seam.

    The bearer form is the canonical seam: ``Authorization: Bearer
    fixture:<subject>``. The legacy X-User-Id fallback is retained only for
    the supplied lab tests and is explicitly not a production identity
    mechanism.
    """

    def __init__(self, *, allow_legacy_header: bool = True):
        self.allow_legacy_header = allow_legacy_header

    def authenticate(self, headers: Mapping[str, str], *, required: bool = True) -> AuthenticatedSubject | None:
        authorization = headers.get("authorization") or headers.get("Authorization")
        if authorization:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() != "bearer" or not token.startswith("fixture:"):
                raise AuthenticationError("invalid fixture bearer credential")
            subject = token.removeprefix("fixture:").strip()
            if not _valid_subject(subject):
                raise AuthenticationError("invalid authenticated subject")
            return AuthenticatedSubject(subject, "fixture_bearer")
        if self.allow_legacy_header:
            legacy = headers.get("x-user-id") or headers.get("X-User-Id")
            if legacy and _valid_subject(legacy):
                return AuthenticatedSubject(legacy, "legacy_fixture_header")
        if required:
            raise AuthenticationError("authentication required")
        return None


def _valid_subject(value: str) -> bool:
    return bool(value) and len(value) <= 128 and all(char.isalnum() or char in "._:-" for char in value)
