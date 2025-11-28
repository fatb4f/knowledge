# Unified Keybindings Reference
Last updated: 2025-11-17

Scope: fish (vi-mode), Zellij (Alt-centered, autolock), Helix, Vim/Neovim, Yazi, fzf, Git tools.  
Goal: vi-homogeneous navigation and actions.

---

## 1. Global Mental Model

- Normal-mode style navigation everywhere:
  - `h/j/k/l` → left/down/up/right (cursor, selections, lines, panes).
  - `w/b/e`   → word-wise motions where supported.
  - `0/^/$`   → line start/first non-blank/line end.
- Window/pane navigation:
  - Zellij: `Alt-h/j/k/l` (and optional `Ctrl-h/j/k/l`).
  - Editors: `Ctrl-w h/j/k/l`.
- Zellij-autolock:
  - When a triggered app runs in a pane (`vim`, `nvim`, `hx`, `fzf`, etc.), Zellij goes to `locked` mode → editor/TUI wins.
  - You explicitly lock/unlock Zellij with `Alt-z`, and enable autolock globally with `Alt-Shift-z`.

---

## 2. Zellij

### 2.1 Modes

- `normal`      — default + Alt-prefix commands.
- `pane`        — splitting / pane config.
- `resize`      — resizing.
- `move`        — moving panes.
- `tab`         — tab management.
- `scroll`      — scrollback navigation.
- `search`      — search in scrollback.
- `entersearch` — edit search query.
- `session`     — quit/detach/session-manager.
- `renamepane`, `renametab` — renaming.
- `locked`      — autolock target; editor keymaps own everything here.

Mode exits (except locked/session/rename):
- `Esc`, `Enter`, `Space`, `Ctrl-c`, `Ctrl-d` → return to `normal`.

### 2.2 Normal mode (Alt-centered)

Navigation and layout:

- `Alt-h` / `Alt-l` → `MoveFocusOrTab Left/Right`.
- `Alt-j` / `Alt-k` → `MoveFocus Down/Up`.
- `Alt-1..9`        → `GoToTab 1..9`.
- `Alt-[` / `Alt-]` → `PreviousSwapLayout` / `NextSwapLayout`.

Panes/tabs:

- `Alt-n` → `NewPane`.
- `Alt-p` → `SwitchToMode pane`.
- `Alt-r` → `SwitchToMode resize`.
- `Alt-t` → `SwitchToMode tab`.
- `Alt-s` → `SwitchToMode scroll`.
- `Alt-m` → `SwitchToMode move`.
- `Alt-o` → `SwitchToMode session`.

Session:

- `Alt-q` → `Quit`.
- `Alt-d` → `Detach`.

Resize:

- `Alt-+`, `Alt-=` → `Resize Increase`.
- `Alt--`          → `Resize Decrease`.

Autolock integration:

- `Enter` → `WriteChars <CR>` + `MessagePlugin autolock {}` (re-check triggers).
- `Alt-Shift-z` (in `shared`) → `MessagePlugin autolock { payload "enable"; }`.
- `Alt-z` (in `shared_except "locked"`)  
  → `MessagePlugin autolock { payload "disable"; }; SwitchToMode "locked"`.
- `Alt-z` (in `locked`)  
  → `MessagePlugin autolock { payload "disable"; }; SwitchToMode "normal"`.

Optional tmux-style focus (in `shared_except "locked"`):

- `Ctrl-h/j/k/l` → `MoveFocus[OrTab] Left/Down/Up/Right`.

### 2.3 Pane mode (`Alt-p`)

- Exit: `Esc`, `Enter`, `Space`, `Ctrl-c/d`.
- Splits:
  - `h` / `j` / `k` / `l` → `NewPane Left/Down/Up/Right`.
- Focus:
  - `p` → `SwitchFocus` (cycle).
- Actions:
  - `n` → `NewPane`.
  - `x` → `CloseFocus`.
  - `f` → `ToggleFocusFullscreen`.
  - `z` → `TogglePaneFrames`.
  - `w` → `ToggleFloatingPanes`.
  - `e` → `TogglePaneEmbedOrFloating`.
  - `r` → `SwitchToMode renamepane; PaneNameInput 0`.

### 2.4 Tab mode (`Alt-t`)

- Exit: `Esc`, `Enter`, `Space`, `Ctrl-c/d`.
- Navigation:
  - `h` / `l` → `GoToPreviousTab` / `GoToNextTab`.
  - `1..9`    → `GoToTab N`.
  - `Tab`     → `ToggleTab` (last tab).
- Management:
  - `n` → `NewTab`.
  - `x` → `CloseTab`.
  - `s` → `ToggleActiveSyncTab`.
  - `b` → `BreakPane`.
  - `[` / `]` → `BreakPaneLeft/Right`.
  - `r` → rename: `SwitchToMode renametab; TabNameInput 0`.

### 2.5 Resize mode (`Alt-r`)

- Exit: `Esc`, `Enter`, `Space`, `Ctrl-c/d`.
- `h/j/k/l` → `Resize Left/Down/Up/Right`.
- `Alt-+` / `Alt-=` / `Alt--` → increase / decrease.
- `Alt-n` → `NewPane`.

### 2.6 Move mode (`Alt-m`)

- Exit: `Esc`, `Enter`, `Space`, `Ctrl-c/d`.
- `h/j/k/l` → `MovePane Left/Down/Up/Right`.
- `Alt-n`   → `NewPane`.

### 2.7 Scroll & search

Scroll mode (`Alt-s`):

- Exit: `Esc`, `Enter`, `Space`.
- `j` / `k` → `ScrollDown` / `ScrollUp`.
- `Alt-f` / `Alt-b` / `Right` / `Left` / `l` / `h` → page down/up.
- `d` / `u` → half-page down/up.
- `Alt-c` → `ScrollToBottom` + back to `normal`.
- `e`     → `EditScrollback` + back to `normal`.
- `s`     → `SwitchToMode entersearch; SearchInput 0`.

Search mode:

- Exit: `Alt-s`, `Esc`, `Enter`, `Space` → `normal`.
- `s`   → back to `entersearch`.
- `n` / `p` → next / previous match.
- `c` / `w` / `o` → toggle case / wrap / whole-word.

Entersearch:

- `Enter` → `SwitchToMode search`.
- `Alt-c`, `Esc` → `SearchInput 27; SwitchToMode scroll`.

### 2.8 Session / rename / locked

Session mode (`Alt-o`):

- Exit: `Esc`, `Enter`, `Space`, `Ctrl-c/d`.
- `d` → `Detach`.
- `q` → `Quit`.
- `s` → `LaunchOrFocusPlugin "zellij:session-manager"` (floating, move_to_focused_tab) + return to `normal`.

Rename:

- `renametab`: `Esc`, `Ctrl-c` → `UndoRenameTab; SwitchToMode normal`.
- `renamepane`: `Esc`, `Ctrl-c` → `UndoRenamePane; SwitchToMode normal`.

Locked:

- `Alt-z` → disable autolock + `SwitchToMode normal`.
- Everything else belongs to the app (Vim/Helix/FZF/etc.).

---

## 3. fish (vi-mode)

Assumes `fish_vi_key_bindings` is enabled.

Modes:

- `Esc` → normal mode.
- `i`, `a`, `A`, `I`, `o`, `O` → enter insert mode (line editing).
- `v` or custom mapping → visual selection (if configured).

Navigation (line editing):

- `h/j/k/l` → left/down/up/history-up/right (depending on your exact bindings).
- `w` / `b` → next/previous word.
- `0` / `^` / `$` → line start / first non-blank / end of line.

Search history:

- `Ctrl-r` → history search, or mapped to `fzf`-based history if set.

Execution:

- `Enter` → accept line.
- `Ctrl-c` → cancel.

---

## 4. Helix (`hx`)

Modes: `normal`, `insert`, `select`, `goto`, `view` etc.

Core motions (normal/select):

- `h/j/k/l` → left/down/up/right.
- `w` / `b` / `e` / `ge` → word motions.
- `0` / `^` / `$` → start / first non-blank / end of line.
- `g g` / `G` → file top/bottom.
- `Ctrl-u` / `Ctrl-d` → half-page up/down.
- `{` / `}` → paragraph or block-wise nav (depending on tree-sitter context).

Selections / text objects:

- `v` (or `V` / `Ctrl-v` equivalent) → toggle selection mode.
- `s i (` / `s a (` etc. depending on your configured object-select commands:
  - Inside/around parentheses, braces, brackets, quotes, word, line, etc.
- `x` / `d` / `c` → delete / change with selection.
- `y` → yank selection.

Windows (Helix):

- `Ctrl-w h/j/k/l` → move to split in direction.
- `Ctrl-w s/v`     → split horizontally/vertically.
- `Ctrl-w c`       → close split.

Search:

- `/` → search forward.
- `n` / `N` → next/prev match.

---

## 5. Vim / Neovim

Standard vi grammar; only the cross-tool pieces:

Windows / splits:

- `Ctrl-w s` / `Ctrl-w v` → horizontal / vertical split.
- `Ctrl-w q`              → close window.
- `Ctrl-w h/j/k/l`        → move to window left/down/up/right.

Tabs:

- `:tabnew`, `:tabnext`, `:tabprev`, `gt` / `gT`.
- Recommended to conceptually align with Zellij tabs (`Alt-1..9`) but not remap unless needed.

Motions and objects:

- `h/j/k/l`, `w/b/e`, `0/^/$`, `gg/G`, `Ctrl-d/u`, text objects `iw`, `aw`, `i(`, `a(`, `i{`, etc.

---

## 6. Yazi

Typical keymap (assuming default vi-like bindings):

- Navigation:
  - `h` → go up directory / parent.
  - `l` → enter directory / open file.
  - `j` / `k` → down / up in list.
- Selections:
  - `v` → toggle select.
  - `V` → select all (if mapped).
- Tabs:
  - `t` → new tab, `T` / numeric keys to switch (depending on config).
- Split / preview:
  - `p` or space as preview (depending on your config).
- Search/filter:
  - `/` → filter or search.
  - `n` / `N` → next/previous match.

Align mental model:

- `h/l` = folder in/out, `j/k` = vertical list navigation; treat Yazi “tabs” parallel to Zellij tabs.

---

## 7. fzf / TUI tools

fzf (standalone):

- Basic:
  - `Ctrl-j` / `Ctrl-k` → down/up.
  - `Enter`            → accept.
- Vim integration:
  - Keep `Ctrl-t` / `Ctrl-x` / `Ctrl-v` etc. consistent where possible.

Other TUI tools (e.g. `tig`, `lazygit`, custom):

- Prefer vi-style navigation: `h/j/k/l`, `/` search, `n`/`N` navigation, `q` to quit.

---

## 8. Git-related commands (conceptual)

CLI (git):

- Aliases can be added to align with motions:
  - `gs` → `git status`.
  - `gl` → `git log --oneline --graph`.
  - `gd` → `git diff`.
  - `gc` → `git commit`.
  - `gp` → `git push`.

TUI (`lazygit`/`tig`):

- Prefer vi navigation: `j/k` for selection, `h/l` for hierarchy, `/` for search, `n/N` for next/prev.

---

# Unified Motion Grammar
Last updated: 2025-11-17

Goal: define motions once; apply across fish, Helix, Vim/Neovim, Zellij, Yazi, fzf, etc.

---

## 1. Axes of Motion

### 1.1 Linear cursor motions (within a buffer/line)

Canonical motions:

- Left/right: `h` / `l`.
- Up/down (lines): `k` / `j`.
- Word-wise:
  - Forward word start: `w`.
  - Backward word start: `b`.
  - Forward word end: `e`.
- Line boundaries:
  - Hard start: `0`.
  - Soft start (first non-blank): `^`.
  - End: `$`.
- File boundaries:
  - Top: `gg` (or home command).
  - Bottom: `G`.

Mapping examples:

- fish: `h/l`, `Ctrl-b/f`, `w/b`, `0/^/$`.
- Helix: identical semantics (`w/b/e`, `0/^/$`, `gg/G`).
- Vim: native vi.
- Yazi: `j/k` for vertical; treat `h`/`l` as step “out/in”.

---

## 2. Structural motions

### 2.1 Page / viewport

Canonical:

- Half-page: `Ctrl-u` (up), `Ctrl-d` (down) or `u` / `d` in some tools.
- Full page: `Ctrl-b` (back), `Ctrl-f` (forward) or tool-specific.

Mapping:

- Helix: `Ctrl-u` / `Ctrl-d`.
- Vim: `Ctrl-u` / `Ctrl-d`, `Ctrl-b` / `Ctrl-f`.
- Zellij scroll mode:
  - `u` / `d` → half-page up/down.
  - `Alt-b` / `Alt-f` → page up/down.

### 2.2 Paragraph / block / semantic unit

Canonical:

- `{` / `}` → previous/next paragraph or block.

Mapping:

- Helix: structured via tree-sitter; keep `{` / `}` semantics where possible.
- Vim: paragraph/block motions out-of-the-box.

---

## 3. Text object grammar

Canonical objects: `iX` / `aX`, where `X` is one of:

- `w` → word.
- `s` → sentence (if available).
- `p` → paragraph.
- `(`, `)`, `{`, `}`, `[`, `]`, `<`, `>`, `'`, `"`, ``` ` ``` → delimiters/quotes.
- `"` / `'` / ``` ` ``` for strings.
- `t` or custom for “tag”/HTML-like.

Operations:

- `d` + object → delete.
- `c` + object → change.
- `y` + object → yank.
- `v` + object → select.

Mapping:

- Vim/Neovim: native.
- Helix: use selection “object” commands, e.g.:
  - `s i w` → select inner word.
  - `s a w` → select around word.
  - `s i (` / `s a (` etc.
- fish / Zellij / Yazi: not applicable directly; treat text object grammar as editor-only.

---

## 4. Window/pane/tab motions

### 4.1 Editor windows/splits

Canonical motion:

- `Ctrl-w h/j/k/l` → move to window left/down/up/right.
- `Ctrl-w s/v` → split horizontally/vertically.
- `Ctrl-w c`   → close window.

Mapping:

- Vim/Neovim: native.
- Helix: `Ctrl-w` window keyspace configured to match.

### 4.2 Multiplexer panes/tabs (Zellij)

Canonical:

- Global focus (Zellij, non-locked):

  - Primary: `Alt-h/j/k/l` → `MoveFocus[OrTab] Left/Down/Up/Right`.
  - Optional: `Ctrl-h/j/k/l` (tmux-style alias).

- Tab motions:

  - `Alt-1..9` → go to tab N.
  - `Alt-[` / `Alt-]` → previous/next layout.
  - `Alt-t` → enter tab mode:
    - `h/l` → prev/next tab.
    - `n/x` → new/close tab.
    - `1..9` → go to tab N.

- Pane splits:

  - `Alt-p` → pane mode:
    - `h/j/k/l` → `NewPane Left/Down/Up/Right`.

### 4.3 Autolock transitions (Zellij ↔ editor/TUI)

Conceptual states:

- **Unlocked / managed by Zellij**:
  - Use `Alt-h/j/k/l`, `Alt-1..9`, `Alt-p/r/t/s/m`, etc.
- **Locked / managed by editor/TUI**:
  - Use editor’s `hjkl`, `Ctrl-w h/j/k/l`, etc.

Motion grammar:

- Enter locked via:
  - Autolock plugin detecting trigger (`vim|nvim|hx|fzf|...`).
  - Explicit: `Alt-z` from non-locked (disables autolock but puts you in locked mode).
- Exit locked:
  - `Alt-z` → disable autolock (if active), go to `normal`.

Enabling autolock:

- `Alt-Shift-z` → autolock enable; “let editor/TUI win” when matched.

---

## 5. Search motions

Canonical search:

- `/pattern` → search forward.
- `?pattern` → search backward (where supported).
- `n` / `N` → next/prev match.

Mapping:

- Vim/Neovim: `/`, `?`, `n`, `N`.
- Helix: `/`, `n`, `N`.
- Zellij scrollback:
  - `Alt-s` → enter `search` / exit to `normal`.
  - `s` in `scroll` → `entersearch` for query.
  - `n` / `p` → next/prev match.
- Yazi/fzf:
  - `/` → filter/search.
  - `n` / `N` (or enter/prev) depending on tool.

---

## 6. Mode transitions (summary)

### 6.1 Editor family (Vim/Helix)

- `Esc` → normal.
- `i/a/I/A/o/O` → insert.
- `v/V` / select-keys → visual/select mode.
- `:` → command-line.
- `/` → search mode.

### 6.2 Shell (fish, vi-mode)

- `Esc` → normal (command editing).
- `i/a/A` → insert at cursor/append.
- `v` (if bound) → edit command in `$EDITOR`.

### 6.3 Zellij

- From anywhere non-locked:
  - `Alt-p` / `Alt-r` / `Alt-t` / `Alt-s` / `Alt-m` / `Alt-o` into respective modes.
  - `Esc` / `Enter` / `Space` / `Ctrl-c/d` → `normal`.
- Locked:
  - `Alt-z` → `normal`.

---

## 7. Practical recipes

### 7.1 Move from Helix to another pane

1. You’re in Helix:
   - Zellij is likely in `locked` (autolock), editor owns keys.
2. Hit `Alt-z`:
   - Zellij unlocks, editor still running but no longer locked.
3. Use:
   - `Alt-h/j/k/l` or `Ctrl-w h/j/k/l` (if you prefer tmux-style) to move to another terminal pane.
4. Re-enable autolock when ready:
   - `Alt-Shift-z`.

### 7.2 Select and operate on “object between delimiters”

In Vim/Neovim:

- Example: delete inside parentheses:
  - Cursor anywhere in `foo(bar|baz)`.
  - Type: `d i (`.

In Helix:

- Equivalent conceptual sequence:
  - `s i (` (select inside parens).
  - Then `d` / `c` / `y` according to operation.

---

_End of documents._

