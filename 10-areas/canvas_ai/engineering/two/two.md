# TWO.core — PipelineSpec + Intent→Pipeline Variants

## Goal
Define (1) a minimal, canonical **PipelineSpec** format (graph-first, string-later) and (2) show how a single **intent phrase** maps to multiple concrete pipeline variants across `fd`/`rg`/`fzf`/`bat`/`sd`.

---

## 1) Minimal Canonical PipelineSpec

### 1.1 Principles
- **Graph-first**: represent pipelines as a sequence of stages with typed edges (pipes / xargs / direct args).
- **Deterministic**: schema → adapter → PipelineSpec is reproducible.
- **Inspectable**: can render to a shell pipeline string, but the string is not the source of truth.
- **Testable**: PipelineSpec is stable for snapshots and golden tests.

### 1.2 Core Types (minimal)

#### Request (input to orchestrator)
```json
{
  "intent": "find TODOs in rust files under src, include hidden, preview, open selection in hx",
  "context": {
    "cwd": "/home/baf/src/repo",
    "project_root": "/home/baf/src/repo",
    "tty": true
  },
  "schema": {
    "search": {
      "pattern": "TODO",
      "mode": "content",
      "globs": ["*.rs"],
      "type": "file"
    },
    "scope": {"path": "src"},
    "visibility": {"hidden": true, "respect_vcs_ignore": true},
    "view": {"preview": "syntax"},
    "action": {"open": {"cmd": "hx"}}
  }
}
```

#### PipelineSpec (output of planner)
```json
{
  "version": 1,
  "stages": [
    {
      "id": "discover",
      "tool": "fd",
      "argv": ["-t","f","-H","--glob","*.rs",".","src"],
      "emits": {"kind": "paths", "format": "lines"}
    },
    {
      "id": "search",
      "tool": "rg",
      "argv": ["--with-filename","--line-number","--color","always","TODO"],
      "reads": {"from": "discover", "kind": "paths"},
      "emits": {"kind": "matches", "format": "lines"}
    },
    {
      "id": "select",
      "tool": "fzf",
      "argv": ["--ansi","--preview","bat --color=always {1}","--delimiter",":","--with-nth","1.."],
      "reads": {"from": "search", "kind": "matches"},
      "emits": {"kind": "selection", "format": "lines"}
    },
    {
      "id": "act",
      "tool": "hx",
      "argv": [],
      "reads": {"from": "select", "kind": "selection"},
      "edge": {"kind": "xargs", "template": ["hx","{path}"]}
    }
  ],
  "render": {
    "shell": "bash",
    "safe_quoting": true
  }
}
```

### 1.3 Edge Model (minimal)
Each stage can declare how it consumes prior output:

- **pipe**: stdout → stdin (text stream)
- **xargs**: lines → repeated argv invocations
- **args**: structured output → injected argv (rare, but useful)

Minimal enum:
```json
{"edge_kind": "pipe|xargs|args"}
```

### 1.4 Rendering: PipelineSpec → shell string
Renderer rules:
- `pipe`: `cmd1 | cmd2`
- `xargs`: `... | xargs -I{} hx {}` (or `xargs hx` depending on template)
- `safe_quoting`: always quote args containing spaces or shell metas

Example rendered (one possible output):
```sh
fd -t f -H --glob '*.rs' . src \
| rg --with-filename --line-number --color always 'TODO' \
| fzf --ansi --delimiter ':' --with-nth '1..' --preview "bat --color=always {1}" \
| sed -E 's/:.*$//' \
| xargs -I{} hx {}
```

Notes:
- `fzf` selection often includes `file:line:col`, so an additional wrangle stage (e.g., `sd`/`sed`) may be inserted to extract `{path}`.

### 1.5 Minimal, Practical Subset (stage fields)
If you want ultra-minimal, keep only:
```json
{
  "stages": [
    {"tool":"fd","argv":[...]},
    {"tool":"rg","argv":[...],"edge":"pipe"},
    {"tool":"fzf","argv":[...],"edge":"pipe"},
    {"tool":"xargs","argv":["hx"],"edge":"pipe"}
  ]
}
```

---

## 2) Single Intent → Multiple Pipeline Variants

### Intent (canonical)
> “Find TODOs in Rust files under `src`, include hidden files, show previews, open the selected file in Helix.”

Below are **variants** that satisfy the same intent using different tool responsibilities.

---

### Variant A — `rg` as primary (fastest for content search)
Best when you only care about matches and don’t need pre-discovery.

```sh
rg --hidden --glob '*.rs' --with-filename --line-number --color always 'TODO' src \
| fzf --ansi --delimiter ':' --preview "bat --color=always {1}" \
| sed -E 's/:.*$//' \
| xargs -I{} hx {}
```

Why:
- `rg` can traverse + filter by glob; `fd` is unnecessary.

---

### Variant B — `fd` discovery then `rg` (better control over file set)
Best when you want fine-grained file filtering (types, excludes) before searching.

```sh
fd -t f -H --glob '*.rs' . src \
| xargs -0 -I{} rg --with-filename --line-number --color always 'TODO' {} \
| fzf --ansi --delimiter ':' --preview "bat --color=always {1}" \
| sed -E 's/:.*$//' \
| xargs -I{} hx {}
```

Why:
- Lets `fd` define the file universe; `rg` runs on explicit paths.

---

### Variant C — `fd` + `fzf` first (interactive selection before searching)
Best when you want to pick a subset of files before searching content.

```sh
fd -t f -H --glob '*.rs' . src \
| fzf --preview "bat --color=always {}" \
| xargs -I{} rg --with-filename --line-number --color always 'TODO' {} \
| fzf --ansi --delimiter ':' --preview "bat --color=always {1}" \
| sed -E 's/:.*$//' \
| xargs -I{} hx {}
```

Why:
- Two-phase interact: file pick → match pick.

---

### Variant D — Replace action: “Replace TODO → DONE in Rust files under src”
Same discovery/search shape, different action.

```sh
rg --hidden --glob '*.rs' -l 'TODO' src \
| xargs -I{} sd 'TODO' 'DONE' {}
```

Why:
- `rg -l` produces file list; `sd` performs the transformation.

---

## 3) What TWO extracts as recurring high-fidelity patterns
Across variants, the recurring semantic slots are:

- **scope.path**: `src` / `.` / project root
- **visibility.hidden**: `-H`, `--hidden`, `--all`
- **search.pattern**: `'TODO'`
- **search.filter**: `--glob '*.rs'` / `--type` / `-t f`
- **view.preview**: `bat --color=always ...`
- **action.open**: `hx` (or other editor)
- **wrangle.extract_path**: `sed`/`sd` step to turn `file:line:...` into `file`

This set is the backbone of the unified TWO grammar.

---

## 4) Implementation Notes (for TWO.core)
- Keep PipelineSpec **shell-agnostic**; rendering is a backend.
- Prefer a **stage output kind** taxonomy (`paths`, `matches`, `selection`) so adapters can reason about edges.
- Treat “wrangling” helpers (`sd`, `sed`, `cut`, `awk`) as first-class stages.
- Start with 5–10 canonical intents and lock them as golden tests.

---

## 5) Suggested next step
Create a `tools/` adapter table for:
- `rg`, `fd`, `fzf`, `bat`, `sd`

Each adapter implements:
- `Schema → argv` mapping
- input/output `kind`
- required wrangle stages (e.g., extracting file path)

