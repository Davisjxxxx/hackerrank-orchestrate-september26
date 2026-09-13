# Next action: resume bounded semantic recurrence experiment

This handoff is for a fresh Codex session after the remote checkpoint was pushed.
Do not modify `dataset/*`, `output.csv`, packaging, the product worktree, or the
release branch until a semantic candidate has completed the promotion gates.

## 1. Verify the remote checkpoint

```bash
cd /home/jd/hackerrank-orchestrate-september26
git fetch origin
git switch work/semantic-recurrence
git pull --ff-only origin work/semantic-recurrence
git branch --show-current
git rev-parse HEAD
sha256sum code/main.py
git diff --check
```

Expected branch:

```text
work/semantic-recurrence
```

The semantic checkpoint branch descends from frozen R0 commit:

```text
e383c33267b856acace35ce39abb93fe9f01c403
```

The original checkpoint commit is:

```text
bb0db663f28f42c8baddd7f55eaf5fda31b08ea5
```

`code/main.py` must remain:

```text
SHA256 2be2ba0189107f791d3007cb01d420eeaf682571a7dca27ac4c945ea0abc7c30
```

A later documentation-only handoff commit may make branch HEAD newer than
`bb0db663...`; this is expected. The production finance file hash above is the
important frozen-base check.

## 2. Read the checkpoint before doing work

Read, in this order:

```text
evaluation/semantic_recurrence/STATE.md
evaluation/semantic_recurrence/REMOTE_HANDOFF.md
evaluation/semantic_recurrence_policy.py
evaluation/semantic_recurrence_evaluate.py
evaluation/residual_forensics.csv
evaluation/residual_cashflow_items.csv
evaluation/conflict_chain_inventory.md
```

Do not restart the broad audit. The unresolved problem is recurrence
materialization/stream semantics.

## 3. Resume the local semantic experiment

Local Ollama was available with `llama3.2:3b`. Existing exact cache hits may
still exist on the same workstation under:

```text
/tmp/buy_or_wait_semantic_cache/
```

Check before running:

```bash
find /tmp/buy_or_wait_semantic_cache -maxdepth 1 -type f -name '*.json' 2>/dev/null | wc -l
```

Then run:

```bash
SEMANTIC_MODEL=llama3.2:3b \
  PYTHONPATH=code:evaluation \
  python3 evaluation/semantic_recurrence_evaluate.py
```

Keep model temperature `0` and seed `0`. Do not pass solved sample outputs to
the recurrence resolver. The semantic model may classify participant-visible
evidence only; affordability arithmetic and plan selection remain deterministic.

## 4. Token/context safety

Do not depend on one Codex context to finish everything.

If the session approaches roughly 60-70% of usable context, stop exploration and
write a durable checkpoint before continuing in a fresh session. Record:

```text
cache-file count
completed users if available
model used
commands run
errors
files changed
exact next command
```

Do not leave material reasoning only in the conversation.

## 5. Improve progress visibility before a long rerun if needed

If the evaluator still provides no useful partial progress, make only an
evaluation-layer change so completed users/batches are persisted to a progress
manifest. Do not change `code/main.py` for this purpose.

The semantic model output must remain isolated from solved labels. If touching
the evaluator, prefer loading solved expected rows only after `resolve_users()`
returns so the process boundary is also obvious in code review.

## 6. After a complete 25-user pass

Require all of the following before considering promotion:

1. Write complete semantic candidate metrics.
2. Run the exact command again from cache; model calls must be zero for cache
   hits and result metrics must reproduce.
3. Run metamorphic checks without solved labels:
   - reorder packet event rows;
   - consistently rename event IDs and evidence references;
   - change external user identifiers while preserving evidence.
4. Run finance contract/invariant tests.
5. Produce request-level diagnostics for every changed sample request.
6. Compare against frozen R0:

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

Promotion is disallowed unless gains are multi-user, explainable from actual
evidence, free of sample/request special-casing, and do not introduce hard-rule
regressions.

## 7. Stop conditions

If the complete semantic candidate does not materially beat R0, stop with:

```text
SEMANTIC RECURRENCE DID NOT BEAT R0
```

If a complete run cannot be obtained, stop with:

```text
BLOCKED — SEMANTIC RUN INCOMPLETE
```

If it passes the promotion gates, stop with:

```text
SEMANTIC RECURRENCE CANDIDATE READY FOR INDEPENDENT REVIEW
```

Do not merge to `main`, regenerate the final 250-row submission, rebuild
`code.zip`, or submit to HackerRank until the independent review occurs.
