---
name: spec-python
description: Use when normalizing JSON Schema, OpenAPI fragments, or example payloads into CUE and deterministically generating typed Python artifacts plus validation fixtures and reports.
---

# Spec-Python

Use this workflow for a narrow, schema-first pipeline:

- ingest source specs or examples
- normalize into CUE
- validate fixtures with CUE
- generate typed Python artifacts
- run bounded verification

## Read First

- `AGENTS.md`
- `specs/cue/AGENTS.md`
- `tasks/AGENTS.md`

## Workflow

1. Update authority inputs under `specs/source/`.
2. Normalize or refine the CUE model under `specs/cue/`.
3. Keep valid and invalid fixtures aligned under `specs/fixtures/`.
4. Update Python generator templates or config under `generators/python/`.
5. Run the bounded task flow:
   - `validate`
   - `generate-python`
   - `generate-schemas`
   - `verify`

## Runtime Review Surface

Use the marimo review surface under `review/` for human inspection of generated reports.

- Prefer `marimo edit --sandbox review/inspect_generated.py` for interactive review.
- Prefer `uv run review/inspect_generated.py` for non-interactive smoke checks.
- Keep notebook dependencies inlined with PEP 723 metadata so the notebook remains shareable as a single Python file.

## Constraints

- Treat CUE as the normalized model layer, not the transport itself.
- Treat generated Python and schema outputs as derived artifacts.
- Prefer `msgspec.Struct` for the first Python target.
- Keep v1 limited to `state`, `session`, and `output`.
