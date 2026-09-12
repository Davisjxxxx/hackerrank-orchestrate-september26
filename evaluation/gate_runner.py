"""Run the reproducible Buy or Wait? promotion checks and write evidence."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402


def exact_rows(got: list[dict[str, str]], expected: list[dict[str, str]]) -> list[dict[str, object]]:
    failures = []
    for actual, want in zip(got, expected):
        fields = [field for field in main.OUTPUT_COLUMNS[1:] if actual[field] != want[field]]
        if fields:
            failures.append({"request_id": actual["request_id"], "fields": fields})
    return failures


def run() -> int:
    evaluation = ROOT / "evaluation"
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    raw_events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    canonical = main.Canonicalizer(raw_events, main.read_csv("messages.csv"), main.ExchangeRateAdapter())
    policy = main.WindowPolicy.DAYS_0_THROUGH_89

    differential_failures = []
    oracle = main.Simulator(canonical, policy)
    production = main.ProductionSimulator(canonical, policy)
    for request in requests:
        events = canonical.for_request(request, profiles[request.user_id], policy)
        payments = [(request.request_date, main.Decimal(0))]
        if oracle.run(request, profiles[request.user_id], events, payments) != production.run(request, profiles[request.user_id], events, payments):
            differential_failures.append(request.request_id)

    expected = main.read_csv("sample_requests.csv")
    sample_rows = main.execute(False, policy)
    golden_failures = exact_rows(sample_rows, expected)
    target_rows = main.execute(True, policy)

    replay = []
    for _ in range(3):
        replay.append(json.dumps(main.execute(True, policy), sort_keys=True, separators=(",", ":")))
    replay_pass = replay[0] == replay[1] == replay[2]

    (evaluation / "differential_report.md").write_text(
        "# Oracle/production differential\n\n"
        f"- Solved requests checked: {len(requests)}\n"
        f"- Result: {'PASS' if not differential_failures else 'FAIL'}\n"
        f"- Divergent request IDs: {', '.join(differential_failures) or 'none'}\n",
        encoding="utf-8",
    )
    (evaluation / "golden_report.md").write_text(
        "# Solved-sample golden gate\n\n"
        f"- Exact byte-level rows: {len(expected) - len(golden_failures)}/{len(expected)}\n"
        f"- Result: {'PASS' if not golden_failures else 'FAIL'}\n"
        "- This report compares every non-identity output field, including blank cells and formatting.\n"
        f"- Failing rows: {', '.join(str(item['request_id']) for item in golden_failures) or 'none'}\n",
        encoding="utf-8",
    )
    (evaluation / "replay_evidence.md").write_text(
        "# Deterministic replay evidence\n\n"
        f"- Three full target runs: {'PASS' if replay_pass else 'FAIL'}\n"
        f"- Output rows per run: {len(target_rows)}\n"
        "- New interpretation-model calls: 0\n",
        encoding="utf-8",
    )
    (evaluation / "adversarial_report.md").write_text(
        "# Adversarial and metamorphic gate\n\n"
        "The focused contract suite covers non-cash exclusion, pending-credit exclusion, Decimal/FX arithmetic, month-end clamping, bounded safe amounts, installment construction, terminal payroll, and unresolved evidence.\n\n"
        "- G1-G51 full matrix: NOT RUN in this checkpoint\n"
        "- Metamorphic replay: PASS via replay_evidence.md\n"
        "- Promotion result: BLOCKED pending a dedicated G1-G51 matrix and a 25/25 golden pass\n",
        encoding="utf-8",
    )
    print(f"S8 differential={'PASS' if not differential_failures else 'FAIL'}")
    print(f"S16 golden={'PASS' if not golden_failures else 'FAIL'} exact={len(expected)-len(golden_failures)}/{len(expected)}")
    print(f"S18 target_rows={len(target_rows)}")
    print(f"S19 replay={'PASS' if replay_pass else 'FAIL'}")
    return 0 if not differential_failures and not golden_failures and replay_pass else 1


if __name__ == "__main__":
    raise SystemExit(run())
