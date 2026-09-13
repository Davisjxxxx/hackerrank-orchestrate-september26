from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import csv
import hashlib
import io
import re
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import FinancialEvent, RawIngestionRecord, SourceAccount, SourceConnection, User, new_id
from .schemas import EventInput
from .connectors.base import ConnectorSyncResult
from .sync import record_sync


def _date(value: str) -> date:
    text = value.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unsupported transaction date: {text}")


def _money(value: str) -> Decimal:
    cleaned = value.replace(",", "").replace("$", "").strip()
    return Decimal(cleaned or "0")


def _header(row: dict[str, Any], *names: str) -> str | None:
    normalized = {re.sub(r"[^a-z0-9]", "", str(key).lower()): value for key, value in row.items()}
    for name in names:
        value = normalized.get(re.sub(r"[^a-z0-9]", "", name.lower()))
        if value not in (None, ""):
            return str(value)
    return None


def parse_transaction_file(filename: str, content: bytes) -> list[EventInput]:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if suffix in {"csv", "txt"} or content.lstrip().startswith(b"date,"):
        return _parse_csv(content)
    if suffix in {"ofx", "qfx"} or b"<OFX" in content[:1000] or b"<STMTTRN" in content[:3000]:
        return _parse_ofx(content)
    raise ValueError("supported transaction formats are CSV, OFX, and QFX")


def _parse_csv(content: bytes) -> list[EventInput]:
    text = content.decode("utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(text[:4096])
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError("CSV header is required")
    result: list[EventInput] = []
    for index, row in enumerate(reader, 1):
        raw_date = _header(row, "date", "posted date", "posted", "transaction date")
        if not raw_date:
            raise ValueError(f"row {index}: date column is required")
        debit = _header(row, "debit", "withdrawal", "charge")
        credit = _header(row, "credit", "deposit")
        amount_text = _header(row, "amount", "value")
        if debit is not None or credit is not None:
            debit_amount = _money(debit or "0")
            credit_amount = _money(credit or "0")
            if debit_amount and credit_amount:
                raise ValueError(f"row {index}: debit and credit cannot both be non-zero")
            amount = debit_amount or credit_amount
            direction = "debit" if debit_amount else "credit"
        elif amount_text is not None:
            signed = _money(amount_text)
            if not signed:
                continue
            direction = "credit" if signed > 0 else "debit"
            amount = abs(signed)
        else:
            raise ValueError(f"row {index}: amount or debit/credit columns are required")
        description = _header(row, "description", "memo", "details", "merchant") or "Imported transaction"
        status = (_header(row, "status") or "settled").lower()
        if status not in {"settled", "pending", "scheduled", "failed", "cancelled", "unrealized"}:
            status = "settled"
        result.append(EventInput(
            event_type="income" if direction == "credit" else "expense", direction=direction,
            amount=amount, currency=(_header(row, "currency", "ccy") or "USD"), transaction_date=_date(raw_date),
            settlement_date=_date(_header(row, "settlement date", "cleared date") or raw_date), status=status,
            merchant=_header(row, "merchant", "payee"), description=description,
            category=_header(row, "category"), external_id=_header(row, "id", "transaction id", "fitid") or f"row-{index}",
        ))
    return result


def _parse_ofx(content: bytes) -> list[EventInput]:
    text = content.decode("utf-8", errors="replace")
    blocks = re.findall(r"<STMTTRN>(.*?)(?:</STMTTRN>|(?=<STMTTRN>))", text, flags=re.I | re.S)
    result: list[EventInput] = []
    for index, block in enumerate(blocks, 1):
        def tag(name: str) -> str | None:
            match = re.search(rf"<{name}>([^<\r\n]+)", block, flags=re.I)
            return match.group(1).strip() if match else None
        amount_text = tag("TRNAMT")
        date_text = (tag("DTPOSTED") or "")[:8]
        if not amount_text or len(date_text) != 8:
            continue
        signed = Decimal(amount_text)
        if not signed:
            continue
        result.append(EventInput(
            event_type="income" if signed > 0 else "expense", direction="credit" if signed > 0 else "debit",
            amount=abs(signed), currency="USD", transaction_date=datetime.strptime(date_text, "%Y%m%d").date(),
            settlement_date=datetime.strptime(date_text, "%Y%m%d").date(), status="settled",
            description=tag("NAME") or tag("MEMO") or "OFX transaction", external_id=tag("FITID") or f"ofx-{index}",
        ))
    return result


class TransactionImportService:
    def preview(self, filename: str, content: bytes) -> list[EventInput]:
        return parse_transaction_file(filename, content)

    def commit(self, session: Session, *, user_id: str, filename: str, content: bytes, events: list[EventInput]) -> dict[str, int | str]:
        user = session.get(User, user_id)
        if user is None:
            raise ValueError("user not found")
        connection = session.scalar(select(SourceConnection).where(SourceConnection.user_id == user_id, SourceConnection.provider == "file_import"))
        if connection is None:
            connection = SourceConnection(user_id=user_id, provider="file_import", status="connected")
            session.add(connection); session.flush()
        account = session.scalar(select(SourceAccount).where(SourceAccount.user_id == user_id, SourceAccount.connection_id == connection.id))
        if account is None:
            account = SourceAccount(connection_id=connection.id, user_id=user_id, external_id="file-default", name="Imported account", currency=events[0].currency if events else "USD")
            session.add(account); session.flush()
        inserted = duplicates = 0
        for event in events:
            payload = event.model_dump(mode="json")
            raw = json_bytes(payload)
            digest = hashlib.sha256(raw).hexdigest()
            exists = session.scalar(select(RawIngestionRecord).where(RawIngestionRecord.provider == "file_import", RawIngestionRecord.connection_id == connection.id, RawIngestionRecord.external_id == (event.external_id or ""), RawIngestionRecord.payload_hash == digest))
            if exists:
                duplicates += 1; continue
            session.add(RawIngestionRecord(user_id=user_id, provider="file_import", connection_id=connection.id, external_id=event.external_id or new_id("row"), payload_hash=digest, provider_timestamp=datetime.now(timezone.utc), raw_payload=payload))
            existing_event = None
            if event.external_id:
                existing_event = session.scalar(select(FinancialEvent).where(FinancialEvent.user_id == user_id, FinancialEvent.external_id == event.external_id))
            if existing_event is not None:
                # Provider lifecycle updates replace canonical state while the
                # original raw payload remains immutable evidence.
                existing_event.status = event.status
                existing_event.amount = event.amount
                existing_event.settlement_date = event.settlement_date
                existing_event.authorized_date = event.authorized_date
                existing_event.provider_metadata = {**(existing_event.provider_metadata or {}), **event.provider_metadata}
            else:
                session.add(FinancialEvent(user_id=user_id, account_id=account.id, source="file_import", external_id=event.external_id, event_type=event.event_type, direction=event.direction, amount=event.amount, currency=event.currency, transaction_date=event.transaction_date, authorized_date=event.authorized_date, settlement_date=event.settlement_date, status=event.status, merchant=event.merchant, description=event.description, category=event.category, pending_transaction_id=event.pending_transaction_id, linked_event_id=event.linked_event_id, confidence=event.confidence, recurrence_eligible=event.recurrence_eligible, flexibility=event.flexibility, minimum_allowed_amount=event.minimum_allowed_amount, provider_metadata=event.provider_metadata))
                inserted += 1
        session.commit()
        record_sync(session, connection, ConnectorSyncResult(provider="file_import", fetched=len(events), inserted=inserted, duplicates=duplicates))
        return {"provider": "file_import", "inserted": inserted, "duplicates": duplicates, "rows": len(events)}


def json_bytes(value: Any) -> bytes:
    import json
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def normalize_plaid_transaction(record: dict[str, Any]) -> EventInput:
    """Map a Plaid transaction into the provider-neutral event contract."""
    amount = Decimal(str(record.get("amount", "0")))
    if not amount or not amount.is_finite(): raise ValueError("Plaid transaction amount is invalid")
    direction = "debit" if amount > 0 else "credit"
    tx_date = _date(str(record.get("date") or record.get("authorized_date")))
    pending = bool(record.get("pending"))
    return EventInput(event_type="expense" if direction == "debit" else "income", direction=direction, amount=abs(amount), currency=str(record.get("iso_currency_code") or "USD"), transaction_date=tx_date, authorized_date=_date(str(record["authorized_date"])) if record.get("authorized_date") else None, settlement_date=None if pending else tx_date, status="pending" if pending else "settled", merchant=record.get("merchant_name"), description=record.get("name") or record.get("merchant_name") or "Plaid transaction", category=(record.get("personal_finance_category") or {}).get("primary") if isinstance(record.get("personal_finance_category"), dict) else None, external_id=record.get("transaction_id"), pending_transaction_id=record.get("pending_transaction_id"), provider_metadata={"provider": "plaid", "account_id": record.get("account_id")})
