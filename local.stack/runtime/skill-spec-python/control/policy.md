# Policy

## Purpose

Keep this workflow narrow:

- normalize source specs into CUE
- validate fixtures
- generate typed Python artifacts
- expose generated results for human review

## Runtime Rules

- `marimo` is the default review host.
- `uv` is the launcher and sandbox substrate.
- Prefer single-file marimo notebooks with inline dependencies for review surfaces.
- `jsonargparse` is a candidate runtime ingress layer for nested config parsing and JSON Schema validation, not the canonical spec owner.
- runtime ingress should reject unknown keys by default and emit structured error reports instead of silently stripping input.

## Editing Rules

- hand-edit only `specs/source`, `specs/cue`, `specs/fixtures`, `generators`, `tasks`, and `control`
- treat `generated` as derived
