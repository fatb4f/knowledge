# Terminal Project Management Setup (Worktree + Zellij + Codex)

## Recommended method (practical + scalable)

- **One worktree per task/packet/issue**, rooted at `../wt/<repo>/<task>` with its own terminal session.
- **One terminal session per worktree** (Zellij or tmux), named to match the worktree folder.
- **One agent session per worktree** (Codex TUI attached to that session), not per repo.
- A tiny **session index note** per worktree (e.g., `../wt/<repo>/ledger/sessions/<date>-<task>.md`) to keep human context stable.

### Why this works

- Worktrees isolate git state (no dirty main, no accidental branch mixing).
- Session naming prevents sending commands to the wrong repo.
- Codex TUI tied to a single worktree reduces context contamination.

---

## Concrete conventions (low-friction)

- **Worktrees:** `../wt/<repo>/<packet-id>-<shortname>`
- **Branch names:** `packet/<id>-<shortname>`
- **Zellij session name:** `wt:$WORKTREE_NAME` (via lazyworktree config)
- **Codex TUI:** always launched from the worktree root

---

## Implementation (lazyworktree + Zellij)

Lazyworktree handles worktree creation, branch naming, and session lifecycle. Zellij tabs are configured via `custom_commands` and `zellij` fields.

### Core config

Add a Zellij command to `~/.config/lazyworktree/config.yaml`:

```yaml
session_prefix: "wt-"

custom_commands:
  "Z":
    description: Zellij session
    show_help: true
    zellij:
      session_name: "wt:$WORKTREE_NAME"
      attach: true
      on_exists: "switch"
      windows:
        - name: backlog
          command: "bash -lc \"$EDITOR backlog.md\""
        - name: session
          command: "bash -lc \"$EDITOR .session.md\""
        - name: shell
          command: fish
        - name: files
          command: yazi
        - name: codex
          command: codex
```

Notes:
- `session_prefix` controls which sessions show up in the command palette.
- Zellij session names are sanitized by lazyworktree (`/`, `\`, `:` → `-`).

### Fish shell integration

Lazyworktree ships fish helpers and completion generation. Source the fish functions once and add completions:

```fish
# config.fish
source /path/to/lazyworktree/shell/functions.fish

# completions
lazyworktree completion fish --code > ~/.config/fish/completions/lazyworktree.fish
```

---

## Usage

```bash
# from repo root
lazyworktree

# create a worktree (press "c") and jump into it (Enter)
# open the Zellij session (press "Z")
```

---

# Python project managers / environments (high-signal)

Most projects are Python-based, so standardize on one of these:

- **uv**: fast, unified toolchain (project mgmt, lockfiles, tool installs, Python installs, scripts).
- **Poetry**: mature, common choice for dependency + packaging with `poetry.lock`.
- **PDM**: PEP-focused manager with lockfiles and optional PEP 582 (rejected PEP) workflow.
- **Hatch**: project manager + build backend (Hatchling) + envs.
- **Pixi**: conda-forge + PyPI, multi-language envs, lockfiles, tasks.
- **Miniforge**: conda-forge installer including conda + mamba for robust binary envs.

Pick **uv** as the default unless you need conda-forge (then use Pixi or Miniforge).

---

# Tools (yazi-centric)

Yazi is the preferred file manager for this workflow:

- Add a Zellij tab for yazi (see config above).
- Use yazi plugins (e.g., custom-shell to run lazygit) inside the worktree.
- Leverage yazi IPC (`ya emit ...`) to script file/navigation actions when needed.
- Optional: open yazi in a floating Neovim window via yazi.nvim; launch lazyworktree from yazi with a custom-shell command.

### Plugin + IPC examples

`keymap.toml` (plugin example: lazygit via custom-shell):

```toml
[[mgr.prepend_keymap]]
on  = [ "g", "l" ]
run = "plugin custom-shell -- custom auto lazygit"
desc = "lazygit"
```

`keymap.toml` (IPC example: jump to git root):

```toml
[[mgr.prepend_keymap]]
on  = [ "g", "r" ]
run = 'shell -- ya emit cd "$(git rev-parse --show-toplevel)"'
desc = "cd to git root"
```

Optional plugin to run arbitrary commands (e.g., launch lazyworktree from yazi):

```toml
[[mgr.prepend_keymap]]
on  = [ "g", "w" ]
run = "plugin custom-shell -- custom fish 'lazyworktree' --orphan"
desc = "lazyworktree (shell)"
```

---

# Plugin provider scope + stability notes

“Plugin provider” here includes runtime/API surface, distribution/versioning, and the stated stability/compatibility contract.

### Capability snapshot

**Yazi (plugins + `ya pkg`)**
- Runtime/language: Lua.
- Plugins can be: functional key-bound actions + previewers/preloaders in the preview pipeline.
- Execution model: async-first with a sync context for UI/state; async plugins can sync-block to read/modify state.
- Cross-instance/eventing: DDS pub/sub across instances via Lua `ps` API and CLI `ya pub/emit`.
- Packaging: `ya pkg` clones from GitHub and locks revisions/hashes in `package.toml`.

**Zellij (WASM/WASI plugins)**
- Runtime/language: WASM/WASI (Rust officially supported; other languages possible).
- Plugins can: subscribe to events, call commands, access the launch folder, offload work to async workers, and render UI as panes.
- Distribution: load `.wasm` via URL schemes (`http(s)`, `file:`, `zellij:`); no built-in package manager.

### Stability / compatibility posture

**Yazi**
- Plugin system labeled beta/early; many plugins track latest Yazi (HEAD).
- `ya` and `yazi` versions must match exactly.
- Practical risk: higher churn; pin Yazi + `ya` + plugin revisions together.

**Zellij**
- Plugin system is early-stage but publishes upgrade notes and aims for forward-compat (with caveats).
- Practical risk: still evolving, but more explicit upgrade guidance.

### Practical guidance

- Need deep file-manager integration (previewers, preloaders, file actions, multi-instance sync): invest in Yazi, but pin versions.
- Need lower-maintenance plugin posture for UI panes/dashboards/multiplexer control: prefer Zellij’s plugin surface.

---

# Backlog.md (repo-local project management)

## Role in this workflow

Backlog.md provides a **repo-native task system** that works well with worktrees:

- Use **Backlog.md CLI** (if installed) to manage richer task metadata and a Kanban board.
- Keep “human context” in a simple `.session.md` note inside the worktree (manual or generated by a post-create hook).
- Optionally keep a lightweight `backlog.md` scratchpad in the worktree for quick notes.

## Two modes

### Mode A — Minimal (no Backlog.md CLI required)

Use `backlog.md` as the task scratchpad for the worktree:

- `backlog.md` holds a tiny checklist.
- `.session.md` holds constraints, command log, and state (GREEN/YELLOW/RED).

### Mode B — Backlog.md CLI (terminal Kanban)

When Backlog.md is installed:

- Initialize once per repo: `backlog init "<Project Name>"`
- Create tasks: `backlog task create "<task>"`
- Show terminal board in a pane: `backlog board view`

## Suggested task ↔ worktree linkage

Inside the session note (`.session.md`), include:

- `task_id:` (packet-id)
- `worktree:` path
- `branch:` name
- `done:` explicit criteria

This keeps “project management” deterministic while preserving isolation.
