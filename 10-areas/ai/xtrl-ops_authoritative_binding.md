# xtrl-ops — Authoritative Binding Standard
**Status:** authoritative / binding  
**Version:** v0.2 (binding)  
**Last updated:** 2026-02-01  
**Owner:** baf  

This document defines **mandatory** requirements for xtrl-controlled execution (GPT↔Codex collaboration).  
Normative keywords: **MUST**, **SHOULD**, **MAY**.

---

## 0) Purpose (binding)
xtrl-ops defines a repeatable OSS-aligned methodology for tool conception + implementation and dev learning, where:
- control primitives are explicit,
- reasoning is auditable,
- execution is governable,
- outcomes are measurable,
- drift is prevented.

---

## 1) Scope boundaries (binding)

### In scope
- Engineering work executed via packet contracts and evidence gating.
- Controlled GPT↔Codex workflows that produce bounded plans and mechanical evidence.

### Out of scope (hard boundaries)
- Unbounded remote-agent behavior.
- Claims without evidence (performance/correctness/safety/determinism).

---

## 2) Canonical nouns (binding vocabulary)
Implementations and docs MUST use these nouns consistently:

- **PlantSpec**
- **TransitionSpec**
- **PlanCard (5W+H)**
- **EvidenceCapsule**
- **ReasonCodes**
- **DecisionTrace**
- **Modes**: `NORMAL`, `REPAIR`, `SAFE`
- **Budgets**

---

## 3) Directory model (XDG compliance)

### 3.1 Roots (MUST)
- `CODEX_HOME` MUST be config-only (small, declarative).
- Runtime state MUST NOT be written under `CODEX_HOME`.

Recommended defaults:
- `CODEX_HOME=${XDG_CONFIG_HOME}/codex`
- `CODEX_STATE=${XDG_STATE_HOME}/codex`
- `CODEX_DATA=${XDG_DATA_HOME}/codex`
- `CODEX_CACHE=${XDG_CACHE_HOME}/codex`

### 3.2 xtrl state (MUST)
xtrl runtime MUST write under:
- `XTRL_STATE = $CODEX_STATE/xtrl`

xtrl state subtrees (MUST if used):
- `$XTRL_STATE/out`
- `$XTRL_STATE/packets`
- `$XTRL_STATE/worktrees`
- `$XTRL_STATE/log`
- `$XTRL_STATE/sessions`
- `$XTRL_STATE/history`
- `$XTRL_STATE/tmp`

### 3.3 Forbidden repo-local roots (MUST)
Target repos MUST NOT contain `.codex/` or `.quint/` anywhere (tracked or untracked).  
xtrl preflight MUST deny execution if either root exists.

---

## 4) Skill layout (MUST)
- Canonical skill roots MUST live under `skills-pack/`:
  - `skills-pack/xtrl.packet-runner`
  - `skills-pack/xtrl.packet-template`
- `skills/` MAY exist only as a compatibility symlink layer pointing at `skills-pack/`.

---

## 5) Target resolution + clean gate (MUST)

### 5.1 repo_root resolution (MUST)
- If `--repo-root PATH` is provided, it MUST be used.
- Else `repo_root` MUST be `git rev-parse --show-toplevel`.
- If neither is available, the run MUST be denied.

### 5.2 Clean gate (MUST)
Before any mutation, xtrl MUST enforce:
- `git -C "$repo_root" status --porcelain` returns empty.
Untracked files count as dirty.

### 5.3 codex home/state resolution (MUST)
- If `--codex-home PATH` is provided, it MUST be used.
- Else `CODEX_HOME` env var MUST be used if set; else default to `$XDG_CONFIG_HOME/codex`.
- If `--codex-state PATH` is provided, it MUST be used.
- Else `CODEX_STATE` env var MUST be used if set; else default to `$XDG_STATE_HOME/codex`.

---

## 6) Actuator chain (MUST)
- **Yazi** (or any UI) MUST contain no business logic; it MAY only invoke `just …`.
- **just** is the actuator surface; it MUST call xtrl with explicit `--repo-root/--codex-home/--codex-state`.
- **xtrl** is the controller; it MUST enforce gates, constraints, and evidence emission.

---

## 7) Contract model (binding)

### 7.1 Contract file (MUST)
A run MUST have a materialized `contract.json` in OUT_DIR before Codex execution begins.

Minimum fields (MUST):
- `schema_version`
- `packet_id`
- `base_ref`
- `constraints`:
  - `clean_repo_required: true`
  - `deny_repo_local_roots: [".codex",".quint"]`
  - `allowed_paths: [ ... ]` (glob patterns)
  - `forbidden_paths: [ ... ]` (glob patterns)
  - `diff_budget: { max_files_changed, max_lines_changed }`
  - `forbidden_patterns: [ ... ]`
- `actions: { <action_name>: ["argv0","arg1",...] }`  (ACTION-based exec)
- `evidence.required_files: [...]`

### 7.2 ACTION execution (MUST)
Codex (or any executor) MUST NOT run arbitrary shell commands.  
Only contract-declared ACTIONs are allowed.

If an action is required but not declared:
- the run MUST stop with `ACTION_NOT_AUTHORIZED` (and produce evidence).

### 7.3 Allowed paths (MUST)
All edits MUST be restricted to `constraints.allowed_paths`.  
Edits to any forbidden path MUST stop with `FORBIDDEN_PATH_TOUCHED`.

---

## 8) Evidence standard (binding)

### 8.1 OUT_DIR (MUST)
Evidence MUST be written under a controller-resolved OUT_DIR:
- `OUT_DIR = $CODEX_STATE/xtrl/out/<repo>/<packet_id>` (unless explicitly overridden)

OUT_DIR MUST NOT be inside the target repo.

### 8.2 EvidenceCapsule layout (MUST)
Required:
```text
OUT_DIR/
  evidence.json
  evidence/
    plan.md
    decision.md
    scope.json
    integrity.json
    tests.junit.xml
    regression.md
  commands.log
  summary.md
  packet.json
  contract.json
  exec-prompt.md
```
Optional:
```text
OUT_DIR/
  evidence/perf.json
  evidence/runtime.json
  logs/
```

### 8.3 Minimum signals (MUST)
A packet MUST emit:
- Correctness (tests)
- Integrity (lint/format/type when applicable)
- Scope (diffstat + touched files)
- DecisionTrace (5–10 lines tied to invariants/tests)

### 8.4 evidence.json (MUST)
evidence.json MUST include at least:
- `schema_version`
- `packet_id`, `repo`, `base_ref`, `timestamp`
- `status`: PASS|FAIL|BLOCKED
- `reason_codes`: array
- `commands_run`: array
- `checks`: array (name, status, summary)
- `diffstat`, `touched_files`
- `artifacts`: array (path, sha256)
- `decision_trace`: (path, line_count)

---

## 9) Supervisory modes + budgets (binding)

### 9.1 Modes (MUST)
- `NORMAL`: standard loop
- `REPAIR`: only for bounded, diagnosable failures
- `SAFE`: freeze expansion; only stabilization

Mode transitions MUST be recorded in evidence (decision.md).

### 9.2 Budgets (MUST)
Each packet MUST declare budgets:
- time budget (minutes)
- diff budget (files/lines)
- iteration budget (attempts)

If a budget is exceeded, the run MUST stop with a corresponding ReasonCode.

---

## 10) ReasonCodes (binding)

### 10.1 Seed SSOT (MUST)
Implementations MUST support at least:
- ITERATION_LIMIT_REACHED
- TIME_LIMIT_EXCEEDED
- COST_BUDGET_EXCEEDED
- LOOP_DETECTED
- FLAKY_TEST_DETECTED
- NONDETERMINISM_DETECTED
- SCHEMA_DRIFT
- SCOPE_CREEP_DETECTED
- MISSING_EVIDENCE
- DEPENDENCY_RULE_VIOLATION
- BENCHMARK_REGRESSION

### 10.2 Controller-deny additions (MUST)
- DIRTY_REPO_DENIED
- FORBIDDEN_ROOT_PRESENT
- FORBIDDEN_PATH_TOUCHED
- ACTION_NOT_AUTHORIZED
- OUT_DIR_NOT_WRITABLE
- BASE_REF_MISMATCH

---

## 11) Minimal compliance checklist (binding)
A run is compliant only if:
- repo_root resolved and clean gate passes
- forbidden repo-local roots absent
- contract.json exists pre-exec
- only contract ACTIONs executed
- all edits within allowed paths
- EvidenceCapsule complete with minimum signals
- evidence.json lists hashes for required artifacts
- any stop is tagged with a ReasonCode

---

## Appendix A — Spec interfaces (non-exhaustive)
xtrl SHOULD expose (direct CLI or via just recipes):
- `xtrl doctor`
- `xtrl paths`
- `xtrl preflight`
- `xtrl emit contract|prompt`
- `xtrl check`
- `xtrl evidence`
- `xtrl promote` (MAY be deny-by-default until enforcement is complete)
