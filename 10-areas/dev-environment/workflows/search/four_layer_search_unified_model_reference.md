# Unified 4-Layer Search Model – Full Reference

A complete conceptual map for filesystem, text, structural, and semantic search, plus the interactive selection layer.

Layers:
- **Layer 1** – File-Level Search ("Where are things?")
- **Layer 2** – Text-Level Search ("Search raw text")
- **Layer 3** – Structural/Syntax-Level Search ("Find real code shapes")
- **Layer 4** – Semantic/Meaning-Level Search ("What does this symbol mean?")
- **Layer 5** – Selection/UI Layer ("Pick the exact thing I want")

---

## Layer 1 — File-Level Search (Where are things?)

**Purpose:** Work with *files and directories*, not content.

**Core tools:**
- `fd` – fast file and directory finder
- `zoxide` – smart directory jumper
- `eza` – modern `ls` replacement with rich metadata

**Typical questions:**
- "Which files exist here?"
- "Where are all `.rs` or `.cpp` files?"
- "What are the project roots?"

**Common patterns:**
- `fd -e rs` – all Rust source files
- `fd config` – find files/dirs whose name matches `config`
- `zoxide query --interactive` – jump to a recent project directory

**Notes:**
- No understanding of file content
- Fastest way to define the search scope for higher layers

---

## Layer 2 — Text-Level Search (Search raw text now)

**Purpose:** Search and transform *raw text* using patterns and regular expressions.

**Core tools:**
- `rg` (ripgrep) – fast recursive text search
- `grep` – classic line-based search
- `sed` / `sd` – stream editors for replacements
- `awk`, `mlr` – structured text/log processing
- `xsv` – CSV/TSV utilities

**Typical questions:**
- "Where does this string appear?"
- "Search logs for ERROR entries."
- "Replace `foo` with `bar` in these files."

**Common patterns:**
- `rg "pattern"` – fast search for pattern
- `rg -n "pattern"` – show file:line:match
- `sed 's/foo/bar/g' file` – in-place stream transform
- `awk '{print $2}' file.log` – extract field

**Notes:**
- Sees bytes/lines only (no parse tree)
- Good for strings, logs, and simple code/text matches
- Can overmatch or undermatch when semantics matter

---

## Layer 3 — Structural/Syntax-Level Search (Find the real code shape)

**Purpose:** Understand *grammar and structure* using AST or structured parsing.

**Core tools:**
- `ast-grep` – tree-sitter-based AST search and rewrite
- `semgrep` – language-aware pattern search for many languages
- `comby` – structural search/replace without full AST
- `difftastic` – syntax-aware diff tool
- `jq`, `yq`, `dasel` – JSON/YAML/TOML query tools

**Typical questions:**
- "Find all calls to this function."
- "Find all functions missing a return type."
- "Which structs have this field?"
- "Which configs have this key set to a given value?"

**Common patterns:**
- `ast-grep -p 'process_data($ARGS)'` – match call expressions
- `semgrep -e 'if ($X) {$Y}' --lang=js` – match JS if-statements
- `comby 'foo(:[x])' 'bar(:[x])' .` – structural replacement
- `jq '.items[].name' data.json` – extract field from JSON

**Notes:**
- Operates over parse trees or structural patterns
- Much more precise than text search
- Excellent for refactors and policy enforcement

---

## Layer 4 — Semantic/Meaning-Level Search (What does this symbol mean?)

**Purpose:** Ask the language server or compiler about the *meaning* of symbols: definitions, types, references, and diagnostics.

**Core tools (via LSP):**
- Rust Analyzer, Clangd, Pyright, Gopls, tsserver, Zig LSP, etc.
- Editor integrations: Helix `g d`, `g r`, `:lsp-rename`, code actions

**Typical questions:**
- "Where is this function defined?"
- "What type does this variable have?"
- "Where is this symbol referenced?"
- "Can I safely rename this symbol?"

**Common patterns (Helix-style):**
- `g d` – go to definition
- `g r` – find references
- `:lsp-rename` – rename symbol across project
- Jump through diagnostics and apply code actions

**Notes:**
- Deepest layer of correctness
- Requires a running language server
- Knows types, scopes, imports, and the build environment

---

## Layer 5 — Selection / UI Layer (Pick the exact thing I want)

**Purpose:** Interactively filter and choose from large sets of results from other layers.

**Core tools:**
- `fzf` – general-purpose fuzzy finder
- `skim` – `fzf`-like alternative
- `yazi` – TUI file manager with preview

**Typical uses:**
- Choose a file from `fd` output
- Choose a match from `rg` or `ast-grep` results
- Use previews to inspect before opening or editing

**Common patterns:**
- `fd -e rs | fzf | xargs hx`
- `rg -n pattern | fzf | cut -d: -f1,2 | xargs hx`
- `ast-grep pattern | fzf`

**Notes:**
- Provides the human-in-the-loop layer
- Not a search engine itself, but a selector for search results

---

## How the Layers Interact

### Recommended mental model:

- **Layer 1 (fd)**: Define the universe of files.
- **Layer 2 (rg)**: Search for raw textual patterns.
- **Layer 3 (ast-grep / semgrep / jq/yq)**: Match and manipulate structured content.
- **Layer 4 (LSP)**: Work with symbol meaning, types, and semantic correctness.
- **Layer 5 (fzf / yazi)**: Interactively refine and select from results at any layer.

### Typical workflows:
- `fd → fzf → editor` – navigate files
- `rg → fzf → editor` – jump to text matches
- `ast-grep → fzf → editor` – jump to structural matches
- LSP definitions/references → optionally filter with `fzf` if exported

---

## Extended Tool Classification

### More Layer 1 (Filesystem-Level)
- `ripgrep-all` – search many file types
- `tokei` – count lines of code per language

### More Layer 2 (Text-Level)
- `sd` – ergonomic replacement for `sed`
- `mlr` (Miller) – awk for structured logs
- `xsv` – CSV slicing and queries

### More Layer 3 (Structural)
- `cst-grep` – concrete syntax tree grep
- `pglast` – parse SQL AST (library-level)
- `fx`, `jless` – interactive JSON viewers

### More Layer 4 (Semantic)
- Language-specific LSP tools (Rust Analyzer, Clangd, etc.)
- Linting and formatting frameworks that leverage LSP

### More Layer 5 (Selection/UI)
- `gitui`, `lazygit` – domain-specific selectors for Git
- `yazi` – file + preview interface

---

## Unified Purpose Table

| Purpose                              | Best tools                                | Layer |
|--------------------------------------|-------------------------------------------|-------|
| Find files                           | fd, zoxide                               | 1     |
| Jump to project dirs                 | zoxide                                   | 1     |
| Raw text/regex search                | ripgrep (rg)                             | 2     |
| In-place text edits                  | sed, sd                                  | 2     |
| Structured text/log processing       | awk, mlr, xsv                            | 2     |
| Syntax-aware code search             | ast-grep, semgrep                        | 3     |
| Structural rewrites                  | ast-grep, comby                          | 3     |
| JSON/YAML/TOML queries               | jq, yq, dasel                            | 3     |
| Syntax-aware diffing                 | difftastic                               | 3     |
| Symbol meaning/definition            | LSP (rust-analyzer, clangd, etc.)        | 4     |
| Find references                      | LSP + ast-grep cross-check               | 4     |
| Safe refactors/renames               | LSP code actions                         | 4     |
| Interactive fuzzy selection          | fzf, skim, yazi                          | 5     |

---

## Guiding Principles

1. **Use the lowest layer that solves the problem correctly.**  
   Start with files (fd), then text (rg), then structure (ast-grep), then semantics (LSP) only if needed.

2. **Combine layers for power.**  
   Example: `fd` to scope, `rg` to search, `fzf` to choose, editor to act.

3. **Let LSP own meaning; let structural tools own pattern detection.**  
   LSPs know types and references; ast-grep/semgrep know shapes and styles.

4. **fzf is the universal selector.**  
   It sits above all layers as the interactive narrowing interface.

---

This document is intended as a stable conceptual reference for how search and analysis tools fit together in a modern CLI- and editor-centric workflow.

