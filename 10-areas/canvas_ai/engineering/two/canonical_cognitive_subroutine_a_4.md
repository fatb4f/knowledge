# Canonical Form (Final)

**INTENT → TOOL → PATTERN → ROOT**

- **Flat**: no nesting, no bundling
- **Concise**: 4 atoms, no auxiliaries
- **Acyclic**: single forward pass, no feedback edges

---

## Atom Contracts (Frozen)

- **INTENT** = `verb + noun + type-id` (≤ 3 words)
  - `type-id ∈ {file | path | content}` → directs tool choice, declaratively

- **TOOL** = `fd | rg` (extend later)

- **PATTERN** = `type:value` where `type ∈ {literal | glob | regex}`
  - reserved: `$type.strategy:value`

- **ROOT** = finite scope (`. | project | src/ | docs/ | config/ | <path>`)

