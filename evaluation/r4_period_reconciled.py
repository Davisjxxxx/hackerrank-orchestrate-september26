"""R4: period-reconciled R0 recurrence, evaluation-only.

R0 supplies all dates and individual inferred events.  This resolver changes
only the amount materialized inside a compatible cadence bucket.  It never
creates merchant/source identity and never adds an inferred credit.
"""
from __future__ import annotations

import statistics
from collections import defaultdict
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Iterable

import main


class EnvelopeEstimator(str, Enum):
    E1 = "R4-E1_recent_period_median"
    E2 = "R4-E2_conservative_debit_max"
    E3 = "R4-E3_recent_period_pattern"


def dimensions(event: main.CanonicalEvent) -> tuple[str, ...]:
    return (event.event_type, event.category, event.direction, event.currency, event.flexibility)


def supported_cadence(rows: list[main.CanonicalEvent]) -> tuple[str, int] | None:
    days = sorted(e.settlement_date or e.event_date for e in rows)
    if len(days) < 2:
        return None
    gaps = [(b - a).days for a, b in zip(days, days[1:])]
    if all(27 <= gap <= 32 for gap in gaps):
        return "month", 1
    if len(days) < 3:
        return None
    med = int(statistics.median(gaps))
    if med >= 7 and sum(abs(gap - med) <= 3 for gap in gaps) >= 2:
        return "gap", med
    return None


def month_index(day: date) -> int:
    return day.year * 12 + day.month


def bucket_for(day: date, cadence: tuple[str, int], origin: date) -> int:
    kind, step = cadence
    return month_index(day) if kind == "month" else (day - origin).days // step


class PeriodReconciledCanonicalizer:
    """Compatibility adapter around R0 with amount-only period reconciliation."""

    def __init__(self, events: list[main.CanonicalEvent], messages: list[dict[str, str]], fx: main.ExchangeRateAdapter, estimator: EnvelopeEstimator) -> None:
        self.base = main.Canonicalizer(events, messages, fx)
        self.events = events
        self.messages = messages
        self.fx = fx
        self.estimator = estimator
        self.envelope_diagnostics: dict[str, dict[str, object]] = {}

    def converted(self, event: main.CanonicalEvent, profile: main.Profile) -> Decimal | None:
        return self.base.converted(event, profile)

    @staticmethod
    def _valid(rows: Iterable[main.CanonicalEvent]) -> list[main.CanonicalEvent]:
        return [e for e in rows if e.status not in {"failed", "cancelled", "unrealized"} and e.direction != "non_cash" and e.amount is not None]

    def _envelope(self, historical: list[main.CanonicalEvent], projected: list[main.CanonicalEvent], explicit: list[main.CanonicalEvent], request: main.Request, horizon: date) -> list[main.CanonicalEvent]:
        by_dim_history: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        by_dim_projected: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in historical:
            by_dim_history[dimensions(event)].append(event)
        for event in projected:
            by_dim_projected[dimensions(event)].append(event)

        changed: list[main.CanonicalEvent] = []
        diagnostics: dict[str, object] = {}
        for dim, future in sorted(by_dim_projected.items()):
            hist = by_dim_history.get(dim, [])
            cadence = supported_cadence(hist)
            if cadence is None:
                diagnostics["|".join(dim)] = {"state": "NOT_APPLICABLE", "reason": "cadence_or_two_period_prerequisite"}
                changed.extend(future)
                continue
            kind, step = cadence
            origin = min((e.settlement_date or e.event_date) for e in hist)
            historical_buckets: dict[int, Decimal] = defaultdict(lambda: Decimal(0))
            for event in hist:
                historical_buckets[bucket_for(event.settlement_date or event.event_date, cadence, origin)] += event.amount or Decimal(0)
            if len(historical_buckets) < 2:
                diagnostics["|".join(dim)] = {"state": "NOT_APPLICABLE", "reason": "fewer_than_two_comparable_periods"}
                changed.extend(future)
                continue
            comparable = [value for _, value in sorted(historical_buckets.items())[-3:]]
            if self.estimator is EnvelopeEstimator.E1:
                envelope = Decimal(str(statistics.median(comparable)))
            elif self.estimator is EnvelopeEstimator.E2 and dim[2] == "debit":
                envelope = max(comparable)
            else:
                envelope = comparable[-1]
            future_buckets: dict[int, list[main.CanonicalEvent]] = defaultdict(list)
            for event in future:
                future_buckets[bucket_for(event.settlement_date or event.event_date, cadence, origin)].append(event)
            dim_diag = {"state": "PASS", "cadence": cadence, "historical_periods": len(historical_buckets), "comparable_totals": [str(x) for x in comparable], "buckets": []}
            for bucket, bucket_events in sorted(future_buckets.items()):
                total = sum((e.amount or Decimal(0) for e in bucket_events), Decimal(0))
                residual = envelope - total
                action = "none"
                if dim[2] == "debit" and residual > 0:
                    anchor = min(bucket_events, key=lambda e: ((e.settlement_date or e.event_date), e.event_id))
                    changed.extend(bucket_events)
                    changed.append(main.CanonicalEvent(f"aggregate_recurring_reserve:{request.request_id}:{bucket}", request.user_id, anchor.event_type, "aggregate recurring reserve", anchor.category, "debit", residual.quantize(Decimal("0.01")), anchor.currency, anchor.event_date, anchor.settlement_date, "scheduled", "fixed", None, projected=True, source_event_id=None, provenance=f"R4:{self.estimator.value}:aggregate_recurring_reserve"))
                    action = "add_debit_reserve"
                elif residual < 0 and (dim[2] == "debit" or dim[2] == "credit"):
                    # Only inferred rows are eligible.  Preserve every date
                    # and dimension while scaling the inferred amounts to the
                    # evidence-supported envelope.  Explicit rows never enter
                    # this list and are therefore never capped.
                    if total > 0 and envelope >= 0:
                        factor = envelope / total
                        changed.extend(replace(e, amount=((e.amount or Decimal(0)) * factor).quantize(Decimal("0.01")), provenance=f"{e.provenance}+R4:{self.estimator.value}:period_cap") for e in bucket_events)
                        action = "cap_inferred_period"
                    else:
                        changed.extend(bucket_events)
                else:
                    changed.extend(bucket_events)
                dim_diag["buckets"].append({"bucket": bucket, "r0_projected": str(total), "envelope": str(envelope), "residual": str(residual), "action": action, "dates": [(e.settlement_date or e.event_date).isoformat() for e in bucket_events]})
            diagnostics["|".join(dim)] = dim_diag
        self.envelope_diagnostics[request.request_id] = diagnostics
        return changed

    def for_request(self, request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        horizon = request.request_date + timedelta(days=policy.upper_bound_offset())
        base_events = self.base.for_request(request, profile, policy)
        explicit = [e for e in base_events if not e.projected]
        projected = [e for e in base_events if e.projected]
        # Evidence-supported same-dimension/date replacement prevents a
        # confirmed future obligation from being double-counted, while keeping
        # all explicit records intact.  Description equality is not required.
        explicit_keys = {(dimensions(e), e.settlement_date or e.event_date) for e in explicit}
        projected = [e for e in projected if (dimensions(e), e.settlement_date or e.event_date) not in explicit_keys]
        raw = self._valid(self.base.message_adjustments(request.user_id, self.base.by_user.get(request.user_id, []), request.request_date))
        historical = [e for e in raw if (e.settlement_date or e.event_date) < request.request_date]
        adjusted = self._envelope(historical, projected, explicit, request, horizon)
        return sorted(explicit + adjusted, key=lambda e: ((e.settlement_date or e.event_date), e.event_id))
