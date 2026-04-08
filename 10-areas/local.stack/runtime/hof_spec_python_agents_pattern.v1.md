# Hof Spec-Python AGENTS Pattern v1

## Purpose

This file defines the recursive `AGENTS.md` pattern for the `hof`-based spec-to-python workflow.

Each `AGENTS.md` should be short and navigational.
It should not duplicate detailed reference material.

## Root `AGENTS.md`

Required sections:

1. Purpose
2. Directory index
3. Primary task flow
4. Boundary rules
5. Generated-file rule

Suggested content:

```md
# Spec-Python Guide

This directory hosts a narrow `hof` workflow for spec ingestion, CUE normalization, deterministic Python generation, and bounded verification.

## Directory Index

- `specs/source/`: authority inputs
- `specs/cue/`: normalized CUE model
- `specs/fixtures/`: validation fixtures
- `generators/python/`: Python typed generation
- `tasks/`: bounded hof tasks
- `generated/`: derived outputs only
- `tests/`: verification layer

## Primary Flow

`validate -> generate-python -> generate-schemas -> verify`

## Boundary Rules

- edit source specs, CUE files, fixtures, templates, and control docs
- do not hand-edit generated outputs
- validate before generation
```

## `specs/source/AGENTS.md`

State:

- these files are authority inputs
- accepted formats
- do not add generated material here

## `specs/cue/AGENTS.md`

State:

- this directory is the normalized model layer
- prefer explicit constraints over prose notes
- keep definitions reusable and stable

## `specs/fixtures/AGENTS.md`

State:

- valid vs invalid fixture convention
- edge cases belong here
- fixtures must stay aligned with current CUE constraints

## `generators/python/AGENTS.md`

State:

- templates and generator config live here
- target output is typed Python, preferably `msgspec.Struct`
- generator changes must not directly edit `generated/python/*`

## `tasks/AGENTS.md`

State:

- each task is bounded and deterministic
- tasks emit machine-readable reports
- aggregate tasks should expand to named subtasks, not hide behavior

## `generated/AGENTS.md`

State:

- all files are derived
- do not hand-edit
- regenerate from source, CUE, and templates

## `tests/AGENTS.md`

State:

- verify generated artifacts, not author them
- include fixture conformance and import smoke checks

## Style Rule

Keep every `AGENTS.md` under one screen when possible.
Use it as a routing and invariants surface, not as a long tutorial.
