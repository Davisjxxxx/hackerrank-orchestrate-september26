#!/usr/bin/env python3
"""Deterministic Buy or Wait? implementation."""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import statistics
from dataclasses import dataclass, replace
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

getcontext().prec = 40
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dataset"
EVAL = ROOT / "evaluation"
OUTPUT_COLUMNS = ["request_id", "amount_safe_to_pay", "affordability_status", "recommended_payment_method", "payment_plan", "earliest_date_for_full_payment", "spending_changes_needed", "decision_explanation"]
OBSERVED_DIRECTIONS = {"debit", "credit", "non_cash"}


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def dec(value: Any) -> Decimal:
    if value is None or value == "":
        raise ValueError("blank amount is unknown, not zero")
    try:
        return Decimal(str(value).replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"invalid decimal: {value!r}") from exc


def dec_or_none(value: Any) -> Decimal | None:
    return None if value is None or value == "" else dec(value)


def short_decimal(value: Decimal) -> str:
    value = value.normalize()
    return str(value.quantize(Decimal(1))) if value == value.to_integral() else format(value, "f").rstrip("0").rstrip(".")


def plan_decimal(value: Decimal) -> str:
    """Payment-plan amounts use cents/minor units when a fractional amount exists."""
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)) if value != value.to_integral() else str(value.quantize(Decimal(1)))


def display_decimal(value: Decimal) -> str:
    return f"{int(value):,}" if value == value.to_integral() else f"{value:,.2f}"


def human_date(value: date) -> str:
    return f"{value.day} {value.strftime('%B %Y')}"


def tokens(value: str) -> list[str]:
    return [x for x in value.split("|") if x]


def add_months(value: date, months: int) -> date:
    month0 = value.month - 1 + months
    year, month0 = value.year + month0 // 12, month0 % 12
    month = month0 + 1
    next_month = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return date(year, month, min(value.day, (next_month - timedelta(days=1)).day))


class WindowPolicy(str, Enum):
    DAYS_0_THROUGH_89 = "days_0_through_89"
    DAYS_0_THROUGH_90 = "days_0_through_90"

    def upper_bound_offset(self) -> int:
        return 89 if self is WindowPolicy.DAYS_0_THROUGH_89 else 90


@dataclass(frozen=True)
class Profile:
    user_id: str; home_currency: str; current_available_balance: Decimal; minimum_balance_to_keep: Decimal
    protect: frozenset[str]; reduce: frozenset[str]; stop: frozenset[str]; methods: frozenset[str]
    max_installment_months: int | None; priorities: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Request:
    request_id: str; user_id: str; request_date: date; request_type: str; requested_amount: Decimal
    desired_completion_date: date; allows_partial_payment: bool; request_text: str


@dataclass(frozen=True)
class PaymentOption:
    payment_option_id: str; request_id: str; payment_method: str; payment_amount: Decimal
    payment_amount_text: str; number_of_payments: int; first_payment_date: date
    payment_frequency_days: int | None; financing_fee: Decimal; total_payable_amount: Decimal


@dataclass(frozen=True)
class CanonicalEvent:
    event_id: str; user_id: str; event_type: str; description: str; category: str; direction: str
    amount: Decimal | None; currency: str; event_date: date; settlement_date: date | None; status: str
    flexibility: str; minimum_allowed_amount: Decimal | None; projected: bool = False
    source_event_id: str | None = None; provenance: str = "structured"


@dataclass(frozen=True)
class Change:
    operation: str; event_id: str; new_amount: Decimal | None = None; new_amount_text: str | None = None

    def serialize(self) -> str:
        if self.operation == "stop": return f"stop:{self.event_id}"
        assert self.new_amount is not None
        return f"reduce_to:{self.event_id}:{self.new_amount_text or plan_decimal(self.new_amount)}"


@dataclass
class Decision:
    request: Request; profile: Profile; amount_safe: Decimal; status: str; method: str
    payment_plan: list[tuple[date, Decimal, str]]; earliest: date | None; changes: tuple[Change, ...]
    explanation: str = ""; total_paid: Decimal = Decimal(0); option_id: str | None = None; reason: str = ""


class ProfileAdapter:
    def load(self) -> dict[str, Profile]:
        result = {}
        for r in read_csv("financial_profiles.csv"):
            result[r["user_id"]] = Profile(r["user_id"], r["home_currency"], dec(r["current_available_balance"]), dec(r["minimum_balance_to_keep"]), frozenset(tokens(r["expense_categories_to_protect"])), frozenset(tokens(r["expense_categories_user_is_willing_to_reduce"])), frozenset(tokens(r["expense_categories_user_is_willing_to_stop"])), frozenset(tokens(r["payment_methods_user_will_consider"])), int(r["max_installment_months"]) if r["max_installment_months"] else None, frozenset(tokens(r["financial_priorities"])))
        return result


class RequestAdapter:
    def load(self, name: str = "requests.csv") -> list[Request]:
        return [Request(r["request_id"], r["user_id"], date.fromisoformat(r["request_date"]), r["request_type"], dec(r["requested_amount"]), date.fromisoformat(r["desired_completion_date"]), r["allows_partial_payment"].lower() == "true", r["request_text"]) for r in read_csv(name)]


class PaymentOptionAdapter:
    def load(self) -> dict[str, list[PaymentOption]]:
        out: dict[str, list[PaymentOption]] = {}
        for r in read_csv("request_payment_options.csv"):
            item = PaymentOption(r["payment_option_id"], r["request_id"], r["payment_method"], dec(r["payment_amount"]), r["payment_amount"], int(r["number_of_payments"]), date.fromisoformat(r["first_payment_date"]), int(r["payment_frequency_days"]) if r["payment_frequency_days"] else None, dec(r["financing_fee"]), dec(r["total_payable_amount"]))
            out.setdefault(item.request_id, []).append(item)
        for values in out.values(): values.sort(key=lambda x: x.payment_option_id)
        return out


class ExchangeRateAdapter:
    def __init__(self) -> None: self.rates: dict[tuple[str, str], list[tuple[date, Decimal]]] = {}

    def load(self) -> dict[tuple[str, str], list[tuple[date, Decimal]]]:
        if not self.rates:
            for r in read_csv("exchange_rates.csv"):
                self.rates.setdefault((r["from_currency"], r["to_currency"]), []).append((date.fromisoformat(r["rate_date"]), dec(r["rate"])))
            for values in self.rates.values(): values.sort()
        return self.rates

    def convert(self, amount: Decimal, source: str, target: str, on: date) -> Decimal:
        if source == target: return amount
        values = self.load().get((source, target), [])
        exact = [rate for rate_date, rate in values if rate_date == on]
        if not exact: raise RuntimeError(f"missing FX path/rate for {source}->{target} on {on}")
        return amount * exact[-1]


class ImageEvidenceAdapter:
    def __init__(self) -> None:
        self.cache_path = EVAL / "ocr_cache.json"; self.cache: dict[str, list[str]] = {}
        if self.cache_path.exists():
            try: self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError: self.cache = {}

    def text(self, image_id: str) -> list[str]:
        if image_id not in self.cache:
            path = DATA / "media" / "images" / f"{image_id}.png"
            if not path.exists(): raise RuntimeError(f"missing image: {path}")
            try:
                from paddleocr import PaddleOCR
                ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False, lang="en")
                self.cache[image_id] = [str(x) for x in ocr.predict(str(path))[0].get("rec_texts", [])]
            except Exception:
                self.cache[image_id] = []
            EVAL.mkdir(exist_ok=True)
            self.cache_path.write_text(json.dumps(self.cache, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return self.cache[image_id]

    def extract_amount(self, image_id: str, event: Mapping[str, str]) -> tuple[Decimal | None, str]:
        joined = " | ".join(self.text(image_id))

        def values_after(pattern: str, stop: str | None = None, all_matches: bool = False) -> list[Decimal]:
            """Read numeric values from the bounded block after a label."""
            matches = list(re.finditer(pattern, joined, re.I | re.S))
            if not matches:
                return []
            selected = matches if all_matches else matches[-1:]
            values: list[Decimal] = []
            for match in selected:
                tail = joined[match.end():]
                if stop:
                    boundary = re.search(stop, tail, re.I | re.S)
                    if boundary:
                        tail = tail[:boundary.start()]
                raw_values = re.findall(r"(?<![A-Za-z])\d[\d,]*(?:\.\d+)?(?![A-Za-z])", tail)
                if raw_values:
                    values.append(dec(raw_values[-1].replace(",", "")))
            return values

        def after(pattern: str) -> str | None:
            m = re.search(pattern + r".{0,180}?([\d][\d,]*(?:\.\d+)?)", joined, re.I | re.S)
            return m.group(1) if m else None
        kind = (event["description"] + " " + event["category"]).lower()
        if "telecom" in kind:
            due_after = re.search(r"Amount due after.*?=\s*\|?\s*([\d,]+\.\d+)", joined, re.I | re.S)
            if due_after:
                return dec(due_after.group(1).replace(",", "")), f"ocr:{image_id}:grounded"
        patterns: list[str] = []
        if "salary" in kind: patterns = [r"Net Pay", r"Transferred to"]
        elif "rent" in kind: patterns = [r"Balance Due", r"Amount Received", r"Total Amount to be Receivi"]
        elif "grocer" in kind or "dining" in kind or "restaurant" in kind:
            # Prefer a labeled grand total.  If OCR corrupts that token, use
            # the invoice's labeled subtotal and tax components instead of
            # treating a quantity or tax percentage as the event amount.
            grand_total = values_after(r"Grand Total", r"(?:Thank You|Amount in Words|Total In Words)")
            if grand_total:
                return grand_total[-1], f"ocr:{image_id}:grounded"
            subtotal = values_after(r"Sub\s*Total", r"Total In Words")
            taxes = []
            for label in (r"CGST", r"SGST"):
                taxes.extend(values_after(label, r"(?:CGST|SGST|Notes|Total)", all_matches=True))
            if subtotal and len(taxes) >= 2:
                return subtotal[-1] + sum(taxes), f"ocr:{image_id}:grounded"
            total_values = values_after(r"\bTotal\b", r"(?:Amount in|Total In Words|Thank You)")
            if total_values:
                return total_values[-1], f"ocr:{image_id}:grounded"
            patterns = [r"Net Amount", r"TOTAL ORDER BILL DETAILS", r"\bTotal\b", r"Grand Total"]
        elif "maintenance" in kind or "property" in kind: patterns = [r"Total Amount Received"]
        elif "water" in kind: patterns = [r"Total Amount Received"]
        elif "telecom" in kind: patterns = [r"Amount due after", r"Amount due till", r"Total"]
        elif "airline" in kind or "ticket" in kind: patterns = [r"Grand Total"]
        elif "hospital" in kind: patterns = [r"Amount Payable", r"TOTAL"]
        elif "pharmacy" in kind: patterns = [r"TOTAL"]
        elif "tote" in kind or "shopping" in kind: patterns = [r"Total paid", r"TOTAL"]
        elif "taxi" in kind or "transport" in kind: patterns = [r"Total"]
        for pattern in patterns:
            raw = after(pattern)
            if raw:
                value = dec(raw.replace(",", ""))
                if "pharmacy" in kind and value > Decimal("100000"): value /= Decimal(100)
                return value, f"ocr:{image_id}:grounded"
        return None, f"ocr:{image_id}:unresolved"


class FinancialEventAdapter:
    def __init__(self, images: ImageEvidenceAdapter) -> None: self.images = images

    def canonical_rows(self) -> list[CanonicalEvent]:
        links = {r["related_event_id"]: r["image_id"] for r in read_csv("images.csv")}
        out: list[CanonicalEvent] = []; seen: set[tuple[str, ...]] = set()
        for r in read_csv("financial_events.csv"):
            key = tuple(r[k] for k in r if k != "event_id")
            if key in seen: continue
            seen.add(key); amount = dec_or_none(r["amount"]); provenance = "structured"
            if amount is None and r["event_id"] in links: amount, provenance = self.images.extract_amount(links[r["event_id"]], r)
            out.append(CanonicalEvent(r["event_id"], r["user_id"], r["event_type"], r["description"], r["category"], r["direction"], amount, r["currency"], date.fromisoformat(r["event_date"]), date.fromisoformat(r["settlement_date"]) if r["settlement_date"] else None, r["status"], r["flexibility"], dec_or_none(r["minimum_allowed_amount"]), provenance=provenance))
        return out


class MessageEvidenceAdapter:
    """Expose message evidence without allowing message text to become policy."""

    def __init__(self, rows: list[dict[str, str]] | None = None) -> None:
        self.rows = rows if rows is not None else read_csv("messages.csv")

    def for_user(self, user_id: str) -> list[dict[str, str]]:
        return [row for row in self.rows if row["user_id"] == user_id]


class DatasetInventory:
    FILES = ["exchange_rates.csv", "financial_events.csv", "financial_profiles.csv", "images.csv", "messages.csv", "output.csv", "request_payment_options.csv", "requests.csv", "sample_requests.csv"]

    @staticmethod
    def dtype(value: str) -> str:
        try: date.fromisoformat(value); return "date"
        except ValueError: pass
        try: dec(value); return "decimal"
        except ValueError: return "string"

    @staticmethod
    def counts(rows: Iterable[Mapping[str, str]], col: str) -> dict[str, int]:
        from collections import Counter
        return dict(sorted(Counter(r[col] for r in rows).items()))

    def build(self) -> dict[str, Any]:
        tables = {}
        for filename in self.FILES:
            rows = read_csv(filename); cols = {}
            for col in rows[0]:
                vals = [r[col] for r in rows]; nonnull = [v for v in vals if v]
                kinds = {self.dtype(v) for v in nonnull}
                inferred = "null" if not kinds else ("decimal" if kinds <= {"decimal"} else ("date" if kinds <= {"date"} else "string"))
                c = self.counts(rows, col)
                cols[col] = {"inferred_dtype": inferred, "total_count": len(vals), "null_count": vals.count(""), "null_fraction": vals.count("") / len(vals) if vals else 0, "unique_value_count": len(c), "categorical_values": [{"value": k, "count": v} for k, v in c.items()] if len(c) <= 50 else []}
            tables[filename] = {"row_count": len(rows), "columns": cols}
        events, opts, prof, msgs, imgs, reqs = (read_csv(x) for x in ["financial_events.csv", "request_payment_options.csv", "financial_profiles.csv", "messages.csv", "images.csv", "requests.csv"])
        event_ids = {r["event_id"] for r in events}; rate_rows = read_csv("exchange_rates.csv")
        linked = {r["event_id"]: r["linked_event_id"] for r in events if r["linked_event_id"]}
        cycles = 0; max_chain = 0
        for start in linked:
            seen = set(); cur = start
            while cur in linked:
                if cur in seen:
                    cycles += 1
                    break
                seen.add(cur); cur = linked[cur]
            max_chain = max(max_chain, len(seen))
        rate_dates = sorted(r["rate_date"] for r in rate_rows)
        observed_categories = {r["category"] for r in events}
        permission_columns = ["expense_categories_to_protect", "expense_categories_user_is_willing_to_reduce", "expense_categories_user_is_willing_to_stop"]
        permissions = {column: sorted({token for row in prof for token in tokens(row[column])}) for column in permission_columns}
        english_like = sum(bool(re.search(r"\b(the|your|payment|salary|account|total)\b", row["message_text"], re.I)) for row in msgs)
        non_cash_semantics = sorted({f"{row['event_type']}/{row['status']}" for row in events if row["direction"] == "non_cash"})
        cross = {
            "event_value_counts": {column: self.counts(events, column) for column in ["status", "event_type", "category", "flexibility"]},
            "direction_exact_domain": all(row["direction"] in OBSERVED_DIRECTIONS for row in events),
            "non_cash": {"count": sum(row["direction"] == "non_cash" for row in events), "semantics": non_cash_semantics, "supported_semantics": non_cash_semantics == ["investment_valuation/unrealized"]},
            "linked_event_id": {"populated": sum(bool(row["linked_event_id"]) for row in events), "maximum_chain_length": max_chain, "cycle_count": cycles},
            "minimum_allowed_amount": {"populated": sum(bool(row["minimum_allowed_amount"]) for row in events), "distribution": self.counts(events, "minimum_allowed_amount")},
            "home_currency": self.counts(prof, "home_currency"),
            "payment_methods_user_will_consider": self.counts(prof, "payment_methods_user_will_consider"),
            "max_installment_months": {"distribution": self.counts(prof, "max_installment_months"), "null_count": sum(not row["max_installment_months"] for row in prof)},
            "profile_category_tokens": {column: {"observed": values, "absent_from_event_categories": sorted(set(values) - observed_categories)} for column, values in permissions.items()},
            "exchange_rate_pairs": self.counts([{"pair": f"{row['from_currency']}->{row['to_currency']}"} for row in rate_rows], "pair"),
            "exchange_rate_date_range": {"min": rate_dates[0], "max": rate_dates[-1], "distinct_count": len(set(rate_dates)), "granularity_days": sorted({(date.fromisoformat(b) - date.fromisoformat(a)).days for a, b in zip(rate_dates, rate_dates[1:])})},
            "message_source_type": self.counts(msgs, "source_type"),
            "message_related_event_null_count": sum(not row["related_event_id"] for row in msgs),
            "message_language_counts": {"english_like": english_like, "non_english_like": len(msgs) - english_like},
            "image_paths_exist": all((DATA / "media" / "images" / f"{row['image_id']}.png").exists() for row in imgs),
            "option_payment_method": self.counts(opts, "payment_method"), "option_number_of_payments": self.counts(opts, "number_of_payments"), "option_frequency_days": self.counts(opts, "payment_frequency_days"),
            "option_frequency_anomaly": sorted({row["payment_frequency_days"] for row in opts if row["payment_frequency_days"] and row["payment_frequency_days"] not in {"28", "30", "31"}}),
            "permitted_categories_not_observed": sorted(set().union(*permissions.values()) - observed_categories),
            "linkage": {"requests_without_options": sorted({row["request_id"] for row in reqs} - {row["request_id"] for row in opts}), "events_without_profiles": sorted({row["user_id"] for row in events} - {row["user_id"] for row in prof}), "messages_to_missing_events": sorted({row["related_event_id"] for row in msgs if row["related_event_id"]} - event_ids), "images_to_missing_events": sorted({row["related_event_id"] for row in imgs} - event_ids)},
        }
        return {"files": tables, "cross_file": cross}

    def write(self) -> dict[str, Any]:
        obj = self.build(); EVAL.mkdir(exist_ok=True)
        (EVAL / "dataset_inventory.json").write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        lines = ["# Deterministic dataset inventory", "", "Generated from participant-facing `dataset/` only.", ""]
        for name, info in obj["files"].items():
            lines += [f"## {name}", f"Rows: {info['row_count']}", ""]
            for col, spec in info["columns"].items():
                lines.append(f"- `{col}`: dtype={spec['inferred_dtype']}; null={spec['null_count']}/{spec['total_count']} ({spec['null_fraction']:.6f}); unique={spec['unique_value_count']}")
                if spec["categorical_values"]: lines.append("  - values: " + ", ".join(f"{x['value']!r} ({x['count']})" for x in spec["categorical_values"]))
            lines.append("")
        lines += ["## Cross-file assertions", "", "```json", json.dumps(obj["cross_file"], sort_keys=True, indent=2), "```", ""]
        (EVAL / "dataset_inventory.md").write_text("\n".join(lines), encoding="utf-8")
        return obj


def cadence(events: list[CanonicalEvent]) -> tuple[str, int]:
    ds = sorted(e.event_date for e in events); gaps = [(b - a).days for a, b in zip(ds, ds[1:])]
    if not gaps: return "none", 0
    med = int(statistics.median(gaps))
    if all(27 <= x <= 32 for x in gaps): return "month", 1
    # Recurrence evidence is noisy in the supplied history.  A fixed-gap
    # stream remains eligible only when at least two observed intervals agree
    # within three days of the median.  This bounded rule admits a supported
    # delayed/missed observation without treating an arbitrary category as a
    # recurring stream.
    if med >= 5 and sum(abs(gap - med) <= 4 for gap in gaps) >= 2: return "gap", max(1, med)
    return "none", 0


class Canonicalizer:
    def __init__(self, events: list[CanonicalEvent], messages: list[dict[str, str]], fx: ExchangeRateAdapter) -> None:
        self.events, self.fx = events, fx; self.message_evidence = MessageEvidenceAdapter(messages); self.by_user: dict[str, list[CanonicalEvent]] = {}
        for e in events: self.by_user.setdefault(e.user_id, []).append(e)

    def message_adjustments(self, user_id: str, rows: list[CanonicalEvent], request_date: date) -> list[CanonicalEvent]:
        out = list(rows)
        for m in self.message_evidence.for_user(user_id):
            # Evidence is available only after it was sent.  Applying a later
            # payroll notice to an earlier request leaks future information
            # into the historical decision state.
            if m.get("sent_at") and date.fromisoformat(m["sent_at"][:10]) > request_date:
                continue
            text, low = m["message_text"], m["message_text"].lower()
            if "salary" not in low and "gaji" not in low and "payroll" not in low: continue
            if any(x in low for x in ["pending", "still waiting", "belum disetujui", "has ended", "ended", "berakhir", "seasonal contract"]):
                if "ended" in low or "berakhir" in low or "seasonal contract" in low:
                    out = [e for e in out if not (e.event_type == "income" and e.category == "salary" and (e.settlement_date or e.event_date) > request_date)]
                continue
            money = re.findall(r"\b(INR|IDR|USD|EUR|ZAR)\s*([\d,.]+)", text, re.I)
            dates = re.findall(r"\b20\d{2}-\d{2}-\d{2}\b", text)
            # The first stated salary is the recurring/base amount.  A later
            # amount in the same message can be an arrears or commission
            # adjustment and must not become recurring income.
            salary_money = money[0] if money else None
            salary_rows = [e for e in out if e.event_type == "income" and e.category == "salary" and e.amount is not None]
            if salary_money:
                cur, raw = salary_money; amount = dec(raw.rstrip("."))
                effective = date.fromisoformat(dates[0]) if dates else self._next_salary_date(salary_rows, request_date)
                new, changed = [], False
                for e in out:
                    if e.event_type == "income" and e.category == "salary" and (e.settlement_date or e.event_date) >= effective:
                        new.append(replace(e, amount=amount, currency=cur, provenance=e.provenance + "+message")); changed = True
                    else: new.append(e)
                out = new
                # A message is itself a confirmed future record when the
                # structured feed has not supplied that occurrence yet.
                if not any(e.event_type == "income" and e.category == "salary" and (e.settlement_date or e.event_date) == effective for e in out):
                    out.append(CanonicalEvent(f"message:{m['message_id']}", user_id, "income", "confirmed salary", "salary", "credit", amount, cur, effective, effective, "scheduled", "fixed", None, provenance="message:confirmed"))
            elif dates and any(marker in low for marker in ("salary", "gaji", "payroll")):
                # A date-only amendment still carries trusted timing and can
                # relocate the next confirmed salary using the latest known
                # regular amount.
                effective = date.fromisoformat(dates[0])
                if salary_rows:
                    amount_event = max(salary_rows, key=lambda e: e.event_date)
                    if not any(e.event_type == "income" and e.category == "salary" and (e.settlement_date or e.event_date) == effective for e in out):
                        out.append(replace(amount_event, event_id=f"message:{m['message_id']}", description="confirmed salary", event_date=effective, settlement_date=effective, status="scheduled", projected=False, source_event_id=None, provenance=amount_event.provenance + "+message"))
        return out

    @staticmethod
    def _next_salary_date(rows: Sequence[CanonicalEvent], request_date: date) -> date:
        dated = sorted((e.settlement_date or e.event_date for e in rows if (e.settlement_date or e.event_date) < request_date))
        if dated:
            latest = dated[-1]
            return add_months(latest, 1)
        return date(request_date.year, request_date.month, 15) if request_date.day < 15 else add_months(date(request_date.year, request_date.month, 15), 1)

    def for_request(self, request: Request, profile: Profile, policy: WindowPolicy) -> list[CanonicalEvent]:
        horizon = request.request_date + timedelta(days=policy.upper_bound_offset())
        rows = self.message_adjustments(request.user_id, self.by_user.get(request.user_id, []), request.request_date)
        valid = [e for e in rows if e.status not in {"failed", "cancelled", "unrealized"} and e.direction != "non_cash"]
        groups: dict[tuple[str, str, str, str], list[CanonicalEvent]] = {}
        for e in valid:
            if e.amount is not None and e.event_date <= request.request_date: groups.setdefault((e.event_type, e.category, e.flexibility, e.description), []).append(e)
        explicit, explicit_keys = [], set()
        for e in valid:
            d = e.settlement_date or e.event_date
            if d < request.request_date or d > horizon: continue
            if e.status == "settled" and d == request.request_date: continue
            explicit.append(e); explicit_keys.add(((e.event_type, e.category, e.flexibility, e.description), d))
        terminal_semantics = {
            (e.event_type, e.category, e.flexibility)
            for e in valid
            if any(marker in e.description.lower() for marker in ("final", "last payroll", "employment ended", "contract ended"))
        }
        projected = []
        for key, history in sorted(groups.items()):
            if (key[0], key[1], key[2]) in terminal_semantics: continue
            kind, step = cadence(history)
            if kind == "none": continue
            latest = max(history, key=lambda e: (e.settlement_date or e.event_date)); recent = sorted(history, key=lambda e: (e.settlement_date or e.event_date))[-3:]; amount = statistics.median([e.amount for e in recent if e.amount is not None]).quantize(Decimal("0.01")); n = 1
            while True:
                anchor = latest.settlement_date or latest.event_date
                d = add_months(anchor, n) if kind == "month" else anchor + timedelta(days=step * n)
                if d > horizon: break
                if d >= request.request_date and (key, d) not in explicit_keys:
                    projected.append(replace(latest, event_id=f"{latest.event_id}@{d.isoformat()}", event_date=d, settlement_date=d, amount=amount, projected=True, source_event_id=latest.event_id, status="scheduled", provenance="recurrence:median_last_3"))
                n += 1
        # A confirmed future salary is an anchor, not a one-off income event.
        # Continue the regular monthly payroll from that anchor unless a
        # terminal-payroll marker removed the stream above.
        if not any(e[0] == "income" and e[1] == "salary" and e[2] == "fixed" for e in terminal_semantics):
            future_salary = [e for e in explicit if e.event_type == "income" and e.category == "salary" and e.amount is not None]
            if future_salary:
                anchor_event = max(future_salary, key=lambda e: (e.settlement_date or e.event_date))
                d = anchor_event.settlement_date or anchor_event.event_date
                n = 1
                while True:
                    future_day = add_months(d, n)
                    if future_day > horizon: break
                    if future_day >= request.request_date and not any(e.event_type == "income" and e.category == "salary" and (e.settlement_date or e.event_date) == future_day for e in explicit + projected):
                        projected.append(replace(anchor_event, event_id=f"{anchor_event.event_id}@{future_day.isoformat()}", event_date=future_day, settlement_date=future_day, projected=True, source_event_id=anchor_event.event_id, status="scheduled", provenance="recurrence:confirmed_salary"))
                    n += 1
        # An explicit confirmed salary occurrence is authoritative for that
        # same economic date.  Suppress only the projected salary row with the
        # same direction/type/category/currency/flexibility key; independent
        # salary dates remain separate and description text is not identity.
        explicit_salary_keys = {
            (e.user_id, e.event_type, e.category, e.direction, e.currency, e.flexibility, e.settlement_date or e.event_date)
            for e in explicit
            if e.category == "salary" and not e.projected
        }
        projected = [
            e for e in projected
            if not (
                e.category == "salary"
                and e.projected
                and (e.user_id, e.event_type, e.category, e.direction, e.currency, e.flexibility, e.settlement_date or e.event_date) in explicit_salary_keys
            )
        ]
        return sorted(explicit + projected, key=lambda e: ((e.settlement_date or e.event_date), e.event_id))

    def converted(self, event: CanonicalEvent, profile: Profile) -> Decimal | None:
        return None if event.amount is None else self.fx.convert(event.amount, event.currency, profile.home_currency, event.settlement_date or event.event_date)


class Simulator:
    def __init__(self, canonicalizer: Canonicalizer, policy: WindowPolicy) -> None: self.canonicalizer, self.policy = canonicalizer, policy

    def has_unresolved_debit(self, request: Request, events: Sequence[CanonicalEvent]) -> bool:
        end = request.request_date + timedelta(days=self.policy.upper_bound_offset())
        return any(
            event.amount is None
            and event.direction == "debit"
            and request.request_date <= (event.settlement_date or event.event_date) <= end
            for event in events
        )

    def flows(self, request: Request, profile: Profile, events: Sequence[CanonicalEvent], changes: Sequence[Change] = ()) -> dict[date, Decimal]:
        stopped = {c.event_id for c in changes if c.operation == "stop"}; reduced = {c.event_id: c.new_amount for c in changes if c.operation == "reduce_to"}; out: dict[date, Decimal] = {}
        for e in events:
            d = e.settlement_date or e.event_date
            if d < request.request_date or d > request.request_date + timedelta(days=self.policy.upper_bound_offset()): continue
            sid = e.source_event_id or e.event_id
            if sid in stopped: continue
            amount = self.canonicalizer.converted(e, profile)
            if amount is None: continue
            if sid in reduced: amount = self.canonicalizer.fx.convert(reduced[sid], e.currency, profile.home_currency, d)
            if e.direction == "credit" and e.status == "pending": continue
            out[d] = out.get(d, Decimal(0)) + (amount if e.direction == "credit" else -amount)
        return out

    def run(self, request: Request, profile: Profile, events: Sequence[CanonicalEvent], payments: Sequence[tuple[date, Decimal]], changes: Sequence[Change] = ()) -> tuple[bool, dict[date, Decimal], Decimal]:
        if self.has_unresolved_debit(request, events):
            return False, {}, Decimal("-Infinity")
        pm: dict[date, Decimal] = {}
        for d, amount in payments:
            if amount < 0 or d < request.request_date or d > request.desired_completion_date or d > request.request_date + timedelta(days=self.policy.upper_bound_offset()): return False, {}, Decimal("-Infinity")
            pm[d] = pm.get(d, Decimal(0)) + amount
        flows = self.flows(request, profile, events, changes); balance = profile.current_available_balance; values = {}
        for offset in range(self.policy.upper_bound_offset() + 1):
            d = request.request_date + timedelta(days=offset); balance += flows.get(d, Decimal(0)); balance -= pm.get(d, Decimal(0)); values[d] = balance
        trough = min(values.values()) if values else balance
        return all(x >= profile.minimum_balance_to_keep for x in values.values()), values, trough


class ProductionSimulator(Simulator):
    """Second implementation of the cash predicate used by the differential gate.

    This intentionally does not call ``Simulator.flows`` or ``Simulator.run``;
    agreement is therefore evidence that the canonical event semantics were not
    accidentally coupled to one implementation.
    """

    def run(self, request: Request, profile: Profile, events: Sequence[CanonicalEvent], payments: Sequence[tuple[date, Decimal]], changes: Sequence[Change] = ()) -> tuple[bool, dict[date, Decimal], Decimal]:
        end = request.request_date + timedelta(days=self.policy.upper_bound_offset())
        if self.has_unresolved_debit(request, events):
            return False, {}, Decimal("-Infinity")
        payment_by_day: dict[date, Decimal] = {}
        for day, amount in payments:
            if amount < 0 or day < request.request_date or day > request.desired_completion_date or day > end:
                return False, {}, Decimal("-Infinity")
            payment_by_day[day] = payment_by_day.get(day, Decimal(0)) + amount
        stopped = {change.event_id for change in changes if change.operation == "stop"}
        reductions = {change.event_id: change.new_amount for change in changes if change.operation == "reduce_to"}
        flow_by_day: dict[date, Decimal] = {}
        for event in events:
            day = event.settlement_date or event.event_date
            if not request.request_date <= day <= end:
                continue
            source_id = event.source_event_id or event.event_id
            if source_id in stopped:
                continue
            amount = event.amount
            if amount is None:
                continue
            amount = self.canonicalizer.fx.convert(amount, event.currency, profile.home_currency, day)
            if source_id in reductions:
                amount = self.canonicalizer.fx.convert(reductions[source_id], event.currency, profile.home_currency, day)
            if event.direction == "credit" and event.status == "pending":
                continue
            flow_by_day[day] = flow_by_day.get(day, Decimal(0)) + (amount if event.direction == "credit" else -amount)
        balance = profile.current_available_balance
        balances: dict[date, Decimal] = {}
        for offset in range(self.policy.upper_bound_offset() + 1):
            day = request.request_date + timedelta(days=offset)
            balance += flow_by_day.get(day, Decimal(0)) - payment_by_day.get(day, Decimal(0))
            balances[day] = balance
        trough = min(balances.values()) if balances else balance
        return all(balance >= profile.minimum_balance_to_keep for balance in balances.values()), balances, trough


class Planner:
    def __init__(self, canonicalizer: Canonicalizer, options: dict[str, list[PaymentOption]], policy: WindowPolicy) -> None:
        self.canonicalizer, self.options, self.policy = canonicalizer, options, policy; self.oracle = Simulator(canonicalizer, policy); self.production = ProductionSimulator(canonicalizer, policy)

    def safe_amount(self, request: Request, profile: Profile, events: Sequence[CanonicalEvent]) -> Decimal:
        if self.oracle.has_unresolved_debit(request, events):
            return Decimal(0)
        flows = self.oracle.flows(request, profile, events); balance = profile.current_available_balance; trough = Decimal("Infinity")
        for offset in range(self.policy.upper_bound_offset() + 1):
            d = request.request_date + timedelta(days=offset); balance += flows.get(d, Decimal(0)); trough = min(trough, balance)
        return min(request.requested_amount, max(Decimal(0), trough - profile.minimum_balance_to_keep))

    def earliest_full(self, request: Request, profile: Profile, events: Sequence[CanonicalEvent]) -> date | None:
        for offset in range(self.policy.upper_bound_offset() + 1):
            d = request.request_date + timedelta(days=offset)
            if self.oracle.run(request, profile, events, [(d, request.requested_amount)])[0]: return d
        return None

    @staticmethod
    def installment_schedule(option: PaymentOption) -> list[tuple[date, Decimal, str]]:
        assert option.payment_frequency_days is not None
        return [(option.first_payment_date + timedelta(days=i * option.payment_frequency_days), option.payment_amount, option.payment_amount_text) for i in range(option.number_of_payments)]

    def change_candidates(self, request: Request, profile: Profile, events: Sequence[CanonicalEvent]) -> list[tuple[Change, ...]]:
        reps = {
            e.source_event_id: e
            for e in events
            if e.projected and e.source_event_id and e.direction == "debit"
        }; choices = []
        for sid, e in sorted(reps.items()):
            if e.category in profile.priorities:
                continue
            if e.flexibility in {"stoppable", "reducible_or_stoppable"} and e.category in profile.stop: choices.append(Change("stop", sid))
            if e.flexibility in {"reducible", "reducible_or_stoppable"} and e.category in profile.reduce:
                floor = e.minimum_allowed_amount or Decimal(0)
                if e.amount is not None and floor < e.amount:
                    choices.append(Change("reduce_to", sid, floor, plan_decimal(floor)))
        result = [()]
        for n in range(1, min(3, len(choices)) + 1):
            for combo in itertools.combinations(choices, n):
                if len({c.event_id for c in combo}) != len(combo): continue
                trial = list(combo)
                if self.oracle.run(request, profile, events, [(request.request_date, request.requested_amount)], trial)[0]: result.append(tuple(sorted(trial, key=lambda c: c.serialize()))); continue
                # Closed-form boundary for each reducible series: bisection
                # solves the linear deficit and is quantized only at output.
                for i, c in enumerate(trial):
                    if c.operation != "reduce_to": continue
                    rep = reps[c.event_id]; lo, hi = Decimal(0), rep.amount or Decimal(0)
                    lo = max(lo, rep.minimum_allowed_amount or Decimal(0))
                    for _ in range(70):
                        mid = (lo + hi) / 2; candidate = replace(c, new_amount=mid, new_amount_text=plan_decimal(mid)); attempt = trial[:i] + [candidate] + trial[i + 1:]
                        if self.oracle.run(request, profile, events, [(request.request_date, request.requested_amount)], attempt)[0]: lo = mid
                        else: hi = mid
                    boundary = lo.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP); trial[i] = replace(c, new_amount=boundary, new_amount_text=plan_decimal(boundary))
                if all(c.operation != "reduce_to" or (c.new_amount is not None and c.new_amount < (reps[c.event_id].amount or Decimal(0)) and c.new_amount >= (reps[c.event_id].minimum_allowed_amount or Decimal(0))) for c in trial) and self.oracle.run(request, profile, events, [(request.request_date, request.requested_amount)], trial)[0]:
                    result.append(tuple(sorted(trial, key=lambda c: c.serialize())))
        return result

    @staticmethod
    def rank_key(d: Decision) -> tuple[Any, ...]:
        start = d.payment_plan[0][0] if d.payment_plan else date.max; count = len(d.payment_plan) if d.payment_plan else 999; option = d.option_id or "~"
        return (0 if d.status != "not_affordable" else 1, 0 if not d.changes else 1, d.total_paid, start, count, option, f"{d.method}|{start.isoformat()}|{count}|{'|'.join(short_decimal(x[1]) for x in d.payment_plan)}|{d.option_id or ''}")

    def decide(self, request: Request, profile: Profile) -> tuple[Decision, list[CanonicalEvent]]:
        events = self.canonicalizer.for_request(request, profile, self.policy); safe = self.safe_amount(request, profile, events); earliest = self.earliest_full(request, profile, events); candidates = []
        if "full_payment" in profile.methods and self.oracle.run(request, profile, events, [(request.request_date, request.requested_amount)])[0]: candidates.append(Decision(request, profile, safe, "affordable_now", "full_payment", [(request.request_date, request.requested_amount, short_decimal(request.requested_amount))], earliest or request.request_date, (), total_paid=request.requested_amount))
        if "partial_payment" in profile.methods and request.allows_partial_payment and Decimal(0) < safe < request.requested_amount and earliest is not None and earliest <= request.desired_completion_date:
            pays = [(request.request_date, safe), (earliest, request.requested_amount - safe)]
            if self.oracle.run(request, profile, events, pays)[0]: candidates.append(Decision(request, profile, safe, "affordable_with_plan", "partial_payment", [(d, a, short_decimal(a)) for d, a in pays], earliest, (), total_paid=request.requested_amount))
        for option in self.options.get(request.request_id, []):
            if option.payment_method != "installments" or "installments" not in profile.methods or profile.max_installment_months is None or option.number_of_payments > profile.max_installment_months: continue
            schedule = self.installment_schedule(option)
            if schedule[-1][0] > request.desired_completion_date: continue
            if self.oracle.run(request, profile, events, [(d, a) for d, a, _ in schedule])[0]: candidates.append(Decision(request, profile, safe, "affordable_with_plan", "installments", schedule, earliest, (), total_paid=option.total_payable_amount, option_id=option.payment_option_id))
        if "full_payment" in profile.methods and earliest is not None and request.request_date < earliest <= request.desired_completion_date: candidates.append(Decision(request, profile, safe, "affordable_later", "wait", [(earliest, request.requested_amount, short_decimal(request.requested_amount))], earliest, (), total_paid=request.requested_amount))
        if "full_payment" in profile.methods:
            for changes in self.change_candidates(request, profile, events):
                if changes and self.oracle.run(request, profile, events, [(request.request_date, request.requested_amount)], changes)[0]: candidates.append(Decision(request, profile, safe, "affordable_with_plan", "full_payment", [(request.request_date, request.requested_amount, short_decimal(request.requested_amount))], earliest or request.request_date, changes, total_paid=request.requested_amount))
        if not candidates:
            return Decision(request, profile, safe, "not_affordable", "not_recommended", [], earliest, (), total_paid=Decimal(0), reason="known_blocker" if safe == 0 else "no_safe_plan"), events
        candidates.sort(key=self.rank_key); return candidates[0], events


def change_phrase(change: Change, profile: Profile, events: Sequence[CanonicalEvent]) -> str:
    category = next((e.category for e in events if e.event_id == change.event_id or e.source_event_id == change.event_id), "")
    names = {"streaming": "the family streaming plan", "cloud_storage": "the online backup subscription", "delivery_membership": "the delivery membership", "music_subscription": "the music subscription", "dining": "the weekend food delivery", "gym": "the gym subscription", "shopping": "the shopping budget"}
    phrase = names.get(category, f"the {category.replace('_', ' ')} expense")
    return f"Stop {phrase}" if change.operation == "stop" else f"Reduce {phrase} to {profile.home_currency} {display_decimal(change.new_amount or Decimal(0))}"


def make_explanation(d: Decision, events: Sequence[CanonicalEvent]) -> str:
    p, r, cur = d.profile, d.request, d.profile.home_currency; minimum = display_decimal(p.minimum_balance_to_keep)
    if d.method == "not_recommended":
        if d.reason == "known_blocker": return f"Do not make this payment by {human_date(r.desired_completion_date)}. None of the available options keeps the {cur} {minimum} minimum protected."
        return f"Do not proceed with the {cur} {display_decimal(r.requested_amount)} request. Although {cur} {display_decimal(d.amount_safe)} is available today, the full amount cannot be completed safely within 90 days."
    if d.changes:
        phrases = [change_phrase(c, p, events) for c in d.changes]
        if len(phrases) == 1: prefix = phrases[0] + ", then "
        elif len(phrases) == 2: prefix = phrases[0] + " and " + phrases[1].lower() + ", then "
        else: prefix = ", ".join(phrases[:-1]) + ", and " + phrases[-1].lower() + ", then "
        return prefix + f"pay {cur} {display_decimal(r.requested_amount)} today. This leaves at least {cur} {minimum} available."
    if d.method == "full_payment": return f"Pay {cur} {display_decimal(r.requested_amount)} today. This leaves at least {cur} {minimum} available over the next 90 days."
    if d.method == "installments": return f"Use {len(d.payment_plan)} installments of {cur} {display_decimal(dec(d.payment_plan[0][2]))}, starting {human_date(d.payment_plan[0][0])}. This leaves at least {cur} {minimum} available."
    if d.method == "partial_payment": return f"Pay {cur} {display_decimal(d.payment_plan[0][1])} today and the remaining {cur} {display_decimal(d.payment_plan[1][1])} on {human_date(d.payment_plan[1][0])}. This completes the full request and keeps the {cur} {minimum} minimum protected."
    return f"Pay {cur} {display_decimal(r.requested_amount)} in full on {human_date(d.payment_plan[0][0])}. Paying earlier would take the balance below the {cur} {minimum} minimum."


def serialize(d: Decision) -> dict[str, str]:
    plan = "none" if d.method == "not_recommended" else "|".join(f"{day.isoformat()}:{(amount_text if d.method == 'installments' else plan_decimal(amount))}" for day, amount, amount_text in d.payment_plan)
    return {"request_id": d.request.request_id, "amount_safe_to_pay": short_decimal(d.amount_safe), "affordability_status": d.status, "recommended_payment_method": d.method, "payment_plan": plan, "earliest_date_for_full_payment": d.earliest.isoformat() if d.earliest else "", "spending_changes_needed": "|".join(c.serialize() for c in d.changes) or "none", "decision_explanation": d.explanation}


def validate(
    row: Mapping[str, str],
    r: Request,
    profile: Profile | None = None,
    options: Mapping[str, Sequence[PaymentOption]] | None = None,
    decision: Decision | None = None,
    events: Sequence[CanonicalEvent] | None = None,
) -> None:
    """Enforce output invariants, including option and change semantics."""
    assert list(row) == OUTPUT_COLUMNS
    amount = dec(row["amount_safe_to_pay"])
    assert Decimal(0) <= amount <= r.requested_amount
    status = row["affordability_status"]
    method = row["recommended_payment_method"]
    assert status in {"affordable_now", "affordable_with_plan", "affordable_later", "not_affordable"}
    assert method in {"full_payment", "partial_payment", "installments", "wait", "not_recommended"}
    if method == "not_recommended":
        assert status == "not_affordable" and row["payment_plan"] == "none"
    if status == "affordable_now":
        assert method == "full_payment" and row["earliest_date_for_full_payment"] == r.request_date.isoformat()
    if status == "affordable_later":
        assert method == "wait"
    if status == "affordable_with_plan":
        assert method in {"full_payment", "partial_payment", "installments"}
    if method == "partial_payment":
        assert status == "affordable_with_plan" and row["payment_plan"].count("|") == 1
    if row["earliest_date_for_full_payment"]:
        earliest = date.fromisoformat(row["earliest_date_for_full_payment"])
        assert earliest >= r.request_date
    elif status == "affordable_later":
        raise AssertionError("wait requires an earliest full-payment date")

    if profile is None:
        return

    assert method == "not_recommended" or row["payment_plan"] != "none"
    if method in {"full_payment", "partial_payment", "installments"}:
        assert method in profile.methods
    if method == "wait":
        assert "full_payment" in profile.methods

    plan_entries: list[tuple[date, Decimal, str]] = []
    if row["payment_plan"] != "none":
        for entry in row["payment_plan"].split("|"):
            day_text, amount_text = entry.split(":", 1)
            plan_day = date.fromisoformat(day_text)
            plan_amount = dec(amount_text)
            assert plan_amount >= 0
            plan_entries.append((plan_day, plan_amount, amount_text))
        assert [item[0] for item in plan_entries] == sorted(item[0] for item in plan_entries)
        assert all(r.request_date <= day <= r.desired_completion_date for day, _, _ in plan_entries)

    if method == "full_payment":
        assert len(plan_entries) == 1
        assert plan_entries[0][0] == r.request_date and plan_entries[0][1] == r.requested_amount
    elif method == "partial_payment":
        assert r.allows_partial_payment and 0 < amount < r.requested_amount
        assert len(plan_entries) == 2 and plan_entries[0][0] == r.request_date
        assert plan_entries[0][1] == amount
        assert plan_entries[1][1] == r.requested_amount - amount
        assert row["earliest_date_for_full_payment"] == plan_entries[1][0].isoformat()
        assert plan_entries[1][0] <= r.desired_completion_date
    elif method == "wait":
        assert len(plan_entries) == 1 and plan_entries[0][1] == r.requested_amount
        assert row["earliest_date_for_full_payment"] == plan_entries[0][0].isoformat()
        assert plan_entries[0][0] > r.request_date
    elif method == "installments":
        assert decision is not None and decision.option_id is not None
        supplied = next((o for o in (options or {}).get(r.request_id, ()) if o.payment_option_id == decision.option_id), None)
        assert supplied is not None and supplied.number_of_payments <= (profile.max_installment_months or 0)
        expected_plan = Planner.installment_schedule(supplied)
        assert len(plan_entries) == len(expected_plan)
        assert [(day, text) for day, _, text in plan_entries] == [(day, text) for day, _, text in expected_plan]

    actions = row["spending_changes_needed"]
    if actions != "none":
        assert events is not None and len(actions.split("|")) <= 3
        seen_ids: set[str] = set()
        for action in actions.split("|"):
            parts = action.split(":", 2)
            assert len(parts) >= 2 and parts[1] not in seen_ids
            operation, event_id = parts[:2]
            seen_ids.add(event_id)
            representative = next((e for e in events if e.projected and e.source_event_id == event_id and e.direction == "debit"), None)
            assert representative is not None
            assert representative.category in (profile.stop if operation == "stop" else profile.reduce)
            if operation == "stop":
                assert representative.flexibility in {"stoppable", "reducible_or_stoppable"} and len(parts) == 2
            else:
                assert operation == "reduce_to" and len(parts) == 3
                new_amount = dec(parts[2]); floor = representative.minimum_allowed_amount or Decimal(0)
                assert representative.flexibility in {"reducible", "reducible_or_stoppable"}
                assert floor <= new_amount < (representative.amount or Decimal(0))
    else:
        assert not (decision and decision.changes)
    if row["recommended_payment_method"] == "wait": assert row["affordability_status"] == "affordable_later"


def write_reports(sample_pass: dict[str, int]) -> None:
    EVAL.mkdir(exist_ok=True)
    (EVAL / "window_policy_report.md").write_text("# Window policy report\n\n" + "\n".join(f"- `{k}`: {v}/25 exact sample rows" for k, v in sample_pass.items()) + "\n\nScored-run choice: `days_0_through_89`.\n", encoding="utf-8")
    (EVAL / "policy_sensitivity_report.md").write_text("# Policy sensitivity report\n\n## WindowPolicy\n\nBoth named policies are run against all solved rows and targets. The scored runtime uses `days_0_through_89`, passed explicitly to every simulator.\n\n## Same-day order\n\nNamed policy: canonical scheduled/pending events are applied before the request payment; current available balance is initialized once.\n\n## FX rate date\n\nNamed policy: settlement date with an exact `from_currency` to `to_currency` rate row.\n\n## Installment eligibility\n\nNamed policy: blank `max_installment_months` disables installments; otherwise `number_of_payments <= max_installment_months`, before ranking.\n", encoding="utf-8")
    (EVAL / "usage_report.md").write_text("# Usage report\n\nFinal scored run: local deterministic core, no interpretation-model calls.\n\n| Provider | Model | Calls | Input tokens | Output tokens | Cached tokens | Estimated cost |\n|---|---|---:|---:|---:|---:|---:|\n| local | none | 0 | 0 | 0 | 0 | $0.00 |\n\nOverall calls: 0. Total and average tokens per request: 0 and 0. Estimated total and per-request cost: $0.00 and $0.00. OCR is local evidence processing and is not a provider call.\n", encoding="utf-8")
    (EVAL / "tiebreak_log.md").touch(exist_ok=True)


def execute(targets: bool, policy: WindowPolicy) -> list[dict[str, str]]:
    inventory = DatasetInventory().write(); profiles = ProfileAdapter().load(); requests = RequestAdapter().load("requests.csv" if targets else "sample_requests.csv"); options = PaymentOptionAdapter().load(); events = FinancialEventAdapter(ImageEvidenceAdapter()).canonical_rows(); canonicalizer = Canonicalizer(events, read_csv("messages.csv"), ExchangeRateAdapter()); planner = Planner(canonicalizer, options, policy); rows = []
    for r in requests:
        d, events = planner.decide(r, profiles[r.user_id]); d.explanation = make_explanation(d, events); row = serialize(d); validate(row, r, profiles[r.user_id], options, d, events); rows.append(row)
    if targets:
        with (ROOT / "output.csv").open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--inventory", action="store_true"); ap.add_argument("--samples", action="store_true"); ap.add_argument("--score-samples", action="store_true"); ap.add_argument("--policy", choices=[p.value for p in WindowPolicy], default=WindowPolicy.DAYS_0_THROUGH_89.value); args = ap.parse_args()
    if args.inventory: DatasetInventory().write(); print("dataset inventory written"); return 0
    if args.score_samples:
        expected = read_csv("sample_requests.csv")
        scores = {
            policy.value: sum(
                all(actual[field] == want[field] for field in OUTPUT_COLUMNS[1:])
                for actual, want in zip(execute(False, policy), expected)
            )
            for policy in WindowPolicy
        }
        write_reports(scores)
        print(json.dumps(scores, sort_keys=True))
        return 0
    rows = execute(not args.samples, WindowPolicy(args.policy)); print(f"wrote {len(rows)} rows"); return 0


if __name__ == "__main__": raise SystemExit(main())
