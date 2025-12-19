# Terminal Ontology Bootcamp — TL;DR

Use this as a **quick-reference intro**.

---

## Core Axiom

> **The WHAT determines the HOW.**  
> Entity → Operation → Toolchain → Context → Action.

---

## 1. The 7 Entities (WHAT)

- **PATH** – where things live
- **DIR** – collections (folders)
- **FILE** – containers (files)
- **CONTENT** – text/data inside files
- **CODESTRUCT** – functions, classes, symbols (AST)
- **PROCESS** – running programs
- **SESSION** – workspaces (Zellij/terminal sessions)

---

## 2. The 7 Operations (OP)

- **NAV** — navigation (get me there)
- **DISCOVER** — find information in content
- **FM** — file management (move/rename/delete)
- **REF** — refactor (change structure safely)
- **DF** — data filtering / triage
- **AUDIT** — disk usage / cleanup
- **WS** — workspace management

Mapping:

- PATH/DIR → NAV  
- CONTENT → DISCOVER  
- FILE/DIR → FM  
- CODESTRUCT → REF  
- CONTENT/PROCESS → DF  
- DIR/FILE → AUDIT  
- SESSION → WS  

---

## 3. The 7 Toolchain Shapes

| OP        | Toolchain Shape                      |
|-----------|---------------------------------------|
| NAV       | `fd` → `fzf` → `cd` / `z`             |
| DISCOVER  | `rg` → `fzf` → `bat/hx`               |
| FM        | `eza` / `yazi` → act (mv/rm/etc.)     |
| REF       | `rg` → `ast-grep` / `comby` → `hx`    |
| DF        | `cmd | fzf --preview 'bat {}'`        |
| AUDIT     | `dust` / `ncdu`                       |
| WS        | `zellij attach -c NAME`               |

Memorize the **mapping**:

- NAV → fd, z, eza  
- DISCOVER/REF (CONTENT) → rg, bat, ast-grep  
- FM → yazi, eza, fd + fzf + xargs  
- DF → fzf (+ bat for preview)  
- WS → zellij  
- AUDIT → dust, ncdu  

---

## 4. Cognitive Loop (Always)

For **every** task:

1. **WHAT** — What am I acting on?  
   (PATH, DIR, FILE, CONTENT, CODESTRUCT, PROCESS, SESSION)
2. **OP** — Given this entity, what is the operation?  
   (NAV, DISCOVER, FM, REF, DF, AUDIT, WS)
3. **Toolchain** — Use the canonical shape for that OP.
4. **CONTEXT** — Only now decide:
   - roots: `@p @n @c @.`
   - language: `!py !ts !rs !sh`
   - flags: `+g +dN +C`

Formula:

```text
TASK := OP(WHAT | CONTEXT) -> RESULT
```

---

## 5. Bootcamp Use

- Day 1:
  - Practice classifying scenarios as WHAT → OP → toolchain.
- Day 2:
  - Ghost-run commands (no execution) using the same mapping.

Once you can do this from memory, you’re ready to implement:

- function pipelines (funclines)
- DSL commands like `nv` / `dc`
- split-kbd layers (one per OP family)
