from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .targets import RuntimeIngress


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "generated" / "reports"


def _load_jsonargparse() -> Any:
    try:
        from jsonargparse import ActionConfigFile, ArgumentParser  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "jsonargparse is not installed. Add it to the runtime env before using this adapter."
        ) from exc
    return ActionConfigFile, ArgumentParser


def build_parser() -> Any:
    ActionConfigFile, ArgumentParser = _load_jsonargparse()
    parser = ArgumentParser(
        prog="spec-python-runtime-ingress",
        env_prefix="SPEC_PY",
        default_env=True,
        exit_on_error=False,
    )
    parser.add_argument("--config", action=ActionConfigFile)
    parser.add_argument("--mode", choices=["validate", "normalize"], default="validate")
    parser.add_class_arguments(RuntimeIngress, "input")
    return parser


def write_report(name: str, data: dict[str, Any]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / name
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = build_parser()
    cfg = parser.parse_args()

    parser.validate(cfg)
    normalized = parser.dump(cfg)

    report = {
        "ok": True,
        "mode": cfg.mode,
        "artifact": cfg.input.artifact,
        "reject_unknown_keys": cfg.input.reject_unknown_keys,
    }
    write_report("runtime_ingress.json", report)

    normalized_path = REPORTS / "runtime_ingress.normalized.yaml"
    normalized_path.write_text(normalized, encoding="utf-8")
    print(normalized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
