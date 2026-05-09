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
