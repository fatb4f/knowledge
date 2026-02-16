1) Code Quality and Debugging
What “semantic” means here

Analysis that understands program structure and meaning, not just text patterns:

Types (what values can be here?)

Control flow (what paths can execute?)

Data flow (where does this value come from / go to?)

Effects (I/O, network, filesystem, mutation)

Invariants (rules that must hold)

Typical problems it catches

Unreachable code / dead branches

Exception paths you didn’t consider

Wrong assumptions about types (e.g., Optional usage)

Resource misuse (files not closed, context manager gaps)

Risky APIs in the wrong contexts (e.g., shell invocation in a runner)

High-signal OSS tools for Python

pyright / mypy (type semantics + flow-sensitive narrowing)

Semgrep (AST + optional dataflow/taint rules)

CodeQL (deeper semantic queries and dataflow when you need it)

Pysa (Pyre) (taint-style dataflow for “source → sink” reasoning)

Dev methodology that matches

Treat invariants as tests:

“No shell execution in controller code”

“All path checks use resolve()+relative_to()”

“All contract parsing must schema-validate”

Encode them as Semgrep/CodeQL/Pysa rules and maintain a TP/TN corpus.


A — Fast static checks (lint / hygiene; no rewrite)

Ruff (lint + formatter; supports autofix/“fix” flows)

Bandit (Python security lint; flags risky API use like shell execution patterns)

mypy / pyright (type checking as robustness gate; catches “missing key / wrong type” paths early)

detect-secrets / gitleaks (secrets scanning in-repo)

pip-audit / OSV-Scanner (dependency vulnerability matching; good to run alongside Semgrep)

B — Structural search/replace and codemods (rewrite + rule-style testing)

LibCST codemods (Python codemod framework; supports multi-pass transforms + CLI scaffolding)

Bowler (Python AST refactoring tool; safe large-scale modifications)

Comby (structural search/replace templates across languages; useful for “codemod without full AST modeling”)

Difftastic (structural diff for reviewing large mechanical rewrites; parses syntax via tree-sitter)

ast-grep rule tests + snapshots (invalid/valid test cases + snapshot baselines for rule output)

C — Dataflow / taint / semantic security (beyond pattern matching)

Semgrep taint mode (mode: taint, sources→propagators→sinks tracking)

Pysa (Pyre) (taint analysis for Python; rules/models + saved taint output)

CodeQL for Python (semantic queries; security-extended suites, CWE-linked query packs)

PyT (python-taint) (Python taint analysis tool; more niche/legacy, but in the same “taint engine” neighborhood)
