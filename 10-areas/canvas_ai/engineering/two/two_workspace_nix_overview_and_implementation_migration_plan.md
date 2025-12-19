# TWO.workspace + Nix

## Purpose
Define a stable, declarative **workspace contract** for TWO (paths, scopes, defaults, state locations) and integrate it cleanly with a Nix-based system (home-manager / flakes) so that:

- Nix controls **tooling + environment reproducibility**
- TWO controls **semantic filesystem meaning + pipeline behavior**

Result: `intent → schema → pipeline` becomes deterministic across machines.

---

## Conceptual Overview

### Layers
1. **Input**
   - `two …` CLI, shell keybinds, editor commands
2. **Process**
   - Parse intent, normalize to unified schema, select strategy
3. **Wrangling**
   - Build argv for tools (or modules), wire pipes, execute
4. **Output**
   - TTY / TUI / JSON results

### Why Workspaces
Workspaces reduce variability by pinning down:

- canonical project roots
- named scopes (`src`, `tests`, `docs`, `notes`, `data`, `scratch`)
- defaults (hidden, ignore rules, depth, preview)
- state locations (history, cache, indices)

### Nix Relationship
- **Nix:** packages, versions, shells, services, environment variables
- **TWO.workspace:** semantic resolution + runtime orchestration policy

They complement: Nix ensures tools exist; TWO ensures consistent behavior.

---

## Workspace Model

### Global (per-user / per-device)
File: `~/.config/two/global.toml`

Defines stable roots and defaults:
- `home`, `projects_root` (e.g., `~/src`), `notes_root`, `scratch_root`
- default editor/pager
- default ignore/hidden behavior
- runtime socket/state dirs

### Local (per-workspace)
Folder: `./.metainfo/`

Minimal files:
- `./.metainfo/two.workspace.toml`  (the contract)
- `./.metainfo/state/`             (history/cache/index)

Local config defines:
- `workspace.id`, `kind`
- scope mappings (relative paths)
- search defaults and tool overrides

### Resolution Rules
When invoked from `$PWD`:
1. Walk up to find nearest `.metainfo/two.workspace.toml`
2. If found: load it and compute absolute scopes
3. Else: fall back to global defaults
4. Emit `PipelineSpec` graph (not a string)
5. Execution engine renders graph → pipeline

---

## Minimal Spec

### `two.workspace.toml` (local)

```toml
[workspace]
id = "life"
kind = "project"

[root]
path = "."

[scopes]
src = "src"
tests = "tests"
docs = "docs"

[search.defaults]
include_hidden = false
respect_gitignore = true
max_depth = 12

[tools]
editor = "hx"
previewer = "bat"
selector = "fzf"
```

### `global.toml` (global)

```toml
[paths]
home = "~"
projects = "~/src"
notes = "~/notes"
scratch = "~/scratch"

[defaults]
editor = "hx"
pager = "less"
metainfo_dir = ".metainfo"

[state]
run_dir = "~/.local/run/two"
data_dir = "~/.local/share/two"
cache_dir = "~/.cache/two"
```

---

## Output Contract: PipelineSpec
TWO should generate a structured plan:

```json
{
  "workspace": "life",
  "cwd": "/home/baf/src/life",
  "pipeline": [
    {"tool":"fd","argv":["TODO","/home/baf/src/life/src","-t","f"]},
    {"tool":"fzf","argv":["--preview","bat --color=always {}"]},
    {"tool":"xargs","argv":["hx"]}
  ]
}
```

Rendering to a shell pipeline is a view:

```sh
fd TODO /home/baf/src/life/src -t f | fzf --preview 'bat --color=always {}' | xargs hx
```

---

## Implementation Plan (Phased)

### Phase 0 — Decision Baselines
- Choose metainfo directory name: `.metainfo/` (recommended)
- Choose config format: TOML (recommended)
- Choose workspace root detection rule:
  - file: `.metainfo/two.workspace.toml`

Deliverable:
- `spec/` document for file names + resolution algorithm

---

### Phase 1 — Spec + Parser + Resolver (No execution)
Build a small Rust (or Python) library that:

- loads `global.toml`
- finds nearest local workspace config
- merges global + local
- computes absolute scopes

Deliverables:
- `two resolve` → prints resolved workspace JSON (no pipeline)
- Unit tests for:
  - no local workspace
  - nested workspaces
  - scope resolution

---

### Phase 2 — PipelineSpec Generator (Deterministic planning)
Implement:

- unified schema slots (pattern, scope, filters, actions)
- tool adapters for the core set (start with `fd`, `rg`, `fzf`, `bat`, `sd`)
- deterministic planner that produces `PipelineSpec`

Deliverables:
- `two plan <intent>` → outputs PipelineSpec JSON
- golden tests for key workflows

---

### Phase 3 — Execution Engine (CLI mode)
Implement pipeline execution:

- spawn commands
- connect stdout → stdin
- support `--dry-run` (print pipeline)
- support `--json` output for plan

Deliverables:
- `two run <intent>`
- `two --dry-run …`

---

### Phase 4 — State: History / Cache / Index
Add per-workspace state directory:

- `./.metainfo/state/history.sqlite` (or simple log)
- `./.metainfo/state/cache/`

Scope:
- store last N plans
- store commonly used scopes
- optional: cache expensive resolves

Deliverables:
- `two history`
- `two cache prune`

---

### Phase 5 — Daemonization (Optional)
Promote planner + executor into a long-lived service:

- Unix socket at `~/.local/run/two/two.sock`
- request/response protocol:
  - `{cwd, intent, options} → {pipelinespec, result}`

Deliverables:
- `two daemon` (server)
- `two` (client shim)
- systemd user service

---

## Migration Plan (From “ad-hoc repos” to TWO.workspace)

### Step 1 — Standardize Directory Layout
Target:
- `~/src` = projects
- `~/notes` = notes
- `~/scratch` = experiments

Action:
- Move/alias repos gradually; no big-bang.

### Step 2 — Add `.metainfo/` to 1–2 pilot repos
Pick:
- one high-traffic repo
- one “notes/life” repo

Action:
- add `.metainfo/two.workspace.toml`
- define `scopes` you actually use

### Step 3 — Teach TWO to resolve scopes
Action:
- implement `two resolve`
- validate scope meaning in those repos

### Step 4 — Implement 3 canonical workflows
Example workflows to lock first:
1. `find` + preview + open (fd → fzf → hx)
2. content search (rg → fzf preview)
3. replace (rg → sd)

### Step 5 — Roll out to more repos
Action:
- template `.metainfo/two.workspace.toml`
- add with minimal scopes
- iterate when friction appears

---

## Nix Integration Plan

### A) Toolchain provisioning
Use Nix (home-manager or flake devShell) to install:
- `fd`, `ripgrep`, `fzf`, `bat`, `eza`, `sd`, `zoxide`, `ast-grep`
- `two` (your orchestrator package)

### B) Global config deployment
- deploy `~/.config/two/global.toml` via home-manager

### C) Systemd user service (daemon mode)
- define `two-daemon.service` in home-manager

### D) Optional: flake + workspace linkage
In project flakes:
- keep `flake.nix` + `.metainfo/` side-by-side
- devShell can export:
  - `TWO_WORKSPACE_ROOT` (optional)
  - tool defaults

---

## Risks / Design Constraints
- Avoid overfitting schemas: keep slots minimal and extensible
- Preserve Unix composability: PipelineSpec should always be renderable
- Don’t lock into daemon too early: design protocol first
- Keep workspace detection fast (cap upward traversal)

---

## Success Criteria
- “project/src/tests/docs” mean the same thing across machines
- `two plan` is deterministic and testable
- `two --dry-run` output matches expectations
- Nix ensures the same tool versions and configs everywhere
- Adding `.metainfo/` to a repo enables better defaults immediately

