# 2-Day Bootcamp (fd / rg / z / fzf Edition)

High-intensity, two-day bootcamp to establish mastery across Kitty → Fish → Zellij → Yazi → Helix, using fd, rg, zoxide, and fzf as the unified navigation engine.

---

# DAY 1 — Shell & Multiplexer Core

## AM BLOCK — Fish vi-mode + fd/rg/z/fzf
### Concepts
- fd: fast file finder
- rg: fast text/code search
- fzf: fuzzy selector
- zoxide: directory jump engine

### Drills
- fd: `fd`, `fd py`, `fd -t d src`
- rg: `rg TODO`, `rg -n term`, `rg --glob '*.py' 'def '`
- fzf: `fzf`, `fd | fzf`, `rg -n pattern | fzf`
- zoxide: `z project`, `z src`, `z -`, `zoxide query -l | fzf`

### Integration
- Jump dirs with z
- Find files via fd|fzf → open with hx
- Code search via rg → fzf → hx
- Return via z -

---

## PM BLOCK — Zellij Modes + Search Integration
### Drills
- Pane grid: `Alt-p → h/j/k/l`
- Pane focus: `Alt-h/j/k/l`
- Resize: `Alt-r → h/j/k/l`
- Tabs: `Alt-t n`, `Alt-1..9`, `Alt-t x`

### Workflows
- Pane 1: `fd | fzf`
- Pane 2: `rg -n term | fzf`
- Pane 3: zoxide navigation
- Pane 4: Editor (autolocked)

---

## NIGHT BLOCK — Autolock + Panic-Proof Drills
### Drills
- Open hx → confirm lock
- `Alt-z` unlock → move focus
- `Alt-Shift-z` re-lock
- Emergency reset: `Esc` → run fd/rg/z/fzf

---

# DAY 2 — Navigator + Editor Integration

## AM BLOCK — Yazi + fd/rg/z/fzf
### Drills
- Navigate: `j/k/h/l`
- Edit: `e`
- Open shell: `!`

### Workflows
- fd + Yazi + Helix: `hx (fd py | fzf)`
- rg + Yazi + Helix: `hx (rg -n pattern | fzf | cut -d: -f1)`
- zoxide inside Yazi: `!` → `z repo`

---

## PM BLOCK — Helix + fd/rg/fzf Integration
### Core motions
- Movement: `w/b/e`, `0/^/$`
- Selections: `s i w`, `s a w`, `s i (`
- Edits: `d`, `c`, `y`, `p`
- Search: `/`, `n/N`

### Workflows
- `hx $(rg -l pattern)`
- `hx (fd | fzf)`
- `rg -n 'def foo' | fzf` → open in hx
- `:run fd | fzf`

---

## NIGHT BLOCK — Full Pipeline Simulation
### Task
1. Kitty → Zellij
2. Pane1: fd/rg/z/fzf
3. Pane2: Yazi
4. Pane3: REPL
5. Pane4: Helix
6. Use unified motions + autolock
7. Search-first navigation everywhere

### Success Criteria
- No mode confusion
- No cd-walking
- Fluid movement across all tools

---

# Outcome
- Search-first, frictionless navigation
- Predictable modal control
- Fully integrated environment ready for the Python then Rust roadmaps

