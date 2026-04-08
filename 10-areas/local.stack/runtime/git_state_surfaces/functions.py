from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from envelopes import RuntimeCheckEnvelope, RuntimeEmitEnvelope

BASE = Path(__file__).resolve().parents[2] / "proposals" / "git_substrate_adapters_v1"


def _run(script_name: str, *extra: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(BASE / script_name), *extra],
        cwd=BASE,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def _parse_json(stdout: str, stderr: str) -> dict[str, Any]:
    for text in (stdout, stderr):
        if not text:
            continue
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            continue
    return {}


def check_gix_runtime() -> RuntimeCheckEnvelope:
    code, stdout, stderr = _run("emit_gix_runtime.py", "--check-only")
    payload = _parse_json(stdout, stderr)
    return RuntimeCheckEnvelope(
        backend="gix",
        status="ok" if code == 0 else "runtime_unavailable",
        runtime_kind="gix",
        payload=payload,
    )


def emit_gix_runtime(output_root: str | None = None) -> RuntimeEmitEnvelope:
    extra = ["--output-root", output_root] if output_root else []
    code, stdout, stderr = _run("emit_gix_runtime.py", *extra)
    payload = _parse_json(stdout, stderr)
    return RuntimeEmitEnvelope(
        backend="gix",
        status="success" if code == 0 else "error",
        runtime_kind="gix",
        manifest_path=payload.get("manifest_path"),
        report_path=payload.get("report_path"),
        payload=payload or None,
    )


def check_sem_runtime() -> RuntimeCheckEnvelope:
    code, stdout, stderr = _run("emit_sem_runtime.py", "--check-only")
    payload = _parse_json(stdout, stderr)
    return RuntimeCheckEnvelope(
        backend="sem",
        status="ok" if code == 0 else "runtime_unavailable",
        runtime_kind="sem",
        payload=payload,
    )


def emit_sem_runtime(output_root: str | None = None) -> RuntimeEmitEnvelope:
    extra = ["--output-root", output_root] if output_root else []
    code, stdout, stderr = _run("emit_sem_runtime.py", *extra)
    payload = _parse_json(stdout, stderr)
    return RuntimeEmitEnvelope(
        backend="sem",
        status="success" if code == 0 else "error",
        runtime_kind="sem",
        manifest_path=payload.get("manifest_path"),
        report_path=payload.get("report_path"),
        payload=payload or None,
    )
