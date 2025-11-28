# Four-Layer Search Workflows Cookbook

A set of practical, repeatable recipes that combine:

- **Layer 1**: `fd`, `zoxide`
- **Layer 2**: `rg`, `sed`, `awk`, `sd`, `xsv`, `mlr`
- **Layer 3**: `ast-grep`, `semgrep`, `jq`, `yq`, `comby`, `difftastic`
- **Layer 4**: LSP (Rust Analyzer, Clangd, etc.)
- **Layer 5**: `fzf`, `yazi`

---

## Recipe 1 — Fuzzy File Open (fd → fzf → hx)

**Goal:** Quickly open any project file in Helix.

```bash
fd -e rs -e toml | fzf | xargs hx
```

- `fd` lists candidate files
- `fzf` lets you select
- `hx` opens the chosen file

Variations:
- Add preview: `fd | fzf --preview 'bat --style=numbers --color=always {}' | xargs hx`

---

## Recipe 2 — Text Search and Jump (rg → fzf → hx)

**Goal:** Search a pattern and jump to the exact match.

```bash
rg -n "pattern" | fzf | cut -d: -f1,2 | xargs -r hx
```

- `rg -n` prints `file:line:match`
- `fzf` filters results interactively
- `cut` keeps only `file:line`
- `hx` opens file at line

---

## Recipe 3 — Structural Code Search (ast-grep → fzf → hx)

**Goal:** Find real code shapes, not just text.

Example: find all calls to `process_data` in Rust.

```bash
ast-grep -p 'process_data($ARGS)' --json \
  | jq -r '.[] | "\(.range.file):\(.range.start.line)"' \
  | fzf \
  | xargs -r hx
```

- `ast-grep` finds call expressions
- `jq` extracts `file:line`
- `fzf` filters
- `hx` jumps to code

---

## Recipe 4 — Jump to Project Root and Open (zoxide → fd → fzf → hx)

**Goal:** Teleport to project and open a file in one flow.

```bash
zoxide query --interactive | while read proj; \
  fd -e rs . "$proj" | fzf | xargs hx
```

- `zoxide` picks project
- `fd` lists files in that project
- `fzf` chooses one
- `hx` opens it

---

## Recipe 5 — JSON Query and Inspect (jq → fzf → bat)

**Goal:** Explore JSON interactively.

```bash
jq -r '.items[].name' data.json | fzf --preview 'jq ".items[] | select(.name == \"{}\")" data.json'
```

- `jq` lists names
- `fzf` selects
- Preview window shows full JSON object for chosen name

---

## Recipe 6 — YAML/Config Pattern Search (yq → rg → fzf)

**Goal:** Find all configs where a given key has a specific value.

```bash
yq '.service.name' **/*.yaml | rg 'api-gateway' | fzf
```

- `yq` prints service names
- `rg` filters by value
- `fzf` refines selection

---

## Recipe 7 — CSV/Log Filtering (xsv/mlr → fzf)

**Goal:** Filter heavy CSV logs.

```bash
xsv select timestamp,level,message logs.csv | fzf
```

Or with Miller:

```bash
mlr --icsv --opprint filter '$level == "ERROR"' logs.csv | fzf
```

---

## Recipe 8 — Structural Rewrite (comby)

**Goal:** Simple structural refactor without full AST.

Example: Replace `foo(x)` with `bar(x)` everywhere.

```bash
comby 'foo(:[x])' 'bar(:[x])' . -extensions rs,ts,js
```

- `:[x]` is a hole; comby keeps its content

---

## Recipe 9 — Semantic Refactor (LSP Rename)

**Goal:** Safely rename a function and all call sites.

**In Helix:**
1. Place cursor on symbol
2. Run `:lsp-rename new_name`
3. Check diagnostics
4. Optionally cross-check with `rg old_name`

---

## Recipe 10 — Syntax-Aware Diff (difftastic)

**Goal:** Compare two versions of a file by structure.

```bash
difftastic old.rs new.rs
```

Use instead of `diff` when structure matters more than lines.

---

## Recipe 11 — Terminal File Explorer as Selector (yazi → hx)

**Goal:** Use Yazi as rich UI, Helix as editor.

Within Yazi, bind a key (e.g., `e`) to:

```bash
hx "$YA_CUR_FILE"
```

Now Yazi = Layer 1+5, Helix = edit target.

---

## Recipe 12 — Unified Search Function (Concept)

**Goal:** Create one shell function that chooses strategy based on mode.

Pseudo-Fish idea:

```fish
function search
    set mode $argv[1]
    set pattern $argv[2]

    switch $mode
        case file
            fd $pattern | fzf | xargs hx
        case text
            rg -n $pattern | fzf | cut -d: -f1,2 | xargs hx
        case ast
            ast-grep -p $pattern --json | jq -r '.[] | "\(.range.file):\(.range.start.line)"' | fzf | xargs hx
    end
end
```

This wraps the 4-layer model into one entrypoint.

---

## Recipe 13 — Grep → Narrow → Rewrite (rg → fzf → sed/sd)

**Goal:** Carefully rewrite matching lines.

1. View matches:

```bash
rg -n "pattern" | fzf
```

2. Once confirmed, apply rewrite:

```bash
rg -l "pattern" | xargs sd 'old' 'new'
```

- Use `rg -n` + `fzf` as a preview step before global edits.

---

## Recipe 14 — Cross-check LSP References with ast-grep

**Goal:** Validate that all call sites are handled in a refactor.

1. Use LSP "find references" in editor and fix them.
2. Then run:

```bash
ast-grep -p 'oldName($ARGS)' src/
```

If nothing is returned, refactor is likely complete.

---

## Recipe 15 — Querying Diagnostics via LSP and Filtering

Conceptual pattern (editor-driven):

1. List diagnostics in editor
2. Pipe diagnostics (if exportable) through `fzf` for quick jump

When combined with CLI LSP clients, diagnostics can be exported to JSON and filtered the same way as any search result.

---

This cookbook is intended to grow with new patterns as your workflow evolves.

