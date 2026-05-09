# Hof Spec-Python Skill Layout v1

## Purpose

This document defines a concrete `hof`-based skill layout for a narrow, high-signal workflow:

- ingest spec inputs
- normalize them into CUE
- validate fixtures and examples
- deterministically generate Python typed artifacts
- run bounded verification gates

It is intentionally not a general agent framework.

## Primary Design Rule

Use `hof` as:

- CUE-backed normalization layer
- deterministic generation layer
- bounded task runner

Do not use it as a substitute for semantic contract ownership.

Contract meaning remains kernel-owned.
Runtime execution remains codex_home-owned.

## Target Repo Shape

```text
skill-spec-python/
  AGENTS.md
  SKILL.md

  specs/
    AGENTS.md
    source/
      AGENTS.md
      state.schema.json
      session.schema.json
      output.schema.json
    cue/
      AGENTS.md
      common.cue
      state.cue
      session.cue
      output.cue
    fixtures/
      AGENTS.md
      state.valid.json
      state.invalid.json
      session.valid.json
      output.valid.json

  generators/
    AGENTS.md
    python/
      AGENTS.md
      hof.module.cue
      templates/
        model.py.tmpl
        codec.py.tmpl
        fixture_test.py.tmpl
    schema/
      AGENTS.md
      hof.module.cue
      templates/
        jsonschema.json.tmpl

  tasks/
    AGENTS.md
    validate.hof
    generate-python.hof
    generate-schemas.hof
    verify.hof
    spec-to-python.hof

  generated/
    AGENTS.md
    python/
      state_models.py
      session_models.py
      output_models.py
      codecs.py
    schemas/
      state.v1.schema.json
      session.v1.schema.json
      output.v1.schema.json
    fixtures/
      state.valid.json
      session.valid.json
      output.valid.json
    reports/
      validation.json
      generation.json
      verify.json

  tests/
    AGENTS.md
    test_generated_models.py
    test_schema_roundtrip.py
    test_fixture_conformance.py

  control/
    AGENTS.md
    mapping.cue
    policy.md
    task-contract.md
```

## Ownership By Directory

### `specs/source/`

Human-owned authority inputs:

- JSON Schema
- OpenAPI fragments
- example JSON

No generated files here.

### `specs/cue/`

Canonical normalized CUE model:

- import or mirror source specs
- encode constraints explicitly
- define reusable schema fragments

This is the control surface for generation.

### `specs/fixtures/`

Validation inputs:

- valid examples
- invalid examples
- edge cases

These are used by `cue vet` and test gates.

### `generators/python/`

Deterministic generation target for Python typed artifacts.

Recommended v1 output:

- `msgspec.Struct` models
- codecs
- fixture-driven smoke tests

### `generators/schema/`

Optional downstream schema projection:

- JSON Schema snapshots
- compatibility projections

### `tasks/`

Bounded `hof` tasks only.

Expected sequence:

- `validate`
- `generate-python`
- `generate-schemas`
- `verify`
- aggregate entrypoint: `spec-to-python`

### `generated/`

Derived outputs only.

Do not hand-edit.

### `tests/`

Verification layer over generated artifacts.

### `control/`

Small human-owned control layer:

- mapping between source spec and CUE normalization
- generation policy
- task contract

## Bounded Task Flow

### `validate`

Responsibilities:

- import or load source spec
- normalize to CUE
- run `cue vet` against fixtures
- emit `generated/reports/validation.json`

### `generate-python`

Responsibilities:

- generate Python typed artifacts from the CUE model
- write outputs under `generated/python/`
- emit `generated/reports/generation.json`

### `generate-schemas`

Responsibilities:

- emit JSON Schema or other compatibility projections
- write outputs under `generated/schemas/`

### `verify`

Responsibilities:

- format
- typecheck
- run tests
- emit `generated/reports/verify.json`

### `spec-to-python`

Aggregate flow:

```text
validate -> generate-python -> generate-schemas -> verify
```

## AGENTS Pattern

Each significant directory should carry a short `AGENTS.md` file that explains:

- purpose
- owned files
- accepted inputs
- invariants
- commands
- generated outputs
- failure modes

This keeps agent navigation deterministic and reduces token burn during exploration.

## V1 Constraints

Keep the first version narrow:

- `state`
- `session`
- `output`

Avoid in v1:

- multi-language generation
- hand-tuned generated exceptions
- broad runtime scaffolding
- open-ended code generation

## Recommended Python Target

Use `msgspec.Struct` first.

Reason:

- typed envelope model
- fast JSON and MsgPack serialization
- good fit for deterministic request/response artifacts

## Boundary Rule

- `kernel` defines semantic contract meaning
- `hof` normalizes and generates against those contracts
- `codex_home` runs the workflow and verification gates
