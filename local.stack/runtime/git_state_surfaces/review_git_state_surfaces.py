from __future__ import annotations

import sys
from pathlib import Path

import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from functions import check_gix_runtime, check_sem_runtime

    return check_gix_runtime, check_sem_runtime, mo


@app.cell
def _(check_gix_runtime, check_sem_runtime):
    gix_status = check_gix_runtime()
    sem_status = check_sem_runtime()
    return gix_status, sem_status


@app.cell
def _(gix_status, mo, sem_status):
    return mo.md(
        "\n".join(
            [
                "# Git Substrate Runtime Review",
                "",
                f"- gix status: `{gix_status.status}`",
                f"- sem status: `{sem_status.status}`",
                "",
                "Use this notebook as a review host over the shared wrapper functions.",
            ]
        )
    )


@app.cell
def _(gix_status, mo, sem_status):
    import json

    body = "\n\n".join(
        [
            "## Payloads",
            "```json",
            json.dumps(gix_status.payload, indent=2, sort_keys=True),
            "```",
            "```json",
            json.dumps(sem_status.payload, indent=2, sort_keys=True),
            "```",
        ]
    )
    return mo.md(body)


if __name__ == "__main__":
    app.run()
