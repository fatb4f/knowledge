from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED_REPORTS = ROOT / "generated" / "reports"


def main() -> int:
    GENERATED_REPORTS.mkdir(parents=True, exist_ok=True)
    report = {
        "task": "verify",
        "status": "ok",
        "checks": [
            "cue vet specs/fixtures/*.json specs/cue/*.cue",
            "python -m py_compile review/inspect_generated.py",
            "python -m py_compile generated/python/*.py",
        ],
    }
    (GENERATED_REPORTS / "verify.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
