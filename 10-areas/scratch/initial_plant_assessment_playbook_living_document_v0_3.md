# Initial Plant Assessment DAG (Living Document)

**Status:** Living document (iterative)  
**Version:** v0.3  
**Last updated:** 2026-02-01

## Purpose
A repeatable first-pass assessment procedure to:
- identify **plants**
- capture **current vs desired state** (S0 vs S*)
- derive **constraints/invariants**, **budgets**, **sensors**, **actuators**
- define **gates + evidence**
- produce the **next smallest promotable transition** (TransitionSpec)
- draft the **first packet contract**
- emit an **Assessment Capsule** you can audit (including DecisionTrace + ReasonCodes)

This is the **mandatory entry gate** before tool conception/implementation work.

---

## Canonical outputs (exit artifacts)
1. **Plant inventory** (bullets)
2. **PlantSpec** (S0 + S* gates + boundaries)
3. **Constraint map** (hard/soft + budgets)
4. **TransitionSpec** (S0→S1)
5. **PlanCard (5W+H)** for the TransitionSpec
6. **Packet draft** (YAML)
7. **Assessment Capsule** (short, audit-ready)

---

## DAG (mental model)

```mermaid
flowchart TD
  A[0. Declare scope
Intent • Out-of-scope • Exit artifacts] --> B[1. Inventory plants
Macro + Micro candidates]

  B --> C[2. Reduced-form classification
(System lens • Control mode • Uncertainty model • Surface)]
  C --> D[3. Pillar injection (3 questions)
System state/invariants • Uncertainty • Feedback/stability]

  D --> E{Select primary plant
closest to objective
+ has a measurable gate}
  E -->|chosen| F[4. Capture current state S0
observable facts only]

  F --> G{Can run an entry command now?}
  G -->|yes| H[4a. Run + record evidence
store outputs]
  G -->|no| I[4b. Mark UNKNOWNs
continue]

  H --> J[5. Define desired state S* as gates
binary checks]
  I --> J

  J --> K{Do you have ≥1 gate?
(test/validator/benchmark)}
  K -->|no| L[Reframe
shrink objective or pick narrower plant]
  L --> B
  K -->|yes| M[6. Derive constraints
Hard invariants vs Soft constraints
+ budgets + sensors + actuators]

  M --> N[7. Define next transition S0→S1
next smallest promotable step]
  N --> O{Transition exceeds budgets
or touches >2–3 subsystems?}
  O -->|yes| P[Split transition
choose smaller step]
  P --> N
  O -->|no| Q[8. Draft PlanCard (5W+H)
WHAT/WHY/WHERE/WHEN/HOW + risks]

  Q --> R[9. Draft packet contract
paths • commands • budgets • checks • evidence • stop rules]

  R --> S[10. Assessment Capsule
PlantSpec • TransitionSpec • PlanCard • Packet draft
Open qs + ReasonCodes + DecisionTrace]
  S --> T((END))

  %% Stop rules (timebox & repetition guards)
  F -.-> U[STOP if:
- timebox exceeded
- same ambiguity twice
- same failure twice
Record ReasonCode + open question]
  J -.-> U
  N -.-> U
```

---

## Node details (what to write at each step)

### 0) Declare scope (2 min)
- **Intent**: what you’re assessing
- **Out-of-scope**: what you will not touch today
- **Exit artifacts**: the 7 items listed above

### 1) Inventory plants (5–10 min)
- **Macro plants**: build/test pipeline, CI gate, packaging/release, deploy/ops loop
- **Micro plants**: target module, generator, validator, specific component

### 2) Reduced-form classification (2–5 min)
Write a one-line 4-tuple:
- **System lens**: (repo / service / pipeline / algorithm / docs)
- **Control mode**: (feedforward / feedback / mixed / supervisory)
- **Uncertainty model**: (low / medium / high; noise/flakiness?)
- **Surface**: (local CLI / CI / runtime / release)

### 3) Pillar injection (2–5 min)
Answer in bullets:
- **Computation**: what is the state, what are invariants, what resources/budgets matter?
- **Inference**: what is uncertain, what signals are noisy/unreliable?
- **Control**: where are actuators/sensors, what delays/loops exist, what stability risks?

### 4) Capture current state S0 (5–10 min)
Observable facts only:
- base ref + repo cleanliness
- passing commands, failing commands (short error label)
- existing gates (tests/lint/type/bench/schema)
- existing artifacts (generated outputs)

### 5) Define desired state S* as gates (5–10 min)
Binary checks:
- must pass: tests/lint/type/validator
- must produce: artifact(s)
- must not: scope violations, nondeterminism, forbidden paths/outputs

**If you cannot name ≥1 gate → reframe** (shrink objective / pick narrower plant).

### 6) Derive constraints (5–10 min)
- **Hard invariants (deny-fast):** allowed paths, forbidden outputs, determinism/schema, safety, immutability
- **Soft constraints:** idioms, architecture alignment, perf goals
- **Budgets:** diff lines/files, iterations, timebox, optional cost units
- **Sensors:** tests, validators, logs/traces, benchmarks
- **Actuators:** allowed commands + allowed file writes

### 7) Define next transition S0→S1 (3–8 min)
Next smallest promotable step:
- action (what changes)
- gate (how success is measured)
- evidence (what artifacts prove it)
- rollback/fallback
- likely failure modes (ReasonCodes)

### 8) Draft PlanCard (5W+H) (3–8 min)
Write this (bounded):
- WHAT: exact change target
- WHY: goal + why safe (tie to invariants/tests)
- WHERE: allowed paths + expected touched files
- WHEN: phase order (preflight → execute → measure → gate)
- HOW: exact commands + checks + evidence paths
- RISKS: 1–3 risks + mitigations
- BUDGETS: diff/time/iterations/cost caps + STOP rules

### 9) Draft packet contract (5–10 min)
```yaml
packet_id: P-INIT-0001
intent: ""
plant_spec_ref: ""        # path or identifier
transition_spec_ref: ""   # path or identifier
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

### 10) Assessment Capsule (2–5 min)
Short, audit-ready:
- Primary plant:
- PlantSpec (S0):
- S* gates:
- Hard invariants + budgets:
- TransitionSpec:
- PlanCard summary:
- Packet drafted:
- DecisionTrace (5–10 lines):
- Open questions (≤3):
- ReasonCodes observed/anticipated:

---

## Stop rules (default)
- **Timebox** 25–45 min (first pass)
- Stop if: same ambiguity twice, same failure twice, no gate after 2 tries
- When stopping: record **ReasonCode + open question + next smallest step**

---

## Version notes
- v0.2: reformatted into a DAG-first mental model.
- v0.3: added reduced-form classification + pillar injection + PlanCard/DecisionTrace requirements.
