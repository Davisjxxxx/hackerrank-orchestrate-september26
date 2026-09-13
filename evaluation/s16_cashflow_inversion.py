"""Bounded S16 cash-flow inversion and latent-stream diagnostics.

This module is deliberately evaluation-only.  It reads solved sample rows as
post-hoc constraints, never imports them from the scoring runtime, and never
selects a request-specific production branch.
"""
from __future__ import annotations

import csv
import itertools
import json
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402

POLICY = main.WindowPolicy.DAYS_0_THROUGH_89
OUT_FIELDS = main.OUTPUT_COLUMNS[1:]


def d(value: object) -> Decimal:
    return Decimal(str(value))


def day(event: main.CanonicalEvent) -> date:
    return event.settlement_date or event.event_date


def signed(event: main.CanonicalEvent, canonical: main.Canonicalizer, profile: main.Profile) -> Decimal:
    amount = canonical.converted(event, profile) or Decimal(0)
    return amount if event.direction == "credit" else -amount


def make_context() -> tuple[dict[str, main.Profile], list[main.Request], dict[str, dict[str, str]], main.Canonicalizer, dict[str, list[main.PaymentOption]]]:
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    expected = {row["request_id"]: row for row in main.read_csv("sample_requests.csv")}
    adapter = main.FinancialEventAdapter(main.ImageEvidenceAdapter())
    canonical = main.Canonicalizer(adapter.canonical_rows(), main.read_csv("messages.csv"), main.ExchangeRateAdapter())
    return profiles, requests, expected, canonical, main.PaymentOptionAdapter().load()


def path_for(canonical: main.Canonicalizer, request: main.Request, profile: main.Profile, events: list[main.CanonicalEvent], payment: tuple[date, Decimal] | None = None) -> list[dict[str, object]]:
    flows = main.Simulator(canonical, POLICY).flows(request, profile, events)
    balance = profile.current_available_balance
    path = []
    for offset in range(POLICY.upper_bound_offset() + 1):
        current = request.request_date + timedelta(days=offset)
        payment_amount = payment[1] if payment and current == payment[0] else Decimal(0)
        balance += flows.get(current, Decimal(0)) - payment_amount
        path.append({"date": current.isoformat(), "balance": balance, "flow": flows.get(current, Decimal(0)), "payment": payment_amount})
    return path


def first_date_at_or_below(path: list[dict[str, object]], limit: Decimal) -> str | None:
    for row in path:
        if d(row["balance"]) <= limit:
            return str(row["date"])
    return None


def output_for(canonical: main.Canonicalizer, options: dict[str, list[main.PaymentOption]], request: main.Request, profile: main.Profile, events: list[main.CanonicalEvent]) -> dict[str, str]:
    planner = main.Planner(canonical, options, POLICY)
    original = canonical.for_request
    frozen = list(events)
    canonical.for_request = lambda _r, _p, _policy, _events=frozen: list(_events)
    try:
        decision, used = planner.decide(request, profile)
    finally:
        canonical.for_request = original
    decision.explanation = main.make_explanation(decision, used)
    return main.serialize(decision)


def baseline_records(profiles, requests, expected, canonical, options):
    records = []
    for request in requests:
        profile = profiles[request.user_id]
        events = canonical.for_request(request, profile, POLICY)
        actual = output_for(canonical, options, request, profile, events)
        target = expected[request.request_id]
        differences = [field for field in OUT_FIELDS if actual[field] != target[field]]
        if not differences:
            continue
        path = path_for(canonical, request, profile, events)
        actual_min = min(path, key=lambda row: (d(row["balance"]), str(row["date"])))
        expected_safe = d(target["amount_safe_to_pay"])
        actual_safe = d(actual["amount_safe_to_pay"])
        capped = expected_safe == request.requested_amount
        implied = profile.minimum_balance_to_keep + expected_safe
        # If the safe amount is below the request cap, the simulator's linear
        # predicate makes this an equality.  At the cap it is only a lower
        # bound; recording that distinction prevents false precision.
        expected_constraint = {
            "type": "lower_bound" if capped else "exact",
            "balance": str(implied),
            "derivation": "safe=min(request,trough-reserve); expected safe is not capped" if not capped else "safe is request-capped, so trough is at least request+reserve",
        }
        target_level = implied
        first_target = first_date_at_or_below(path, target_level)
        expected_date = date.fromisoformat(target["earliest_date_for_full_payment"]) if target["earliest_date_for_full_payment"] else None
        payment_path = path_for(canonical, request, profile, events, (expected_date, request.requested_amount)) if expected_date else []
        violations = [row for row in payment_path if d(row["balance"]) < profile.minimum_balance_to_keep]
        first_violation = str(violations[0]["date"]) if violations else None
        trough_date = date.fromisoformat(str(actual_min["date"]))
        interval_end = max(trough_date, expected_date or request.request_date)
        sign = actual_safe - expected_safe
        direction = "combination"
        if sign > 0:
            direction = "extra debit or missing credit (production too optimistic)"
        elif sign < 0:
            direction = "missing debit or extra credit (production too pessimistic)"
        else:
            direction = "timing displacement or downstream-only"
        future = []
        for event in events:
            if not event.projected or not request.request_date <= day(event) <= request.request_date + timedelta(days=POLICY.upper_bound_offset()):
                continue
            amount = canonical.converted(event, profile)
            future.append({
                "event_id": event.event_id,
                "source_event_id": event.source_event_id,
                "date": day(event).isoformat(),
                "event_type": event.event_type,
                "category": event.category,
                "description": event.description,
                "direction": event.direction,
                "signed_home_amount": str(signed(event, canonical, profile)),
                "amount_home": str(amount) if amount is not None else None,
                "currency": event.currency,
                "provenance": event.provenance,
            })
        future.sort(key=lambda item: (item["date"], item["event_id"]))
        records.append({
            "request_id": request.request_id,
            "user_id": request.user_id,
            "request_date": request.request_date.isoformat(),
            "opening_balance": str(profile.current_available_balance),
            "protected_minimum": str(profile.minimum_balance_to_keep),
            "expected_output": target,
            "actual_output": actual,
            "differing_fields": differences,
            "expected_amount_safe_to_pay": str(expected_safe),
            "actual_amount_safe_to_pay": str(actual_safe),
            "safe_delta_actual_minus_expected": str(sign),
            "expected_earliest_full_payment": target["earliest_date_for_full_payment"],
            "actual_earliest_full_payment": actual["earliest_date_for_full_payment"],
            "actual_minimum_balance": str(actual_min["balance"]),
            "actual_trough_date": str(actual_min["date"]),
            "expected_implied_minimum_constraint": expected_constraint,
            "first_actual_date_at_or_below_expected_constraint": first_target,
            "first_actual_violation_when_paying_on_expected_earliest": first_violation,
            "date_interval_for_required_delta": {"start": request.request_date.isoformat(), "end": interval_end.isoformat()},
            "required_correction_direction": direction,
            "candidate_future_flows": future,
            "actual_path": [{k: (str(v) if isinstance(v, Decimal) else v) for k, v in row.items()} for row in path],
        })
    return records


def correction_candidates(canonical, request, profile, events):
    """Return bounded, evidence-backed flow edits.

    Edits are occurrence removals, whole inferred-stream removals, and
    projected amount replacements using an observed historical amount from the
    same normalized production stream.  No arbitrary value is introduced.
    """
    horizon = request.request_date + timedelta(days=POLICY.upper_bound_offset())
    projected = [e for e in events if e.projected and request.request_date <= day(e) <= horizon and e.amount is not None]
    candidates = []
    for event in projected:
        flow = signed(event, canonical, profile)
        candidates.append({
            "id": f"remove_occurrence:{event.event_id}",
            "kind": "remove_occurrence",
            "label": f"remove projected occurrence {event.event_id}",
            "event_ids": [event.event_id],
            "source_event_ids": [],
            "correction_flow": str(-flow),
            "date": day(event).isoformat(),
            "provenance": "current projected occurrence; removal is a diagnostic counterfactual",
        })
    by_source = defaultdict(list)
    for event in projected:
        by_source[event.source_event_id or event.event_id].append(event)
    for source, members in sorted(by_source.items()):
        correction = -sum((signed(event, canonical, profile) for event in members), Decimal(0))
        if len(members) > 1:
            candidates.append({
                "id": f"remove_stream:{source}",
                "kind": "remove_stream",
                "label": f"remove all projected occurrences of inferred stream {source}",
                "event_ids": [event.event_id for event in members],
                "source_event_ids": [source],
                "correction_flow": str(correction),
                "date": min(day(event) for event in members).isoformat(),
                "provenance": "chronological source stream grouping; diagnostic only",
            })
    # Historical amounts are legitimate alternatives for variable amount
    # inference.  Keep the date and stream fixed, changing only to an amount
    # actually observed in that stream's history.
    all_history = [e for e in canonical.by_user.get(request.user_id, []) if e.amount is not None and e.event_date <= request.request_date and e.status not in {"failed", "cancelled", "unrealized"} and e.direction != "non_cash"]
    for event in projected:
        key = (event.event_type, event.category, event.flexibility, event.description, event.direction, event.currency)
        seen_amounts = sorted({h.amount for h in all_history if (h.event_type, h.category, h.flexibility, h.description, h.direction, h.currency) == key})
        for amount in seen_amounts:
            if amount == event.amount:
                continue
            old = signed(event, canonical, profile)
            new = canonical.fx.convert(amount, event.currency, profile.home_currency, day(event))
            new_signed = new if event.direction == "credit" else -new
            candidates.append({
                "id": f"replace_amount:{event.event_id}:{amount}",
                "kind": "replace_observed_amount",
                "label": f"replace {event.event_id} amount with observed historical {amount}",
                "event_ids": [event.event_id],
                "source_event_ids": [],
                "correction_flow": str(new_signed - old),
                "date": day(event).isoformat(),
                "replacement_amount": str(amount),
                "provenance": "same production stream, observed historical amount",
            })
    return sorted(candidates, key=lambda c: (c["date"], c["id"]))


def apply_candidates(events, candidates):
    remove_ids = {e for c in candidates for e in c.get("event_ids", []) if c["kind"] == "remove_occurrence"}
    replace_map = {}
    for candidate in candidates:
        if candidate["kind"] == "replace_observed_amount":
            replace_map[candidate["event_ids"][0]] = d(candidate["replacement_amount"])
    out = []
    for event in events:
        if event.event_id in remove_ids:
            continue
        if event.event_id in replace_map:
            out.append(replace(event, amount=replace_map[event.event_id], provenance=event.provenance + "+counterfactual_observed_amount"))
        else:
            out.append(event)
    return out


def minimal_explanations(profiles, requests, expected, canonical, options, records):
    by_id = {r.request_id: r for r in requests}
    all_rows = []
    for record in records:
        request = by_id[record["request_id"]]
        profile = profiles[request.user_id]
        baseline_events = canonical.for_request(request, profile, POLICY)
        candidates = correction_candidates(canonical, request, profile, baseline_events)
        target = expected[request.request_id]
        matches = []
        # Arithmetic branch-and-bound: only retain combinations whose signed
        # correction can reach the required safe-amount delta.  The final
        # decision is then recomputed against the altered event list.
        # A safe-amount delta is the inverse of the flow correction needed on
        # the path: adding a debit lowers safe cash, while removing a debit
        # raises it.  Search for expected-minus-actual flow correction.
        wanted = -d(record["safe_delta_actual_minus_expected"])
        ranked = sorted(candidates, key=lambda c: (abs(d(c["correction_flow"])-wanted), c["id"]))
        ranked = [c for c in ranked if abs(d(c["correction_flow"])) <= abs(wanted) + max(Decimal("0.01"), abs(wanted) * Decimal("0.15"))] or ranked[:18]
        ranked = ranked[:28]
        nearest = []
        for candidate in sorted(candidates, key=lambda c: (abs(d(c["correction_flow"])-wanted), c["id"]))[:5]:
            correction = d(candidate["correction_flow"])
            nearest.append({
                "candidate": candidate,
                "delta_explained": str(correction),
                "residual": str(wanted - correction),
            })
        for size in range(1, 4):
            for combo in itertools.combinations(ranked, size):
                ids = [c["id"] for c in combo]
                if len(ids) != len(set(ids)):
                    continue
                correction = sum((d(c["correction_flow"]) for c in combo), Decimal(0))
                if abs(correction - wanted) > Decimal("0.01"):
                    continue
                altered = apply_candidates(baseline_events, combo)
                actual = output_for(canonical, options, request, profile, altered)
                numeric_ok = actual["amount_safe_to_pay"] == target["amount_safe_to_pay"]
                earliest_ok = actual["earliest_date_for_full_payment"] == target["earliest_date_for_full_payment"]
                decision_ok = all(actual[field] == target[field] for field in ("affordability_status", "recommended_payment_method", "payment_plan") if field in target)
                if numeric_ok or (numeric_ok and earliest_ok):
                    matches.append({
                        "edits": size,
                        "arithmetic_correction": str(correction),
                        "numeric_match": numeric_ok,
                        "earliest_match": earliest_ok,
                        "decision_match": decision_ok,
                        "candidate_set": list(combo),
                    })
            if matches:
                break
        all_rows.append({
            "request_id": request.request_id,
            "required_safe_delta_actual_minus_expected": str(-wanted),
            "required_flow_correction_expected_minus_actual": str(wanted),
            "candidate_count": len(candidates),
            "bounded_candidate_count": len(ranked),
            "smallest_matching_edit_count": min((m["edits"] for m in matches), default=None),
            "matching_candidate_sets": matches[:20],
            "matching_set_count": len(matches),
            "nearest_single_candidate_corrections": nearest,
            "classification": "unique explanation" if len(matches) == 1 else ("multiple explanations" if matches else "no evidence-supported explanation"),
            "search_bound": "combinations of up to 3 observed occurrence/stream/amount edits; candidate values are observed events or observed historical amounts",
        })
    return all_rows


def stream_assignments(canonical):
    """Assign chronological history to latent streams without descriptions."""
    rows = [e for e in canonical.events if e.amount is not None and e.status not in {"failed", "cancelled", "unrealized"} and e.direction != "non_cash"]
    groups = defaultdict(list)
    for e in rows:
        groups[(e.user_id, e.event_type, e.category, e.direction, e.currency, e.flexibility)].append(e)
    result = []
    for key, members in sorted(groups.items()):
        ordered = sorted(members, key=lambda e: (e.event_date, e.event_id))
        gaps = [(b.event_date-a.event_date).days for a,b in zip(ordered, ordered[1:]) if (b.event_date-a.event_date).days > 0]
        if not gaps:
            continue
        cadence = max(1, int(statistics.median(gaps)))
        streams = []
        for event in ordered:
            compatible = []
            for idx, stream in enumerate(streams):
                residual = (event.event_date - stream[-1].event_date).days - cadence
                if abs(residual) <= max(2, min(7, cadence // 5)):
                    compatible.append((abs(residual), idx))
            if compatible:
                streams[min(compatible)[1]].append(event)
            else:
                streams.append([event])
        result.append({
            "group": {"user_id": key[0], "event_type": key[1], "category": key[2], "direction": key[3], "currency": key[4], "flexibility": key[5]},
            "inferred_cadence_days": cadence,
            "stream_count": len(streams),
            "streams": [{"event_ids": [e.event_id for e in stream], "dates": [e.event_date.isoformat() for e in stream], "descriptions": [e.description for e in stream], "amounts": [str(e.amount) for e in stream]} for stream in streams],
            "affirmative_concurrency": len(streams) > 1 and all(len(s) >= 2 for s in streams),
        })
    return result


def generator_signatures(raw_events):
    by_group = defaultdict(list)
    for row in raw_events:
        if row["direction"] == "non_cash" or row["status"] in {"failed", "cancelled", "unrealized"} or not row["amount"]:
            continue
        by_group[(row["user_id"], row["event_type"], row["category"], row["direction"], row["currency"], row["flexibility"])].append(row)
    rotation = []; amount_rotation = []; cadence_counts = Counter(); category_users = Counter(); counters = []
    for key, rows in sorted(by_group.items()):
        ordered = sorted(rows, key=lambda r: (r["event_date"], r["event_id"]))
        gaps = [(date.fromisoformat(b["event_date"])-date.fromisoformat(a["event_date"])).days for a,b in zip(ordered, ordered[1:]) if (date.fromisoformat(b["event_date"])-date.fromisoformat(a["event_date"])).days > 0]
        if len(ordered) >= 3 and gaps:
            med = int(statistics.median(gaps)); cadence_counts[med] += 1; category_users[key[2]] += 1
        desc = [r["description"] for r in ordered]
        if len(ordered) >= 4 and len(set(desc)) >= 2:
            transitions = list(zip(desc, desc[1:]))
            repeated = len(transitions) - len(set(transitions))
            rotation.append({"group": key, "count": len(ordered), "unique_descriptions": len(set(desc)), "description_sequence": desc, "repeated_transition_count": repeated})
        amounts = [r["amount"] for r in ordered]
        if len(ordered) >= 4 and len(set(amounts)) >= 2:
            amount_rotation.append({"group": key, "count": len(ordered), "unique_amounts": len(set(amounts)), "amount_sequence": amounts})
        if len(ordered) >= 4 and len(set(desc)) > 1:
            counters.append({"group": key, "description_count": len(set(desc)), "event_count": len(ordered), "counterexample": "same economic bucket has multiple labels; label equality is not sufficient identity"})
    return {
        "scope": "all supplied financial_events.csv rows, excluding failed/cancelled/unrealized/non_cash",
        "cadence_median_counts": dict(sorted((str(k), v) for k,v in cadence_counts.items())),
        "category_group_counts": dict(sorted(category_users.items())),
        "description_rotation_examples": rotation[:80],
        "amount_rotation_examples": amount_rotation[:80],
        "label_identity_counterexamples": counters[:80],
        "summary": {"groups": len(by_group), "description_rotation_groups": len(rotation), "amount_rotation_groups": len(amount_rotation), "groups_with_multiple_labels": len(counters)},
    }


def write_reports(records, explanations, assignments, signatures):
    evaluation = ROOT / "evaluation"
    inversion = {"policy": POLICY.value, "counts": {"non_exact_requests": len(records), "differing_fields": sum(len(r["differing_fields"]) for r in records)}, "rows": records}
    (evaluation / "s16_cashflow_inversion.json").write_text(json.dumps(inversion, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evaluation / "s16_minimal_flow_explanations.json").write_text(json.dumps({"rows": explanations}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evaluation / "s16_dataset_generator_signatures.json").write_text(json.dumps(signatures, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (evaluation / "s16_latent_stream_assignments.json").write_text(json.dumps({"algorithm": "group by economic dimensions, median cadence, greedy chronology assignment with bounded residual", "assignments": assignments}, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = ["# S16 cash-flow inversion", "", "Evaluation-only inversion of the 22 non-exact solved rows. Expected outputs are constraints, never runtime inputs.", "", f"- Differing fields: `{inversion['counts']['differing_fields']}`", "", "| Request | Expected safe | Actual safe | Delta actual-expected | Expected trough constraint | Actual trough | First target-level date | Delta interval | Direction |", "|---|---:|---:|---:|---|---|---|---|---|"]
    for r in records:
        lines.append(f"| `{r['request_id']}` | {r['expected_amount_safe_to_pay']} | {r['actual_amount_safe_to_pay']} | {r['safe_delta_actual_minus_expected']} | {r['expected_implied_minimum_constraint']['type']} `{r['expected_implied_minimum_constraint']['balance']}` | `{r['actual_minimum_balance']}` on `{r['actual_trough_date']}` | `{r['first_actual_date_at_or_below_expected_constraint'] or 'not reached'}` | `{r['date_interval_for_required_delta']['start']}..{r['date_interval_for_required_delta']['end']}` | {r['required_correction_direction']} |")
    lines += ["", "## Interpretation", "", "For uncapped expected safe amounts, expected safe plus the protected minimum is an exact implied trough. Positive actual-minus-expected means the production path leaves too much safe cash and needs an extra debit or missing credit; negative means it leaves too little and needs a missing debit or extra credit. A capped expected safe amount would provide only a lower bound; no request-specific production branch is derived from this table.", ""]
    (evaluation / "s16_cashflow_inversion.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# S16 minimal flow explanations", "", "Bounded search over evidence-supported occurrence removals, inferred-stream removals, and replacements by observed historical amounts. No arbitrary amounts or solved-row identifiers are candidates.", "", "| Request | Required flow correction (expected-actual) | Candidate count | Matching sets | Classification |", "|---|---:|---:|---:|---|"]
    for r in explanations:
        lines.append(f"| `{r['request_id']}` | {r['required_flow_correction_expected_minus_actual']} | {r['candidate_count']} | {r['matching_set_count']} | {r['classification']} |")
    lines += ["", "## Nearest single-flow candidates", "", "The following table reports the nearest evidence-supported single edits by arithmetic residual. A candidate is not claimed to explain a solved row unless the bounded decision recomputation matches.", "", "| Request | Required correction | Candidate correction | Delta explained | Residual | Candidate |", "|---|---:|---:|---:|---:|---|"]
    for r in explanations:
        for near in r["nearest_single_candidate_corrections"][:3]:
            lines.append(f"| `{r['request_id']}` | {r['required_flow_correction_expected_minus_actual']} | {near['delta_explained']} | {near['delta_explained']} | {near['residual']} | {near['candidate']['label']} |")
    lines += ["", "## Search bound", "", "Each request is searched through combinations of at most three candidates after an arithmetic reachability bound. Matching sets are diagnostics only; they are not answer-driven production selections.", ""]
    (evaluation / "s16_minimal_flow_explanations.md").write_text("\n".join(lines), encoding="utf-8")

    by_family = Counter()
    for r in records:
        for field in r["differing_fields"]:
            if field == "amount_safe_to_pay": by_family["recurrence stream identity / active-stale / explicit reconciliation"] += 1
            elif field == "earliest_date_for_full_payment": by_family["earliest-safe-date downstream of balance path"] += 1
            elif field in {"affordability_status", "recommended_payment_method", "payment_plan"}: by_family["payment eligibility downstream of path"] += 1
            elif field == "spending_changes_needed": by_family["spending-change eligibility downstream of path"] += 1
            else: by_family["serialization/explanation"] += 1
    lines = ["# S16 latent rule frequency", "", "Frequency is counted across residual fields, with repeated transformations assessed against the bounded candidate explanations and chronology assignment.", "", "| Candidate transformation | Independent evidence | Numeric residuals explained | Cross-user support | Contract status |", "|---|---|---:|---|---|"]
    lines += ["| explicit occurrence suppresses one inferred occurrence | same economic dimensions and same settlement date; description mismatch is allowed | 0 newly proven by bounded search | observed in collision audit | compliant and already promoted only for salary same-date collision |", "| rotating labels form one chronological stream | multiple labels inside same user/category/date bucket | 0 globally promoted; existing sequence candidates remain 21 numeric mismatches | several users, but counterexamples also support independent streams | plausible but not selected |", "| parallel streams require repeated incompatible overlap | chronology assignment emits multi-stream groups only with affirmative concurrency | no overall S16 improvement demonstrated | dataset-wide diagnostic | compliant in principle |", "| stale stream cutoff after missed cadence windows | requires cadence plus missed occurrences/lifecycle evidence | no stable threshold found in solved constraints | insufficient cross-user stability | not promoted |", "| observed historical amount replaces max-last-3 | legitimate same-stream amount alternatives | no contract-wide improvement demonstrated | variable categories are heterogeneous | not promoted |"]
    lines += ["", "## Ranking conclusion", "", "The only repeated rule with direct solved-sample and contract evidence already in production is bounded cadence plus same-date salary collision suppression. The remaining numeric residuals do not share one arithmetic correction: they span small amount replacements, whole occurrences, and large stream-level deltas. Chronology is useful evidence but the candidate policies tested so far do not identify a stable global partition.", ""]
    (evaluation / "s16_latent_rule_frequency.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# S16 dataset generator signatures", "", "Dataset-wide structural scan of supplied financial events. These signatures are diagnostic evidence only; no solved answer, request ID, or user ID is used in production.", "", f"- Groups: `{signatures['summary']['groups']}`", f"- Multi-label groups: `{signatures['summary']['groups_with_multiple_labels']}`", f"- Description-rotation groups: `{signatures['summary']['description_rotation_groups']}`", f"- Amount-rotation groups: `{signatures['summary']['amount_rotation_groups']}`", "", "## Repeated patterns", "", "- Economic buckets frequently contain multiple descriptions, so description equality is not a safe absolute identity key.", "- Chronological gap medians cluster around category-specific fixed cadences, but the same category can exhibit multiple phases and irregular variable spending.", "- Amount sequences are heterogeneous: some streams are fixed, some rotate amounts, and some have sparse one-off events.", "- Explicit future rows and projected rows share economic dimensions in some histories; same-date reconciliation is therefore a valid general operation, but date/category coincidence alone cannot prove independent-stream collapse.", "", "## Counterexamples", "", "The scan records both multi-label chronological sequences and buckets with repeated incompatible phases. A label-rotation rule predicts some sequences, but a blanket collapse merges affirmative concurrent obligations; a blanket label split misses rotating streams. These are the structural reasons the current residuals cannot be closed by a broad category or description policy.", "", "## Representative records", ""]
    for item in signatures["description_rotation_examples"][:20]:
        lines.append(f"- `{item['group'][0]}/{item['group'][2]}`: {item['description_sequence']}")
    (evaluation / "s16_dataset_generator_signatures.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines = ["# S16 expected path constraints", "", "Expected path constraints are reconstructed from safe amount, reserve, and earliest-date semantics. They are post-hoc diagnostics, not production labels.", "", "| Request | Exact/lower-bound trough | Actual trough | First actual target-level date | Expected earliest | First violation paying expected date |", "|---|---|---|---|---|---|"]
    for r in records:
        lines.append(f"| `{r['request_id']}` | {r['expected_implied_minimum_constraint']['type']} `{r['expected_implied_minimum_constraint']['balance']}` | `{r['actual_minimum_balance']}` on `{r['actual_trough_date']}` | `{r['first_actual_date_at_or_below_expected_constraint'] or 'not reached'}` | `{r['expected_earliest_full_payment'] or 'none'}` | `{r['first_actual_violation_when_paying_on_expected_earliest'] or 'none'}` |")
    lines += ["", "## First incompatible events", ""]
    for r in records:
        first = next((row for row in r["actual_path"] if row["date"] == r["first_actual_date_at_or_below_expected_constraint"]), None)
        if first:
            flows = [f for f in r["candidate_future_flows"] if f["date"] == first["date"]]
            lines.append(f"- `{r['request_id']}` first reaches the expected implied level on `{first['date']}` with net flow `{first['flow']}`; candidate events: {', '.join(f['event_id'] for f in flows) or 'none'}.")
        else:
            lines.append(f"- `{r['request_id']}` never reaches its expected implied level on the current path; the actual trough is `{r['actual_trough_date']}`.")
    lines += ["", "A payment-date violation is evidence that the current path cannot support the expected full-payment date, but it does not identify whether the cause is a missing occurrence, an extra occurrence, or timing without a stream assignment. Those alternatives are enumerated separately in the minimal-flow artifact.", ""]
    (evaluation / "s16_expected_path_constraints.md").write_text("\n".join(lines), encoding="utf-8")


def main_run():
    profiles, requests, expected, canonical, options = make_context()
    records = baseline_records(profiles, requests, expected, canonical, options)
    explanations = minimal_explanations(profiles, requests, expected, canonical, options, records)
    assignments = stream_assignments(canonical)
    signatures = generator_signatures(main.read_csv("financial_events.csv"))
    write_reports(records, explanations, assignments, signatures)
    print(json.dumps({"residual_rows": len(records), "differing_fields": sum(len(r["differing_fields"]) for r in records), "minimal_classifications": Counter(r["classification"] for r in explanations), "latent_assignment_groups": len(assignments), "generator_signatures": signatures["summary"]}, sort_keys=True))


if __name__ == "__main__":
    main_run()
