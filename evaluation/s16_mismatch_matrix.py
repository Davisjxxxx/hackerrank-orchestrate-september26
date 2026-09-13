"""Emit the field-level S16 golden mismatch matrix."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


FIELD_ROOT_CAUSE = {
    "amount_safe_to_pay": "forecast semantics: recurrence/lifecycle/evidence affects the binding trough",
    "affordability_status": "planner eligibility/status derived from the forecast predicate",
    "recommended_payment_method": "planner candidate eligibility/ranking derived from the forecast predicate",
    "payment_plan": "planner date/amount construction or field-specific serialization",
    "earliest_date_for_full_payment": "forecast date calculation / same-day ordering",
    "spending_changes_needed": "spending-change legality/enumeration or binding forecast trough",
    "decision_explanation": "deterministic explanation family follows the selected decision",
}


def run() -> int:
    expected = main.read_csv("sample_requests.csv")
    actual = main.execute(False, main.WindowPolicy.DAYS_0_THROUGH_89)
    rows = []
    clusters: dict[str, list[str]] = defaultdict(list)
    for want, got in zip(expected, actual):
        for field in main.OUTPUT_COLUMNS[1:]:
            if want[field] == got[field]:
                continue
            item = {
                "request_id": want["request_id"],
                "field": field,
                "expected": want[field],
                "actual": got[field],
                "likely_root_cause": FIELD_ROOT_CAUSE[field],
            }
            rows.append(item)
            clusters[FIELD_ROOT_CAUSE[field]].append(want["request_id"])
    payload = {"rows": rows, "field_counts": dict(Counter(x["field"] for x in rows)), "clusters": {k: sorted(v) for k, v in clusters.items()}}
    (ROOT / "evaluation" / "s16_mismatch_matrix.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# S16 exact mismatch matrix", "", "| request_id | differing field | expected | actual | likely root cause |", "|---|---|---:|---:|---|"]
    for x in rows:
        lines.append(f"| `{x['request_id']}` | `{x['field']}` | `{x['expected']}` | `{x['actual']}` | {x['likely_root_cause']} |")
    lines += ["", "## Field counts", ""]
    for field, count in sorted(payload["field_counts"].items()):
        lines.append(f"- `{field}`: {count}")
    lines += ["", "## Shared clusters", ""]
    for cause, ids in sorted(clusters.items()):
        lines.append(f"- **{cause}**: {', '.join(f'`{x}`' for x in ids)}")
    (ROOT / "evaluation" / "s16_mismatch_matrix.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"S16 mismatch fields={len(rows)} rows={len({x['request_id'] for x in rows})}/25")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
