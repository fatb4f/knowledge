# Unified 4-Layer Search Cheat Sheet

## **Purpose Overview**
- **fd** → File-level search (*Where are things?*)
- **rg** → Text-level search (*Search raw text now*)
- **ast-grep** → Structural search (*Find real code shapes*)
- **LSP** → Meaning-level semantic search (*What does this symbol mean?*)
- **fzf** → Selection layer (*Interactive chooser for all results*)

---

## **Layer 1 — File-Level Search**
### Tools: `fd`, `zoxide`, `eza`

**Use for:**
- Finding files and directories
- Filtering by extension or name
- Project root navigation

**Examples:**
- `fd -e rs`
- `fd config`
- `zoxide query --interactive`

---

## **Layer 2 — Text-Level Search**
### Tools: `rg`, `sed`, `sd`, `awk`, `mlr`, `xsv`

**Use for:**
- Raw text/regex search
- Log processing and slicing
- CSV/TSV filters
- Stream edits

**Examples:**
- `rg "pattern"`
- `sed 's/foo/bar/g' file`
- `awk '{print $2}' file.log`

---

## **Layer 3 — Syntax/Structural Search**
### Tools: `ast-grep`, `semgrep`, `comby`, `difftastic`, `jq`, `yq`, `dasel`

**Use for:**
- Finding code structures, not strings
- Pattern-based refactors
- JSON/YAML/TOML queries
- Syntax-aware diffs

**Examples:**
- `ast-grep -p 'call_expr: (foo $ARGS)'`
- `jq '.items[].name' data.json`
- `comby 'foo(:[x])' 'bar(:[x])' -stdin`

---

## **Layer 4 — Meaning/Semantic Layer**
### Tools: LSPs (Rust Analyzer, Clangd, Pyright, tsserver)

**Use for:**
- Navigate definitions and references
- Accurate renames
- Code actions and diagnostics

**Examples (Helix):**
- `g d` → go to definition
- `g r` → find references
- `:lsp-rename` → rename symbol

---

## **Layer 5 — Selection / UI Layer**
### Tools: `fzf`, `skim`, `yazi`

**Use for:**
- Fuzzy filtering
- Selecting files, matches, commands
- Previewing content interactively

**Examples:**
- `fd -e rs | fzf`
- `rg -n foo | fzf`
- `ast-grep -p pattern | fzf`

---

## **Combined Patterns**
- **fd → fzf → hx**: find and open a file
- **rg → fzf → hx**: search text, jump to match
- **ast-grep → fzf → hx**: navigate structural code patterns
- **LSP → fzf**: filter references or diagnostics

---

