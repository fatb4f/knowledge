# Runtime Surface Cleanup Plan v1

## Purpose

This plan aligns `codex_home` with the current runtime factoring:

- Marimo-first operationally
- state-contract-first semantically
- Python-first orchestrationally
- `uv` as environment substrate
- `just` as operator verb layer

It is a cleanup plan, not a semantic authority document.

## Operational Guidance

Use the current project workflow as an execution discipline:

- track work as bounded contract and cleanup slices
- sequence spec-first updates before substrate rewrites
- keep transport and host changes explicit
- close wording drift before broad runtime refactors

## Required Language Corrections

The older wording that must be retired or amended includes:

- "Marimo is not a Python CLI adapter"
- framing Marimo only as a hydration or derivation consumer
- treating `just` as the defining interface rather than the operator verb layer

Replace that framing with:

- Marimo is the default host/runtime shell
- Python state APIs are the orchestration boundary
- `uv` provides the runtime and dependency substrate
- `just` provides named operator verbs and parity entrypoints
- MCP exposes structured request and response reads
- ACP carries direct session execution where boundary crossing is required

## Cleanup Targets

### Policy and guidance

- `control/policy/token_burn_and_structured_output.md`
- `skills/tooling-policy/SKILL.md`

### Proposal-era wording that now drifts

- `kernel/proposals/shell_cli_extension/python_cli_prospect.v1.md`
- `kernel/proposals/cli_extension_v2/*`
- `kernel/proposals/git_substrate_adapters_v1/*`

### Runtime realization follow-ons

- Marimo host bindings
- Python state API wrappers
- `uv` launcher and lock behavior
- `just` parity entrypoints
- MCP and ACP session bindings

## Phased Plan

### Phase 1: terminology cleanup

- remove wording that makes Marimo secondary by default
- reclassify `uv`, `marimo`, and `just` asymmetrically
- mark older proposal language as superseded where rewrite is too large

### Phase 2: runtime binding alignment

- add explicit `marimo.session.state.get`
- add explicit `marimo.session.state.hydrate`
- add explicit `marimo.registry.snapshot.register`
- add explicit `marimo.view.state.render`
- document Python state APIs as the only orchestration boundary above `gix` and `sem`

### Phase 3: entrypoint cleanup

- keep `just` as a parity and operator-verb surface
- avoid treating `just` as the semantic center
- bind `uv` to launcher and environment concerns only

### Phase 4: transport and output cleanup

- make `json`, `ndjson`, and `jsonl` output contracts explicit
- separate local direct calls from MCP and ACP boundary crossings
- keep session persistence and streaming semantics in runtime docs, not semantic contracts

## Deliverables

- updated policy wording
- updated proposal notes or supersession markers
- runtime binding docs for Marimo, Python, `uv`, and `just`
- lineage statements that point back to kernel-owned contracts
- repo factoring map tied to live `kernel` and `codex_home` paths

## Stop Conditions

Do not:

- move semantic truth out of `kernel`
- redefine contract meaning in `codex_home`
- let host/runtime docs silently invent transport semantics
- collapse Python orchestration directly into raw adapter access
