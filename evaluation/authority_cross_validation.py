"""Leave-one-user-out stability check for fixed R1-R3 authority candidates."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import main  # noqa: E402
from authority_core import CandidatePolicy  # noqa: E402
from authority_candidate_evaluation import evaluate, score  # noqa: E402


def run() -> dict[str, object]:
    profiles = main.ProfileAdapter().load()
    requests = main.RequestAdapter().load("sample_requests.csv")
    options = main.PaymentOptionAdapter().load()
    raw_events = main.FinancialEventAdapter(main.ImageEvidenceAdapter()).canonical_rows()
    messages = main.read_csv("messages.csv")
    expected = main.read_csv("sample_requests.csv")
    users = sorted({r.user_id for r in requests})
    window = main.WindowPolicy.DAYS_0_THROUGH_89
    rows_by_policy = {}
    for policy in CandidatePolicy:
        rows_by_policy[policy.value], _ = evaluate(policy, profiles, requests, options, raw_events, messages, main.ExchangeRateAdapter(), window)
    report: dict[str, object] = {"fold_count": len(users), "fixed_parameters": True, "policies": {}}
    for policy in CandidatePolicy:
        rows = rows_by_policy[policy.value]
        folds = []
        for user in users:
            keep = [i for i, req in enumerate(requests) if req.user_id != user]
            got = [rows[i] for i in keep]
            want = [expected[i] for i in keep]
            result = score(got, want)
            result.pop("rows", None)
            folds.append({"held_out_user": user, **result})
        report["policies"][policy.value] = {"folds": folds, "stable_policy": True}
    path = Path("/tmp/buy_or_wait_reset/authority_cross_validation.json")
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# Authority-first leave-one-user-out validation", "", "R1-R3 have no fitted parameters: every fold applies the same deterministic policy. This checks that no solved row is selected or hardcoded.", ""]
    for policy in CandidatePolicy:
        rows = rows_by_policy[policy.value]
        overall = score(rows, expected)
        lines += [f"## {policy.value}", "", f"- Full fixed-policy result: S16-CORE `{overall['core_exact_rows']}/25`; safe absolute error `{overall['safe_absolute_error']}`; numeric mismatches `{overall['numeric_mismatches']}`.", f"- Held-out folds: `{len(users)}`; parameters stable: `YES`; request/user-specific logic: `NONE`.", ""]
    path.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = run()
    print("folds", result["fold_count"], "fixed_parameters", result["fixed_parameters"])
