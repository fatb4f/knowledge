Below is a compact **kitty-first** design that gives you:

- a **session mode**
- a **worktree mode**
- reusable **launch aliases**
- an optional **remote-control helper** path

It stays aligned with your current stack split: `kitty` remains the outer launcher and project/session switcher, `fish` remains thin shell glue, and `tmux` stays optional unless you need durable runtime state.

Kitty supports the pieces this design uses: modal keymaps with `map --new-mode`, multi-action macros with `combine`, session actions such as `goto_session`, `save_as_session`, and `close_session`, and tab/window launch primitives such as `launch --cwd=current --type=tab` and `new_tab_with_cwd`. Kitty also supports scripted control via `remote_control` and `remote_control_script`, plus `kitten @` for command-style control. ([Kovid Goyal's Projects][1])

## `kitty.conf` sketch

```conf
# ----------------------------------------
# launch policy / aliases
# ----------------------------------------

# Canonical "open a tab in the current cwd"
action_alias launch_tab launch --cwd=current --type=tab

# Common tools
action_alias launch_shell launch --cwd=current --type=tab fish
action_alias launch_nvim  launch --cwd=current --type=tab nvim
action_alias launch_lg    launch --cwd=current --type=tab lazygit

# Run helper scripts from config dir
action_alias launch_cfg_tab launch --cwd=current --type=tab sh -lc

# ----------------------------------------
# ergonomic entry points
# ----------------------------------------

# direct launches
map kitty_mod+enter launch_shell
map kitty_mod+e     launch_nvim
map kitty_mod+g     launch_lg

# save session quickly
map kitty_mod+s save_as_session

# ----------------------------------------
# session mode
# ----------------------------------------

map --new-mode session kitty_mod+a>s
map --mode session esc pop_keyboard_mode

# session lifecycle
map --mode session o goto_session
map --mode session s save_as_session
map --mode session x close_session .

# open new tab in active session, same cwd
map --mode session t new_tab_with_cwd

# save current session, then open a fresh tab in same cwd
map --mode session n combine : save_as_session : new_tab_with_cwd

# open config-oriented helper tabs
map --mode session e launch_nvim
map --mode session g launch_lg

# ----------------------------------------
# worktree mode
# ----------------------------------------

map --new-mode worktree kitty_mod+a>w
map --mode worktree esc pop_keyboard_mode

# picker / creator / prune helpers
map --mode worktree w launch_cfg_tab "~/.config/kitty/bin/worktree-pick; exec fish"
map --mode worktree c launch_cfg_tab "~/.config/kitty/bin/worktree-create; exec fish"
map --mode worktree p launch_cfg_tab "~/.config/kitty/bin/worktree-prune; exec fish"

# open editor or lazygit in current cwd as cheap per-worktree actions
map --mode worktree e launch_nvim
map --mode worktree g launch_lg

# ----------------------------------------
# optional remote control helpers
# ----------------------------------------

# inspect kitty state without enabling broad external control
map kitty_mod+a>l remote_control ls

# run a more complex script using remote control infrastructure
map kitty_mod+a>r remote_control_script ~/.config/kitty/bin/kitty-session-inspect
```

This design uses `kitty_mod+a>s` and `kitty_mod+a>w` as mode entry points instead of leaning on function keys. The alias layer keeps launch policy centralized, and the modes keep session control and worktree control distinct. Kitty’s docs explicitly support aliases, modal mappings, `combine`, session actions, `new_tab_with_cwd`, and keybound remote-control commands. ([Kovid Goyal's Projects][2])

## Minimal helper scripts

These keep **git** as the worktree authority and keep kitty as only the control surface. That matches your own rule set: shell helpers should stay thin and launch tools rather than own state.

### `~/.config/kitty/bin/worktree-pick`

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "${repo_root}" ] || { echo "Not in a git repo"; exit 1; }

cd "$repo_root"

pick_cmd() {
  if command -v fzf >/dev/null 2>&1; then
    git worktree list --porcelain \
      | awk '
          /^worktree / { path=$2 }
          /^branch /   { branch=$2; sub("^refs/heads/", "", branch); print branch "\t" path }
        ' \
      | fzf --with-nth=1,2 --delimiter='\t' \
      | cut -f2
  else
    git worktree list --porcelain \
      | awk '/^worktree / { print $2 }' \
      | sed -n '1p'
  fi
}

target="$(pick_cmd)"
[ -n "${target:-}" ] || exit 0

cd "$target"
printf 'Switched shell to %s\n' "$PWD"
exec fish
```

### `~/.config/kitty/bin/worktree-create`

```bash
#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "${repo_root}" ] || { echo "Not in a git repo"; exit 1; }

cd "$repo_root"

read -rp "Branch name: " branch
[ -n "${branch:-}" ] || { echo "No branch"; exit 1; }

base_dir="$(dirname "$repo_root")"
repo_name="$(basename "$repo_root")"
target="${base_dir}/${repo_name}--${branch}"

git worktree add -b "$branch" "$target"
cd "$target"
printf 'Created worktree: %s\n' "$PWD"
exec fish
```

### `~/.config/kitty/bin/worktree-prune`

```bash
#!/usr/bin/env bash
set -euo pipefail
git rev-parse --show-toplevel >/dev/null 2>&1 || { echo "Not in a git repo"; exit 1; }
git worktree prune
git worktree list
exec fish
```

## Optional: session-aware worktree jump

If you want the picker to also jump into a named kitty session, add a second helper that uses `kitten @ goto-session`. Inside kitty, `kitten @` can control the current instance without needing an external `--to` target, while mapped `remote_control` and `remote_control_script` commands do not require broad global remote-control exposure. External control does require a listening socket plus `allow_remote_control` or a tighter password-based policy. ([Kovid Goyal's Projects][3])

Example pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail

target="${1:?target path required}"
session_name="${2:?session name required}"

cd "$target"
kitten @ goto-session "$session_name" >/dev/null 2>&1 || true
exec fish
```

## Optional watcher stance

Kitty watchers exist and can react to window lifecycle events such as resize, focus, title change, and close, either through launch-time watcher attachment or globally via the `watcher` option in `kitty.conf`. They are useful for metadata, cleanup, and light instrumentation. ([Kovid Goyal's Projects][4])

For this setup, I would **not** start with watchers. Keep the baseline deterministic:

- keymap enters mode
- alias launches tab
- shell helper performs git worktree action
- session save/switch stays explicit

Then add watchers only for narrow needs like tab-title normalization or cleanup telemetry. That preserves the boundary in your stack guide: `kitty` for entry and switching, `fish` for glue, `git` for worktree state.

## Recommended operating model

### Core

- `git worktree` owns repo/task isolation
- kitty sessions own tab/session topology
- aliases define launch policy
- shell scripts perform worktree actions

### Leave out by default

- tmux
- global remote control
- watchers as orchestration logic

### Add later if needed

- `tmux` only for persistent runtime lanes
- `kitten @` helpers for richer inspection or scripted jumps
- watchers for metadata/cleanup

## Tight version

If you want the smallest viable version, start with just this:

```conf
action_alias launch_tab launch --cwd=current --type=tab
map kitty_mod+e launch_tab nvim
map kitty_mod+g launch_tab lazygit
map kitty_mod+s save_as_session
map --new-mode session kitty_mod+a>s
map --mode session esc pop_keyboard_mode
map --mode session o goto_session
map --mode session t new_tab_with_cwd
map --mode session x close_session .
map --new-mode worktree kitty_mod+a>w
map --mode worktree esc pop_keyboard_mode
map --mode worktree w launch_tab sh -lc "~/.config/kitty/bin/worktree-pick; exec fish"
```

That is enough to test whether **kitty sessions + worktrees** already cover your real needs before adding anything else.

[1]: https://sw.kovidgoyal.net/kitty/mapping/?utm_source=chatgpt.com "Making your keyboard dance - kitty"
[2]: https://sw.kovidgoyal.net/kitty/conf/?utm_source=chatgpt.com "kitty.conf - Kovid's software projects"
[3]: https://sw.kovidgoyal.net/kitty/remote-control/?utm_source=chatgpt.com "Control kitty from scripts"
[4]: https://sw.kovidgoyal.net/kitty/launch/?utm_source=chatgpt.com "The launch command - kitty"

hat is the cleaner version of the stack.
