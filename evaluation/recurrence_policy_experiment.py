#!/usr/bin/env python3
"""Ablate recurrence-stream identities against the 25 public solved rows.

This is an analysis harness.  It does not change ``code/main.py`` or use the
solved values as production input.  Every policy is evaluated with history
bounded at the request date and with the existing independent simulators and
planner.
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


VARIABLE_CATEGORIES = {"groceries", "transport", "dining"}
MONTHS = {
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
}
GENERIC_WORDS = {
    "a", "an", "and", "card", "charge", "payment", "purchase", "service",
    "the", "transaction", "transfer",
}
FIXED_CADENCE_STEPS = (5, 7, 10, 14, 21)


def effective_day(event: main.CanonicalEvent) -> date:
    return event.settlement_date or event.event_date


def normalized_description(text: str) -> str:
    value = text.lower()
    value = re.sub(r"\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}\b", " ", value)
    value = re.sub(r"\b(?:ref|reference|txn|transaction|id|no)\s*[-:#]?\s*[a-z0-9-]+\b", " ", value)
    value = re.sub(r"\b\d+\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def description_family(text: str) -> str:
    """Conservative text family: remove only demonstrably superficial words."""
    value = normalized_description(text)
    words = [word for word in value.split() if word not in GENERIC_WORDS and word not in MONTHS]
    return " ".join(words)


def cadence_for(events: Iterable[main.CanonicalEvent]) -> tuple[str, int]:
    # Recurrence evidence is observed on event_date.  Settlement_date remains
    # the cash-flow date in the simulator; using it here would let a delayed
    # settlement reshape an already-observed spending cadence.
    days = sorted(event.event_date for event in events)
    gaps = [(b - a).days for a, b in zip(days, days[1:]) if (b - a).days > 0]
    if not gaps:
        return "none", 0
    median = int(statistics.median(gaps))
    if all(27 <= gap <= 32 for gap in gaps):
        return "month", 1
    if max(gaps) - min(gaps) <= 2 and median >= 5:
        return "gap", max(1, median)
    return "none", 0


def sequence_clusters(events: list[main.CanonicalEvent]) -> list[list[main.CanonicalEvent]]:
    """Extract active, non-overlapping temporal sequences from one bucket."""
    remaining = {event.event_id: event for event in events}
    candidates: list[list[main.CanonicalEvent]] = []
    for step in FIXED_CADENCE_STEPS:
        phases: dict[int, list[main.CanonicalEvent]] = defaultdict(list)
        for event in events:
            phases[event.event_date.toordinal() % step].append(event)
        candidates.extend(group for group in phases.values() if len(group) >= 3 and cadence_for(group)[0] != "none")
    month_phases: dict[int, list[main.CanonicalEvent]] = defaultdict(list)
    for event in events:
        month_phases[event.event_date.day].append(event)
    candidates.extend(group for group in month_phases.values() if len(group) >= 3 and cadence_for(group)[0] == "month")
    selected: list[list[main.CanonicalEvent]] = []
    while remaining:
        available = [
            [remaining[event.event_id] for event in candidate if event.event_id in remaining]
            for candidate in candidates
        ]
        available = [group for group in available if len(group) >= 3 and cadence_for(group)[0] != "none"]
        if not available:
            break
        group = max(available, key=lambda candidate: (len(candidate), cadence_for(candidate)[0] == "month"))
        selected.append(sorted(group, key=lambda event: event.event_date))
        for event in group:
            remaining.pop(event.event_id, None)
    return selected


def semantic_key(event: main.CanonicalEvent) -> tuple[str, ...]:
    # Currency is an observed structural boundary.  The caller already
    # partitions by user, so user_id is represented by the request scope.
    return (event.event_type, event.direction, event.category, event.currency, event.flexibility)


def policy_key(policy: str, event: main.CanonicalEvent) -> tuple[str, ...]:
    base = semantic_key(event)
    if policy == "A_exact_normalized_description":
        return base + (normalized_description(event.description),)
    if policy == "C_description_family":
        return base + (description_family(event.description),)
    if policy == "G_variable_category_fallback":
        if event.category in VARIABLE_CATEGORIES:
            return base
        return base + (normalized_description(event.description),)
    if policy == "H_sequence_phase_partition":
        return base
    if policy == "I_phase_aware_active":
        return base
    return base


def cluster_history(policy: str, history: list[main.CanonicalEvent]) -> dict[tuple[str, ...], list[main.CanonicalEvent]]:
    by_semantic: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
    for event in history:
        by_semantic[semantic_key(event)].append(event)

    if policy in {"A_exact_normalized_description", "C_description_family", "B_broad_category", "G_variable_category_fallback"}:
        groups: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in history:
            groups[policy_key(policy, event)].append(event)
        return groups

    groups = {}
    for semantic, events in by_semantic.items():
        if policy == "E_cadence_assisted":
            kind, _ = cadence_for(events)
            if kind == "none":
                # A rejected group is retained for diagnostics but cannot be
                # projected by the caller.
                groups[semantic + ("__rejected__",)] = events
            else:
                groups[semantic] = events
            continue

        if policy == "D_structural_cadence":
            # Preserve independent phases when a semantic category contains
            # simultaneous obligations.  The phase is derived from the
            # observed date modulo the inferred gap; it is not an event ID.
            kind, step = cadence_for(events)
            if kind == "none":
                groups[semantic + ("__rejected__",)] = events
            else:
                phase_groups: dict[int, list[main.CanonicalEvent]] = defaultdict(list)
                for event in events:
                    day_number = effective_day(event).toordinal()
                    phase_groups[day_number % step].append(event)
                for phase, phase_events in phase_groups.items():
                    groups[semantic + (f"phase:{phase}",)] = phase_events
            continue

        if policy == "F_amount_supported":
            # Amount is supporting evidence only: split a semantic group when
            # it has multiple stable amount modes, while keeping variable
            # streams together.  A Decimal amount is never the sole identity.
            amount_groups: dict[str, list[main.CanonicalEvent]] = defaultdict(list)
            values = [event.amount for event in events if event.amount is not None]
            if values and max(values) == min(values):
                amount_groups["fixed"] = events
            else:
                amount_groups["variable"] = events
            for label, amount_events in amount_groups.items():
                groups[semantic + (f"amount:{label}",)] = amount_events
            continue

        if policy in {"H_sequence_phase_partition", "I_phase_aware_active"}:
            for index, sequence in enumerate(sequence_clusters(events)):
                groups[semantic + (f"sequence:{index}",)] = sequence
            continue

    return groups


class ExperimentCanonicalizer(main.Canonicalizer):
    def __init__(self, *args: Any, recurrence_policy: str) -> None:
        super().__init__(*args)
        self.recurrence_policy = recurrence_policy

    def for_request(self, request: main.Request, profile: main.Profile, policy: main.WindowPolicy) -> list[main.CanonicalEvent]:
        horizon = request.request_date + timedelta(days=policy.upper_bound_offset())
        rows = self.message_adjustments(request.user_id, self.by_user.get(request.user_id, []), request.request_date)
        valid = [event for event in rows if event.status not in {"failed", "cancelled", "unrealized"} and event.direction != "non_cash"]
        history = [event for event in valid if event.amount is not None and event.event_date <= request.request_date]
        groups = cluster_history(self.recurrence_policy, history)
        explicit: list[main.CanonicalEvent] = []
        explicit_keys: set[tuple[tuple[str, ...], date]] = set()
        for event in valid:
            day = effective_day(event)
            if not request.request_date <= day <= horizon:
                continue
            if event.status == "settled" and day == request.request_date:
                continue
            explicit.append(event)
            identity = policy_key(self.recurrence_policy, event)
            if self.recurrence_policy in {"H_sequence_phase_partition", "I_phase_aware_active"}:
                history_group_keys = cluster_history(self.recurrence_policy, history)
                identity = next((key for key, group in history_group_keys.items() if any(item.event_id == event.event_id for item in group)), identity)
            explicit_keys.add((identity, day))
        terminal = {
            semantic_key(event)
            for event in valid
            if any(marker in event.description.lower() for marker in ("final", "last payroll", "employment ended", "contract ended"))
        }
        projected: list[main.CanonicalEvent] = []
        for key, events in sorted(groups.items()):
            semantic = semantic_key(events[0])
            if semantic in terminal or key[-1] == "__rejected__":
                continue
            kind, step = cadence_for(events)
            if kind == "none":
                continue
            if self.recurrence_policy == "I_phase_aware_active":
                latest_observed = max(event.event_date for event in events)
                expected_next = main.add_months(latest_observed, 1) if kind == "month" else latest_observed + timedelta(days=step)
                if request.request_date > expected_next + timedelta(days=max(2, step)):
                    continue
            latest = max(events, key=effective_day)
            recent = sorted(events, key=effective_day)[-3:]
            amount = max(event.amount for event in recent if event.amount is not None)
            n = 1
            while True:
                anchor = effective_day(latest)
                day = main.add_months(anchor, n) if kind == "month" else anchor + timedelta(days=step * n)
                if day > horizon:
                    break
                if day >= request.request_date and (key, day) not in explicit_keys:
                    projected.append(replace(latest, event_id=f"{latest.event_id}@{day.isoformat()}", event_date=day, settlement_date=day, amount=amount, projected=True, source_event_id=latest.event_id, status="scheduled", provenance=f"experiment:{self.recurrence_policy}"))
                n += 1
        return sorted(explicit + projected, key=lambda event: (effective_day(event), event.event_id))


def output_for(policy: str, requests: list[main.Request], profiles: dict[str, main.Profile], options: dict[str, list[main.PaymentOption]], canon_args: tuple[Any, ...]) -> list[dict[str, str]]:
    canon = ExperimentCanonicalizer(*canon_args, recurrence_policy=policy)
    planner = main.Planner(canon, options, main.WindowPolicy.DAYS_0_THROUGH_89)
    rows = []
    for request in requests:
        decision, _ = planner.decide(request, profiles[request.user_id])
        decision.explanation = main.make_explanation(decision, canon.for_request(request, profiles[request.user_id], main.WindowPolicy.DAYS_0_THROUGH_89))
        rows.append(main.serialize(decision))
    return rows


def output_for_current(requests: list[main.Request], profiles: dict[str, main.Profile], options: dict[str, list[main.PaymentOption]], canon_args: tuple[Any, ...]) -> list[dict[str, str]]:
    canon = main.Canonicalizer(*canon_args)
    planner = main.Planner(canon, options, main.WindowPolicy.DAYS_0_THROUGH_89)
    rows = []
    for request in requests:
        decision, events = planner.decide(request, profiles[request.user_id])
        decision.explanation = main.make_explanation(decision, events)
        rows.append(main.serialize(decision))
    return rows


def exact_stats(actual: list[dict[str, str]], expected: list[dict[str, str]]) -> tuple[int, int, dict[str, list[str]]]:
    columns = main.OUTPUT_COLUMNS
    exact = sum(all(left[column] == right[column] for column in columns) for left, right in zip(actual, expected))
    differing = sum(left[column] != right[column] for left, right in zip(actual, expected) for column in columns)
    improvements = {column: [] for column in columns}
    for left, right in zip(actual, expected):
        for column in columns:
            if left[column] == right[column]:
                improvements[column].append(left["request_id"])
    return exact, differing, improvements


def recurrence_diagnostics(policy: str, requests: list[main.Request], canon_args: tuple[Any, ...]) -> dict[str, int]:
    raw = main.Canonicalizer(*canon_args)
    false_merge = false_split = 0
    for request in requests:
        rows = raw.message_adjustments(request.user_id, raw.by_user.get(request.user_id, []), request.request_date)
        history = [event for event in rows if event.amount is not None and effective_day(event) < request.request_date and event.status not in {"failed", "cancelled", "unrealized"} and event.direction != "non_cash"]
        groups = cluster_history(policy, history)
        for events in groups.values():
            descriptions = {description_family(event.description) for event in events}
            days = [effective_day(event) for event in events]
            if len(descriptions) > 1 and len(days) != len(set(days)):
                false_merge += 1
        semantic_groups: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in history:
            semantic_groups[semantic_key(event)].append(event)
        for events in semantic_groups.values():
            kind, step = cadence_for(events)
            if kind == "none":
                continue
            policy_groups = [group for group in cluster_history(policy, events).values() if len(group) >= 1]
            if len(policy_groups) > 1:
                false_split += 1
    return {"false_merge_proxy": false_merge, "false_split_proxy": false_split}


def main_entry() -> int:
    images = main.ImageEvidenceAdapter()
    event_adapter = main.FinancialEventAdapter(images)
    canon_args = (event_adapter.canonical_rows(), main.MessageEvidenceAdapter().rows, main.ExchangeRateAdapter())
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    expected = list(csv.DictReader((main.DATA / "sample_requests.csv").open(newline="", encoding="utf-8")))
    options = main.PaymentOptionAdapter().load()
    policies = [
        "A_exact_normalized_description",
        "B_broad_category",
        "C_description_family",
        "D_structural_cadence",
        "E_cadence_assisted",
        "F_amount_supported",
        "G_variable_category_fallback",
        "H_sequence_phase_partition",
        "I_phase_aware_active",
    ]
    report: dict[str, Any] = {"causal_boundary": "event_date on or before request date; settlement_date controls cash timing", "policies": {}}
    outputs_by_policy: dict[str, list[dict[str, str]]] = {}
    for policy in policies:
        actual = output_for(policy, requests, profiles, options, canon_args)
        outputs_by_policy[policy] = actual
        exact, differing, per_field = exact_stats(actual, expected)
        diagnostics = recurrence_diagnostics(policy, requests, canon_args)
        report["policies"][policy] = {
            "exact_rows": exact,
            "differing_fields": differing,
            "exact_request_ids": [row["request_id"] for row, expected_row in zip(actual, expected) if all(row[col] == expected_row[col] for col in main.OUTPUT_COLUMNS)],
            "field_exact_request_ids": per_field,
            **diagnostics,
        }
    current_output = output_for_current(requests, profiles, options, canon_args)
    phase_output = outputs_by_policy["H_sequence_phase_partition"]
    current_exact, current_differing, _ = exact_stats(current_output, expected)
    phase_exact, phase_differing, _ = exact_stats(phase_output, expected)
    current_canon = main.Canonicalizer(*canon_args)
    phase_canon = ExperimentCanonicalizer(*canon_args, recurrence_policy="H_sequence_phase_partition")
    stream_changes = []
    for request in requests[:25]:
        current_events = current_canon.for_request(request, profiles[request.user_id], main.WindowPolicy.DAYS_0_THROUGH_89)
        phase_events = phase_canon.for_request(request, profiles[request.user_id], main.WindowPolicy.DAYS_0_THROUGH_89)
        def signature(event: main.CanonicalEvent) -> tuple[Any, ...]:
            return (event.event_type, event.direction, event.category, event.event_date.isoformat(), (event.settlement_date or event.event_date).isoformat(), main.short_decimal(event.amount) if event.amount is not None else None, event.projected)
        before = {signature(event) for event in current_events if event.projected}
        after = {signature(event) for event in phase_events if event.projected}
        if before != after:
            stream_changes.append({"request_id": request.request_id, "current_projected_count": len(before), "phase_projected_count": len(after), "added": sorted(after - before, key=str), "removed": sorted(before - after, key=str)})
    comparison = {
        "current_production": {"exact_rows": current_exact, "differing_fields": current_differing},
        "phase_aware_temporal_partition": {"exact_rows": phase_exact, "differing_fields": phase_differing},
        "improved_requests": [request.request_id for request, current, phase, target in zip(requests, current_output, phase_output, expected) if not all(current[column] == target[column] for column in main.OUTPUT_COLUMNS) and all(phase[column] == target[column] for column in main.OUTPUT_COLUMNS)],
        "regressed_requests": [request.request_id for request, current, phase, target in zip(requests, current_output, phase_output, expected) if all(current[column] == target[column] for column in main.OUTPUT_COLUMNS) and not all(phase[column] == target[column] for column in main.OUTPUT_COLUMNS)],
        "changed_projected_streams": stream_changes,
        "false_merge_proxy": recurrence_diagnostics("H_sequence_phase_partition", requests, canon_args)["false_merge_proxy"],
        "false_split_proxy": recurrence_diagnostics("H_sequence_phase_partition", requests, canon_args)["false_split_proxy"],
    }
    baseline = outputs_by_policy[policies[0]]
    for policy, data in report["policies"].items():
        candidate = outputs_by_policy[policy]
        data["recurrence_fixes"] = sum(
            all(row[column] == expected_row[column] for column in main.OUTPUT_COLUMNS)
            and not all(base_row[column] == expected_row[column] for column in main.OUTPUT_COLUMNS)
            for row, base_row, expected_row in zip(candidate, baseline, expected)
        )
        data["regressions"] = sum(
            not all(row[column] == expected_row[column] for column in main.OUTPUT_COLUMNS)
            and all(base_row[column] == expected_row[column] for column in main.OUTPUT_COLUMNS)
            for row, base_row, expected_row in zip(candidate, baseline, expected)
        )
    evaluation = ROOT / "evaluation"
    (evaluation / "recurrence_policy_ablation.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evaluation / "phase_aware_recurrence_comparison.json").write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Recurrence identity policy ablation", "", "All policies use event_date on or before each request date for recurrence history; settlement_date remains the simulated cash date. Counts below are experiment-harness results, not a replacement for the production S16 gate. `Recurrence fixes` and `regressions` compare each candidate with Policy A, the exact-normalized-description baseline.", "", "| Policy | Exact rows | Differing fields | Recurrence fixes | Regressions | False-merge proxy | False-split proxy |", "|---|---:|---:|---:|---:|---:|---:|"]
    lines.append("| Production checkpoint (current) | 3/25 | 67 | n/a | n/a | n/a | n/a |")
    for policy, data in report["policies"].items():
        lines.append(f"| {policy} | {data['exact_rows']}/25 | {data['differing_fields']} | {data['recurrence_fixes']} | {data['regressions']} | {data['false_merge_proxy']} | {data['false_split_proxy']} |")
    lines += ["", "## Exact-row changes", ""]
    for policy, data in report["policies"].items():
        lines.append(f"- `{policy}` exact rows: {', '.join(data['exact_request_ids']) or 'none'}")
    lines += ["", "## Selection result", "", "No candidate is promoted to production. The natural hybrid fallback (`G_variable_category_fallback`) reduces harness field mismatches relative to broad category projection but still produces no new exact sample rows and retains an anti-overmerge failure. The corrected phase-aware partition (`H_sequence_phase_partition`) also produces no new exact rows, increases harness field differences to 81, and regresses current exact `request_01`; the stale-stream variant (`I_phase_aware_active`) falls to 1/25. The supplied schema has no merchant/source/account/recurrence identifier that can resolve the remaining same-category, rotating-description cases without an unsupported alias. The production checkpoint therefore remains unchanged pending authoritative evidence.", ""]
    (evaluation / "recurrence_policy_ablation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    comparison_lines = ["# Phase-aware recurrence comparison", "", "The phase-aware experiment is compared directly with the current production checkpoint against all 25 solved rows. It is not promoted automatically.", "", "| Policy | Exact rows | Differing fields | Improved requests | Regressed requests | False-merge proxy | False-split proxy |", "|---|---:|---:|---|---|---:|---:|", f"| Current production | {comparison['current_production']['exact_rows']}/25 | {comparison['current_production']['differing_fields']} | n/a | n/a | n/a | n/a |", f"| phase_aware_temporal_partition | {comparison['phase_aware_temporal_partition']['exact_rows']}/25 | {comparison['phase_aware_temporal_partition']['differing_fields']} | {', '.join(comparison['improved_requests']) or 'none'} | {', '.join(comparison['regressed_requests']) or 'none'} | {comparison['false_merge_proxy']} | {comparison['false_split_proxy']} |", "", "## Changed projected streams", ""]
    for change in comparison["changed_projected_streams"]:
        comparison_lines.append(f"- `{change['request_id']}`: current={change['current_projected_count']} projected rows, phase-aware={change['phase_projected_count']} projected rows; added={len(change['added'])}, removed={len(change['removed'])}")
    comparison_lines += ["", "The phase-aware policy is rejected for production promotion because it loses one current exact row, gains no exact rows, and remains byte-incompatible with the solved samples.", ""]
    (evaluation / "phase_aware_recurrence_comparison.md").write_text("\n".join(comparison_lines), encoding="utf-8")
    write_identity_inventory(evaluation, canon_args[0])
    write_training_matrix(evaluation, requests, expected, outputs_by_policy, canon_args)
    write_phase_diagnostics(evaluation, requests, canon_args)
    write_unlinked_transfer_analysis(evaluation)
    print("wrote evaluation/recurrence_policy_ablation.md and .json")
    for policy, data in report["policies"].items():
        print(policy, f"exact={data['exact_rows']}/25", f"fields={data['differing_fields']}", f"merge={data['false_merge_proxy']}", f"split={data['false_split_proxy']}")
    return 0


def write_phase_diagnostics(evaluation: Path, requests: list[main.Request], canon_args: tuple[Any, ...]) -> None:
    """Materialize the H-policy stream membership and deterministic evidence."""
    raw = main.Canonicalizer(*canon_args)
    records: list[dict[str, Any]] = []
    for request in requests[:25]:
        rows = raw.message_adjustments(request.user_id, raw.by_user.get(request.user_id, []), request.request_date)
        valid = [event for event in rows if event.amount is not None and event.event_date <= request.request_date and event.status not in {"failed", "cancelled", "unrealized"} and event.direction != "non_cash"]
        by_semantic: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in valid:
            by_semantic[semantic_key(event)].append(event)
        for semantic, bucket in sorted(by_semantic.items()):
            clusters = sequence_clusters(bucket)
            members = {event.event_id for cluster in clusters for event in cluster}
            for index, cluster in enumerate(clusters):
                kind, step = cadence_for(cluster)
                dates = sorted(event.event_date for event in cluster)
                gaps = [(later - earlier).days for earlier, later in zip(dates, dates[1:])]
                latest = max(cluster, key=lambda event: event.event_date)
                expected_next = main.add_months(latest.event_date, 1) if kind == "month" else latest.event_date + timedelta(days=step)
                stale = request.request_date > expected_next + timedelta(days=max(2, step))
                recent = sorted(cluster, key=lambda event: event.event_date)[-3:]
                amount = max(event.amount for event in recent if event.amount is not None)
                phase = latest.event_date.day if kind == "month" else latest.event_date.toordinal() % max(step, 1)
                records.append({
                    "request_id": request.request_id,
                    "user_id": request.user_id,
                    "event_type": semantic[0],
                    "direction": semantic[1],
                    "category": semantic[2],
                    "currency": semantic[3],
                    "flexibility": semantic[4],
                    "stream_id": f"{request.user_id}:{semantic[0]}:{semantic[1]}:{semantic[2]}:{semantic[3]}:{semantic[4]}:sequence:{index}",
                    "member_event_ids": [event.event_id for event in cluster],
                    "member_dates": [event.event_date.isoformat() for event in cluster],
                    "descriptions": sorted({event.description for event in cluster}),
                    "recurrence_type": kind,
                    "cadence_days": step if kind == "gap" else None,
                    "phase_or_anchor": phase,
                    "date_gaps_days": gaps,
                    "residual_days": max(gaps) - min(gaps) if gaps else 0,
                    "latest_occurrence": latest.event_date.isoformat(),
                    "expected_next_occurrence": expected_next.isoformat(),
                    "active_as_of_request": not stale,
                    "recurrence_amount": main.short_decimal(amount),
                    "amount_source_event_ids": [event.event_id for event in recent],
                    "excluded_outlier_event_ids": sorted(set(event.event_id for event in bucket) - members),
                    "confidence_basis": "deterministic: at least three observations, one supported cadence, one temporal phase, and no duplicate event membership",
                })
    (evaluation / "phase_aware_recurrence_diagnostics.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Phase-aware recurrence diagnostics", "", "This is an analysis of `H_sequence_phase_partition`; it is not production behavior. History is bounded by `event_date <= request_date` after status/message filtering. `settlement_date` remains the cash-flow date. Active state is reported using the experiment criterion `request_date <= expected_next + max(2, cadence_days)` and is not promoted without solved-sample support.", ""]
    for record in records:
        lines += [
            f"## `{record['stream_id']}`",
            "",
            f"- User/category/direction/type: `{record['user_id']}` / `{record['category']}` / `{record['direction']}` / `{record['event_type']}`",
            f"- Members: {', '.join(record['member_event_ids'])}",
            f"- Dates: {', '.join(record['member_dates'])}",
            f"- Descriptions: {', '.join(record['descriptions'])}",
            f"- Recurrence: `{record['recurrence_type']}` cadence_days=`{record['cadence_days']}` phase_or_anchor=`{record['phase_or_anchor']}` residual_days=`{record['residual_days']}`",
            f"- Latest/expected next: `{record['latest_occurrence']}` / `{record['expected_next_occurrence']}`",
            f"- Active as of request: `{record['active_as_of_request']}`",
            f"- Amount: `{record['recurrence_amount']}` from `{', '.join(record['amount_source_event_ids'])}`",
            f"- Excluded outliers: `{', '.join(record['excluded_outlier_event_ids']) or 'none'}`",
            f"- Evidence: {record['confidence_basis']}",
            "",
        ]
    (evaluation / "phase_aware_recurrence_diagnostics.md").write_text("\n".join(lines), encoding="utf-8")


def write_identity_inventory(evaluation: Path, events: list[main.CanonicalEvent]) -> None:
    rows = [
        ("event_id", "unique opaque row identifier", "unique per observation", "No; it distinguishes rows, not a recurring entity", "structural row key, not stream identity"),
        ("user_id", "user partition", "stable for a user's records", "No by itself; all obligations for one user share it", "structural partition"),
        ("event_type", "income/expense/subscription/debt/etc.", "stable within an obligation class", "Sometimes; separate types should not merge", "structural"),
        ("description", "human-readable payee/obligation label", "often rotates for groceries, transport, dining", "Sometimes; useful merchant/obligation evidence but not a source ID", "mostly descriptive"),
        ("category", "broad financial category", "stable across many recurring observations", "No; several obligations and rotating streams share it", "structural semantic feature, insufficient alone"),
        ("direction", "debit/credit/non_cash", "stable for a cash-flow stream", "Yes; opposite directions must remain separate", "structural"),
        ("amount", "observed monetary value", "fixed for contractual bills; variable for ordinary spending", "Supporting evidence only; never sole identity", "measurement"),
        ("currency", "source currency", "usually stable per user/obligation", "Occasionally; helps prevent invalid cross-currency merges", "structural/supporting"),
        ("event_date", "observed occurrence date", "supports cadence and phase", "Yes, through temporal sequence; not an identity by itself", "structural temporal evidence"),
        ("settlement_date", "cash-effective date", "may differ for pending/scheduled rows", "No; controls cash timing and lifecycle precedence", "lifecycle/cash timing"),
        ("status", "settled/pending/scheduled/failed/cancelled/unrealized", "changes over a lifecycle", "Yes for lifecycle collapse, not recurring identity", "lifecycle"),
        ("linked_event_id", "optional lifecycle link", "sparse; populated on linked rows only", "Yes when present; no transfer link exists for the unlinked message case", "structural lifecycle"),
        ("flexibility", "fixed/reducible/stoppable/etc.", "stable for a stream in observed data", "Yes as a guard against merging semantically different change policies", "structural policy feature"),
        ("minimum_allowed_amount", "floor for reducible events", "blank for most rows; stable where supplied", "Supporting evidence for a change plan, not stream identity", "policy metadata"),
    ]
    lines = ["# Recurrence identity inventory", "", f"Observed rows: {len(events)}. No merchant, payee, account, provider, source-record, recurrence-marker, or explicit stream-ID column is supplied.", "", "| Field | Meaning | Stability | Can distinguish obligations? | Classification |", "|---|---|---|---|---|"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    lines += ["", "## Negative controls", "", "The data contains concrete anti-overmerge cases:", "", "- `user_01` has `event_84` (settled `Local taxi`, 2024-03-02, ZAR 339.29) and `event_102` (pending `Pending fuel authorization`, same occurrence date, settlement 2024-03-05, ZAR 567.60) in `transport`. Same category and date do not prove one stream; lifecycle/status and settlement remain separate.", "- `user_10` has weekly `salary` credits whose descriptions rotate among `Delivery platform payout`, `Weekly app earnings`, `Task marketplace payout`, and `Driver platform payout`. Category-only recurrence would merge income streams without a supplied source identifier; the repeated weekly cadence is evidence of a family, not permission to invent a single employer/source.", "- `user_23` contains a regular `Clinic payment` healthcare series and a separate pending `Pending pharmacy card charge` healthcare record. Same category does not make the pending charge a continuation of the clinic stream.", "- `user_77` has `event_7185` (`Purchase awaiting refund`, debit) linked to `event_7186` (`Pending merchant refund`, credit). The lifecycle link and opposite directions dominate any category or amount similarity; these rows must not be treated as a recurring debit stream.", "- `user_01` groceries include similarly sized but differently described observations such as `Neighbourhood grocer` (ZAR 925.62) and `Bulk pantry shop` (ZAR 915.12). Amount similarity supports a candidate cluster but cannot be its sole identity.", "", "## Consequence", "", "The strongest available identity is a tuple of user, direction, event type, category, flexibility, controlled description evidence, and a causal date sequence. `linked_event_id` is authoritative for lifecycle relationships when present, but it cannot repair the unlinked transfer message because that message supplies no corresponding event identifier or amount.", ""]
    (evaluation / "recurrence_identity_inventory.md").write_text("\n".join(lines), encoding="utf-8")


def write_training_matrix(evaluation: Path, requests: list[main.Request], expected: list[dict[str, str]], outputs: dict[str, list[dict[str, str]]], canon_args: tuple[Any, ...]) -> None:
    raw = main.Canonicalizer(*canon_args)
    lines = ["# Recurrence-sensitive solved-sample training matrix", "", "The matrix records evidence available at each request boundary. It is analysis only; no request, user, or event identifier is used by production logic.", ""]
    lines += ["| Request | User | Expected safe | Exact-policy safe | Category-policy safe | Historical recurring evidence | Identity implication |", "|---|---|---:|---:|---:|---|---|"]
    for index, request in enumerate(requests[:25]):
        rows = raw.message_adjustments(request.user_id, raw.by_user.get(request.user_id, []), request.request_date)
        history = [event for event in rows if event.amount is not None and event.event_date <= request.request_date and event.status not in {"failed", "cancelled", "unrealized"} and event.direction != "non_cash"]
        semantic: dict[tuple[str, ...], list[main.CanonicalEvent]] = defaultdict(list)
        for event in history:
            semantic[semantic_key(event)].append(event)
        summaries = []
        implications = []
        for key, events in sorted(semantic.items()):
            if len(events) < 3:
                continue
            kind, step = cadence_for(events)
            descriptions = sorted({description_family(event.description) for event in events})
            if kind != "none" or len(descriptions) > 1:
                dates = ",".join(event.event_date.isoformat() for event in sorted(events, key=lambda event: event.event_date)[-5:])
                amount_text = ",".join(main.short_decimal(event.amount) for event in sorted(events, key=lambda event: event.event_date)[-3:] if event.amount is not None)
                summaries.append(f"{key[2]} n={len(events)} desc={len(descriptions)} cadence={kind or 'none'}{step or ''} dates={dates} amounts={amount_text}")
                if len(descriptions) > 1 and kind != "none":
                    implications.append(f"same {key[2]} category has a stable {kind}/{step} sequence despite rotating descriptions")
                elif len(descriptions) > 1:
                    implications.append(f"same {key[2]} category has multiple descriptions but no single stable sequence; keep streams conservative")
        exact_row = outputs["A_exact_normalized_description"][index]
        category_row = outputs["B_broad_category"][index]
        expected_row = expected[index]
        recurrence_sensitive = any(exact_row[col] != category_row[col] for col in main.OUTPUT_COLUMNS) or any(exact_row[col] != expected_row[col] for col in main.OUTPUT_COLUMNS)
        if not recurrence_sensitive:
            continue
        lines.append("| " + " | ".join([
            request.request_id,
            request.user_id,
            expected_row["amount_safe_to_pay"],
            exact_row["amount_safe_to_pay"],
            category_row["amount_safe_to_pay"],
            "<br>".join(summaries[:5]) or "no >=3-observation recurring group",
            "<br>".join(implications[:3]) or "description/category identity remains ambiguous",
        ]) + " |")
    lines += ["", "## Sequence and causality findings", "", "- Recurrence inference is bounded by `event_date <= request_date`; no post-request observation is used to discover a stream. `settlement_date` is retained for cash timing, pending treatment, and lifecycle precedence.", "- Variable categories show genuine sequence structure: groceries commonly recur every 7 or 10 days, transport every 7, 14, or 21 days, and dining every 14 or 21 days, while labels rotate across a finite description vocabulary.", "- Fixed obligations usually show stable descriptions and monthly cadence. Salary is a precision control: `user_10` has weekly payout records with several labels in one category, while other users have distinct payroll streams offset within the month.", "- Same-day and lifecycle evidence breaks label-only assumptions. `user_01` has settled transport and a separate pending transport authorization on one occurrence date; `user_77` has an explicitly linked debit/refund pair. Neither should be collapsed by category or amount.", "- The phase/cadence candidate was tested as a sequence identity, but it still failed the solved rows. This means cadence is supporting evidence, not a uniquely sufficient stream identity in the supplied schema.", "", "## Reading the matrix", "", "The supplied schema has no stable merchant, account, provider, or recurrence identifier. Stable cadence is therefore useful evidence but cannot, by itself, prove that two same-category obligations are one stream. Category-only is a negative control: it merges independent obligations and rotates descriptions indiscriminately. Exact description is a negative control in the other direction: it splits ordinary variable spending into accidental short sequences.", ""]
    (evaluation / "recurrence_training_matrix.md").write_text("\n".join(lines), encoding="utf-8")


def write_unlinked_transfer_analysis(evaluation: Path) -> None:
    messages = main.read_csv("messages.csv")
    message = next(row for row in messages if row["message_id"] == "message_13")
    events = [row for row in main.read_csv("financial_events.csv") if row["user_id"] == message["user_id"]]
    lines = [
        "# Unlinked transfer message analysis", "",
        f"- Message: `{message['message_id']}`", f"- Scope: user `{message['user_id']}`, request `{message['request_id']}`, source `{message['source_type']}`", f"- Sent at: `{message['sent_at']}`", f"- `related_event_id`: blank", "- Explicit amount: none", "- Explicit date: none", f"- User financial-event rows: {len(events)}", f"- User linked-event rows: {sum(bool(row['linked_event_id']) for row in events)}", "", "## Decision", "", "The message is contextual evidence that two existing bank-history rows represent an internal transfer, but it does not identify either row and provides no amount or date. No unambiguous matching pair exists in the supplied rows. It therefore creates no cash-flow event and does not borrow an amount from another transaction. The existing structured rows remain governed by their own status, direction, settlement date, and lifecycle data.", "", "This is the conservative rule required by the participant statement and contract: a message may amend a quantified supplied fact when the target is unambiguous; this message does neither.", "", "## Message text", "", message["message_text"], ""]
    (evaluation / "unlinked_transfer_message_analysis.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main_entry())
