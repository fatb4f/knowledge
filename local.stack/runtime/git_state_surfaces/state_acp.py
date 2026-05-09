from __future__ import annotations

from state_core import Backend, Encoding, render_response


def state_get_acp(*, backend: Backend = "gix", encoding: Encoding = "json") -> str:
    return render_response(
        operation="get_state",
        backend=backend,
        encoding=encoding,
        transport="acp",
    )


def state_hydrate_acp(
    *,
    backend: Backend = "gix",
    encoding: Encoding = "json",
    output_root: str | None = None,
) -> str:
    return render_response(
        operation="hydrate_state",
        backend=backend,
        encoding=encoding,
        output_root=output_root,
        transport="acp",
    )

