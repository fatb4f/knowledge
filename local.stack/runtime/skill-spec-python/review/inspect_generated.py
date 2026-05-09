# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    from pathlib import Path
    import marimo as mo

    root = Path(__file__).resolve().parents[1]
    reports_dir = root / "generated" / "reports"
    python_dir = root / "generated" / "python"
    return json, mo, python_dir, reports_dir


@app.cell
def _(python_dir, reports_dir):
    python_paths = sorted(python_dir.glob("*.py"))
    report_paths = sorted(reports_dir.glob("*.json"))
    return python_paths, report_paths


@app.cell
def _(mo, python_paths, report_paths):
    summary = mo.md(
        "\n".join(
            [
                "# Generated Artifact Review",
                "",
                f"- Python artifacts: {len(python_paths)}",
                f"- Report artifacts: {len(report_paths)}",
                "",
                "Use `marimo edit --sandbox review/inspect_generated.py` for interactive review.",
            ]
        )
    )
    summary
    return


@app.cell
def _(json, mo, report_paths):
    if not report_paths:
        report_view = mo.md("No generated reports found yet.")
    else:
        blocks = []
        for path in report_paths:
            content = json.loads(path.read_text())
            blocks.append(f"## {path.name}\n\n```json\n{json.dumps(content, indent=2)}\n```")
        report_view = mo.md("\n\n".join(blocks))
    report_view
    return


@app.cell
def _(mo, python_paths):
    if not python_paths:
        python_view = mo.md("No generated Python artifacts found yet.")
    else:
        listing = "\n".join(f"- `{path.name}`" for path in python_paths)
        python_view = mo.md(f"## Python Artifacts\n\n{listing}")
    python_view
    return


if __name__ == "__main__":
    app.run()
