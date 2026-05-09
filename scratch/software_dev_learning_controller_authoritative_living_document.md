# Software-Dev Learning Controller — Authoritative Living Document

**Status:** Living document (authoritative)  
**Version:** v0.1  
**Last updated:** 2026-02-01  
**Owner:** baf

## Supersedes (merged into this document)
- `software_dev_learning_controller.md`
- `gpt_codex_engineering_methodology_layer_stack_living_document_v0_2.md`
- `initial_plant_assessment_playbook_living_document_v0_3.md`

---

## 0) Purpose

Define a repeatable, OSS-aligned methodology for **tool conception + implementation** and **dev learning** using GPT↔Codex collaboration, where:

- **Control primitives are explicit** (plants, sensors, actuators, budgets, modes).
- **Reasoning is auditable** (PlanCard + DecisionTrace).
- **Execution is governable** (packet contracts + evidence).
- **Outcomes are measurable** (minimum signal set + gates).
- **Drift is prevented** (stop rules, saturation, supervisory modes).

---

## 1) Scope boundaries

### In scope
- Daily OSS-style engineering work: features, refactors, debugging, optimization, testing, tooling, exploration.
- Controlled GPT↔Codex workflows that produce **bounded plans** and **mechanical evidence**.
- Release/operate alignment (minimal) for OSS expectations: release notes, observability, reliability mode.

### Out of scope (hard boundaries)
- “Do anything” remote-agent behavior.
- Unbounded exploratory wandering without gates.
- Claims without evidence (performance, correctness, safety, determinism).

---

## 2) Canonical nouns (shared vocabulary)

These names must be used consistently across tooling, packets, and evidence:

- **PlantSpec**: the system being changed (boundary, interfaces, state, observables, S0, S* gates).
- **TransitionSpec**: the next smallest promotable transition (S0 → S1).
- **PlanCard (5W+H)**: WHAT / WHY / WHERE / WHEN / HOW + risks + mitigations + budgets (bounded).
- **EvidenceCapsule**: standardized evidence bundle emitted by a run (signals + artifacts + hashes).
- **ReasonCodes**: machine-checkable failure/stop taxonomy (deny-fast + predictable failures).
- **DecisionTrace**: 5–10 lines: “why this change” + “why safe” tied to invariants/tests.
- **Modes (supervisory)**: `NORMAL` / `REPAIR` / `SAFE`.
- **Budgets (saturation)**: diff/time/iterations/cost; hard caps with STOP rules.

---

## 3) System model (control lens)

### 3.1 Plant model
A “plant” is any changeable system:
- repo/module, build pipeline, CI gate, release process, runtime service, documentation generator.

**Plant state (x)** is made explicit via:
- base ref, dependency graph/lockfiles, config, environment assumptions, current pass/fail gates.

### 3.2 Sensors (measurement)
Minimum sensor families (see §7):
- correctness, integrity, change scope, decision trace
- plus optional performance and runtime behavior when relevant.

### 3.3 Actuators (allowed actions)
Actuation is constrained by:
- `allowed_paths`, `allowed_commands`, `forbidden_outputs`, budgets, and stop rules.

### 3.4 Controller + interlocks
- **Feedforward control**: contracts, templates, preflight, allowlists, invariants.
- **Feedback control**: tests, benchmarks, runtime signals, rollback/repair loops.
- **Saturation control**: hard caps (diff/time/retries/cost).
- **Supervisory control**: mode switching (`NORMAL`/`REPAIR`/`SAFE`) based on state and failure patterns.
- **Interlock**: promotion gate (mechanical/CI/policy) decides `ALLOW` vs `DENY`.

---

## 4) Foundations (learning controller)

### 4.1 Three foundational pillars (non-negotiable)

#### Pillar 1 — Computation as a System
- Treat code, tools, and workflows as state machines.
- Make interfaces, invariants, and transitions explicit.
- Preserve state via artifacts (specs, evidence, templates).

#### Pillar 2 — Statistics as Inference
- Treat understanding and measurements as uncertain.
- Keep hypotheses explicit and falsifiable.
- Treat errors/confusion as signals, not moral failures.

#### Pillar 3 — Control & Adaptation
- Treat pace/depth as parameters.
- Update policies when drift/overload is observed.
- Prioritize stability over speed.

### 4.2 Complementing methodologies (ergonomics)
- **Systems engineering (light)**: State → Transition → Invariant; interface before implementation; evidence over belief.
- **Scientific method (operational)**: hypothesis → intervention → measurement → model update/discard.
- **Constraint-driven design**: constraints first; optimize within constraints; expand constraints only with evidence.
- **Model-based thinking**: cheap explicit models; models are disposable; wrong-but-useful > vague.

### 4.3 Abstract learning loop (the controller overlay)
1. Define constraints  
2. Propose model  
3. Execute task  
4. Observe signals  
5. Update model/parameters  
6. Preserve state (artifacts + evidence)

---

## 5) OSS-aligned methodology stack

This stack matches common OSS/DevOps flow:

**Issue → (optional) RFC/ADR → Branch/PR → CI Gates → Merge to main → Release → Publish/Deploy → Observe → Improve**

Control application:
- **Feedforward**: contracts, preflight checks, templates, allowlists
- **Feedback**: CI signals, runtime signals, bounded repair loops
- **Saturation**: budgets and stop rules
- **Supervisory**: mode switching, stability mode

### Intake gate (mandatory)
Before new tool conception/implementation work, run **Initial Plant Assessment** (§6).  
Outputs: `PlantSpec + TransitionSpec + PlanCard + Packet draft + Assessment Capsule`.

### L0 — Foundations (principles + invariants)
Outputs:
- Immutable principles checklist
- ReasonCodes taxonomy (SSOT)

### L1 — Daily operational loop
**PlanCard → Run → EvidenceCapsule → Next PlanCard**

Mode selector:
- **GPT-first**: missing sensors, ambiguous “done”, design risk.
- **Codex-first**: mechanical change, reproduce–fix–verify loops, controlled refactors.

Stop rules (pick ≥2):
- iteration cap, time cap, diff budget, “same failure twice”, “same ambiguity twice”

### L2 — Coordination patterns (workflow topologies)
- Linear pipeline
- Contract-first pipeline
- Hypothesis-driven investigation
- Adversarial review (counterexample hunting)
- Coordinator–specialist (fan-out)
- Adaptive entry point (choose the smallest stabilizing loop)

### L3 — Control containers (enforced wrappers)
Repeatable wrappers that always ship:
- signals, gates, detectors, recovery, EvidenceCapsule

Baseline controls:
- structured logs (+ correlation id)
- time/iteration guards
- bounded retry + explicit stop reasons
- boundary validation (inputs/outputs/schema)
- characterization tests for refactors

### L4 — Code-shape patterns (structural)
- functional core / imperative shell
- ports & adapters
- pipeline/stage graph
- CQS (command/query separation)
- orchestrator + workers
- state machine / transition table
- policy vs mechanism split
- validation boundary

### L5 — Architecture patterns (system-level)
- layered / modular monolith
- hexagonal (ports/adapters)
- clean architecture
- event-driven / CQRS / saga / pipeline graphs

### L6 — Optional: DSAs/algorithms as containers
Use only when the plant is an algorithm/DSA implementation.

### L7 — Translation to packet contracts (execution governance)
Mapping:
- actuators → allowed_paths / allowed_commands
- invariants/gates → required_checks + thresholds
- budgets → diff/time/iteration/cost caps
- evidence → required artifact paths + hashes
- stop reasons → ReasonCodes
- DecisionTrace → required 5–10 line artifact

### L8 — Release & distribution (OSS expectations)
- versioning policy (SemVer-like or repo-specific)
- changelog/release notes conventions
- artifact immutability (hashes, tags)
- compatibility statements (public API/config schema)

### L9 — Operate/observe/reliability (DevOps/SRE alignment)
- minimal observability conventions
- incident loop: detect → mitigate → postmortem
- stability mode when reliability degrades
- turn incidents into new PlantSpecs/TransitionSpecs

---

## 6) Initial Plant Assessment (mandatory entry procedure)

### Exit artifacts (canonical)
1. Plant inventory (bullets)
2. PlantSpec (S0 + S* gates + boundaries)
3. Constraint map (hard/soft + budgets)
4. TransitionSpec (S0 → S1)
5. PlanCard (5W+H) for the TransitionSpec
6. Packet draft
7. Assessment Capsule (audit-ready)

### DAG (mental model)
```mermaid
flowchart TD
  A[0. Declare scope] --> B[1. Inventory plants]
  B --> C[2. Reduced-form classification\n(System lens • Control mode • Uncertainty • Surface)]
  C --> D[3. Pillar injection\n(System invariants • Uncertainty • Feedback/stability)]
  D --> E{Select primary plant\n(measurable gate exists)}
  E --> F[4. Capture S0\n(observable facts only)]
  F --> G{Can run an entry command now?}
  G -->|yes| H[4a. Run + record evidence]
  G -->|no| I[4b. Mark UNKNOWNs]
  H --> J[5. Define S* as binary gates]
  I --> J
  J --> K{Have ≥1 gate?}
  K -->|no| L[Reframe / shrink objective] --> B
  K -->|yes| M[6. Derive constraints\n(invariants, budgets, sensors, actuators)]
  M --> N[7. Choose next S0→S1 TransitionSpec]
  N --> O{Exceeds budgets / too wide?}
  O -->|yes| P[Split transition] --> N
  O -->|no| Q[8. Draft PlanCard (5W+H)]
  Q --> R[9. Draft packet contract]
  R --> S[10. Assessment Capsule\n(+ DecisionTrace + ReasonCodes)]
  S --> T((END))
```

### Default stop rules
- timebox: 25–45 minutes
- stop if: same ambiguity twice, same failure twice, no gate after 2 tries
- on stop: record `ReasonCode + open question + next smallest step`

---

## 7) Evidence standard (signals, artifacts, gates)

### 7.1 Minimum signals (per packet; default gate set)

Always required:
- **Correctness**: tests + targeted regression test
- **Integrity**: lint/format/type checks (as applicable)
- **Change scope**: diffstat + touched files list
- **DecisionTrace**: 5–10 lines (“why” + “why safe”)

Conditionally required (when relevant):
- **Performance**: before/after benchmark (same harness)
- **Runtime behavior**: logs/tracing summary (OTel only if already in stack)

### 7.2 EvidenceCapsule layout (canonical)
```
.codex/out/<packet_id>/
  evidence.json
  evidence/
    plan.md
    decision.md
    scope.json
    integrity.json
    tests.junit.xml
    regression.md
    perf.json        # optional
    runtime.json     # optional
  logs/              # optional raw logs
```

### 7.3 EvidenceCapsule rollup (minimum fields)
- id, packet_id, base_ref, commit, timestamp
- status (PASS|FAIL|BLOCKED)
- reason_codes[]
- commands_run[]
- checks[] (tests/lint/type/bench results)
- diffstat + touched_files[]
- artifacts[] (path + hash)
- decision_trace (path + line_count)

---

## 8) Supervisory modes, budgets, stop rules

### Modes
- **NORMAL**: standard loop (Plan → Run → Evidence → Gate)
- **REPAIR**: allowed only when failure is diagnosable and fix is bounded
- **SAFE**: freeze expansion; only stabilization, sensors, and rollback/containment

### Budgets (saturation)
- diff lines/files, timebox, iterations/retries, optional cost units
- budgets must be declared in the PlanCard and packet contract

### Loop detection (minimum policy)
Trigger `LOOP_DETECTED` if any:
- identical patch produced twice
- same error signature ≥ 3 times
- “same ambiguity twice” without new sensor or narrower scope

---

## 9) ReasonCodes v0 (seed SSOT)
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

---

## 10) Audit: learning by assessing GPT/Codex reasoning

### Required reasoning artifacts
- **PlanCard (5W+H)**: bounded, executable commands, explicit signals and gates.
- **DecisionTrace (5–10 lines)**: why change + why safe tied to invariants/tests.
- **Uncertainty bullets (≤3)**: unknowns → sensor to resolve → stop condition.
- **Progress monotonicity**: what changes between attempts and what new evidence is produced.

### Quick rubric (score 0/1 each; /7)
1. Bounded (caps + stop rules)
2. Concrete (commands + paths explicit)
3. Test-linked (regression named, coverage described)
4. Invariant-linked (“why safe” references constraints)
5. Phase-correct (preflight → execute → measure → gate)
6. No hidden work (no “as needed”)
7. Failure plan (mitigation is specific)

Interpretation:
- 0–3: deny or rewrite plan
- 4–5: proceed with strict caps
- 6–7: proceed normally

---

## 11) Templates (copy/paste)

### 11.1 PlantSpec (skeleton)
```md
# PlantSpec: <name>

## Boundary
- In scope:
- Out of scope:
- Interfaces:

## State
- Base ref:
- Environment assumptions:
- Current gates (tests/lint/type/bench/schema):

## S0 (observable facts)
- …

## S* (binary gates)
- Gate 1:
- Gate 2:

## Constraints
- Hard invariants:
- Soft constraints:

## Budgets
- diff_lines_max:
- diff_files_max:
- iterations_max:
- timebox_minutes:
```

### 11.2 TransitionSpec (skeleton)
```md
# TransitionSpec: S0 → S1

## Action
- …

## Success gates
- …

## Evidence
- …

## Rollback/fallback
- …

## Anticipated failure modes (ReasonCodes)
- …
```

### 11.3 PlanCard (5W+H)
```md
## 5W+H PlanCard

### WHAT
- Change:
- Expected behavior change:

### WHY
- Goal:
- Why safe (tie to invariants/tests):

### WHERE
- Allowed paths:
- Forbidden/untouched areas:
- Expected touched files:

### WHEN (phases)
1) Preflight:
2) Execute:
3) Measure:
4) Gate:

### HOW
- Commands to run:
- Tests/validators:
- Evidence paths:

### RISKS + MITIGATIONS
- Risk → mitigation:

### BUDGETS + STOP RULES
- diff/time/iterations/cost caps:
- stop if:
```

### 11.4 DecisionTrace (5–10 lines)
```md
1) Why this change:
2) Why now:
3) Why safe (invariant/test refs):
4) What would falsify success:
5) What we refuse to do (illegal moves):
6) Budget/stop rules used:
```

### 11.5 Packet contract (YAML skeleton)
```yaml
packet_id: P-XXXX
intent: ""
plant_spec_ref: ""
transition_spec_ref: ""
allowed_paths: []
allowed_commands: []
forbidden_outputs: []
budgets:
  diff_lines_max: 250
  diff_files_max: 20
  iterations_max: 2
  timebox_minutes: 30
required_signals:
  - correctness
  - integrity
  - scope
  - decision_trace
checks:
  - tests
  - lint
  - format
  - typecheck
evidence:
  - ".codex/out/<packet_id>/evidence.json"
  - ".codex/out/<packet_id>/evidence/plan.md"
  - ".codex/out/<packet_id>/evidence/decision.md"
reason_codes:
  - ITERATION_LIMIT_REACHED
  - TIME_LIMIT_EXCEEDED
  - LOOP_DETECTED
rollback: "git reset --hard <base_ref>"
stop_conditions:
  - "same failure twice"
  - "diff budget exceeded"
```

### 11.6 EvidenceCapsule rollup (JSON skeleton)
```json
{
  "id": "cap-…",
  "packet_id": "P-…",
  "base_ref": "…",
  "commit": "…",
  "timestamp": "…",
  "status": "PASS",
  "reason_codes": [],
  "commands_run": [],
  "checks": [],
  "diffstat": {"files": 0, "insertions": 0, "deletions": 0},
  "touched_files": [],
  "artifacts": [],
  "decision_trace": {"path": "evidence/decision.md", "line_count": 0}
}
```

---

## 12) Open items (next edits)
1. Observability standard (log keys, span naming, correlation propagation).
2. Benchmarking standard (baseline format, variance handling, thresholds).
3. Dependency-rule enforcement (imports/deps constraints + harness).
4. Promotion protocol (WORK → PROMOTE) as a mechanical gate.
