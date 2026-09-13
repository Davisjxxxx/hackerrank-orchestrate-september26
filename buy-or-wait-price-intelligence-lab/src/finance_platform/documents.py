from __future__ import annotations

from pathlib import Path
import hashlib
import mimetypes
import re

from sqlalchemy.orm import Session

from .db import EvidenceDocument, User, new_id
from .settings import settings

ALLOWED_TYPES = {"application/pdf", "image/png", "image/jpeg"}
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def _safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name)[:180] or "upload"


class DocumentExtractor:
    def extract(self, content_type: str, path: Path) -> tuple[str | None, str]:
        if content_type == "application/pdf":
            try:
                import fitz
                text = "\n".join(page.get_text() for page in fitz.open(path))
                return text, "high" if text.strip() else "low"
            except Exception:
                return None, "low"
        return None, "low"


class DocumentService:
    def __init__(self, extractor: DocumentExtractor | None = None): self.extractor = extractor or DocumentExtractor()

    def store(self, session: Session, *, user_id: str, filename: str, content_type: str | None, content: bytes) -> EvidenceDocument:
        if session.get(User, user_id) is None: raise ValueError("user not found")
        if len(content) > settings.max_upload_bytes: raise ValueError("document exceeds configured size limit")
        ext = Path(filename).suffix.lower().lstrip(".")
        detected = content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
        if detected not in ALLOWED_TYPES or ext not in ALLOWED_EXTENSIONS: raise ValueError("only PDF, PNG, and JPEG documents are accepted")
        digest = hashlib.sha256(content).hexdigest()
        directory = settings.document_root / user_id
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{digest}-{_safe_name(filename)}"
        path.write_bytes(content)
        extracted, confidence = self.extractor.extract(detected, path)
        row = EvidenceDocument(user_id=user_id, filename=_safe_name(filename), content_type=detected, sha256=digest, storage_ref=str(path), extracted_text=extracted, extraction_confidence=confidence, status="ready" if confidence == "high" else "needs_review")
        session.add(row); session.commit(); session.refresh(row)
        return row
