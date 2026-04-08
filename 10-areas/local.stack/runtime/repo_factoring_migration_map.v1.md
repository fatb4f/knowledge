# Repo Factoring Migration Map v1

## Purpose

This map defines the concrete `codex_home` realization work implied by the current kernel-side runtime factoring.

It is implementation-facing.
It does not redefine semantic contract truth.

## Existing Runtime-Basis Assets

The live repo already contains relevant realization and proposal-basis assets:

- `control/policy/token_burn_and_structured_output.md`
- `control/policy/token_burn_and_structured_output.registry.json`
- `control/shell/README.md`
- `control/shell/shell_script_inventory.json`
- `control/shell/shell_script_spec.md`
- `plan.request_response_contract.v1.json`
- `kernel/proposals/cli_extension_v2/control_realize_cli_extension_v2.py`
- `kernel/proposals/cli_extension_v2/unified_realization_manifest.v2.schema.json`
- `kernel/proposals/cli_extension_v2/unified_realization_report.v2.schema.json`
- `kernel/proposals/git_substrate_adapters_v1/control_realize_git_substrate_adapters_v1.py`
- `kernel/proposals/git_substrate_adapters_v1/emit_gix_runtime.py`
- `kernel/proposals/git_substrate_adapters_v1/emit_sem_runtime.py`
- `kernel/proposals/git_substrate_adapters_v1/gix_runtime_contract.v1.json`
- `kernel/proposals/git_substrate_adapters_v1/sem_runtime_contract.v1.json`
- `runtime/runtime_surface_cleanup_plan.v1.md`
- `runtime/stdio_to_ws_transport_bridge.v1.md`

## Codex_home File Actions

| Path | Current role | Action | Target outcome |
| --- | --- | --- | --- |
| `control/policy/token_burn_and_structured_output.md` | shared operator policy | continue revising | keep Marimo-first operational guidance explicit without redefining kernel semantics |
| `kernel/proposals/shell_cli_extension/python_cli_prospect.v1.md` | older Python CLI prospect | amend or supersede | remove shell-first assumptions and preserve Marimo as default host/runtime shell |
| `kernel/proposals/cli_extension_v2/*` | generalized CLI realization lane | review and annotate | separate reusable realization machinery from runtime-contract meaning |
| `kernel/proposals/git_substrate_adapters_v1/control_realize_git_substrate_adapters_v1.py` | Git read-plane aggregation basis | reuse | remain substrate realization beneath Python state APIs |
| `kernel/proposals/git_substrate_adapters_v1/emit_gix_runtime.py` | deterministic Git runtime probe | reuse | stay beneath state API wrapper surfaces |
| `kernel/proposals/git_substrate_adapters_v1/emit_sem_runtime.py` | semantic enrichment runtime emitter | reuse | stay downstream of deterministic Git facts |
| `plan.request_response_contract.v1.json` | request/response contract basis | review and align | ensure it does not drift from kernel-owned `state.v1` and `session.v1` semantics |
| `control/shell/*` | shell realization guidance | retain but demote | keep as operator realization support, not execution-model authority |

## New Runtime Layout To Introduce

Add a bounded runtime family under `codex_home`:

- `runtime/`
- `runtime/`
- `bindings/`
- `marimo/`
- `sessions/`
- `emitters/`

Where WebSocket-facing consumers are needed for stdio-oriented runtimes, keep any `stdio-to-ws` style bridge inside the transport/bindings layer rather than promoting it into contract authority.

These names can vary, but the separation should hold:

- runtime implementation
- transport bindings
- Marimo host units
- session machinery
- output emitters

## First Concrete Runtime Surfaces

The first runtime realization slice should expose one shared Python boundary and project multiple transports from it:

- `nb.py` or equivalent host unit for:
  - `get_state`
  - `hydrate_state`
- direct local call path
- MCP request/response read path
- ACP direct session execution path
- structured emitters for:
  - `json`
  - `ndjson`
  - `jsonl`

## Reuse Rules

Reuse proposal-basis assets where they already match the runtime need:

- Git substrate read aggregation from `git_substrate_adapters_v1`
- unified manifest/report habits from `cli_extension_v2`
- token-burn and structured-output policy from `control/policy`

Do not reuse proposal wording as semantic authority once kernel contracts exist.

## Boundaries To Preserve

Codex_home owns:

- launcher behavior
- environment management
- session storage
- runtime logs
- streaming outputs
- transport bindings

Codex_home does not own:

- state envelope meaning
- session metadata meaning
- transport semantic meaning
- output encoding semantic meaning

Those remain kernel-owned.
