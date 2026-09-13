# Semantic recurrence experiment checkpoint

Checkpoint date: 2026-09-12

## Scope

This checkpoint stops the bounded AI-assisted semantic recurrence experiment at
the user's explicit stop request. No production finance behavior, dataset file,
root `output.csv`, package, product app, release branch, or remote was changed.

The only new source files in this pass are evaluation-only:

- `evaluation/semantic_recurrence_policy.py`
- `evaluation/semantic_recurrence_evaluate.py`

They are untracked working files and were not committed.

## Frozen R0 state

- Branch: `main`
- HEAD: `e383c33267b856acace35ce39abb93fe9f01c403`
- `code/main.py` SHA256: `2be2ba0189107f791d3007cb01d420eeaf682571a7dca27ac4c945ea0abc7c30`
- R0 full exact rows: `3/25`
- R0 exact safe amounts: `4/25`
- R0 numeric mismatches: `21/25`
- R0 absolute safe-amount error: `6,930,596.72`
- R0 status exact: `21/25`
- R0 method exact: `24/25`
- R0 plan exact: `22/25`
- R0 earliest-date exact: `18/25`
- R0 optimistic numeric errors: `19`
- R0 pessimistic numeric errors: `2`

The recovery branch `recovery/e383c33-r0-audit` already points to the frozen
commit. Existing dirty and untracked evaluation/product material was preserved.
`git diff --check` was clean at checkpoint time.

## Prior forensic findings retained

- `evaluation/residual_forensics.csv` contains 21 residual rows.
- `evaluation/residual_cashflow_items.csv` contains 737 attributed forecast
  items; 717 are projected recurrence rows.
- All 29 events on residual binding-trough dates were projected recurrence
  events.
- Optimistic residuals: 19 rows, total absolute signed delta `5,504,734.08`.
- Pessimistic residuals: 2 rows, total absolute signed delta `1,425,862.64`.
- Prior R1-R4/structural-granularity candidates did not meet promotion gates.
- `evaluation/conflict_chain_inventory.md` reports 25,342 events, 58 populated
  links, no missing link targets/cycles, 39 linked messages, 16 linked images,
  and no exact duplicate groups excluding event IDs.

## Model execution availability

Legitimate local Ollama execution is available. Installed models included
`qwen3-vl:2b-instruct-q8_0` and `llama3.2:3b`. No provider secret was printed.
The environment also has Claude credentials and an OpenAI key, but neither was
used. The experiment used local Ollama only, so model cost is `$0`.

Smoke-test evidence:

- `qwen3-vl:2b-instruct-q8_0` returned valid JSON for a tiny empty-history
  request in about 4.6 seconds with prompt/evaluation counts `21/6`.
- Large Qwen evidence packets produced incomplete JSON at the configured output
  boundary twice, so that model was not used for a complete pass.
- `llama3.2:3b` produced valid structured outputs for at least four evidence
  packets, which were persisted in the cache. A full pass was not completed.

## Evaluation implementation created

`evaluation/semantic_recurrence_policy.py` defines:

1. a strict JSON stream schema with member IDs, dimensions, confidence,
   cadence, amount basis, termination evidence, reason codes, and evidence IDs;
2. a participant-visible packet builder that omits request IDs, solved outputs,
   expected amounts, statuses, and sample labels;
3. a SHA256 cache key over model, prompt version, system prompt, and canonical
   evidence packet;
4. Ollama execution at temperature `0`, seed `0`, with local usage counters;
5. deterministic stream verification for member IDs, dimensions, cash status,
   chronology, cadence, currencies, evidence-derived amounts, and terminal
   claims;
6. a deterministic materializer that removes R0 projected rows, retains R0
   explicit rows, and materializes only verified semantic streams;
7. no LLM arithmetic, planner, affordability, payment-option, or ranking logic.

`evaluation/semantic_recurrence_evaluate.py` loads solved sample outputs only
after all user packets have been resolved, then runs the existing deterministic
planner and validator for comparison with R0.

## Commands run and results

Environment/model discovery:

```text
ollama list
ollama ps
claude --version
claude --help
```

Result: local Ollama models were present; Claude Code was installed at
`/home/jd/.nvm/versions/node/v22.18.0/bin/claude`; no external model call was
made.

Smoke test:

```bash
python3 - <<'PY'
import ollama
ollama.chat(model='qwen3-vl:2b-instruct-q8_0', ...)
PY
```

Result: valid JSON `{"streams": []}` for the tiny prompt.

Compilation:

```bash
python3 -m py_compile evaluation/semantic_recurrence_policy.py evaluation/semantic_recurrence_evaluate.py
```

Result: PASS before the interrupted evaluation.

First Qwen full evaluation:

```bash
PYTHONPATH=code:evaluation python3 evaluation/semantic_recurrence_evaluate.py
```

Result: model returned an unterminated JSON string after a large response;
no aggregate result was written.

Second Qwen attempt used a larger context and then a bounded schema. Result:
again incomplete JSON at the output boundary; no aggregate result was written.

Llama full evaluation:

```bash
SEMANTIC_MODEL=llama3.2:3b PYTHONPATH=code:evaluation python3 evaluation/semantic_recurrence_evaluate.py
```

Result: interrupted by the explicit stop request while resolving remaining
packets. No aggregate semantic metrics were written.

The last Llama run had four valid cache files and the prior Qwen attempts had
two valid cache files. Cache files are under `/tmp/buy_or_wait_semantic_cache/`.
They contain model outputs and local usage metadata only; they are not a
complete 25-user result set.

The Llama run was stopped with Ctrl-C while inside `ollama.chat`; the traceback
was an intentional interruption, not a production failure.

## Current limitations / unresolved issues

1. The 25-user semantic pass never completed, so there are no valid semantic
   candidate metrics, request-level effects, contract-test results, or
   promotion decision.
2. The model is available, but large packets are slow and can exhaust the
   structured-output budget. The response was bounded to 10 streams, 12 member
   IDs, and a 4,096-token output cap, but the packet size still makes execution
   expensive in wall-clock time.
3. The evaluator writes its aggregate report only after all users finish. A
   future continuation should add an evaluation-only progress manifest or run
   users in bounded batches so partial completion is visible without changing
   the finance runtime.
4. The current semantic candidate is not production code and must not be
   promoted based on partial cache contents.
5. The existing `SemanticRecurrencePolicy` materializer deliberately replaces
   all inferred R0 rows with verified semantic rows. This is an experiment
   choice that must be validated against explicit-vs-projected collision rules
   and the complete sample before any promotion discussion.

## Repository safety at stop

- `code/main.py` was not edited in this pass.
- `dataset/*` was not edited.
- `output.csv` was not regenerated.
- No package was built.
- No commit was made.
- No GitHub push or HackerRank submission was performed.
- `/home/jd/hackerrank-buy-or-wait-integration` was not touched.
