# Terminal Ontology Bootcamp — Full Edition

This document describes the **Terminal Workflow Ontology (TWO)** and integrates it into a **2-day bootcamp** to build muscle memory for search-first, ontology-driven CLI workflows.

Goal:  
Before writing any wrappers or functions, you should be able to:

- Classify any task as `TASK := OP(WHAT | CONTEXT) -> RESULT`
- Choose the correct toolchain based purely on WHAT + OP
- Apply this mentally in under a few seconds

Only after this becomes automatic do you move on to implementation.

---

## 1. Ontology Overview

### 1.1 Entities (WHAT)

The universe of terminal work is reduced to **seven atomic entities**:

- **PATH** – filesystem locations
- **DIR** – directories containing entries
- **FILE** – files with metadata
- **CONTENT** – text/data stored in files
- **CODESTRUCT** – functions, classes, symbols, AST nodes
- **PROCESS** – running programs
- **SESSION** – workspaces (e.g. Zellij sessions)

You always start by asking: **“What am I acting on?”**

---

### 1.2 Operations (OP)

Operations describe what you are doing to those entities:

- **NAV** — navigation (locate and jump to PATH/DIR)
- **DISCOVER** — find information in CONTENT
- **FM** — file management (create/move/rename/delete FILE/DIR)
- **REF** — refactor/transform CODESTRUCT
- **DF** — data filtering/triage of streams (CONTENT/PROCESS lists)
- **AUDIT** — disk usage and cleanup (DIR/FILE by size/age)
- **WS** — workspace management (SESSION creation/switching)

Canonical mapping:

- PATH/DIR → NAV  
- CONTENT → DISCOVER  
- FILE/DIR → FM  
- CODESTRUCT → REF  
- CONTENT/PROCESS → DF  
- DIR/FILE → AUDIT  
- SESSION → WS  

---

### 1.3 Tools and Primary Roles

Each tool is assigned a **primary OP + WHAT** role:

- `fd` — NAV/FM over PATH, DIR, FILE (candidate generator)
- `rg` — DISCOVER/REF over CONTENT (search engine)
- `fzf` — DF over generic streams (interactive selector)
- `z` — NAV over PATH, DIR (jump primitive)
- `bat` — DISCOVER/DF over CONTENT (preview)
- `eza` — NAV/FM/AUDIT over DIR, FILE (structural listing)
- `yazi` — FM/DISCOVER over DIR, FILE, CONTENT (interactive explorer)
- `zellij` — WS over SESSION (workspace manager)
- `ast-grep` — REF/DISCOVER over CODESTRUCT (structural search)
- `dust` — AUDIT over DIR, FILE (disk usage overview)
- `ncdu` — AUDIT/FM over DIR, FILE (disk usage TUI)

Rule of thumb:

- NAV → `fd`, `z`, `eza`  
- DISCOVER/REF (CONTENT) → `rg`, `bat`, `ast-grep`  
- FM → `yazi`, `eza`, `fd + fzf + xargs`  
- DF → `fzf` (+ `bat` for preview)  
- WS → `zellij`  
- AUDIT → `dust`, `ncdu`  

---

## 2. Canonical Task Formula

Every task is expressed as:

```text
TASK := OP(WHAT | CONTEXT) -> RESULT
```

Where:

- **WHAT** – one of the 7 entities
- **OP** – one of the 7 operation families
- **CONTEXT** – scope/filters (roots, language, depth, size, flags)
- **RESULT** – transformed entity or state (e.g. FILE opened, PATH jumped to, REPORT produced)

Example:

- `DISCOVER(CONTENT | pattern="login", root=~/dev/project) -> FILE`
- `NAV(PATH | name≈"kitty", root=~/.config) -> PATH_TARGET`
- `AUDIT(DIR | root=/home, metric=size) -> REPORT`

---

## 3. Toolchain Shapes

The ontology maps OP → standard toolchain shapes:

| OP        | Toolchain Shape                          |
|-----------|-------------------------------------------|
| NAV       | `fd` → `fzf` → `cd` / `z`                 |
| DISCOVER  | `rg` → `fzf` → `bat/hx`                   |
| FM        | `eza` / `yazi` → act (`mv`, `rm`, etc.)   |
| REF       | `rg` → `ast-grep` / `comby` → `hx`        |
| DF        | `cmd | fzf --preview 'bat {}'`            |
| AUDIT     | `dust` / `ncdu`                           |
| WS        | `zellij attach -c NAME`                   |

These shapes are **fixed** and are meant to become reflexive.

---

## 4. Cognitive Loop (Operating Model)

For every task, run this mental loop:

### Step 1 — Identify WHAT

Ask:

> “What am I acting on?”

Choose one: PATH, DIR, FILE, CONTENT, CODESTRUCT, PROCESS, SESSION.

---

### Step 2 — Identify OP

Ask:

> “Given this entity, what is the operation?”

Pick one of: NAV, DISCOVER, FM, REF, DF, AUDIT, WS.

Use the canonical mapping (e.g. PATH/DIR → NAV, CONTENT → DISCOVER).

---

### Step 3 — OP determines the toolchain

Do not improvise.

Use the standard toolchain shape associated with that OP:

- NAV → fd+fzf+cd/z
- DISCOVER → rg+fzf+bat/hx
- FM → eza/yazi
- REF → rg+ast-grep/comby+hx
- DF → fzf (+ bat)
- AUDIT → dust/ncdu
- WS → zellij

---

### Step 4 — Choose CONTEXT

Only now do you fill in “where, how, how deep”:

- roots (`@p` project, `@n` notes, `@c` config, `@.` current dir)
- language (`!py`, `!ts`, `!rs`, `!sh`, …)
- depth (`+d3`)
- flags (`+g` git root, `+C` case-sensitive)

These tokens can later feed into a mini-DSL for wrappers like `nv` (NAV) and `dc` (DISCOVER).

---

## 5. 2-Day Bootcamp Plan

The bootcamp is **purely cognitive**; no implementation is required.

### Day 1 — Conceptual Reps

Objective:  
Map natural-language tasks to `WHAT → OP → toolchain` and (optionally) DSL tokens.

For each scenario:

1. Identify WHAT  
2. Identify OP  
3. Pick toolchain shape  
4. Sketch DSL form (optional)

Example 1:

> “Find where ‘token’ is used in my project.”

- WHAT = CONTENT  
- OP = DISCOVER  
- Toolchain = `rg | fzf | bat`  
- DSL idea = `dc "token" @p !py`

Example 2:

> “Jump to my terminal config.”

- WHAT = PATH/DIR  
- OP = NAV  
- Toolchain = `fd → fzf → cd`  
- DSL idea = `nv kitty @c #f`

Example 3:

> “See which folders are taking space in my home directory.”

- WHAT = DIR/FILE  
- OP = AUDIT  
- Toolchain = `dust` / `ncdu`  
- DSL idea = `au @.` (future)

Perform 10–15 such mappings.  
Say them out loud, or write them in a small log.

---

### Day 2 — Applied Dry Runs (Ghost Execution)

Objective:  
Simulate commands mentally or on paper without relying on implementation.

For each scenario:

1. Run the same WHAT → OP → toolchain classification.
2. Write the **command shape** you would run.
3. Optionally type it, but do not depend on feedback to validate the mapping.

Example 1:

> “Inspect all uses of `do_login()` and plan a refactor.”

- WHAT = CODESTRUCT  
- OP = REF  
- Toolchain = `rg → ast-grep/comby → hx`  
- Command shape (conceptual):  
  - `rg "do_login(" @p`  
  - `ast-grep 'do_login($ARGS)' --lang py`  
  - `comby 'do_login(:[x])' 'perform_login(:[x])' .`  
- DSL idea: `rf "do_login" !py @p`

Example 2:

> “Filter my running processes and inspect one.”

- WHAT = PROCESS  
- OP = DF  
- Toolchain = `ps aux | fzf | bat` (or just `ps aux | fzf`)  
- DSL idea: `pf` (process filter)

Example 3:

> “Quickly check project structure and jump into `src`.”

- WHAT = DIR  
- OP = NAV/FM  
- Toolchain = `fd` + `fzf` + `cd` plus `eza` on arrival  
- Command shape:  
  - `fd src @p | fzf | cd`  
  - `eza -l --git`

Perform another 10–15 dry runs.

---

## 6. Completion Criteria (Green Light for Implementation)

You are ready to implement funclines and DSL wrappers when:

- You can, from memory, list the 7 entities and 7 operations.
- Given any task description, you can immediately state:
  - WHAT
  - OP
  - Toolchain shape
- You rarely hesitate about which tool to use for:
  - navigation vs discovery vs refactor vs audit
- You can invent a plausible DSL expression in one or two tokens:
  - roots (`@p`, `@n`, `@c`, `@.`)
  - language (`!py`, `!ts`, `!rs`, …)
  - flags (`+g`, `+d3`, `+C`)

At that point, you can safely start:

- Implementing `nv` (NAV wrapper) and `dc` (DISCOVER wrapper).
- Designing keyboard layers aligned with the 7 OP families.
- Building a minimal funcline library on top of the ontology.

The mental model comes first; implementation is simply encoding it.
