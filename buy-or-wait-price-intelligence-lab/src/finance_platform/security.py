from __future__ import annotations

from cryptography.fernet import Fernet


class TokenCipher:
    """Encrypts provider tokens before persistence; no plaintext fallback."""
    def __init__(self, key: str | bytes):
        self._fernet = Fernet(key.encode() if isinstance(key, str) else key)

    def encrypt(self, token: str) -> str: return self._fernet.encrypt(token.encode()).decode()
    def decrypt(self, token: str) -> str: return self._fernet.decrypt(token.encode()).decode()
