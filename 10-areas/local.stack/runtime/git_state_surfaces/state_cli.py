from jsonargparse import ArgumentParser

from state_core import render_response


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="codex-state")
    parser.add_argument("operation", choices=["get_state", "hydrate_state"])
    parser.add_argument("--backend", choices=["gix", "sem"], default="gix")
    parser.add_argument("--encoding", choices=["json", "ndjson", "jsonl"], default="json")
    parser.add_argument("--transport", choices=["direct", "mcp", "acp"], default="direct")
    parser.add_argument("--output-root", default=None)
    return parser


def main() -> int:
    parser = build_parser()
    cfg = parser.parse_args()
    output_root = cfg.output_root or None
    rendered = render_response(
        operation=cfg.operation,
        backend=cfg.backend,
        encoding=cfg.encoding,
        output_root=output_root,
        transport=cfg.transport,
    )
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
