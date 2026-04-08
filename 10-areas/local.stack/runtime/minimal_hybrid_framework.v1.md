# Minimal Hybrid Framework v1

## Purpose

This note defines a stripped-down hybrid framework for Codex.

It borrows:

- `hof`-style recursive guidance and selected-context assembly
- `dagger`-style runtime grouping, checks, and changeset/evidence discipline

It does not adopt either framework wholesale.

## Authority Split

- `kernel` owns semantic authority, contract meaning, and admissible state space
- `dotfiles/chezmoi/dot_config/codex` owns runtime realization, skills, and operator-facing execution surfaces
- local `AGENTS.md` files provide scoped guidance, not semantic authority

## Design Rule

Use:

- recursive local guidance for context selection
- machine-routable skill and surface metadata for selection
- grouped runtime surfaces for execution and evidence emission

Do not:

- collapse semantic truth into runtime notes
- treat notebooks as canonical logic boundaries
- rebuild the full `hof` agent runtime or the full `dagger` module system

## Layer 1: Guidance

### `guidance.v1`

Purpose:

- select only the relevant local context for a request

Minimum fields:

- `request_id`
- `surface_ids`
- `skill_ids`
- `agents_md`
- `selection_reason`
- `render_order`

Rules:

- use recursive `AGENTS.md` discovery only for touched or selected surfaces
- prefer local and bounded guidance over global prompt accumulation
- record exactly which guidance files were included

## Layer 2: Skill Registry

### `skill.registry.v2`

Purpose:

- make the Codex skill surface authoritative and machine-routable

Recommended fields:

- `skill_id`
- `version`
- `tier`: `core | runtime | adapter | migration | experimental`
- `authority_class`: `semantic | runtime | policy | migration`
- `owner_surface`
- `owned_paths`
- `derived_paths`
- `entrypoints`
- `status`

Rules:

- generate the registry from per-skill metadata and manifests
- fail drift where registry, disk, and runtime surfaces disagree
- keep policy/advisory skills explicitly marked if they are not routable

## Layer 3: Runtime Groups

### `runtime.group.v1`

Purpose:

- define runnable surfaces with explicit inputs, outputs, and evidence policy

Minimum fields:

- `group_id`
- `kind`: `check | generator | runtime | transport | replay`
- `surface_id`
- `entrypoints`
- `inputs`
- `outputs`
- `changeset_policy`
- `evidence_policy`

Starter examples:

- `state.get`
- `state.hydrate`
- `state.mcp`
- `state.acp`
- `state.replay`

Rules:

- canonical logic remains in plain Python modules
- Marimo notebooks stay thin host projections
- CLI, MCP, ACP, and replay remain sibling bindings over the same callable surface

## Execution Artifacts

Each runtime group should emit structured artifacts rather than only process success.

Minimum artifact set:

- `changeset.json`
- `checks.ndjson`
- `events.ndjson`
- `summary.json`

These artifacts support:

- replay
- promotion gates
- review
- evidence bundles

## Request Flow

1. Discover touched surfaces.
2. Select relevant skills and local `AGENTS.md`.
3. Build `guidance.v1`.
4. Resolve the matching `runtime.group.v1`.
5. Execute the shared callable Python surface.
6. Emit structured changeset, check, event, and summary artifacts.
7. Promote only through the existing gate path.

## Source Mapping

### Borrowed from `hof`

- recursive `AGENTS.md`
- metadata-driven context selection
- local guidance as runtime-selectable context

### Borrowed from `dagger`

- grouped runtime/check/generator surfaces
- explicit changesets
- explicit check and evidence outputs

### Preserved from Codex

- `kernel` as semantic authority
- runtime realization in the Codex tree
- Marimo-first host model
- Python-first callable logic surface

## Immediate Follow-Ons

1. Add `guidance.v1` as a concrete runtime artifact.
2. Replace `skills/registry.json` with generated `skill.registry.v2`.
3. Add a runtime skill layer aligned with `runtime.binding.v1`.
4. Define `runtime.group.v1` for state surfaces first.
5. Record included `AGENTS.md` fragments in evidence output.

## Stop Conditions

Do not:

- move contract meaning out of `kernel`
- let skill discovery silently drift from the runtime surface
- mix generated and authored boundaries without explicit ownership
- expand this into a full framework rewrite before the minimal path is proven
