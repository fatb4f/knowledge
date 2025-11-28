# Unified 4-Layer Search Decision Tree

A fast, structured guide answering **“Which search tool should I use right now?”**

---

## **Start Here: What are you looking for?**

### **1. I need to find files or directories.**
→ **Use Layer 1 (File-Level Search)**

**Tools:** `fd`, `zoxide`, `eza`

Ask yourself:
- Do I know the filename or extension? → `fd -e rs` or `fd name`
- Do I want to jump to a project quickly? → `zoxide query --interactive`

---

### **2. I need to search text inside files.**
→ **Use Layer 2 (Text-Level Search)**

**Tools:** `rg`, `sed`, `sd`, `awk`, `xsv`, `mlr`

Questions:
- Do I need regex or fuzzy text search? → `rg pattern`
- Do I need to edit text inline? → `sed`, `sd`
- Is this structured logs/CSV? → `awk`, `mlr`, `xsv`

---

### **3. I need to search for real code structures.**
→ **Use Layer 3 (Structural / Syntax-Level)**

**Tools:** `ast-grep`, `semgrep`, `comby`

Ask:
- Do I want exact AST-level matches? → `ast-grep`
- Multi-language structural patterns? → `semgrep`
- Find/replace on structures without AST grammar? → `comby`

Examples:
- "Find all calls to X"
- "Find all functions missing Y"
- "List all async functions"

---

### **4. I need to know what a symbol *means* (semantic).**
→ **Use Layer 4 (Semantic / Meaning-Level)**

**Tools:** LSPs (Rust Analyzer, Clangd, Pyright, tsserver)

Ask:
- Do I need the actual definition? → `g d`
- All references? → `g r`
- Safe rename? → `:lsp-rename`
- Diagnostics and code actions? → LSP commands

Use this layer when correctness matters.

---

### **5. I see many results and must choose one interactively.**
→ **Use Layer 5 (Selection/UI-Level)**

**Tools:** `fzf`, `skim`, `yazi`

Use after any other layer:
- `fd | fzf`
- `rg -n pattern | fzf`
- `ast-grep pattern | fzf`

Add previews:
- `fzf --preview 'bat --style=numbers {}'`

---

## **Decision Tree Diagram (Linear Version)**

1. **Do you know the filename/path?**
   - Yes → `fd`
   - No → 2
2. **Are you searching raw text?**
   - Yes → `rg`
   - No → 3
3. **Are you searching for code *shape* (AST)?**
   - Yes → `ast-grep` / `semgrep`
   - No → 4
4. **Do you need type/definition/reference meaning?**
   - Yes → LSP actions
   - No → 5
5. **Do you need to pick from many results?**
   - Yes → pipe results into `fzf`

---

## **When Multiple Tools Apply**

### **rg vs ast-grep**
Use **rg** for raw matches, **ast-grep** for structural intent.

### **ast-grep vs LSP**
Use **LSP** for definition/reference accuracy.
Use **ast-grep** for *global pattern detection* (e.g. deprecated API calls, stylistic patterns).

### **fzf anywhere**
Use `fzf` whenever:
- There are too many results
- You want previews
- You want interactive narrowing

---

## **Guiding Principle**
> Use the **lowest layer** that solves the problem correctly.

This minimizes complexity and maximizes performance.

---