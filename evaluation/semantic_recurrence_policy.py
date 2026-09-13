"""Bounded local-model semantic recurrence experiment.

This module is evaluation-only.  It never imports solved outputs into the model
prompt and it never changes ``code/main.py``.  The model proposes stream
membership; the verifier and materializer decide what can enter the cash
ledger.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from collections import defaultdict
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

import ollama

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


MODEL = os.environ.get("SEMANTIC_MODEL", "qwen3-vl:2b-instruct-q8_0")
PROMPT_VERSION = "semantic-recurrence-v1"
CACHE_DIR = Path(os.environ.get("SEMANTIC_CACHE_DIR", "/tmp/buy_or_wait_semantic_cache"))

SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "streams": {
            "type": "array", "maxItems": 10,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "stream_id": {"type": "string"},
                    "member_event_ids": {"type": "array", "maxItems": 12, "items": {"type": "string"}},
                    "direction": {"type": "string", "enum": ["credit", "debit"]},
                    "event_type": {"type": "string"},
                    "category": {"type": "string"},
                    "is_recurring": {"type": "boolean"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                    "cadence": {
                        "type": "object", "additionalProperties": False,
                        "properties": {
                            "type": {"type": "string", "enum": ["monthly", "weekly", "biweekly", "fixed_days", "none", "unknown"]},
                            "interval_days": {"type": ["integer", "null"]},
                            "calendar_rule": {"type": ["string", "null"]},
                        },
                        "required": ["type", "interval_days", "calendar_rule"],
                    },
                    "projection_amount": {
                        "type": "object", "additionalProperties": False,
                        "properties": {
                            "amount": {"type": ["number", "null"]},
                            "currency": {"type": "string"},
                            "basis": {"type": "string", "enum": ["latest_authoritative", "stable_amount", "conservative_variable", "message_amendment", "other"]},
                        },
                        "required": ["amount", "currency", "basis"],
                    },
                    "next_expected_date": {"type": ["string", "null"]},
                    "termination_evidence": {"type": ["string", "null"]},
                    "reason_codes": {"type": "array", "maxItems": 2, "items": {"type": "string"}},
                    "evidence_event_ids": {"type": "array", "maxItems": 12, "items": {"type": "string"}},
                },
                "required": ["stream_id", "member_event_ids", "direction", "event_type", "category", "is_recurring", "confidence", "cadence", "projection_amount", "next_expected_date", "termination_evidence", "reason_codes", "evidence_event_ids"],
            },
        },
    },
    "required": ["streams"],
}

SYSTEM_PROMPT = """You are a financial-event recurrence evidence interpreter. Return only the requested JSON.
You classify supplied participant-visible facts; you do not make affordability decisions or perform financial arithmetic.
Use event IDs as evidence references. A stream is recurring only when repeated chronological evidence or explicit future/message evidence supports it.
Do not invent merchants, sources, cadence, amounts, future income, or future expenses. Pending credits are not usable income. Failed, cancelled, unrealized, and non-cash records are not recurring cash flows.
Use linked and message evidence only when the supplied records support it. Terminal evidence ends a stream. When uncertain, use low confidence or omit the stream.
Description is supporting evidence only, never an absolute identity key. Preserve independent cadence phases. For variable debits, use conservative_variable only when repeated debit evidence supports it. For credits, do not create unsupported income.
Return only recurring streams, not one-time events. Group rotating descriptions when the dates and amounts form one supported cadence. Keep the response bounded to at most 10 streams. For each stream return only the most recent 12 supporting member IDs and concise reason codes.
Return every field required by the JSON schema. The answer must contain no prose outside JSON."""


def _compact_event(e: main.CanonicalEvent, image_ids: set[str], linked_by_id: dict[str, str]) -> dict[str, Any]:
    d = e.event_date.isoformat()
    sd = (e.settlement_date or e.event_date).isoformat()
    return {
        "id": e.event_id, "d": d, "sd": sd, "t": e.event_type,
        "cat": e.category, "desc": e.description[:80], "dir": e.direction,
        "amt": None if e.amount is None else str(e.amount), "cur": e.currency,
        "st": e.status, "flex": e.flexibility, "min": None if e.minimum_allowed_amount is None else str(e.minimum_allowed_amount),
        "link": linked_by_id.get(e.event_id),
        "image": e.event_id in image_ids,
    }


def build_packet(user_id: str, events: list[main.CanonicalEvent], messages: list[dict[str, str]], images: list[dict[str, str]], linked_by_id: dict[str, str] | None = None) -> dict[str, Any]:
    """Build a packet with no request IDs, sample labels, or solved fields."""
    image_ids = {r.get("related_event_id", "") for r in images if r.get("related_event_id")}
    rows = sorted((e for e in events if e.user_id == user_id and e.direction != "non_cash" and e.status not in {"failed", "cancelled", "unrealized"}), key=lambda e: (e.event_date, e.event_id))
    msg = []
    for m in messages:
        if m.get("user_id") != user_id:
            continue
        text = m.get("message_text", "")
        if m.get("related_event_id") or any(x in text.lower() for x in ("salary", "payroll", "gaji", "rent", "insurance", "subscription")):
            msg.append({"id": m.get("message_id", ""), "sent": m.get("sent_at", "")[:10], "related": m.get("related_event_id") or None, "source": m.get("source_type", ""), "text": text[:240]})
    return {"events": [_compact_event(e, image_ids, linked_by_id or {}) for e in rows], "messages": sorted(msg, key=lambda x: (x["sent"], x["id"]))}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def cache_key(packet: dict[str, Any]) -> str:
    raw = canonical_json({"model": MODEL, "prompt_version": PROMPT_VERSION, "system": SYSTEM_PROMPT, "packet": packet})
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _clean_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.S).strip()
    obj = json.loads(text)
    if not isinstance(obj, dict) or not isinstance(obj.get("streams"), list):
        raise ValueError("model response is not a stream object")
    return obj


def resolve_packet(packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, int | str | bool]]:
    """Resolve one packet using the local model or an exact cache hit."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = cache_key(packet)
    path = CACHE_DIR / f"{key}.json"
    if path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        obj = _clean_json(json.dumps(cached.get("response", cached), sort_keys=True))
        return obj, {"cached": True, "calls": 0, "input_tokens": 0, "output_tokens": 0, "model": MODEL}
    user_prompt = "Classify recurrence streams in this evidence packet. Do not infer beyond the packet.\nEVIDENCE_PACKET_JSON\n" + canonical_json(packet)
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}],
        format=SCHEMA,
        options={"temperature": 0, "seed": 0, "num_ctx": 12288, "num_predict": 4096},
        keep_alive="10m",
    )
    obj = _clean_json(response.message.content)
    # Store only model output and metadata, never expected sample labels.
    path.write_text(json.dumps({"key": key, "model": MODEL, "prompt_version": PROMPT_VERSION, "response": obj, "usage": {"input_tokens": response.prompt_eval_count or 0, "output_tokens": response.eval_count or 0}}, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return obj, {"cached": False, "calls": 1, "input_tokens": response.prompt_eval_count or 0, "output_tokens": response.eval_count or 0, "model": response.model or MODEL}


def _amount(v: Any) -> Decimal | None:
    if v is None or isinstance(v, bool):
        return None
    try:
        return Decimal(str(v))
    except Exception:
        return None


def verify_streams(obj: dict[str, Any], events: list[main.CanonicalEvent], user_id: str) -> tuple[list[dict[str, Any]], list[str]]:
    by_id = {e.event_id: e for e in events if e.user_id == user_id}
    accepted: list[dict[str, Any]] = []
    rejects: list[str] = []
    assigned: set[str] = set()
    for index, stream in enumerate(obj.get("streams", [])):
        try:
            members = list(dict.fromkeys(stream.get("member_event_ids", [])))
            if not stream.get("is_recurring") or stream.get("confidence") not in {"high", "medium"}:
                rejects.append(f"{index}:non_authoritative_confidence_or_nonrecurring"); continue
            if not members or any(x not in by_id for x in members):
                rejects.append(f"{index}:unknown_member_event_id"); continue
            rows = [by_id[x] for x in members]
            if any(e.status in {"failed", "cancelled", "unrealized"} or e.direction == "non_cash" or e.amount is None for e in rows):
                rejects.append(f"{index}:invalid_cash_member"); continue
            direction = stream.get("direction")
            if any(e.direction != direction for e in rows) or stream.get("event_type") not in {e.event_type for e in rows} or stream.get("category") not in {e.category for e in rows}:
                rejects.append(f"{index}:incompatible_stream_dimensions"); continue
            if assigned.intersection(members):
                rejects.append(f"{index}:duplicate_member_assignment"); continue
            cadence = stream.get("cadence") or {}
            ctype = cadence.get("type")
            if ctype not in {"monthly", "weekly", "biweekly", "fixed_days"}:
                rejects.append(f"{index}:unsupported_cadence"); continue
            dates = sorted(e.settlement_date or e.event_date for e in rows)
            if len(dates) < 2:
                rejects.append(f"{index}:insufficient_members"); continue
            gaps = [(b - a).days for a, b in zip(dates, dates[1:])]
            interval = cadence.get("interval_days")
            if ctype == "weekly": expected = 7
            elif ctype == "biweekly": expected = 14
            elif ctype == "monthly": expected = None
            else: expected = int(interval or 0)
            if expected and not all(abs(g - expected) <= 3 for g in gaps):
                rejects.append(f"{index}:cadence_incompatible"); continue
            if ctype == "monthly" and not all(27 <= g <= 32 for g in gaps):
                rejects.append(f"{index}:monthly_cadence_incompatible"); continue
            if stream.get("termination_evidence"):
                # Evidence is retained for diagnostics but a terminal claim
                # cannot silently create future events.
                rejects.append(f"{index}:termination_evidence_present"); continue
            projection = stream.get("projection_amount") or {}
            currency = projection.get("currency")
            if any(e.currency != currency for e in rows):
                rejects.append(f"{index}:unsupported_projection_currency"); continue
            basis = projection.get("basis")
            amounts = [e.amount for e in rows if e.amount is not None]
            if basis == "latest_authoritative": materialized = amounts[-1]
            elif basis == "stable_amount" and len(set(amounts)) == 1: materialized = amounts[-1]
            elif basis == "conservative_variable": materialized = max(amounts[-3:])
            elif basis == "message_amendment": materialized = amounts[-1]
            else:
                rejects.append(f"{index}:unsupported_amount_basis"); continue
            proposed = _amount(projection.get("amount"))
            if proposed is not None and proposed != materialized:
                rejects.append(f"{index}:amount_not_derived_from_evidence"); continue
            accepted.append({"stream": stream, "rows": rows, "amount": materialized, "cadence_type": ctype, "interval_days": expected})
            assigned.update(members)
        except Exception as exc:
            rejects.append(f"{index}:verification_exception:{type(exc).__name__}")
    return accepted, rejects


def _next_month(day: date) -> date:
    return main.add_months(day, 1)


def materialize(request: main.Request, profile: main.Profile, base: main.Canonicalizer, events: list[main.CanonicalEvent], streams: list[dict[str, Any]], policy: main.WindowPolicy) -> tuple[list[main.CanonicalEvent], list[dict[str, Any]]]:
    horizon = request.request_date + timedelta(days=policy.upper_bound_offset())
    explicit = [e for e in events if not e.projected]
    history_by_id = {e.event_id: e for e in base.by_user.get(request.user_id, [])}
    explicit_keys = {(e.event_type, e.category, e.direction, e.currency, e.flexibility, e.settlement_date or e.event_date) for e in explicit}
    out = list(explicit)
    diagnostics: list[dict[str, Any]] = []
    for item in streams:
        rows = [e for e in item["rows"] if e.event_id in history_by_id and (e.settlement_date or e.event_date) < request.request_date]
        if len(rows) < 2:
            continue
        latest = max(rows, key=lambda e: (e.settlement_date or e.event_date, e.event_id))
        anchor = latest.settlement_date or latest.event_date
        n = 1
        while True:
            if item["cadence_type"] == "monthly": day = _next_month(anchor) if n == 1 else main.add_months(anchor, n)
            else: day = anchor + timedelta(days=int(item["interval_days"] or 0) * n)
            if day > horizon: break
            if day >= request.request_date:
                key = (latest.event_type, latest.category, latest.direction, latest.currency, latest.flexibility, day)
                if key not in explicit_keys:
                    new = replace(latest, event_id=f"semantic:{item['stream'].get('stream_id','stream')}@{day.isoformat()}", event_date=day, settlement_date=day, amount=item["amount"], projected=True, source_event_id=latest.event_id, status="scheduled", provenance="semantic_policy:" + ",".join(item["stream"].get("reason_codes", [])))
                    out.append(new)
                    diagnostics.append({"event_id": new.event_id, "date": day.isoformat(), "direction": new.direction, "category": new.category, "amount": str(new.amount), "source_event_ids": item["stream"].get("evidence_event_ids", []), "reason_codes": item["stream"].get("reason_codes", [])})
            n += 1
    return sorted(out, key=lambda e: ((e.settlement_date or e.event_date), e.event_id)), diagnostics


class SemanticRecurrencePolicy:
    def __init__(self, events: list[main.CanonicalEvent], messages: list[dict[str, str]], images: list[dict[str, str]], fx: main.ExchangeRateAdapter, resolved_by_user: dict[str, dict[str, Any]]) -> None:
        self.events = events
        self.messages = messages
        self.images = images
        self.fx = fx
        self.base = main.Canonicalizer(events, messages, fx)
        self.resolved_by_user = resolved_by_user
        self.diagnostics: dict[str, Any] = {}

    def converted(self, event: main.CanonicalEvent, profile: main.Profile) -> Decimal | None:
        return self.base.converted(event, profile)

    def for_request(self, request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        base_events = self.base.for_request(request, profile, policy)
        obj = self.resolved_by_user.get(request.user_id, {"streams": []})
        verified, rejects = verify_streams(obj, self.events, request.user_id)
        out, materialized = materialize(request, profile, self.base, base_events, verified, policy)
        # The semantic candidate owns inferred recurrence. Keep explicit R0
        # events, but remove R0 projected rows so model decisions cannot be
        # mixed with the old description-keyed projection.
        explicit = [e for e in out if not e.projected]
        self.diagnostics[request.request_id] = {"verified_streams": len(verified), "rejected_streams": rejects, "materialized": materialized, "r0_projected": sum(e.projected for e in base_events)}
        return out


def resolve_users(user_ids: list[str], events: list[main.CanonicalEvent], messages: list[dict[str, str]], images: list[dict[str, str]], linked_by_id: dict[str, str] | None = None) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    resolved: dict[str, dict[str, Any]] = {}
    totals = {"provider": "ollama-local", "model": MODEL, "temperature": 0, "calls": 0, "input_tokens": 0, "output_tokens": 0, "cache_hits": 0, "users": len(user_ids)}
    for user_id in user_ids:
        packet = build_packet(user_id, events, messages, images, linked_by_id)
        obj, use = resolve_packet(packet)
        # Cache files contain an envelope; resolve_packet returns bare object.
        resolved[user_id] = obj
        for key in ("calls", "input_tokens", "output_tokens"):
            totals[key] += int(use.get(key, 0))
        totals["cache_hits"] += int(bool(use.get("cached")))
    return resolved, totals
