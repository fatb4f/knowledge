# Annex: Proposal Decisions (Worktrees + Zellij + Yazi + Helix)

This annex captures the implementation decisions needed to make the workflow concrete.

## Current workflow anchor

- kitty → zellij → zellij_session (zsm) → {pane-yazi, pane-codex}
- Primary editor: Helix (with optional Neovim upgrade if QoL is compelling)
- Default key prefix in yazi: `g`

---

## Implementation decision checklist

- **Worktree manager**: lazyworktree config path + worktree base directory + session_prefix.
- **Branch naming**: default branch naming convention (packet/ID vs issue/PR).
- **Session lifecycle**: when/how zellij sessions are created/attached (lazyworktree keybinding vs manual).
- **Zellij layout**: layout file vs lazyworktree `zellij.windows`; pane order and naming.
- **Pane commands**: yazi, codex, shell; any init commands (env activation).
- **Yazi plugins**: shell plugin + git utilities; keybindings (see below).
- **Codex launch**: command, cwd, env (per-worktree venv/uv).
- **Python env**: tool of record (uv/poetry/pdm/etc.), venv location, auto-activation policy.
- **Backlog.md**: CLI vs scratchpad; creation strategy for `.session.md`.
- **Shell integration**: fish helpers + completions for lazyworktree.
- **Kitty integration**: whether kitty launches zellij or attaches.
- **Notes/logging**: where state/command logs live (repo vs external ledger).
- **Automation hooks**: lazyworktree init/terminate or post-create commands.

---

## Default picks (can be edited)

- **Worktree manager**: lazyworktree
- **Session prefix**: `wt-`
- **Zellij sessions**: created by lazyworktree `Z` custom command
- **Editor**: Helix (`$EDITOR=helix`)
- **Python env**: uv unless conda-forge is required

---

## Yazi keymap (Helix-first)

```toml
[[mgr.prepend_keymap]]
on  = [ "g", "l" ]
run = "plugin custom-shell -- custom auto lazygit"
desc = "lazygit"

[[mgr.prepend_keymap]]
on  = [ "g", "w" ]
run = "plugin custom-shell -- custom fish 'lazyworktree' --orphan"
desc = "lazyworktree (shell)"

[[mgr.prepend_keymap]]
on  = [ "g", "r" ]
run = 'shell -- ya emit cd "$(git rev-parse --show-toplevel)"'
desc = "cd to git root"

[[mgr.prepend_keymap]]
on  = [ "g", "e" ]
run = 'shell -- $EDITOR "$@"'
desc = "open selection in editor"
```

---

## Optional Neovim QoL

If you switch to Neovim, consider `yazi.nvim` to open yazi as a floating picker and return selections back to the editor.

