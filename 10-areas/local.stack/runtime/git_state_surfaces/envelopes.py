from __future__ import annotations

from typing import Any, Literal

import msgspec

Backend = Literal["gix", "sem"]
Status = Literal["ok", "runtime_unavailable", "success", "error"]


class RuntimeCheckEnvelope(msgspec.Struct, forbid_unknown_fields=True):
    backend: Backend
    status: Status
    runtime_kind: str
    payload: dict[str, Any]


class RuntimeEmitEnvelope(msgspec.Struct, forbid_unknown_fields=True):
    backend: Backend
    status: Status
    runtime_kind: str
    manifest_path: str | None = None
    report_path: str | None = None
    payload: dict[str, Any] | None = None
