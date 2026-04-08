# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "marimo",
#     "msgspec",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from state_core import render_response

    return mo, render_response


@app.cell
def _(mo):
    mode = mo.app_meta().mode
    backend = mo.ui.dropdown(options=["gix", "sem"], value="gix", label="backend")
    operation = mo.ui.dropdown(
        options=["get_state", "hydrate_state"],
        value="get_state",
        label="operation",
    )
    encoding = mo.ui.dropdown(
        options=["json", "ndjson", "jsonl"],
        value="json",
        label="encoding",
    )
    output_root = mo.ui.text(label="output-root", placeholder="optional output root")
    controls = mo.hstack([backend, operation, encoding])
    return backend, controls, encoding, mode, operation, output_root


@app.cell
def _(controls, mo, output_root):
    mo.vstack(
        [
            mo.md("# Default Agent Marimo code_mode Environment"),
            mo.md(
                "This notebook is a thin Marimo host over the canonical `state_core.py` runtime surface for the recovered `gix` and `sem` adapters."
            ),
            controls,
            output_root,
        ]
    )
    return


@app.cell
def _(backend, encoding, mode, operation, output_root, render_response):
    output_root_value = output_root.value.strip() or None
    rendered = render_response(
        operation=operation.value,
        backend=backend.value,
        encoding=encoding.value,
        output_root=output_root_value,
        transport="direct" if mode != "script" else "acp",
    )
    return output_root_value, rendered


@app.cell
def _(mo, rendered):
    mo.md(
        "\n".join(
            [
                "## Structured Response",
                "```json",
                rendered.rstrip(),
                "```",
            ]
        )
    )
    return


if __name__ == "__main__":
    app.run()
