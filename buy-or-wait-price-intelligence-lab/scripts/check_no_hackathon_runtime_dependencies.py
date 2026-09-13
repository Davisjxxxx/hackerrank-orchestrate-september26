"""Fail if production finance modules depend on organizer artifacts."""
from __future__ import annotations

import ast
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "src" / "finance_platform"]
BAD = ("dataset/", "dataset\\", "sample_requests.csv", "output.csv", "financial_events.csv", "request_01", "request_02")

def main() -> int:
    violations: list[str] = []
    for target in TARGETS:
        for path in target.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            try: ast.parse(source)
            except SyntaxError as exc:
                violations.append(f"{path}: syntax error: {exc}"); continue
            for line_no, line in enumerate(source.splitlines(), 1):
                if any(token in line for token in BAD) or re.search(r"request_\d{2}", line):
                    violations.append(f"{path}:{line_no}: organizer reference")
    if violations:
        print("\n".join(violations)); return 1
    print("PASS: finance_platform has no organizer-data runtime dependencies")
    return 0

if __name__ == "__main__": sys.exit(main())
