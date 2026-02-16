# Initial Plant Assessment DAG (Living Document)

**Purpose**
A repeatable first-pass assessment procedure to identify **plants**, capture **current vs desired state**, derive **constraints/invariants**, define **gates + evidence**, and render the **first packet draft**.

---

## DAG (mental model)

```mermaid
flowchart TD
  A[0. Declare scope
Intent • Out-of-scope • Exit artifacts] --> B[1. Inventory plants
Macro + Micro candidates]

  B --> C{Select primary plant
closest to objective
+ has a measurable gate}
  C -->|chosen| D[2. Capture current state S0
observable facts only]

  D --> E{Can run an entry command
now?}
  E -->|yes| F[2a. Run + record evidence
store outputs]
  E -->|no| G[2b. Mark UNKNOWNs
continue]
  F --> H[3. Define desired state S* as gates
binary checks]
  G --> H

  H --> I{Do you have ≥1 gate?
(test/validator/benchmark)}
  I -->|no| J[Reframe
shrink objective or pick narrower plant]
  J --> B
  I -->|yes| K[4. Derive constraints
Hard invariants vs Soft constraints
+ budgets + sensors + actuators]

  K --> L[5. Define next transition S0→S1
next smallest promotable step]
  L --> M{Transition exceeds budgets
or touches >2–3 subsystems?}
  M -->|yes| N[Split transition
choose smaller step]
  N --> L
  M -->|no| O[6. Draft packet contract
paths • budgets • checks • evidence • stop rules]

  O --> P[7. Assessment capsule
primary plant • S0 • S* gates • invariants
first transition • packet draft • open qs]
  P --> Q((END))

  %% Stop rules (timebox & repetition guards)
  D -.-> R[STOP if:
- timebox exceeded
- same ambiguity twice
- same failure twice
Record reason code + open question]
  H -.-> R
  L -.-> R
```

---

## Node details (what to write at each step)

### 0) Declare scope (2 min)
- **Intent**: what you’re assessing
- **Out-of-scope**: what you will not touch today
- **Exit artifacts**: what you will produce (below)

### 1) Inventory plants (5–10 min)
- Macro: build/test pipeline, content-gen pipeline, CI/promotion gate, packaging
- Micro: target module, generator, validator, specific algorithm/component

### 2) Capture current state S₀ (5–10 min)
Observable facts only:
- repo cleanliness + base ref
- passing commands, failing commands (with short error label)
- existing gates (tests/lint/type/bench/schema)
- existing artifacts (generated outputs)

### 3) Define desired state S\* as gates (5–10 min)
Binary checks:
- must pass: tests/lint/type/validator
- must produce: artifact(s)
- must not: new deps, API drift, nondeterminism (if relevant)

**If you cannot name ≥1 gate → reframe** (shrink objective / pick narrower plant).

### 4) Derive constraints (5–10 min)
- **Hard invariants (deny-fast):** allowed paths, forbidden outputs, determinism/schema, safety, immutability
- **Soft constraints:** idioms, architecture alignment, perf goals
- **Budgets:** diff lines, iterations, timebox
- **Sensors:** tests, validators, logs/traces, benchmarks
- **Actuators:** what changes are allowed

### 5) Define next transition S₀→S₁ (3–8 min)
Next smallest promotable step:
- action
- gate
- evidence
- rollback
- likely failure modes

### 6) Draft packet contract (5–10 min)
```yaml
packet_id: P-INIT-0001
intent: ""
allowed_paths: []
forbidden_outputs: []
budgets:
  diff_lines_max: 250
  iterations_max: 2
  timebox_minutes: 30
checks:
  - ""
evidence:
  - ""  # required log/result paths
reason_codes:
  - ITERATION_LIMIT_REACHED
  - TIME_LIMIT_EXCEEDED
  - LOOP_DETECTED
rollback: "git reset --hard <base_ref>"
stop_conditions:
  - "same failure twice"
  - "diff budget exceeded"
```

### 7) Assessment capsule (2–5 min)
- Primary plant:
- S₀ summary:
- S\* gates:
- Hard invariants:
- First transition:
- Packet drafted:
- Open questions (≤3):

---

## Exit artifacts (what “done” means)
1. Plant inventory (bullets)
2. PlantSpec summary (S₀ + S\*)
3. Constraint map (hard/soft + budgets)
4. TransitionSpec (S₀→S₁)
5. Packet draft (YAML)
6. Assessment capsule (short)

---

## Stop rules (default)
- **Timebox** 25–45 min (first pass)
- Stop if: same ambiguity twice, same failure twice, no gate after 2 tries
- When stopping: record **reason code + open question + next smallest step**

---

## Version notes
- v0.2: reformatted into a DAG-first mental model.

