# TWO-Aligned 2-Day Terminal Workflow Bootcamp

## 1. Minimal TWO-Aligned `$argv` Schema

### 1.1 Verbs (mapping to OP)
- `nv` – Navigation
- `dc` – Discovery (search / content queries)
- `fm` – File management (inspect, modify)
- `ws` – Workspace (Zellij)
- `df` – Data filtering / triage
- `rf` – Refactor (code-structure aware)
- `au` – Audit (storage, cleanup)

### 1.2 Argument Slots
```
<verb> <target> [@root] [!lang] [flags...]
```
- `<target>` – pattern/symbol/dir/file name
- `@root` – root context (`@p` project, `@c` config, `@.` cwd)
- `!lang` – language filter (`!py`, `!rs`, etc.)
- Flags:
  - `+g` – git root
  - `+dN` – depth
  - `+m` – multi-select
  - `+C` – case-sensitive
  - `+t=file|dir` – constrain WHAT

### 1.3 Canonical Toolchain (manual execution)
| OP | Verb | Toolchain |
|----|------|-----------|
| NAV | `nv` | `fd` → `fzf` → `cd` / `z` |
| DISCOVER | `dc` | `rg` → `fzf` → `bat`/`hx` |
| FM | `fm` | `eza` / `yazi` / `mv`/`rm` |
| WS | `ws` | `zellij attach -c NAME` |
| REF | `rf` | `rg` → `ast-grep`/`comby` → `hx` |
| DF | `df` | `command | fzf` |
| AUDIT | `au` | `dust` / `ncdu` |

---

## 2. Day 1 — Shell & Multiplexer Core (TWO-Aligned)

### 2.1 AM — Fish + fd / rg / zoxide / fzf

#### A. NAV: jump to any directory named `src`
**Equation**: `NAV(PATH | name≈"src", root=@p) -> cwd'`

**$argv**: `nv "src" @p +t=dir`

**Pipeline**:
```
fd -t d src @p | fzf | xargs -r cd
```

#### B. NAV: jump via zoxide
**Equation**: `NAV(PATH | frecency>τ) -> cwd'`

**$argv**: `nv "proj-name" @. +z`

**Pipeline**:
```
z proj-name
# or
zoxide query -l | fzf | xargs -r z
```

#### C. DISCOVER: find all TODOs
**Equation**: `DISCOVER(CONTENT | pattern="TODO", root=@p) -> MATCH_SET`

**$argv**: `dc "TODO" @p`

**Pipeline**:
```
rg -n "TODO" @p | fzf --preview 'bat -n {1} --highlight-line {2}'
```

#### D. DISCOVER: search only in Python files
**Equation**: `DISCOVER(CONTENT | pattern="def ", lang=py, root=@p) -> FILE'`

**$argv**: `dc "def " @p !py`

**Pipeline**:
```
file=$(rg -l --glob '*.py' 'def ' @p | fzf)
[ -n "$file" ] && hx "$file"
```

#### E. DF: free-form fzf over paths
**Equation**: `DF(PATH | root=@.) -> PATH_TARGET`

**$argv**: `df "*" @.`

**Pipeline**:
```
fd . @. | fzf
```

#### F. NAV: return via z `-`
**Equation**: `NAV(PATH | prev_cwd) -> cwd'`

**$argv**: `nv "-" @.`

**Pipeline**:
```
z -
```

---

### 2.2 PM — Zellij Modes + Search Integration

#### G. WS: attach/create session
**Equation**: `WS(SESSION | name="app") -> SESSION'`

**$argv**: `ws "app"`

**Pipeline**:
```
zellij attach -c app
```

#### H. WS + DF: fuzzy-pick session
**Equation**: `DF(SESSION | all_sessions) -> SESSION'`

**$argv**: `df "session" @ws`

**Pipeline**:
```
zellij list-sessions | fzf | awk '{print $1}' | xargs -r zellij attach -c
```

#### I. NAV inside pane 1 (fd+fzf)
**Equation**: `NAV(PATH | pattern≈target, root=@p) -> cwd'`

**$argv**: `nv "target" @p`

**Pipeline**:
```
fd . @p | fzf | xargs -r cd
```

#### J. DISCOVER inside pane 2 (rg+fzf)
**Equation**: `DISCOVER(CONTENT | pattern, root=@p) -> inspected_match`

**$argv**: `dc "pattern" @p`

**Pipeline**:
```
rg -n "pattern" @p | fzf --preview 'bat -n {1} --highlight-line {2}'
```

---

### 2.3 Night — Autolock + Panic Reset Routine

- Re-establish NAV first, then DISCOVER.
- **Equation** (macro): `WS(SESSION | layout=nav/disc/editor) -> SESSION'`

Reset macro:
1. `nv "*" @p` → fd|fzf→cd
2. `dc "symbol" @p` → rg|fzf
3. `ws "app"` → reattach session

---

## 3. Day 2 — Navigator + Editor Integration

### 3.1 AM — Yazi + fd/rg/z

#### K. FM: explore tree with Yazi
**Equation**: `FM(DIR/FILE | root=@p) -> fs_tree'`

**$argv**: `fm @p`

**Pipeline**:
```
cd @p && ya
```

#### L. DISCOVER+FM: `fd + fzf + hx`
**Equation**: `DISCOVER(FILE | ext=py, root=@p) -> FILE'`

**$argv**: `dc "*.py" @p !py`

**Pipeline**:
```
file=$(fd -e py . @p | fzf)
[ -n "$file" ] && hx "$file"
```

#### M. DISCOVER: `rg` → pick → open at line
**Equation**: `DISCOVER(CONTENT | pattern, root=@p) -> CONTENT'`

**$argv**: `dc "pattern" @p`

**Pipeline**:
```
hit=$(rg -n "pattern" @p | fzf)
file=${hit%%:*}
line=${hit#*:}; line=${line%%:*}
[ -n "$file" ] && hx "$file" +"$line"
```

#### N. NAV in Yazi shell via z
**Equation**: `NAV(PATH | name≈"repo", frecency>τ) -> cwd'`

**$argv**: `nv "repo" @. +z`

**Pipeline**:
```
# inside ya '!' shell
z repo
```

---

### 3.2 PM — Helix + fd/rg/fzf

#### O. DISCOVER: open all matching files
**Equation**: `DISCOVER(FILE | content≈pattern, root=@p) -> FILE_SET'`

**$argv**: `dc "pattern" @p +m`

**Pipeline**:
```
hx $(rg -l "pattern" @p)
```

#### P. NAV+DISCOVER: choose file by name
**Equation**: `NAV(FILE | name≈pattern, root=@p) -> FILE'`

**$argv**: `nv "*" @p`

**Pipeline**:
```
file=$(fd . @p | fzf)
[ -n "$file" ] && hx "$file"
```

#### Q. DISCOVER: jump to function definition
**Equation**: `DISCOVER(CONTENT | pattern="def foo", root=@p) -> CONTENT'`

**$argv**: `dc "def foo" @p`

**Pipeline**:
```
hit=$(rg -n 'def foo' @p | fzf)
file=${hit%%:*}
line=${hit#*:}; line=${line%%:*}
hx "$file" +"$line"
```

#### R. DF inside Helix: `:run fd | fzf`
**Equation**: `DF(FILE | root=@p) -> FILE'`

**$argv**: `df "*" @p`

**Pipeline (inside hx)**:
```
:run fd . @p | fzf
```

---

## 4. Day 2 Night — Full 4-Pane Pipeline Simulation

**Equation**: `WS(SESSION | layout={NAV, DISCOVER, REPL, EDITOR}, root=@p) -> SESSION'`

**$argv**: `ws "app" @p +layout=nav/disc/repl/edit`

Pane drill mapping:
- Pane 1 → NAV/DISCOVER (A–F)
- Pane 2 → FM/DISCOVER via Yazi (K–N)
- Pane 3 → REPL tasks
- Pane 4 → Helix DISCOVER/REF (O–R)

Drill cycle:
1. State natural goal.
2. Write TWO equation.
3. Fill `$argv`.
4. Run manual pipeline.

---

This file aligns the entire 2-day bootcamp with a minimal working iteration of TWO + `$argv` schema.

