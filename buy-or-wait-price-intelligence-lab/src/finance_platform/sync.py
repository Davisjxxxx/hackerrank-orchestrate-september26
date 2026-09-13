from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .connectors.base import ConnectorSyncResult
from .db import ConnectorSyncRun, SourceConnection


def record_sync(session: Session, connection: SourceConnection, result: ConnectorSyncResult, *, error: str | None = None) -> ConnectorSyncRun:
    """Persist bounded sync diagnostics without logging provider payloads."""
    row = ConnectorSyncRun(connection_id=connection.id, started_at=datetime.now(timezone.utc), completed_at=datetime.now(timezone.utc), status="failed" if error else "completed", fetched=result.fetched, inserted=result.inserted, updated=result.updated, duplicates=result.duplicates, review_required=result.review_required, cursor=result.cursor, error_summary=error[:500] if error else None)
    session.add(row); session.commit(); session.refresh(row)
    return row
