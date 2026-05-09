from __future__ import annotations

from state_core import Backend, Encoding, render_response


def state_get_mcp(*, backend: Backend = "gix", encoding: Encoding = "json") -> str:
    return render_response(
        operation="get_state",
        backend=backend,
        encoding=encoding,
        transport="mcp",
    )

