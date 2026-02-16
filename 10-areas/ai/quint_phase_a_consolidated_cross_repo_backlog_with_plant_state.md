# Quint-Phase-A — Consolidated Cross-Repo Backlog

This is the single consolidated backlog artifact that merges:

- The **current plant state** (what is already true/working and should be treated as constraints), and
- The **cross-repo backlog** (P0/P1/P2) with explicit dependencies and references.

> Naming note: the current implementation name is **`ctrlex`**. A later preferred final name is **`ctrlx`**. Treat `ctrlx` as the target canonical name; until renamed, keep `ctrlex` as the operational name and retain aliases as needed.

---

## Current plant state (locked + working)

### A) Global-only roots
- `CODEX_HOME=$XDG_CONFIG_HOME/codex`
- `QUINT_HOME=$XDG_CONFIG_HOME/quint`
- **No repo-local roots**: deny any target repo containing `.codex/` or `.quint/` anywhere.

### B) Target-aware execution (required)
- Every action is explicitly scoped via `--repo-root` and `--codex-home`.
- All git operations are performed as `git -C <repo_root> …`.
- **Strict clean gate**: `git status --porcelain` must be empty (untracked counts as dirty).

### C) Skills export surface (spec-aligned)
- Export roots under `skills-pack/<tool>.*` (currently `skills-pack/ctrlex.*`).
- `skills/packet-*` remains a symlink compatibility layer pointing into `skills-pack/…`.

### D) Native CLI + stable wrapper (no PATH flakiness)
- Native `<tool>` CLI exists (currently `ctrlex`).
- Canonical executable path: `$CODEX_HOME/bin/<tool>` (currently `$CODEX_HOME/bin/ctrlex`).

### E) Global Just + MCP actuator surface (live)
- Rendered global Justfile: `$CODEX_HOME/Justfile` with recipes:
  - `preflight`, `enter_work`, `run_packet`, `collect_evidence`, `doctor`
- `just-mcp` watches `$CODEX_HOME:<tool>` (currently `$CODEX_HOME:ctrlex`) and registers 5 tools when the Justfile is rendered.
- Recipes call the wrapper (`$CODEX_HOME/bin/<tool>`) and include parameter docs for MCP schema generation.

---

## Backlog (cross-repo)

### P0 — unblock + standardize (next)

#### 1) Finalize the 5 ProjectOps decisions (sets all naming + paths)
**Reference pack:** `terminal_project_management_set…`

**Decisions to lock:**
1. **ID derivation**: `<id>-<slug>` vs prompt-derived vs branch-derived
2. **Worktree base path**: `../wt/...` vs `$CODEX_HOME/<tool>/worktrees/...` (or legacy `.codex/.worktrees/...`)
3. **Session naming**: `<repo>-<id>`
4. **`just wt` implementation**: lazyworktree vs custom selector
5. **Gate log SSOT location**: `$CODEX_HOME/<tool>/out/<id>/…` vs `ledger/…` vs `./logs/…`

**Plant-state constraint:** global-only roots and `$CODEX_HOME`-scoped state already works; any decision that reintroduces repo-local roots is invalid.

**Exit criteria:** a single “ProjectOps Naming + Paths” decision record (DRR) committed (Quint L0 → promote) that downstream repos can treat as binding.

---

#### 2) Plant-A: ship Layer 1 control surface (`ctrl.*`) + downstream import pattern
**Reference pack:** `plant_a_justfile_controller_pro…`

**Scope:** define a stable public command surface above the existing `<tool>` CLI and Just/MCP plumbing.

**Deliverables (Layer 1):**
- `ctrl.help`
- `ctrl.list`
- `ctrl.doctor`
- `ctrl.paths`
- `ctrl.preflight`
- `ctrl.exec`
- `ctrl.check`
- `ctrl.evidence`
- `ctrl.promote` (can remain deny-by-default initially)

**Import pattern (downstream):**
- Downstream repos/Yazi bindings call only `ctrl.*` (never raw python scripts).
- `ctrl.*` recipes/tools invoke `$CODEX_HOME/bin/<tool>` with explicit `--repo-root/--codex-home`.

**Exit criteria:**
- `ctrl.*` exists in the global Justfile render (or imports from a module) and is discoverable via MCP.
- `ctrl.promote` exists but may deny-by-default until Layer 3 gates are complete.

---

#### 3) Align ProjectOps “Yazi → just” wiring (no logic in Yazi)
**Reference pack:** `terminal_project_management_set…`

**Deliverables:**
- Install/confirm Yazi plugins
- Keybinds that invoke:
  - `just wt`
  - `just sess`
  - `just ctrl.preflight`
  - `just ctrl.check`
  - `just ctrl.promote`

**Rules:**
- Yazi contains **no logic**, only command invocations.
- All repo targeting flows through explicit `repo_root`.

**Exit criteria:** keybinds work from any directory context and always target the intended repo root deterministically.

---

#### 4) HQ backlog topology: hub-and-spoke
**Reference pack:** `hq_repo_backlog_strategy`

**Deliverables:**
- HQ Phase 1: add `README.md` + `backlog-index.md`
- Repo alignment:
  - ensure root `backlog.md`
  - add README pointer line to HQ index

**Exit criteria:** navigating the backlog is 1-hop from any repo.

---

### P1 — enforcement + evidence

#### 5) Plant-A Layer 3: ComplianceReport SSOT + gate `ctrl.exec` on `evidence.ok`
**Reference pack:** `plant_a_justfile_controller_pro…`

**Deliverables:**
- Define ComplianceReport schema + SSOT location
- Gate `ctrl.exec` on `evidence.ok==true`

**Plant-state constraint:** evidence/outputs must remain under `$CODEX_HOME/<tool>/out/...`.

---

#### 6) Plant-A Layer 4: Pydantic-authoritative models + controller CLI
**Reference pack:** `plant_a_justfile_controller_pro…`

**Deliverables:**
- Pydantic as authoritative models
- Controller CLI support for env/check/evidence

**Rule:** this layer strengthens correctness/typing; it should not create a parallel interface that bypasses `ctrl.*`.

---

#### 7) Plant-A Layer 5: ACTION-based exec + `{VAR}` allowlist substitution
**Reference pack:** `plant_a_justfile_controller_pro…`

**Deliverables:**
- ACTION-based execution in enforce mode (deny-by-default)
- `{VAR}` allowlist substitution rules

---

### P2 — local Codex↔ChatGPT collaboration substrate

#### 8) Decide shared root + sync strategy; implement Phase 0 skeleton
**Reference pack:** `codex-chatgpt-collab-proposal`

**Deliverables (Phase 0):**
- shared root folders
- DuckDB init
- stub prompts
- starter `memory.json`

---

#### 9) Implement Phase 1–2 scripts
**Reference pack:** `codex-chatgpt-collab-proposal`

**Deliverables:**
- `import_webui.py`
- `prompt_bundle.py`

---

#### 10) Phase 3: per-thread worktrees + lightweight thread rotation helpers
**Reference pack:** `codex-chatgpt-collab-proposal`

---

## Ongoing standards (apply as you implement)

### Python tooling baseline for Plant-A / ctrlr tools
**Reference pack:** `python_standard`

- Boundary validation
- Stable error taxonomy
- Deterministic behavior

### Minimum CI gates
- ruff
- pytest
- type check (pyright/mypy)
- secrets scan
- dependency scan
n
---

## Dependency notes (to keep sequencing clean)

- P0.1 (ProjectOps decisions) should land **before** finalizing `ctrl.*` naming/paths.
- `ctrl.*` (P0.2) should become the stable surface that Yazi and MCP target.
- P1.5 (evidence gating) should be the point where `ctrl.exec` is meaningfully enforced; until then, keep `ctrl.promote` deny-by-default.
- P2 work should not proceed until P0 naming/path decisions are locked, to avoid duplicating incompatible path assumptions.

