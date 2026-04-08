# Task Contract

## Aggregate Flow

`validate -> generate-python -> generate-schemas -> verify`

## Required Reports

- `generated/reports/validation.json`
- `generated/reports/generation.json`
- `generated/reports/verify.json`

## Optional Runtime Ingress

- `runtime/jsonargparse_adapter.py`
- emits `generated/reports/runtime_ingress.json` when used
- checked example: `runtime/examples/state.valid.yaml`

## Human Review Surface

- `review/inspect_generated.py`

Run:

- `marimo edit --sandbox review/inspect_generated.py`
- `uv run review/inspect_generated.py`

## Hof Entry Point

- `hof flow tasks/flow.cue @specToPython`
