from __future__ import annotations

from pathlib import Path

from jsonargparse import ArgumentParser

from state_core import Backend, Encoding, Operation, render_response


def replay_state(
    *,
    operation: Operation = "get_state",
    backend: Backend = "gix",
    encoding: Encoding = "json",
    output_root: str | None = None,
    destination: str | None = None,
) -> str:
    rendered = render_response(
        operation=operation,
        backend=backend,
        encoding=encoding,
        output_root=output_root,
        transport="direct",
    )
    if destination:
        Path(destination).write_text(rendered, encoding="utf-8")
    return rendered


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="codex-state-replay")
    parser.add_argument("operation", choices=["get_state", "hydrate_state"], default="get_state", nargs="?")
    parser.add_argument("--backend", choices=["gix", "sem"], default="gix")
    parser.add_argument("--encoding", choices=["json", "ndjson", "jsonl"], default="json")
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--destination", default=None)
    return parser


def main() -> int:
    parser = build_parser()
    cfg = parser.parse_args()
    rendered = replay_state(
        operation=cfg.operation,
        backend=cfg.backend,
        encoding=cfg.encoding,
        output_root=cfg.output_root or None,
        destination=cfg.destination or None,
    )
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
