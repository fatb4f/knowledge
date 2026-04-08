# Tasks

These tasks are bounded and deterministic.

## Expected Tasks

- `validate`
- `generate-python`
- `generate-schemas`
- `runtime-ingress-check`
- `verify`
- `spec-to-python`

## Rules

- tasks should emit machine-readable reports
- aggregate tasks should expand to named subtasks

## Execution Notes

- `flow.cue` is the executable `hof flow` entrypoint for v1.
- The `.hof` files in this directory remain task contracts and scope documents.
- Run from the `skill-spec-python` root:
  - `hof flow tasks/flow.cue @specToPython`
