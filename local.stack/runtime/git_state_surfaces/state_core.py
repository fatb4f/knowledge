from __future__ import annotations

import json
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import msgspec

from envelopes import Backend, RuntimeCheckEnvelope, RuntimeEmitEnvelope
from functions import (
    check_gix_runtime,
    check_sem_runtime,
    emit_gix_runtime,
    emit_sem_runtime,
)

Operation = Literal["get_state", "hydrate_state"]
Encoding = Literal["json", "ndjson", "jsonl"]
Transport = Literal["direct", "mcp", "acp"]


class SessionEnvelope(msgspec.Struct, forbid_unknown_fields=True):
    artifact_type: Literal["session"] = "session"
    artifact_version: Literal["v1"] = "v1"
    session_id: str = ""
    host: Literal["marimo"] = "marimo"
    transport: Transport = "direct"
    staleness: dict[str, str] = msgspec.field(default_factory=dict)
    lineage_refs: list[str] = msgspec.field(default_factory=list)


class StatePayloadEnvelope(msgspec.Struct, forbid_unknown_fields=True):
    operation: Operation
    backend: Backend
    session: SessionEnvelope
    result: dict[str, Any]
    output: dict[str, str | bool]


class RuntimeEnvelope(msgspec.Struct, forbid_unknown_fields=True):
    host: Literal["marimo"] = "marimo"
    python: str = ""


class ResponseLineage(msgspec.Struct, forbid_unknown_fields=True):
    generated_from: None = None
    validated_against: list[str] = msgspec.field(default_factory=list)


class ResponseEnvelope(msgspec.Struct, forbid_unknown_fields=True):
    backend: Backend
    operation: Operation
    transport: Transport
    encoding: Encoding
    runtime: RuntimeEnvelope
    payload: dict[str, Any]
    session: SessionEnvelope
    output: dict[str, str | bool]
    artifact_type: Literal["response_envelope"] = "response_envelope"
    artifact_version: Literal["v1"] = "v1"
    kind: Literal["response"] = "response"
    errors: list[str] = msgspec.field(default_factory=list)
    lineage: ResponseLineage = msgspec.field(default_factory=ResponseLineage)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def build_session(
    *,
    operation: Operation,
    backend: Backend,
    transport: Transport = "direct",
    staleness_mode: Literal["fresh", "stale", "unknown"] = "unknown",
) -> SessionEnvelope:
    return SessionEnvelope(
        session_id=f"{operation}:{backend}:{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}",
        transport=transport,
        staleness={"mode": staleness_mode, "observed_at": _utc_now()},
        lineage_refs=[f"backend:{backend}", f"operation:{operation}"],
    )


def _get_backend_check(backend: Backend) -> RuntimeCheckEnvelope:
    if backend == "gix":
        return check_gix_runtime()
    return check_sem_runtime()


def _get_backend_emit(backend: Backend, output_root: str | None) -> RuntimeEmitEnvelope:
    if backend == "gix":
        return emit_gix_runtime(output_root=output_root)
    return emit_sem_runtime(output_root=output_root)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_state_v1(
    *,
    operation: Operation,
    backend: Backend,
) -> tuple[dict[str, Any], SessionEnvelope, dict[str, str | bool], list[str]]:
    with tempfile.TemporaryDirectory(prefix=f"codex-{operation}-{backend}-") as tmpdir:
        output_root = Path(tmpdir)
        gix = emit_gix_runtime(output_root=str(output_root))
        repo_state = _load_json(output_root / "repo_state.json")
        diff_state = _load_json(output_root / "diff_state.json")

        semantic_state: dict[str, Any] = {}
        warnings: list[str] = []
        provenance_backend: Literal["gix", "sem", "combined"]
        if backend == "sem":
            sem = emit_sem_runtime(output_root=str(output_root))
            semantic_diff = _load_json(output_root / "semantic_diff.json")
            review_basis = _load_json(output_root / "review_basis.json")
            semantic_state = {
                "semantic_diff": semantic_diff,
                "review_basis": review_basis,
                "runtime_status": sem.status,
            }
            provenance_backend = "combined"
            if sem.status != "success":
                warnings.append(f"semantic_runtime:{sem.status}")
        else:
            provenance_backend = "gix"

        if gix.status != "success":
            warnings.append(f"git_runtime:{gix.status}")

        observed_at = _utc_now()
        snapshot_id = f"{operation}:{backend}:{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
        state_payload = {
            "schema_version": "state.v1",
            "snapshot_id": snapshot_id,
            "repo_ref": {
                "root": repo_state["repository_path"],
                "head": repo_state["head"],
                "branch": repo_state["branch"],
            },
            "observed_at": observed_at,
            "freshness": {
                "mode": "fresh" if operation == "get_state" else "hydrated"
            },
            "state": {
                "git": {
                    "repo_state": repo_state,
                    "diff_state": diff_state,
                },
                "semantic": semantic_state,
                "workspace": {
                    "runtime_host": "marimo",
                    "repo_root": repo_state["repository_path"],
                },
            },
            "provenance": {
                "backend": provenance_backend,
                "inputs": [
                    "emit_gix_runtime.py",
                    *(["emit_sem_runtime.py"] if backend == "sem" else []),
                ],
                "warnings": warnings,
            },
        }

        session = SessionEnvelope(
            session_id=snapshot_id,
            transport="direct",
            staleness={"mode": "fresh", "observed_at": observed_at},
            lineage_refs=[f"backend:{backend}", f"operation:{operation}"],
        )
        output = {
            "artifact_type": "output",
            "artifact_version": "v1",
            "encoding": "json",
            "schema_ref": "state.v1",
            "streaming": False,
        }
        return state_payload, session, output, warnings


def get_state(
    *,
    backend: Backend = "gix",
    transport: Transport = "direct",
) -> StatePayloadEnvelope:
    state_payload, session, output, warnings = _build_state_v1(operation="get_state", backend=backend)
    session.transport = transport
    return StatePayloadEnvelope(
        operation="get_state",
        backend=backend,
        session=session,
        result={"state": state_payload, "warnings": warnings},  # type: ignore[arg-type]
        output=output,
    )


def hydrate_state(
    *,
    backend: Backend = "gix",
    output_root: str | None = None,
    transport: Transport = "direct",
) -> StatePayloadEnvelope:
    state_payload, session, output, warnings = _build_state_v1(operation="hydrate_state", backend=backend)
    session.transport = transport
    return StatePayloadEnvelope(
        operation="hydrate_state",
        backend=backend,
        session=session,
        result={"state": state_payload, "warnings": warnings},  # type: ignore[arg-type]
        output=output,
    )


def build_response_envelope(
    *,
    payload: StatePayloadEnvelope,
    encoding: Encoding,
) -> ResponseEnvelope:
    payload_dict = msgspec.to_builtins(payload)
    payload_dict["output"]["encoding"] = encoding
    payload_dict["output"]["streaming"] = encoding in {"ndjson", "jsonl"}
    errors: list[str] = []
    warnings = payload.result.get("warnings", []) if isinstance(payload.result, dict) else []
    errors.extend(str(item) for item in warnings)
    return ResponseEnvelope(
        backend=payload.backend,
        operation=payload.operation,
        transport=payload.session.transport,
        encoding=encoding,
        runtime=RuntimeEnvelope(python=_python_version()),
        payload=payload.result["state"] if isinstance(payload.result, dict) else {},
        session=payload.session,
        output=payload.output,
        errors=errors,
        lineage=ResponseLineage(
            validated_against=[
                "/home/chronos/src/kernel/control/modules/state/state.request_response_contract.v1.json",
                "/home/chronos/src/kernel/control/modules/state/session.metadata.v1.json",
                "/home/chronos/src/kernel/control/modules/state/output.encodings.v1.json",
                "/home/chronos/src/kernel/runtime/runtime.binding.v1.json",
                "/home/chronos/.local/opt/knowledge/10-areas/local.stack/runtime/response.envelope.v1.json"
            ]
        ),
    )


def render_response(
    *,
    operation: Operation,
    backend: Backend = "gix",
    encoding: Encoding = "json",
    output_root: str | None = None,
    transport: Transport = "direct",
) -> str:
    payload = (
        get_state(backend=backend, transport=transport)
        if operation == "get_state"
        else hydrate_state(backend=backend, output_root=output_root, transport=transport)
    )
    response = build_response_envelope(payload=payload, encoding=encoding)
    response_dict = msgspec.to_builtins(response)
    response_dict["output"]["encoding"] = encoding
    response_dict["output"]["streaming"] = encoding in {"ndjson", "jsonl"}
    if encoding == "json":
        return json.dumps(response_dict, indent=2, sort_keys=True)
    return f"{json.dumps(response_dict, sort_keys=True)}\n"
