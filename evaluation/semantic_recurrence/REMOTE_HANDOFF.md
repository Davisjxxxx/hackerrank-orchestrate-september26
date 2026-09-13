# Remote semantic recurrence handoff

This file records the post-checkpoint remote state after the local Codex session
was stopped safely and its durable work was pushed.

## Remote branch

```text
work/semantic-recurrence
```

Original semantic checkpoint commit:

```text
bb0db663f28f42c8baddd7f55eaf5fda31b08ea5
```

The branch is intentionally separate from `main` and
`release/hackathon-final`.

## Frozen production baseline

The semantic branch descends from R0:

```text
e383c33267b856acace35ce39abb93fe9f01c403
```

Frozen production finance hash:

```text
code/main.py SHA256
2be2ba0189107f791d3007cb01d420eeaf682571a7dca27ac4c945ea0abc7c30
```

Baseline sample metrics:

```text
exact rows: 3/25
exact safe amounts: 4/25
numeric mismatches: 21/25
absolute safe error: 6,930,596.72
status exact: 21/25
method exact: 24/25
plan exact: 22/25
earliest-date exact: 18/25
```

## What is actually committed remotely

The checkpoint commit contains the authority/recurrence forensic artifacts and
the evaluation-only semantic experiment implementation, including:

```text
evaluation/semantic_recurrence_policy.py
evaluation/semantic_recurrence_evaluate.py
evaluation/semantic_recurrence/STATE.md
evaluation/semantic_recurrence/NEXT_ACTION.md
```

plus the prior residual, authority, recurrence, and test artifacts committed by
the checkpoint.

`STATE.md` was originally written before the final branch commit/push, so any
sentence inside it saying the semantic files were still untracked or that no
commit/push had occurred describes the instant of the local stop, not the later
remote checkpoint. This file is the authoritative correction for remote state.

## What is not remotely preserved

Partial Ollama response cache files were intentionally not committed. On the
same workstation they may still exist at:

```text
/tmp/buy_or_wait_semantic_cache/
```

There were six partial cache files at the checkpoint, but there was no complete
25-user semantic pass and therefore no valid semantic candidate metrics or
promotion decision.

No dataset files, root `output.csv`, submission package, product worktree,
secrets, or temporary caches were changed by the semantic checkpoint.

## Current interpretation

The deterministic forensic analysis found that the remaining numeric sample
residuals are dominated by recurrence materialization/stream reconstruction:
717 of 737 attributed forecast items were projected recurrence rows, and all 29
items on residual binding-trough dates were projected recurrence rows.

The semantic experiment is therefore narrow and evaluation-only. The model may
interpret participant-visible recurrence evidence, but deterministic code must
continue to own cash arithmetic, safety constraints, payment eligibility,
ranking, and final recommendations.

## Promotion prohibition

Do not merge the semantic experiment into production unless a complete run:

- materially improves exact safe amounts/core rows across multiple users;
- has no hard-rule regression;
- has deterministic cache replay;
- passes metamorphic/generalization checks;
- passes finance contract tests;
- contains no request-specific logic or solved-label leakage;
- has request-level changes explainable from participant-visible evidence.

Until then, R0 remains the frozen production control rather than an approved
submission candidate.
