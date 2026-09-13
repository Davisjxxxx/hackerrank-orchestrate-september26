# Usage report

Final scored run: local deterministic core, no interpretation-model calls.

| Provider | Model | Calls | Input tokens | Output tokens | Cached tokens | Estimated cost |
|---|---|---:|---:|---:|---:|---:|
| local | none | 0 | 0 | 0 | 0 | $0.00 |

Overall calls: 0. Total tokens: 0. Average tokens per request: 0. Estimated total cost: $0.00. Estimated per-request cost: $0.00.

## Runtime facts

- Entry point: `python3 code/main.py`
- Frozen `code/main.py` SHA256: `7a92094d5999aa9355efc3a07785b4e289aae9a28711a405bc2efd89fd58d1c4`
- Deterministic final `output.csv` SHA256: `580233223fbf85dbd502bbc42143b390e335f1833b0a8dfc052af7af174b4a1d`
- Rows produced: 250 (one per `dataset/requests.csv` entry, matching required schema)
- Three consecutive full-dataset runs are byte-identical (hash equality PASS)

## Provider/model calls

The scored runtime imports only Python standard library modules (`argparse`, `csv`, `itertools`, `json`, `re`, `statistics`, `dataclasses`, `datetime`, `decimal`, `enum`, `pathlib`, `typing`). It performs no HTTP calls, no third-party API calls, and no LLM/interpretation-model calls. There is nothing to bill for the final scored run.

## OCR note

`ImageEvidenceAdapter` optionally invokes a local PaddleOCR model against the packaged image evidence in `dataset/media/images/` and caches the extracted text in `evaluation/ocr_cache.json`. This is local OCR against local pixels; it is not a network or provider call and consumes no token budget. The submitted package ships the pre-populated `evaluation/ocr_cache.json`, so the final scored run reads from cache and does not invoke PaddleOCR at all.

## Development-time note

AI coding assistants (Claude Code, Codex) were used during development for source authoring, review, and forensic analysis. Those interactions are documented in `chat_transcript.txt`. They are development-time tooling and did not participate in the final scored runtime, which produces `output.csv` deterministically from local inputs.
