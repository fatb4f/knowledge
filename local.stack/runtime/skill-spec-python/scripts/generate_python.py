from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "specs" / "source"
GENERATED_PYTHON = ROOT / "generated" / "python"
GENERATED_REPORTS = ROOT / "generated" / "reports"


MODELS = {
    "state_models.py": '''
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

import msgspec


FreshnessMode = Literal["cached", "fresh", "hydrated"]
Backend = Literal["gix", "sem", "combined"]


class RepoRef(msgspec.Struct, forbid_unknown_fields=True):
    root: str
    head: str | None = None
    branch: str | None = None


class Freshness(msgspec.Struct, forbid_unknown_fields=True):
    mode: FreshnessMode
    source_snapshot_id: str | None = None


class StatePayload(msgspec.Struct, forbid_unknown_fields=True):
    git: dict[str, Any]
    semantic: dict[str, Any]
    workspace: dict[str, Any]


class Provenance(msgspec.Struct, forbid_unknown_fields=True):
    backend: Backend
    inputs: list[str]
    warnings: list[str]


class StateV1(msgspec.Struct, forbid_unknown_fields=True):
    schema_version: Literal["state.v1"] = "state.v1"
    snapshot_id: str
    repo_ref: RepoRef
    observed_at: datetime
    freshness: Freshness
    state: StatePayload
    provenance: Provenance
'''.strip()
    + "\n",
    "session_models.py": '''
from __future__ import annotations

from datetime import datetime
from typing import Literal

import msgspec


Host = Literal["marimo"]
Transport = Literal["direct", "mcp", "acp"]
StalenessMode = Literal["fresh", "stale", "unknown"]


class Staleness(msgspec.Struct, forbid_unknown_fields=True):
    mode: StalenessMode
    observed_at: datetime | None = None


class SessionV1(msgspec.Struct, forbid_unknown_fields=True):
    artifact_type: Literal["session"] = "session"
    artifact_version: Literal["v1"] = "v1"
    session_id: str
    host: Host
    transport: Transport
    staleness: Staleness
    lineage_refs: list[str] | None = None
'''.strip()
    + "\n",
    "output_models.py": '''
from __future__ import annotations

from typing import Literal

import msgspec


Encoding = Literal["json", "ndjson", "jsonl"]


class OutputV1(msgspec.Struct, forbid_unknown_fields=True):
    artifact_type: Literal["output"] = "output"
    artifact_version: Literal["v1"] = "v1"
    encoding: Encoding
    schema_ref: str
    streaming: bool | None = None
    notes: list[str] | None = None
'''.strip()
    + "\n",
    "codecs.py": '''
from __future__ import annotations

import json
from typing import Any

import msgspec


json_encoder = msgspec.json.Encoder()


def encode_json(value: Any) -> bytes:
    return json_encoder.encode(value)


def encode_jsonl(values: list[Any]) -> bytes:
    return b"".join(json_encoder.encode(value) + b"\\n" for value in values)


def pretty_json(value: Any) -> str:
    return json.dumps(msgspec.to_builtins(value), indent=2, sort_keys=True)
'''.strip()
    + "\n",
    "__init__.py": '''
from .codecs import encode_json, encode_jsonl, pretty_json
from .output_models import OutputV1
from .session_models import SessionV1, Staleness
from .state_models import Freshness, Provenance, RepoRef, StatePayload, StateV1
'''.strip()
    + "\n",
}


def main() -> int:
    GENERATED_PYTHON.mkdir(parents=True, exist_ok=True)
    GENERATED_REPORTS.mkdir(parents=True, exist_ok=True)

    source_titles = {}
    for name in ("state.schema.json", "session.schema.json", "output.schema.json"):
        payload = json.loads((SOURCE / name).read_text())
        source_titles[name] = payload.get("title")

    written = []
    for name, content in MODELS.items():
        path = GENERATED_PYTHON / name
        path.write_text(content)
        written.append(path.name)

    report = {
        "task": "generate-python",
        "status": "ok",
        "written": written,
        "target": "msgspec.Struct",
        "sources": source_titles,
    }
    (GENERATED_REPORTS / "generation.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
