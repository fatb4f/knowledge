## 1-page implementation blueprint

## Goal

Build a small shell-based **picker/workbench** with these properties:

* **walk** directories under a prefix
* **preview** hovered entries by type
* **act** on the selected path
* optionally perform **source → destination** workflows

The only `fzf` surfaces you need first are:

* `--scheme=path`
* `--preview`
* `--bind`
* `reload(...)`
* `execute(...)` / `execute-silent(...)`
* `become(...)`
* `_fzf_comprun` only for completion customization, not for your main picker workflow.

---

## Layer 0: stable defaults

Keep this layer dumb.

Use it only for static presentation:

```bash
FZF_UI_OPTS=(
  --height=80%
  --layout=reverse
  --border
  --info=inline
  --scheme=path
)
```

Do **not** put file-specific previews in global defaults. `fzf` is a general-purpose filter, and the README explicitly warns against globally assuming file input.

---

## Layer 1: candidate generators

These define your modes.

```bash
cand_walk() {  # dirs only
  local prefix="${1:-.}"
  fd -t d . "$prefix"
}

cand_pick() {  # files + dirs
  local prefix="${1:-.}"
  fd . "$prefix"
}

cand_files() { # files only
  local prefix="${1:-.}"
  fd -t f . "$prefix"
}
```

### Contract

* **walk mode** → `cand_walk`
* **pick mode** → `cand_pick`
* **file mode** → `cand_files`

This is the layer that gives `fzf` its filesystem meaning.

---

## Layer 2: preview dispatcher

One function. Type branch here.

```bash
preview_path() {
  local p="$1"

  if [ -d "$p" ]; then
    tree -C -L 2 -- "$p" | head -200
  elif [ -f "$p" ]; then
    bat --color=always --style=numbers --line-range=:200 -- "$p"
  else
    file --brief -- "$p"
  fi
}
export -f preview_path
```

### Contract

* dir → `tree -L 2`
* file → `bat`
* fallback → `file`

This works because `fzf --preview` just runs your shell command against the focused candidate. `fzf` itself does not provide a built-in directory preview mode.

---

## Layer 3: primitive picker

Start here.

```bash
pick_path() {
  local mode="${1:-pick}"
  local prefix="${2:-.}"

  local gen
  case "$mode" in
    walk) gen="cand_walk" ;;
    files) gen="cand_files" ;;
    *) gen="cand_pick" ;;
  esac

  "$gen" "$prefix" |
    fzf "${FZF_UI_OPTS[@]}" \
      --preview 'preview_path {}'
}
```

### This gives you

* typed candidates
* typed preview
* plain selection

No actions yet.

---

## Layer 4: action bindings

This is where it becomes your Yazi replacement.

### Minimal useful actions

* `enter` → accept current selection
* `ctrl-o` → open in `nvim`
* `ctrl-g` → open `lazygit`
* `ctrl-y` → copy path
* `ctrl-f` → switch source mode
* `ctrl-r` → reload current mode

Use:

* `become(...)` when `fzf` should be replaced by the target process
* `execute(...)` / `execute-silent(...)` when you want to return to `fzf`
* `reload(...)` when you want to rebuild candidates dynamically.

### Example skeleton

```bash
pick_action() {
  local prefix="${1:-.}"

  cand_pick "$prefix" |
    fzf "${FZF_UI_OPTS[@]}" \
      --preview 'preview_path {}' \
      --bind 'ctrl-o:become(nvim {})' \
      --bind 'ctrl-g:become(lazygit -p {})' \
      --bind 'ctrl-y:execute-silent(printf %s {} | wl-copy)'
}
```

---

## Layer 5: walk mode with reload

This is the key feature for your directory descent model.

### Contract

* candidate source = dirs only
* preview = depth-2 tree
* accept or bound key = descend into hovered dir by reloading from that new prefix

`reload(...)` is the correct primitive for swapping candidate lists dynamically.

### Implementation pattern

Use a wrapper loop first. It is simpler and easier to debug than trying to persist all state inside one heroic `fzf` invocation.

```bash
walk_dirs() {
  local prefix="${1:-.}"
  local sel

  while true; do
    sel="$(cand_walk "$prefix" |
      fzf "${FZF_UI_OPTS[@]}" \
        --preview 'preview_path {}')" || return 1

    [ -d "$sel" ] || { printf '%s\n' "$sel"; return 0; }
    prefix="$sel"
  done
}
```

### Why start with a shell loop

* clearer state
* easier to inspect
* simpler error handling
* no quoting fights around `reload(...)`

After this works, compress it into in-session `reload(...)` if still needed.

---

## Layer 6: two-phase source → destination actions

Do **not** start with one-session wizard logic.

Start with this contract:

```bash
yank_action() {
  local src dst

  src="$(pick_path pick .)" || return 1
  dst="$(walk_dirs .)" || return 1

  yank "$src" "$dst"
}
```

### Why this is the correct V1

* explicit state
* easy to test
* separate previews for source and destination
* no reliance on fragile terminal key semantics

Later, if you still want a single-session flow:

* bind a key to capture current `{}` as source
* `reload(...)` into destination mode
* second accept runs the action

But that is V2, not V1.

---

## Layer 7: shell integration

Keep this separate from the workbench.

### `_fzf_comprun`

Use it only to customize **completion-time** `fzf` behavior per command. In the shell integration, the first arg is the command name and the rest are forwarded to `fzf`, which is why the common pattern is:

```bash
local command=$1
shift
```

That is completion policy, not your main picker engine.

### Good use of `_fzf_comprun`

* `cd` completion → directory tree preview
* generic file completion → `bat`
* ssh completion → host metadata preview

### Bad use of `_fzf_comprun`

* implementing source/destination workflows
* implementing your main walk/action picker
* storing picker state

---

## Recommended build order

### V1

* `cand_walk`
* `cand_pick`
* `preview_path`
* `pick_path`

### V2

* wrapper loop for directory walk

### V3

* action binds: `nvim`, `lazygit`, copy path

### V4

* dedicated wrappers:

  * `walk_open`
  * `walk_edit`
  * `walk_copy`
  * `walk_move`
  * `walk_yank`

### V5

* optional in-session `reload(...)` mode switching

---

## Suggested file split

```text
~/.local/lib/bash/fzf/
  candidates.sh   # cand_walk, cand_pick, cand_files
  preview.sh      # preview_path
  picker.sh       # pick_path, walk_dirs
  actions.sh      # walk_open, walk_yank, etc
  completion.sh   # _fzf_comprun only
```

---

## Minimal success criteria

You are done with the first useful version when you can:

* descend directories with a depth-2 preview
* pick a file or dir from a scoped prefix
* open in `nvim`
* launch `lazygit`
* copy/yank selected paths
* perform a 2-phase source → destination action with two explicit picks

That already covers the retained Yazi surface you described.

