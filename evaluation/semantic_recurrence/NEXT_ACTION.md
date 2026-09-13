# Next action: finish or formally stop the bounded semantic experiment

This is the exact continuation point after `STATE.md`. Do not modify
`code/main.py`, `dataset/*`, `output.csv`, packaging, the product worktree, or
the release branch.

## 1. Verify the frozen base

```bash
cd /home/jd/hackerrank-orchestrate-september26
git branch --show-current
git rev-parse HEAD
sha256sum code/main.py
git diff --check
```

Expected: `main`, `e383c33267b856acace35ce39abb93fe9f01c403`, and
`2be2ba0189107f791d3007cb01d420eeaf682571a7dca27ac4c945ea0abc7c30`.

## 2. Continue from the local cache using the faster model

Use the same model name so existing Llama cache keys remain valid:

```bash
SEMANTIC_MODEL=llama3.2:3b \
  PYTHONPATH=code:evaluation \
  python3 evaluation/semantic_recurrence_evaluate.py
```

The resolver will reuse exact cache hits and call Ollama only for unresolved
sample users. Keep the model temperature at `0` and seed at `0`. Do not pass
`sample_requests.csv` or any solved output to the resolver process; the current
evaluator loads expected rows only after `resolve_users()` returns.

## 3. If another interruption is needed, preserve progress before stopping

Before interrupting, record:

```bash
find /tmp/buy_or_wait_semantic_cache -maxdepth 1 -type f -name '*.json' | wc -l
```

For every cache file, record its `.model`, `.usage.input_tokens`,
`.usage.output_tokens`, and `.response.streams | length`. Do not claim sample
metrics unless `semantic_recurrence_results.json` exists and was produced by a
complete 25-user run.

## 4. After a complete pass, run the cache replay

Run the exact command a second time. It must report `calls: 0` and reproduce the
same semantic metrics and diagnostics. Compare the serialized result hashes.

Then run the resolver metamorphic checks, without solved labels:

- reorder packet event rows;
- consistently rename event IDs and the corresponding evidence references;
- consistently replace the user ID outside the packet while keeping evidence
  unchanged.

The structural stream assignment must remain equivalent modulo identifiers and
ordering.

## 5. Promotion decision

Compare the complete candidate against the frozen R0 metrics in `STATE.md`.
Promotion is disallowed unless the candidate has explainable, multi-user gains
in exact safe amounts/core rows, no hard-rule regression, valid deterministic
replay, valid contract tests, and no request-specific or solved-label leakage.

If it does not beat R0, stop with:

```text
SEMANTIC RECURRENCE DID NOT BEAT R0
```

If no complete run can be obtained, stop with:

```text
BLOCKED — SEMANTIC RUN INCOMPLETE
```

Do not invent candidate metrics from the partial cache and do not promote the
evaluation files into production.
