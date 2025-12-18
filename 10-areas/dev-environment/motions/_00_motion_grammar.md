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
