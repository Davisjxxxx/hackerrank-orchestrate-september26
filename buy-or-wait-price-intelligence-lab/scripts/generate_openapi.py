from __future__ import annotations

import json
from pathlib import Path

from price_intel.api import create_app


root = Path(__file__).resolve().parents[1]
(root / "docs").mkdir(exist_ok=True)
(root / "docs" / "openapi.json").write_text(json.dumps(create_app().openapi(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(root / "docs" / "openapi.json")
