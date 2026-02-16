# xtrl-ops — Spec Reference (quick)
**Version:** v0.2-ref (derived from binding standard)  
**Purpose:** fast lookup; no narrative.

---

## A) Variables
- `CODEX_HOME = ${XDG_CONFIG_HOME}/codex` (config-only)
- `CODEX_STATE = ${XDG_STATE_HOME}/codex` (runtime)
- `XTRL_STATE = $CODEX_STATE/xtrl`

## B) Forbidden in target repos
- `.codex/` (anywhere)
- `.quint/` (anywhere)

## C) Skill layout
- `skills-pack/xtrl.packet-runner`
- `skills-pack/xtrl.packet-template`
- `skills/` = compatibility symlink layer only

## D) repo_root resolution
1. `--repo-root PATH` wins
2. else `git rev-parse --show-toplevel`
3. else DENY

Clean gate:
- `git -C "$repo_root" status --porcelain` must be empty

## E) OUT_DIR (state)
Default:
- `OUT_DIR = $CODEX_STATE/xtrl/out/<repo>/<packet_id>`
Must not be inside repo.

## F) EvidenceCapsule required files
```
OUT_DIR/
  contract.json
  exec-prompt.md
  packet.json
  evidence.json
  commands.log
  summary.md
  evidence/
    plan.md
    decision.md
    scope.json
    integrity.json
    tests.junit.xml
    regression.md
```

## G) Minimum signals
- tests + regression
- lint/format/type (as applicable)
- diffstat + touched files
- DecisionTrace (5–10 lines)

## H) Contract required fields (minimum)
- `schema_version`
- `packet_id`
- `base_ref`
- `constraints` (clean gate, deny roots, allowed/forbidden paths, diff budget, forbidden patterns)
- `actions` (ACTION → argv)
- `evidence.required_files`

## I) ACTION rule
- No arbitrary shell
- Only `actions` from contract
- Missing action → `ACTION_NOT_AUTHORIZED`

## J) ReasonCodes (minimum support)
**Budgets/loops**
- ITERATION_LIMIT_REACHED
- TIME_LIMIT_EXCEEDED
- COST_BUDGET_EXCEEDED
- LOOP_DETECTED

**Quality**
- FLAKY_TEST_DETECTED
- NONDETERMINISM_DETECTED
- BENCHMARK_REGRESSION

**Integrity/scope**
- SCHEMA_DRIFT
- SCOPE_CREEP_DETECTED
- DEPENDENCY_RULE_VIOLATION
- MISSING_EVIDENCE

**Controller denials**
- DIRTY_REPO_DENIED
- FORBIDDEN_ROOT_PRESENT
- FORBIDDEN_PATH_TOUCHED
- ACTION_NOT_AUTHORIZED
- OUT_DIR_NOT_WRITABLE
- BASE_REF_MISMATCH

## K) Minimal command surface (recommended)
- `xtrl doctor`
- `xtrl paths`
- `xtrl preflight`
- `xtrl emit` (contract + prompt)
- `xtrl check`
- `xtrl evidence`
- `xtrl promote` (may deny-by-default early)

## L) Smoke tests
Inside repo:
```bash
python $CODEX_HOME/xtrl/tools/run_packet.py packets/examples/packet-000-foundation.json
```

Outside repo:
```bash
bash $CODEX_HOME/skills/xtrl.packet-runner/scripts/run_packet.sh   packets/examples/packet-000-foundation.json   --repo-root /path/to/target   --codex-home "$CODEX_HOME"   --codex-state "$CODEX_STATE"
```
