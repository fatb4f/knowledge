from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs" / "source"
GENERATED_SCHEMAS = ROOT / "generated" / "schemas"
GENERATED_REPORTS = ROOT / "generated" / "reports"


MAP = {
    "state.schema.json": "state.v1.schema.json",
    "session.schema.json": "session.v1.schema.json",
    "output.schema.json": "output.v1.schema.json",
}


def main() -> int:
    GENERATED_SCHEMAS.mkdir(parents=True, exist_ok=True)
    GENERATED_REPORTS.mkdir(parents=True, exist_ok=True)

    written = []
    for src_name, dst_name in MAP.items():
        src = SOURCE / src_name
        dst = GENERATED_SCHEMAS / dst_name
        payload = json.loads(src.read_text())
        payload["_generated_from"] = src_name
        dst.write_text(json.dumps(payload, indent=2) + "\n")
        written.append(dst.name)

    report = {
        "task": "generate-schemas",
        "status": "ok",
        "written": written,
    }
    (GENERATED_REPORTS / "schemas.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
