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
