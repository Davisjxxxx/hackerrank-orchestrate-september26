"""Bounded, evaluation-only search over recurrence chronology and debit completion.

This module deliberately keeps the production ``main.py`` untouched.  It uses
the solved sample file only in the scoring harness, never in the candidate
canonicalizer.
"""
from __future__ import annotations

import csv
import itertools
import json
import statistics
import sys
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


FIELDS = main.OUTPUT_COLUMNS[1:]
WINDOW = main.WindowPolicy.DAYS_0_THROUGH_89
AMOUNT_NAMES = ("latest", "median", "mean", "max", "min")


def cash_date(e: main.CanonicalEvent) -> date:
    return e.settlement_date or e.event_date


def amount_estimator(values: list[Decimal], name: str) -> Decimal:
    values = list(values)
    if name == "latest":
        return values[-1]
    if name == "median":
        return statistics.median(values).quantize(Decimal("0.01"))
    if name == "mean":
        return (sum(values, Decimal(0)) / Decimal(len(values))).quantize(Decimal("0.01"))
    if name == "max":
        return max(values)
    if name == "min":
        return min(values)
    raise ValueError(name)


class SearchCanonicalizer(main.Canonicalizer):
    """R0-compatible canonicalizer with explicit bounded policy switches."""

    def __init__(self, events, messages, fx, params):
        super().__init__(events, messages, fx)
        self.params = params
        self.diagnostics: dict[str, list[dict[str, object]]] = {}

    def recurrence_date(self, e: main.CanonicalEvent) -> date:
        return e.event_date if self.params["chronology"] == "A0" else cash_date(e)

    def cadence(self, history: list[main.CanonicalEvent]) -> tuple[str, int]:
        ds = sorted(self.recurrence_date(e) for e in history)
        gaps = [(b - a).days for a, b in zip(ds, ds[1:])]
        if not gaps:
            return "none", 0
        monthly_lo, monthly_hi = self.params["monthly_range"]
        if all(monthly_lo <= gap <= monthly_hi for gap in gaps):
            return "month", 1
        med = int(statistics.median(gaps))
        tolerance = self.params["fixed_tolerance"]
        needed = self.params["consistent_intervals"]
        if med >= 5 and sum(abs(gap - med) <= tolerance for gap in gaps) >= needed:
            return "gap", max(1, med)
        return "none", 0

    @staticmethod
    def stream_key(e: main.CanonicalEvent) -> tuple[str, str, str, str]:
        # Deliberately preserve R0's exact-description stream base.
        return (e.event_type, e.category, e.flexibility, e.description)

    @staticmethod
    def compatible_key(e: main.CanonicalEvent) -> tuple[str, str, str, str, str, str]:
        return (e.event_type, e.category, e.direction, e.currency, e.flexibility, e.description)

    def projected_amount(self, history: list[main.CanonicalEvent]) -> Decimal:
        ordered = sorted(history, key=lambda e: (cash_date(e), e.event_id))
        values = [e.amount for e in ordered[-3:] if e.amount is not None]
        return amount_estimator(values, self.params["debit_amount"] if ordered[-1].direction == "debit" else self.params["credit_amount"])

    def _future_day(self, anchor: date, kind: str, step: int, n: int) -> date:
        return main.add_months(anchor, n) if kind == "month" else anchor + timedelta(days=step * n)

    def for_request(self, request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        horizon = request.request_date + timedelta(days=policy.upper_bound_offset())
        rows = self.message_adjustments(request.user_id, self.by_user.get(request.user_id, []), request.request_date)
        valid = [e for e in rows if e.status not in {"failed", "cancelled", "unrealized"} and e.direction != "non_cash"]
        groups: dict[tuple[str, str, str, str], list[main.CanonicalEvent]] = {}
        for e in valid:
            cutoff = self.recurrence_date(e) < request.request_date if self.params["chronology"] != "A0" else e.event_date <= request.request_date
            if e.amount is not None and cutoff:
                groups.setdefault(self.stream_key(e), []).append(e)

        explicit: list[main.CanonicalEvent] = []
        explicit_keys: set[tuple[tuple[str, str, str, str], date]] = set()
        for e in valid:
            d = cash_date(e)
            if d < request.request_date or d > horizon:
                continue
            if e.status == "settled" and d == request.request_date:
                continue
            explicit.append(e)
            explicit_keys.add((self.stream_key(e), d))

        terminal_semantics = {
            (e.event_type, e.category, e.flexibility)
            for e in valid
            if any(marker in e.description.lower() for marker in ("final", "last payroll", "employment ended", "contract ended"))
        }
        projected: list[main.CanonicalEvent] = []
        for key, history in sorted(groups.items()):
            if (key[0], key[1], key[2]) in terminal_semantics:
                continue
            kind, step = self.cadence(history)
            if kind == "none":
                continue
            ordered = sorted(history, key=lambda e: (cash_date(e), e.event_id))
            latest = ordered[-1]
            amount = self.projected_amount(ordered)
            anchor_event = latest
            anchor = cash_date(latest)
            if self.params["chronology"] == "A2":
                future_same = [e for e in explicit if self.compatible_key(e) == self.compatible_key(latest)]
                if future_same:
                    anchor_event = max(future_same, key=lambda e: (cash_date(e), e.event_id))
                    anchor = cash_date(anchor_event)
                    amount = anchor_event.amount if anchor_event.amount is not None else amount
            n = 1
            while True:
                d = self._future_day(anchor, kind, step, n)
                if d > horizon:
                    break
                if d >= request.request_date and (key, d) not in explicit_keys:
                    projected.append(replace(anchor_event, event_id=f"{anchor_event.event_id}@{d.isoformat()}", event_date=d, settlement_date=d, amount=amount, projected=True, source_event_id=anchor_event.event_id, status="scheduled", provenance=f"search:{self.params['chronology']}:{self.params['debit_amount']}/{self.params['credit_amount']}"))
                n += 1

        # Preserve R0's explicit confirmed-salary continuation semantics.
        if not any(e[0] == "income" and e[1] == "salary" and e[2] == "fixed" for e in terminal_semantics):
            future_salary = [e for e in explicit if e.event_type == "income" and e.category == "salary" and e.amount is not None]
            if future_salary:
                anchor_event = max(future_salary, key=lambda e: (cash_date(e), e.event_id))
                anchor = cash_date(anchor_event)
                n = 1
                while True:
                    d = main.add_months(anchor, n)
                    if d > horizon:
                        break
                    if d >= request.request_date and not any(e.event_type == "income" and e.category == "salary" and cash_date(e) == d for e in explicit + projected):
                        projected.append(replace(anchor_event, event_id=f"{anchor_event.event_id}@{d.isoformat()}", event_date=d, settlement_date=d, projected=True, source_event_id=anchor_event.event_id, status="scheduled", provenance="search:confirmed_salary"))
                    n += 1

        explicit_salary_keys = {(e.user_id, e.event_type, e.category, e.direction, e.currency, e.flexibility, cash_date(e)) for e in explicit if e.category == "salary" and not e.projected}
        projected = [e for e in projected if not (e.category == "salary" and e.projected and (e.user_id, e.event_type, e.category, e.direction, e.currency, e.flexibility, cash_date(e)) in explicit_salary_keys)]
        base = sorted(explicit + projected, key=lambda e: (cash_date(e), e.event_id))
        changes = []
        if self.params["shortfall"]:
            base, changes = self.add_debit_shortfalls(request, horizon, valid, base)
        self.diagnostics[request.request_id] = changes
        return base

    def _bucket(self, anchor: date, kind: str, step: int, d: date) -> int:
        if kind == "month":
            return 12 * (d.year - anchor.year) + d.month - anchor.month
        return (d - anchor).days // step

    def _bucket_bounds(self, anchor: date, kind: str, step: int, index: int) -> tuple[date, date]:
        if kind == "month":
            start = main.add_months(date(anchor.year, anchor.month, 1), index)
            end = main.add_months(start, 1) - timedelta(days=1)
        else:
            start = anchor + timedelta(days=index * step)
            end = start + timedelta(days=step - 1)
        return start, end

    def _phase_date(self, anchor: date, kind: str, step: int, index: int, history: list[main.CanonicalEvent]) -> date:
        ds = [cash_date(e) for e in history]
        if kind == "month":
            day_values = [d.day for d in ds]
            if self.params["phase"] == "latest":
                day = day_values[-1]
            elif self.params["phase"] == "median":
                day = int(statistics.median(day_values))
            else:
                day = min(day_values)
            start = main.add_months(date(anchor.year, anchor.month, 1), index)
            next_start = main.add_months(start, 1)
            return min(start.replace(day=day), next_start - timedelta(days=1))
        offsets = [((d - anchor).days % step) for d in ds]
        if self.params["phase"] == "latest":
            offset = offsets[-1]
        elif self.params["phase"] == "median":
            offset = int(statistics.median(offsets))
        else:
            offset = min(offsets)
        return anchor + timedelta(days=index * step + offset)

    def add_debit_shortfalls(self, request, horizon, valid, base):
        historical = [e for e in valid if e.direction == "debit" and e.amount is not None and cash_date(e) < request.request_date]
        groups: dict[tuple[str, str, str, str, str], list[main.CanonicalEvent]] = {}
        for e in historical:
            groups.setdefault((e.event_type, e.category, e.currency, e.flexibility, e.user_id), []).append(e)
        out = list(base)
        diagnostics = []
        for gkey, history in sorted(groups.items()):
            kind, step = self.cadence(history)
            if kind == "none":
                continue
            if len(history) < 3:
                continue
            ordered = sorted(history, key=lambda e: (cash_date(e), e.event_id))
            anchor = cash_date(ordered[0])
            buckets: dict[int, Decimal] = {}
            for e in ordered:
                idx = self._bucket(anchor, kind, step, cash_date(e))
                buckets[idx] = buckets.get(idx, Decimal(0)) + (e.amount or Decimal(0))
            complete = []
            for idx, total in buckets.items():
                _, end = self._bucket_bounds(anchor, kind, step, idx)
                if end < request.request_date:
                    complete.append((idx, total))
            complete.sort()
            window = self.params["periods"]
            if len(complete) < window:
                continue
            recent = [total for _, total in complete[-window:]]
            expected = amount_estimator(recent, self.params["period_estimator"])
            future_indices = []
            first_idx = self._bucket(anchor, kind, step, request.request_date)
            last_idx = self._bucket(anchor, kind, step, horizon)
            for idx in range(first_idx, last_idx + 1):
                start, end = self._bucket_bounds(anchor, kind, step, idx)
                if end < request.request_date or start > horizon:
                    continue
                future_indices.append(idx)
            for idx in future_indices:
                start, end = self._bucket_bounds(anchor, kind, step, idx)
                day = self._phase_date(anchor, kind, step, idx, ordered)
                if day < request.request_date or day > horizon:
                    continue
                dims = (gkey[0], gkey[1], "debit", gkey[2], gkey[3])
                represented = sum((e.amount or Decimal(0) for e in out if e.direction == "debit" and (e.event_type, e.category, e.direction, e.currency, e.flexibility) == dims and cash_date(e) == day), Decimal(0))
                explicit_total = sum((e.amount or Decimal(0) for e in out if not e.projected and e.direction == "debit" and (e.event_type, e.category, e.direction, e.currency, e.flexibility) == dims and start <= cash_date(e) <= end), Decimal(0))
                projected_total = sum((e.amount or Decimal(0) for e in out if e.projected and e.direction == "debit" and (e.event_type, e.category, e.direction, e.currency, e.flexibility) == dims and start <= cash_date(e) <= end), Decimal(0))
                shortfall = expected - explicit_total - projected_total
                if shortfall <= 0:
                    continue
                template = ordered[-1]
                synthetic = replace(template, event_id=f"category_shortfall:{gkey[1]}@{day.isoformat()}", event_date=day, settlement_date=day, amount=shortfall, projected=True, source_event_id=None, status="scheduled", provenance=f"search:debit_category_shortfall:{self.params['period_estimator']}:{self.params['phase']}")
                out.append(synthetic)
                diagnostics.append({"action": "debit_category_shortfall", "category": gkey[1], "date": day.isoformat(), "amount": str(shortfall), "expected": str(expected), "periods": window, "phase": self.params["phase"]})
        return sorted(out, key=lambda e: (cash_date(e), e.event_id)), diagnostics


def metrics(actual, expected):
    signed = [main.dec(a["amount_safe_to_pay"]) - main.dec(e["amount_safe_to_pay"]) for a, e in zip(actual, expected)]
    return {
        "exact_rows": sum(all(a[f] == e[f] for f in FIELDS) for a, e in zip(actual, expected)),
        "exact_safe_amounts": sum(a["amount_safe_to_pay"] == e["amount_safe_to_pay"] for a, e in zip(actual, expected)),
        "numeric_mismatches": sum(x != 0 for x in signed),
        "absolute_safe_error": str(sum(abs(x) for x in signed)),
        "status_exact": sum(a["affordability_status"] == e["affordability_status"] for a, e in zip(actual, expected)),
        "method_exact": sum(a["recommended_payment_method"] == e["recommended_payment_method"] for a, e in zip(actual, expected)),
        "plan_exact": sum(a["payment_plan"] == e["payment_plan"] for a, e in zip(actual, expected)),
        "earliest_exact": sum(a["earliest_date_for_full_payment"] == e["earliest_date_for_full_payment"] for a, e in zip(actual, expected)),
        "optimistic": sum(x > 0 for x in signed),
        "pessimistic": sum(x < 0 for x in signed),
    }


def run_policy(params, profiles, requests, options, expected):
    events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    messages = main.read_csv("messages.csv")
    canonical = SearchCanonicalizer(events, messages, main.ExchangeRateAdapter(), params)
    planner = main.Planner(canonical, options, WINDOW)
    rows = []
    for request in requests:
        decision, used = planner.decide(request, profiles[request.user_id])
        decision.explanation = main.make_explanation(decision, used)
        row = main.serialize(decision)
        main.validate(row, request, profiles[request.user_id], options, decision, used)
        rows.append(row)
    return rows, canonical.diagnostics


def base_params(chronology, debit_amount, credit_amount, consistency, fixed_tolerance, monthly_range):
    return {"chronology": chronology, "debit_amount": debit_amount, "credit_amount": credit_amount, "consistent_intervals": consistency, "fixed_tolerance": fixed_tolerance, "monthly_range": monthly_range, "shortfall": False, "periods": 2, "period_estimator": "latest", "phase": "latest"}


def policy_label(p):
    return ";".join(f"{k}={p[k]}" for k in ("chronology", "debit_amount", "credit_amount", "consistent_intervals", "fixed_tolerance", "monthly_range", "shortfall", "periods", "period_estimator", "phase"))


def rank_key(item):
    m = item["metrics"]
    return (-m["exact_safe_amounts"], -m["exact_rows"], m["numeric_mismatches"], -m["status_exact"], -m["method_exact"], -m["plan_exact"], -m["earliest_exact"], Decimal(m["absolute_safe_error"]))


def main_run():
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    expected = main.read_csv("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    r0 = main.execute(False, WINDOW)
    r0m = metrics(r0, expected)
    results = []
    cadence_variants = [(2, 3, (27, 32)), (2, 2, (27, 32)), (2, 4, (27, 32)), (3, 3, (27, 32)), (2, 3, (26, 33)), (3, 4, (26, 33))]
    amount_pairs = [("max", "latest"), ("median", "latest"), ("latest", "latest"), ("max", "median"), ("median", "median")]
    for chronology, (debit, credit), (consistency, tolerance, monthly_range) in itertools.product(("A0", "A1", "A2"), amount_pairs, cadence_variants):
        params = base_params(chronology, debit, credit, consistency, tolerance, monthly_range)
        rows, diagnostics = run_policy(params, profiles, requests, options, expected)
        results.append({"label": policy_label(params), "params": params, "metrics": metrics(rows, expected), "diagnostics": diagnostics, "rows": rows})
    base_sorted = sorted(results, key=rank_key)
    top_bases = base_sorted[:4]
    # A bounded 48-way debit-only completion matrix over the four strongest
    # R0-preserving bases.  This stays well below the requested 500 policies.
    for base in top_bases:
        for periods, estimator, phase, consistency in itertools.product((2, 3), ("latest", "median", "mean", "max"), ("latest", "median", "earliest"), (2, 3)):
            params = dict(base["params"])
            params.update({"shortfall": True, "periods": periods, "period_estimator": estimator, "phase": phase, "consistent_intervals": consistency})
            rows, diagnostics = run_policy(params, profiles, requests, options, expected)
            results.append({"label": policy_label(params), "params": params, "metrics": metrics(rows, expected), "diagnostics": diagnostics, "rows": rows})
    ranked = sorted(results, key=rank_key)
    serial = []
    for i, item in enumerate(ranked):
        serial.append({"rank": i + 1, "label": item["label"], **item["metrics"]})
    outdir = ROOT / "evaluation"
    with (outdir / "final_recurrence_search.csv").open("w", newline="", encoding="utf-8") as fh:
        fields = ["rank", "label", "exact_rows", "exact_safe_amounts", "numeric_mismatches", "absolute_safe_error", "status_exact", "method_exact", "plan_exact", "earliest_exact", "optimistic", "pessimistic"]
        writer = csv.DictWriter(fh, fieldnames=fields); writer.writeheader(); writer.writerows(serial)
    winner = ranked[0]
    changed = []
    for candidate, baseline, want in zip(winner["rows"], r0, expected):
        if any(candidate[f] != baseline[f] for f in FIELDS):
            changed.append({"request_id": candidate["request_id"], "r0_safe": baseline["amount_safe_to_pay"], "candidate_safe": candidate["amount_safe_to_pay"], "expected_safe": want["amount_safe_to_pay"], "diagnostics": winner["diagnostics"].get(candidate["request_id"], [])})
    report = {"count": len(results), "R0": r0m, "top10": serial[:10], "winner": {"label": winner["label"], "params": winner["params"], "metrics": winner["metrics"], "changed": changed}, "best_bases": [{"label": x["label"], "metrics": x["metrics"]} for x in top_bases]}
    (outdir / "final_recurrence_search.json").write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    lines = ["# Final bounded recurrence policy search", "", f"Policies evaluated: **{len(results)}**. Production code and dataset were not modified.", "", "## Top 10", "", "| Rank | Policy | Exact rows | Exact safe | Numeric mismatches | Absolute safe error | Status | Method | Plan | Earliest | Optimistic | Pessimistic |", "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for x in serial[:10]:
        lines.append("| {rank} | `{label}` | {exact_rows}/25 | {exact_safe_amounts}/25 | {numeric_mismatches} | {absolute_safe_error} | {status_exact}/25 | {method_exact}/25 | {plan_exact}/25 | {earliest_exact}/25 | {optimistic} | {pessimistic} |".format(**x))
    lines += ["", "## Winner request-level changes", ""]
    for x in changed:
        lines.append(f"- `{x['request_id']}`: R0 `{x['r0_safe']}` -> candidate `{x['candidate_safe']}`; expected `{x['expected_safe']}`; diagnostics `{json.dumps(x['diagnostics'], sort_keys=True)}`")
    (outdir / "final_recurrence_search.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"policies": len(results), "R0": r0m, "winner": {k: winner[k] for k in ("label", "metrics")}, "top10": serial[:10]}, sort_keys=True, default=str))


if __name__ == "__main__":
    main_run()
