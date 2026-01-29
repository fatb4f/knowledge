# Proposal: Layered Control Surface for Codex Packets via `just` (Plant-A)

**Revision:** r3 (2026-01-29)

**Status:** LOCKED (finalized)


## Goal
Standardize Codex packet execution across downstream repos using a canonical `just` control surface exported by **Plant-A (plant-a-codex)**. Increase mechanical enforcement in layers, ending with **Pydantic + controller CLI** as the authoritative controller and `just` as the actuator.

---

## Principles
- **`just` is the actuator**: executes bounded phases and commands.
- **Controller is authoritative**: packet + contract parsing, normalization, invariants, decisions.
- **Evidence is first-class**: every run emits a stable, machine-readable bundle.
- **Deny-by-default** in enforcement mode.
- **Downstream repos import** Plant-A control surface and optionally add local aliases.

---

## Canonical paths and artifacts

### Inputs
- Packet: `.codex/packets/<packet_id>/packet.{json,yaml}`
- Contract: resolved from `contract_path` in packet (repo-local path)

### Derived paths (resolved by controller)
- `CODEX_ROOT` (resolved by controller; see resolution rules below)
- `PACKET_ID`
- `PACKET_DIR = $CODEX_ROOT/.codex/packets/$PACKET_ID`
- `WORKTREE_DIR = $CODEX_ROOT/.codex/.worktrees/$PACKET_ID`
- `OUT_DIR = $CODEX_ROOT/.codex/out/$PACKET_ID`

### Resolution rules (recommended)
- **CODEX_ROOT**: resolve via `git rev-parse --show-toplevel` when available; otherwise fall back to invocation dir.
- **PACKET_ID**: priority order: explicit CLI arg > `PACKET_ID` env var > infer from **packet descriptor** (see below). If no descriptor can be found, **deny** (PACKET_ID required).

#### Packet descriptor files
- Canonical descriptor: `.codex/packets/<packet_id>/packet.{json,yaml}`
- Optional worktree-local pointer: `.codex/.worktrees/<packet_id>/.codex.packet.{json,yaml}` (may be a pointer with `packet_id` + `packet_path`)

**Rule**: inference is descriptor-driven only (no `$PWD` regex heuristics).

#### Base path overrides (optional)
- **WORKTREE_DIR**: allow `WT_BASE` env var to override `.codex/.worktrees` (e.g., external worktree farms like `../wt`).
- **PACKET_DIR**: allow `PKT_BASE` env var to override `.codex/packets`.
- **OUT_DIR**: allow `OUT_BASE` env var to override `.codex/out`.

### Outputs (stable per packet)
- `OUT_DIR/env.vars` (shell KEY=VALUE)
- `OUT_DIR/evidence.json` (ComplianceReport)
- `OUT_DIR/manifest.json` (hashes; deterministic replay anchors)
- `OUT_DIR/commands.log` (executed commands + output)
- `OUT_DIR/summary.md` (human capsule)

### Versioning fields (early, even before Pydantic)
- `evidence.json`: include `evidence_version` (semver) + `model_version` (int or semver).
- `manifest.json`: include `manifest_version` (semver) + `hash_algo` (e.g., `sha256`).
- Both should include `controller_version` (git SHA or package version) to make replay/debug evidence useful.

---

## Public control surface (stable API)
Export as `ctrl.*`:
- `ctrl.help`
- `ctrl.list`
- `ctrl.doctor`
- `ctrl.paths`
- `ctrl.preflight`
- `ctrl.exec`
- `ctrl.check`
- `ctrl.evidence`
- `ctrl.promote` (deny by default; CI/repo-specific)

Downstream repos can alias:
- `preflight -> ctrl.preflight`
- `run -> ctrl.exec ACTION=...`
- `check -> ctrl.check`
- `evidence -> ctrl.evidence`

---

## Layered plan

### Layer 0 — Baseline `justfile` only
**What**
- Root `justfile` with introspection (`help/list/doctor/paths`).
- Variable-driven conventions; no packet parsing.

**Pros**
- Immediate adoption, zero deps.

**Cons**
- Weak guarantees; relies on discipline.

**Deliverables**
- `plant-a-codex/justfile`
- Optional `plant-a-codex/just/ctrl.just` module wrapper.

---

### Layer 1 — Plant-A exports `ctrl.*`; downstream imports
**What**
- Stable `ctrl.*` API.
- Downstream repos `import` or `mod` Plant-A and re-export local aliases.

**Pros**
- Uniform actuator interface across repos.

**Cons**
- Still convention-based; no authoritative packet/contract parsing.

**Deliverables**
- `plant-a-codex/just/ctrl.just` (module)
- Minimal downstream import docs.

---

### Layer 2 — Mechanical parsing + env export (no Pydantic)
**What**
- Controller parses packet + contract, resolves paths, performs basic checks.
- Emits `env.vars`, `evidence.json`, `manifest.json`.
- `just` sources `env.vars` for execution.

**Pros**
- First real mechanical enforcement and evidence standardization.

**Cons**
- Format drift risk without schema authority.

**Deliverables**
- `src/plant_a_ctrlr/` parser/resolver/checker
- CLI: `ctrlr env`, `ctrlr check`, `ctrlr evidence`

---

### Layer 3 — Object-report controller (ComplianceReport is SSOT)
**What**
- Controller decision object is canonical:
  - `ComplianceReport { ok, errors, warnings, ctx, invariants, hashes }`
- `ctrl.exec` refuses to run unless `evidence.ok == true`.

**Pros**
- Deterministic decision artifact; CI and tooling can consume it.

**Cons**
- Still not schema-authoritative.

**Deliverables**
- Stable `evidence.json` schema (documented keys)
- `ctrl.preflight/check/evidence` all update/consume `evidence.json`.

---

### Layer 4 — Pydantic models + controller CLI (authoritative controller)
**What**
Pydantic becomes the authority:
- `Packet` model (intent + pointers)
- `Contract` model (constraints + actions)
- `ResolvedContext` (derived canonical paths)
- `ComplianceReport` (decision + evidence)

Controller CLI:
- `ctrlr env --packet ... --contract ...` → `env.vars`
- `ctrlr check ...` → writes `evidence.json` + `manifest.json` and exits non-zero on denial
- `ctrlr evidence ...` → writes `evidence.json` only (CI-friendly)

`just` remains actuator-only: it calls controller, then runs bounded execution.

**Pros**
- Strongest correctness, versionable formats.

**Cons**
- Dependency management (recommend: `uv`, pinned versions).

**Deliverables**
- `src/plant_a_ctrlr/models.py` (Pydantic)
- `src/plant_a_ctrlr/cli.py`
- `model_version` keys and upgrade strategy.

---

### Layer 5 — ACTION-based exec (deny-by-default)
**What**
- `ctrl.exec` accepts `ACTION`, not raw shell.
- Contract authoritatively maps:
  - `actions: { name: [argv...] }`
- Enforcement:
  - `TX_MODE=enforce`: deny unknown actions (`evidence.ok=false`, exit non-zero).
  - `TX_MODE=telemetry`: allow unknown actions but **record** `invariants.action_authorized=false` and add `WARN_UNAUTHORIZED_ACTION`; keep `evidence.ok=true` (exit 0).
- **Arg handling**: disallow shell interpolation; allow only fixed argv arrays or strict `{VAR}` placeholders substituted from a validated allowlist (reject on missing/extra vars).

**Example contract snippet**
```yaml
actions:
  test:
    - "pytest"
    - "-q"
    - "{TEST_PATH}"
  fmt:
    - "ruff"
    - "format"
    - "{TARGET}"
allowed_vars:
  - "TEST_PATH"
  - "TARGET"
```

**Pros**
- Removes largest degree of freedom (arbitrary commands).
- Contracts become true controllers.

**Cons**
- Requires maintaining action maps (good cost).

**Deliverables**
- Contract field `actions`
- Controller invariant: unknown ACTION ⇒ DENY in enforce

---


## TX_MODE and exit-code semantics (authoritative)

### Invariant classes
- **Structural invariants (always DENY):** descriptor/contract missing or unreadable, parse/validation failures, output directory not writable, required files/keys missing, hash/materialization failures.
- **Authorization invariants (telemetry can WARN):** e.g., `action_authorized=false` (unknown ACTION), or other “not permitted but observable” conditions you intentionally allow in telemetry mode.

### Unknown ACTION behavior
| TX_MODE | Behavior | `evidence.ok` | `invariants.action_authorized` | Warning code | Exit code |
|---|---|---:|---:|---|---:|
| `telemetry` | allow execution, record non-concordance | `true` | `false` | `WARN_UNAUTHORIZED_ACTION` | `0` |
| `enforce` | deny execution | `false` | `false` | *(error)* | `2` |

### Standard exit codes
- `0` — allowed (including telemetry-warn cases)
- `2` — denied by controller (preflight/check/exec)
- `3` — promote denied / unimplemented promote path (recommended default until CI-gated promote exists)


## Recommended adoption sequence
1. **Layer 1 now**: ship `ctrl.*` with introspection and downstream import pattern.
2. **Layer 3 next**: implement ComplianceReport + evidence bundle; gate `ctrl.exec` on `evidence.ok`.
3. **Layer 4 then**: upgrade to Pydantic-authoritative models + controller CLI.
4. **Layer 5 last**: move execution to ACTION-based deny-by-default.

---

## Definition of done (Layer 4+)
- `ctrl.preflight` always produces: `env.vars`, `evidence.json`, `manifest.json`.
- `ctrl.exec` refuses to run if:
  - `evidence.ok != true`, or
  - `TX_MODE=enforce` and execution is not contract-authorized.
- `ctrl.check` updates `evidence.json` with post-state invariants.
- All outputs are written under `.codex/out/<packet_id>/`.

---

## Change control (LOCKED)
This document is locked at **r3**. Any future changes must follow an explicit promotion protocol:
1. Create a new revision `r{N+1}` with a dated changelog section.
2. Record the migration impact: model/schema changes, backward compatibility, and required downstream updates.
3. Update `model_version` and/or `evidence_version`/`manifest_version` only when a consumer-facing contract changes.
4. Re-issue the document as a new file; never mutate a locked revision in-place.
