# Yazi-Driven ProjectOps (Nav/FileOps/GitStats/ProjectOps)

Rev: 5 | Last Updated: 2026-01-29

## Control map

| Layer | Responsibility | Mechanism (SSOT) | Notes |
|---|---|---|---|
| **Nav** | browse/select repos/files | **Yazi core** | Pre-worktree driver. |
| **File ops** | extra file actions | **Yazi `shell` commands** | Use `%h/%s/%d` + `--block` for TUIs. |
| **Git stats** | local git context | **Yazi git plugins** | `vcs-files` + `githead` + `path-from-root` + `lazygit`. |
| **ProjectOps** | WT/session/gates | **Yazi `shell` → `just …`** | `just` is the control plane; Yazi triggers it. |

---

## Core invariant

**ProjectOps is never implemented in Yazi.**

- Yazi only launches `just <verb>` from the current selection context.
- `just` (and underlying scripts) is the authoritative controller for:
  - worktree creation/selection
  - session attach/create
  - layout selection
  - gates/runbooks
  - notes/backlog policy

---

## Yazi keybinds (ProjectOps)

Place in `~/.config/yazi/keymap.toml`.

**Notes**
- `%h` = hovered path
- `--block` is required for interactive TUIs

```toml
[[mgr.prepend_keymap]]
on   = ["g", "w"]
run  = "shell --block -- bash -lc 'cd \"$(dirname \"%h\")\" && just wt'"
desc = "ProjectOps: worktree menu (from hovered)"

[[mgr.prepend_keymap]]
on   = ["g", "s"]
run  = "shell --block -- bash -lc 'cd \"$(dirname \"%h\")\" && just sess'"
desc = "ProjectOps: zellij session attach/create"

[[mgr.prepend_keymap]]
on   = ["g", "p"]
run  = "shell --block -- bash -lc 'cd \"$(dirname \"%h\")\" && just preflight'"
desc = "ProjectOps: preflight gate"

[[mgr.prepend_keymap]]
on   = ["g", "c"]
run  = "shell --block -- bash -lc 'cd \"$(dirname \"%h\")\" && just check'"
desc = "ProjectOps: check gate"

[[mgr.prepend_keymap]]
on   = ["g", "m"]
run  = "shell --block -- bash -lc 'cd \"$(dirname \"%h\")\" && just promote'"
desc = "ProjectOps: promote gate"
```

---

## Yazi plugins (high-signal)

### Shell helpers
- `custom-shell.yazi`
- `command.yazi`
- `yazi-prompt.sh` (optional)

### Git utils
- `lazygit.yazi`
- `vcs-files.yazi`
- `githead.yazi`
- `path-from-root.yazi`
- `git.yazi` (optional)

Example installs (ya pkg)

```bash
ya pkg add AnirudhG07/custom-shell
ya pkg add KKV9/command
ya pkg add Lil-Dank/lazygit

ya pkg add yazi-rs/plugins:vcs-files
ya pkg add llanosrocas/githead
ya pkg add aresler/path-from-root
ya pkg add yazi-rs/plugins:git
```

---

## `just` contract (ProjectOps SSOT)

Implement these recipes in your repo-root `justfile` (or a shared include):

- `wt`        — worktree menu/create/enter (calls `lazyworktree` or wrapper)
- `sess`      — attach/create zellij session for the current worktree root
- `preflight` — run gate 1
- `check`     — run gate 2
- `promote`   — run gate 3

### Expectations (to avoid surprises)

- `sess` assumes you are in a worktree root whose directory name is `<id>-<slug>` so it can derive `id` via `${base%%-*}`.
- If you trigger `sess` from Yazi, do so while hovering inside `../wt/<repo>/...` (existing worktrees), or prefer `wt` for the pre-WT flow.
  - If your worktrees live under `.codex/.worktrees/...`, hover there instead.
  - `sess` normalizes to the git worktree root; avoid running it in non-git directories.

### Minimal `justfile` skeleton (composable)

This version avoids backtick variables so it can be included cleanly; other recipes can call `just repo-root` / `just repo-name`.

```make
set shell := ["bash", "-uc"]

# ---- repo identity (composable) ----
repo-root:
  git rev-parse --show-toplevel

repo-name:
  basename "$(just repo-root)"

# ---- worktree ops ----
wt:
  # choose: run lazyworktree or your wrapper
  lazyworktree

# ---- session ops (worktree-scoped) ----
# Derives id from worktree dir name: <id>-<slug>
# Uses an ABSOLUTE layout path rooted at repo-root for determinism.
sess:
  wt_root="$$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; \
  repo_root="$$(just repo-root)"; \
  repo_name="$$(just repo-name)"; \
  layout="$$repo_root/tools/wt/layout.packet.kdl"; \
  base="$$(basename "$$wt_root")"; \
  case "$$base" in *-*) : ;; *) echo "ERR: worktree dir must be <id>-<slug>"; exit 2 ;; esac; \
  id="$${base%%-*}"; \
  sess="$$repo_name-$$id"; \
  if zellij list-sessions 2>/dev/null | awk '{print $$1}' | grep -qx "$$sess"; then \
    zellij attach "$$sess"; \
  else \
    cd "$$wt_root"; \
    zellij --new-session-with-layout "$$layout" -s "$$sess"; \
  fi

# ---- gates/runbooks ----
preflight:
  tools/tasks/preflight.sh

check:
  tools/tasks/check.sh

promote:
  tools/tasks/promote.sh
```

---

## Decisions required to finalize (5)

1. **Packet/worktree ID derivation**: directory name (`<id>-<slug>`) vs prompt vs git branch.
2. **Worktree base path**: `../wt/...` vs `.codex/.worktrees/...`.
3. **Session naming**: keep deterministic (recommended: `<repo>-<id>`).
4. **`just wt` implementation**: call `lazyworktree` vs custom selector.
5. **Log capture location for gates**: `.codex/out/<id>/…` vs `ledger/…` vs `./logs/…` (pick one as SSOT; gates should write there and print the pointer).
