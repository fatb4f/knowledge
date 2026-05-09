# ble.sh vi-mode walk-through

## 1) Operating model

This setup gives you a shell command line that behaves like a small vi buffer.

There are two distinct navigation domains:

* **within the current command buffer**
* **across command history entries**

Your config already biases `gg` and `G` toward **current-buffer multiline movement**, which is the right choice for shell editing:

* `gg` → first line of current command entry
* `G` → last line of current command entry

With the added bindings, history traversal becomes explicit:

* `C-up` → previous history entry
* `C-down` → next history entry

That is a good split:

* `j` / `k`, `gg`, `G` = move inside current multiline command
* `C-up` / `C-down` = move between history entries

---

## 2) Basic modes

## Insert mode

Prompt tag: **`(ins)`**

This is text-entry mode.
You are typing directly into the shell buffer.

Typical use:

* type commands
* insert spaces, quotes, flags, pipelines
* create multiline commands
* paste text
* jump out to Neovim with `C-x C-e`

Enter insert mode from normal mode with:

| Key       | Effect                                                                |
| --------- | --------------------------------------------------------------------- |
| `i`       | insert before cursor                                                  |
| `a`       | insert after cursor                                                   |
| `I`       | insert at start of line                                               |
| `A`       | insert at end of line                                                 |
| `o` / `O` | line-opening style behavior where supported by ble’s vi editing model |

Leave insert mode with:

| Key   | Effect                         |
| ----- | ------------------------------ |
| `Esc` | return to normal mode          |
| `C-[` | same as `Esc`                  |
| `C-c` | cancel current insert/vi state |

---

## Normal mode

Prompt tag: **`(cmd)`**

This is motion/operator mode.
You are no longer inserting text directly; you are issuing editing commands.

Typical use:

* move by char/word/line
* delete/change/yank text
* jump around multiline buffers
* select regions
* repeat edits

This is the main control mode for command-line editing.

---

## Visual mode

Prompt tag: **`(vis)`**

This selects a region in the current command buffer.

Typical use:

* select a word/phrase/range
* delete selected text
* change selected text
* yank selected text

Conceptually it works like Vim visual mode, but against the shell command buffer.

Common flow:

1. start in normal mode
2. press a visual key
3. expand selection with motions
4. apply an operator or replace by entering insert/change

---

## Select mode

Prompt tag: **`(sel)`**

Less central than insert/normal/visual.
It is another selection-oriented state used by ble’s vi machinery.

For daily shell work, most interaction will stay in:

* insert
* normal
* visual

---

# 3) Single-line basic shortcuts

## Core motion

In normal mode:

| Key       | Effect                      |
| --------- | --------------------------- |
| `h`       | move left                   |
| `l`       | move right                  |
| `0`       | beginning of line           |
| `^`       | first non-blank on line     |
| `$`       | end of line                 |
| `w`       | next word                   |
| `b`       | previous word               |
| `e`       | end of word                 |
| `f<char>` | find next char on line      |
| `t<char>` | move before next char       |
| `;`       | repeat last `f`/`t`         |
| `,`       | reverse-repeat last `f`/`t` |

These are the main high-frequency motions for shell work.

---

## Fast insertion entry points

| Key | Effect               |
| --- | -------------------- |
| `i` | insert before cursor |
| `a` | insert after cursor  |
| `I` | insert at line start |
| `A` | insert at line end   |

These are the fastest way to move between navigation and typing.

---

## Basic editing operators

| Key  | Effect                                       |
| ---- | -------------------------------------------- |
| `x`  | delete char under cursor                     |
| `dw` | delete word forward                          |
| `db` | delete backward to word start                |
| `d$` | delete to end of line                        |
| `cw` | change word                                  |
| `cc` | change current line/editable line region     |
| `yy` | yank line/line region semantics as supported |
| `p`  | paste after                                  |
| `P`  | paste before                                 |

For shell command work, the most useful are usually:

* `x`
* `dw`
* `d$`
* `cw`
* `p`

---

## Undo / redo

| Key   | Effect |
| ----- | ------ |
| `u`   | undo   |
| `C-r` | redo   |

Your config leaves normal-mode `C-r` as redo, which is appropriate if you want actual vi-style editing rather than readline-style reverse history search on `C-r`.

---

## Search / recall mindset

For quick shell editing, treat history search and vi motion as separate layers:

* use **history recall** to get the right command
* use **vi operators/motions** to reshape it

With your added bindings, that split becomes cleaner:

* `C-up` / `C-down` = history entry switching
* vi motions/operators = edit the current recalled entry

---

# 4) Multi-line basic shortcuts

This is where your config is strongest.

## Newline insertion

Because your vi insert-mode meta bindings are enabled:

```bash
ble-decode/keymap:vi_imap/define-meta-bindings
```

you get explicit newline insertion support.

Relevant behavior:

| Key     | Effect                                            |
| ------- | ------------------------------------------------- |
| `RET`   | newline for multiline/incomplete command contexts |
| `M-RET` | explicit newline insertion                        |
| `C-j`   | execute/accept line buffer                        |

The practical model is:

* use `RET` or `M-RET` to keep building the command
* use `C-j` when you want to run it

That is a good shell-oriented arrangement.

---

## In-buffer multiline navigation

Because you remapped `gg` and `G`:

| Key  | Effect                               |
| ---- | ------------------------------------ |
| `gg` | first line of current command buffer |
| `G`  | last line of current command buffer  |
| `j`  | next displayed line                  |
| `k`  | previous displayed line              |

This matters because default history-oriented `gg`/`G` behavior is less useful once you are editing a real multiline shell construct.

Use this for:

* heredocs
* `for` / `while` blocks
* long pipelines
* nested quoting
* multi-line JSON payloads
* long `find` / `rg` / `fd` commands

---

## History versus current buffer

This is the main distinction to internalize.

### Current command buffer movement

Use these when you want to stay inside the command you already have loaded:

* `h` `j` `k` `l`
* `w` `b` `e`
* `0` `^` `$`
* `gg`
* `G`

### History entry movement

Use these when you want a different command entirely:

* `C-up`
* `C-down`

That keeps history traversal from fighting with multiline cursor movement.

---

## Useful multiline edit patterns

## Pattern: trim the tail of a long command

1. `Esc`
2. move where needed with `w` / `b` / `j` / `k`
3. `d$` or `C`-style line-tail change semantics
4. re-enter insert mode

## Pattern: fix one option in a long pipeline

1. recall command
2. `Esc`
3. navigate with word motions or `f<char>`
4. `cw`
5. type replacement
6. `Esc`

## Pattern: jump to top or bottom of a block

* `gg` → top
* `G` → bottom

## Pattern: switch to an older command, then refine it

* `C-up` to older entry
* `Esc`
* use `dw`, `cw`, `A`, `I`, etc.

---

# 5) Editing the command line in Neovim

This is now the highest-leverage addition.

Assuming you added:

```bash
ble-bind -m vi_imap -f 'C-x C-e' edit-and-execute-command
ble-bind -m vi_nmap -f 'C-x C-e' edit-and-execute-command
```

and have:

```bash
export VISUAL=nvim
export EDITOR=nvim
```

the flow is:

## From insert mode or normal mode

Press:

```text
C-x C-e
```

ble.sh opens the current shell buffer in your external editor, which should now be `nvim`.

## Edit in Neovim

Use full editor power:

* motions
* search
* macros
* multi-line formatting
* text objects
* substitutions
* register operations

This is the right path for anything that is bigger than “small command-line surgery”.

## Save and quit

When you write and exit Neovim, ble.sh takes the edited buffer back.

With `edit-and-execute-command`, the intended flow is:

* edit
* return
* execute

So this is best for commands you are ready to run after final inspection.

---

## When to prefer Neovim editing

Use `C-x C-e` when the command crosses from “line edit” into “buffer edit”.

Typical triggers:

* heredoc
* shell function snippet
* nested quoting
* multiline curl payload
* long awk/sed fragment
* compound command with `&&` / `||`
* loop or case block
* command you may later promote into a script

Good rule:

* **small correction** → stay in vi normal mode
* **structural rewrite** → `C-x C-e`

---

# 6) Recommended everyday command-line workflow

## Fast path: short command

1. start in insert mode
2. type
3. `Esc`
4. adjust with `b`, `w`, `cw`, `x`, `A`
5. `Enter` or `C-j`

## Recall-and-edit path

1. `C-up` to older history entry
2. `Esc`
3. use normal-mode edits
4. run

## Long-command path

1. type rough draft
2. `C-x C-e`
3. finish in Neovim
4. save + quit
5. let ble execute it

## Multiline shell block path

1. build with `RET` / `M-RET`
2. navigate with `j`, `k`, `gg`, `G`
3. use normal-mode operators for local fixes
4. `C-j` to execute

---

# 7) Prompt interpretation

Your prompt is intentionally minimal:

```text
[user@host dir](mode)$
```

Mode segment meanings:

| Tag     | Meaning     |
| ------- | ----------- |
| `(ins)` | insert mode |
| `(cmd)` | normal mode |
| `(vis)` | visual mode |
| `(sel)` | select mode |

Operationally:

* if you see `(ins)`, typing inserts text
* if you see `(cmd)`, typing issues vi commands
* if you see `(vis)`, motion extends a selection

That makes mode errors easier to spot immediately.

---

# 8) Practical command set to memorize first

If you only memorize one small shell-editing set, use this:

## Mode control

* `Esc`
* `i`
* `a`
* `A`

## Motion

* `h` `l`
* `w` `b`
* `0` `$`
* `gg` `G`

## Editing

* `x`
* `dw`
* `cw`
* `d$`
* `u`
* `C-r`

## History / execution

* `C-up`
* `C-down`
* `C-j`

## External editor

* `C-x C-e`

That set is enough for most daily command-line work.

---

# 9) Mental model summary

Your setup now has a clean three-tier editing model:

## Tier 1: inline edits

Use:

* `i`, `a`, `A`
* `w`, `b`, `x`, `cw`, `d$`

Best for short commands.

## Tier 2: multiline buffer control

Use:

* `j`, `k`
* `gg`, `G`
* `RET`, `M-RET`, `C-j`

Best for pipelines and shell blocks.

## Tier 3: full-editor escape hatch

Use:

* `C-x C-e`

Best for commands large enough to deserve real editing.

That is a strong shell-centric vi-mode arrangement.

If you want, I can also turn this into a **compact cheat sheet version** suitable for a comment block in `120-vim-mode.bash` or a small `blesh-vi.md` doc.

