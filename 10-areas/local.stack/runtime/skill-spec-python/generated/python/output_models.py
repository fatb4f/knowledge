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
