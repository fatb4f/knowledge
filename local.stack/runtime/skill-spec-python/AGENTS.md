# Spec-Python Guide

This directory hosts a narrow `hof` workflow for spec ingestion, CUE normalization, deterministic Python generation, and bounded verification.

## Directory Index

- `specs/source/`: authority inputs
- `specs/cue/`: normalized CUE model
- `specs/fixtures/`: validation fixtures
- `generators/python/`: Python typed generation
- `runtime/`: optional Python ingress adapters
- `tasks/`: bounded hof tasks
- `generated/`: derived outputs only
- `tests/`: verification layer

## Primary Flow

`validate -> generate-python -> generate-schemas -> verify`

## Runtime Notes

- `marimo` is the default human review host for this skill.
- `uv` is the environment and launcher substrate.
- The review notebook is a pure Python file and should stay runnable with `--sandbox`.
- Keep runtime notes here and semantic contract meaning in the kernel repo.

## Boundary Rules

- edit source specs, CUE files, fixtures, templates, and control docs
- do not hand-edit generated outputs
- validate before generation
