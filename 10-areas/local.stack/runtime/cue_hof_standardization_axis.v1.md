# CUE Hof Standardization Axis v1

## Purpose

This note defines the standardization axis for Codex skill and runtime substrates:

- CUE is the authority and normalization layer
- `hof` is the operational discovery, projection, and workflow layer around that authority
- Python and Marimo remain downstream runtime realizations over already-admissible models

This note is narrower than the hybrid framework note.
It focuses on CUE and `hof`, not the broader `hof` plus `dagger` mix.

## Core Rule

Define every substrate as:

`imported/raw -> normalized CUE -> policy-unified CUE -> generated/exported outputs`

Use `hof` modules and `hof` flows as the reusable machinery around that pipeline.

## Why This Axis

The high-signal patterns are:

- import existing JSON, YAML, and schema-bearing inputs into CUE first
- accumulate defaults and constraints through unification
- organize reusable definitions as modules and packages
- project many outputs from one authority model
- preserve local edits during regeneration
- drive workflows and DAG legality from CUE rather than scattered scripts

## Lifecycle

### 1. Ingest

- collect raw JSON, YAML, schema, or manifest input
- classify substrate type
- import it into a canonical CUE package

### 2. Normalize

- convert the raw input into reusable CUE definitions
- eliminate transport-specific incidental shape where possible
- establish one canonical model per substrate

### 3. Constrain

- unify policy, defaults, overlays, and cross-field rules
- run compatibility and admissibility checks
- attach provenance and control metadata

### 4. Discover

- expose operational roots via `#hof` and shorthand metadata where needed
- classify roots as generator, flow, datamodel, or support package

### 5. Project

- emit generated files, typed artifacts, manifests, indexes, and reports
- keep generated outputs downstream of already-constrained CUE models

### 6. Execute

- run `hof` flow or CUE-declared task graphs where orchestration is required
- keep Python as the executor for hard runtime work rather than the authority surface

### 7. Evolve

- checkpoint authority-model changes
- diff projections
- regenerate safely

## Standard Skill Shape

Each contract-first skill should converge on this structure:

```text
skill/
  SKILL.md
  schema/
  policy/
  projections/
  flow/
  examples/
  tests/
```

Each skill should answer:

1. What raw inputs it accepts
2. What normalized CUE model it produces
3. What policy and gate logic must unify or validate
4. What `#hof` roots exist
5. What projections it emits
6. What execution graph can run

## First Skill Families

Recommended first families:

- `normalize`
- `constrain`
- `project`
- `orchestrate`
- `evolve`

These are capability families, not necessarily final skill directory names.

## Immediate Deliverables

### Shared `cue-lib`

Create a shared CUE pattern library for:

- `#OneOf`
- `#AnyOf`
- defaults and overlays
- compatibility checks via subsumption
- environment and tag injection stubs
- cross-field validators

### Generator Module Contract

Define one reusable `hof` generator-module contract per substrate, with a predictable layout such as:

```text
schema/
gen/
templates/
partials/
statics/
examples/
```

### Regeneration Safety Rules

Make generation safety explicit:

- stable edit seams
- generated-vs-user ownership rules
- shadow-copy policy
- formatter normalization before merge
- diff3-safe expectations for regeneration

## Next Deliverables

- add `#hof` metadata on control/module roots and skill roots where it improves discovery
- add a CUE-declared workflow layer for build, validate, review, and promote graphs
- keep Python task runners thin and deterministic

## Selective Later Adoption

Adopt `hof` datamodel features selectively for:

- registries
- manifests
- contracts
- workflow state objects
- migration-aware artifacts

## Relationship To Existing Notes

- [minimal_hybrid_framework.v1.md](/home/chronos/.local/opt/knowledge/10-areas/local.stack/runtime/minimal_hybrid_framework.v1.md)
  describes the broader stripped-down `hof` plus `dagger` runtime mix
- [hof_spec_python_skill_layout.v1.md](/home/chronos/.local/opt/knowledge/10-areas/local.stack/runtime/hof_spec_python_skill_layout.v1.md)
  is one concrete narrow instance of this broader CUE plus `hof` pipeline

## Stop Conditions

Do not:

- treat CUE as a final checker only
- let `hof` become semantic authority
- bypass normalized CUE models when generating runtime artifacts
- spread the same substrate truth across JSON Schema, Python, templates, and runtime notes without one authority layer
