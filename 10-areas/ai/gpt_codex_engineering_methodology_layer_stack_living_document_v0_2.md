# GPT–Codex Engineering Methodology Layer Stack (OSS-aligned)

**Status:** Living document (iterative)  
**Version:** v0.2  
**Last updated:** 2026-02-01

## Purpose
Define a repeatable methodology for daily OSS-style engineering work (features, refactors, optimization, testing, tooling, exploration) using GPT↔Codex exchange patterns, with:
- **clear boundaries (PlantSpec)**
- **explicit control primitives (constraints, budgets, modes)**
- **standard signals + evidence (EvidenceCapsule)**
- **promotion interlocks (CI/policy gates)**
- **translation into **packet contracts** (execution governance)

---

## Canonical nouns (shared vocabulary)

These names must be used consistently across docs and tooling:

- **PlantSpec**: what system is being changed (boundary, interfaces, state, observables).
- **TransitionSpec**: the next smallest state transition (S0→S1) that is promotable.
- **PlanCard (5W+H)**: WHAT/WHY/WHERE/WHEN/HOW + risks + mitigations (bounded).
- **EvidenceCapsule**: standardized evidence bundle emitted by a run (signals + artifacts + hashes).
- **ReasonCodes**: machine-checkable failure/stop taxonomy (predictable failures, deny-fast).
- **DecisionTrace**: 5–10 lines: “why this change” + “why safe” tied to invariants/tests.
- **Modes**: NORMAL / REPAIR / SAFE (supervisory mode switching).
- **Budgets (saturation)**: diff/time/iterations/cost; hard caps with STOP rules.

---

## Where this fits in recognizable OSS methodology

This stack matches the common OSS/DevOps flow:

**Issue → (optional) RFC/ADR → Branch/PR → CI Gates → Merge to main → Release → Deploy/Publish → Observe → Improve**

Control is applied as:
- **Feedforward**: contracts, templates, preflight checks, allowlists
- **Feedback**: tests, benchmarks, runtime signals, rollback/repair loops
- **Saturation**: budgets, retry caps, time/cost ceilings
- **Supervisory control**: mode switching (NORMAL/REPAIR/SAFE) based on state

---

## Entry gate (mandatory)
Before executing work on a new problem/tool/plant, run:

- **Initial Plant Assessment DAG** → outputs **PlantSpec + TransitionSpec + Packet draft + Assessment capsule**  
(See: *Initial Plant Assessment DAG (Living Document)*)

This prevents “unbounded wandering” and forces measurability and safe actuation.

---

## Layer stack

### L0 — Foundations (Principles + invariants)
- Loop premise: iterate until **desired state** is met (measured via gates).
- Three-lens reflex:
  - **Computation as a System**: resources, determinism, state transitions
  - **Statistics as Inference**: measurement, baselines, uncertainty/noise
  - **Control & Adaptation**: feedback, stability, bounded updates
- Evidence-first collaboration: every meaningful run yields an **EvidenceCapsule**.
- Illegal moves: no hidden work, no unbounded scope, no unverifiable claims.

**Outputs**
- Immutable principles checklist
- **ReasonCodes** taxonomy (SSOT)

---

### L1 — Operational loop (daily driver)
**PlanCard → Run → EvidenceCapsule → Next PlanCard**

Mode selector:
- **GPT-first**: unclear “done”, design risk, missing sensors, ambiguity
- **Codex-first**: mechanical change, reproduce–fix–verify loops, controlled refactors

Default stop rules (pick ≥2):
- iteration cap, time cap, diff budget, “same failure twice”, “same ambiguity twice”

**Outputs**
- Task/PlanCard template
- EvidenceCapsule template
- Mode selector rules

---

### L2 — Coordination patterns (workflow topologies)
- Linear pipeline
- Contract-first pipeline
- Hypothesis-driven investigation
- Adversarial review (counterexample hunting)
- Coordinator–specialist (fan-out)
- Adaptive entry point (pick the smallest stabilizing loop)

**Outputs**
- Pattern-specific step lists (phases + gates + evidence)
- Pattern chooser (decision rules)

---

### L3 — Control containers (code wrappers that enforce control)
**Definition**: repeatable wrappers that enclose variable logic but always ship:
- **signals** (logs/metrics/traces/counters)
- **gates** (tests/invariants/benchmarks/schema checks)
- **detectors** (failure prediction + ReasonCodes)
- **recovery** (rollback/fallback/retry budgets)
- **EvidenceCapsule** emission

Baseline controls (high ROI):
- structured logging + correlation id
- time/iteration budget guards
- bounded retry + explicit stop reasons
- boundary validation (inputs/outputs/schema)
- characterization tests for refactors

**Outputs**
- Minimal container API: Budget, Invariant, Signals, EvidenceCapsule, ReasonCodes
- Container library: controlled_function, pipeline_stage, troubleshoot_probe, refactor_safety, optimization_measure

---

### L4 — Code-shape patterns (structural shapes)
- Functional core / imperative shell
- Ports & adapters
- Pipeline / stage graph
- CQS (command/query separation)
- Orchestrator + workers
- State machine / transition table
- Policy vs mechanism split
- Validation boundary pattern

**Outputs**
- Shape-spec checklists (review + tests)
- Skeleton module layouts per shape

---

### L5 — Architecture patterns (system-level)
Boundary and dependency patterns:
- Layered
- Hexagonal (ports/adapters)
- Clean architecture
- Modular monolith

Coordination patterns:
- Event-driven
- CQRS
- Saga
- Pipeline graph

**Outputs**
- Boundary rules (imports/allowed deps)
- Contract tests at boundaries
- Observability standards per boundary (log keys, span names, correlation propagation)

---

### L6 — Optional: DSAs/algorithms as containers (course/algorithm contexts)
Use when the “plant” is an algorithm or DSA implementation.

**Container requirements**
- invariants + validate()
- budget guard (iterations/time/visited)
- signals (counts, queue depth, branch hits)
- property tests where applicable
- stop reasons: ITER_LIMIT, TIMEOUT, LOOP_DETECTED, NO_SOLUTION

**Outputs**
- DSA/algo template library (implementation + tests + instrumentation)

---

### L7 — Translation to packet contracts (execution governance)
**Mapping**
- actuators → allowed_paths / allowed_commands
- invariants/gates → required_checks + thresholds
- budgets → diff/time/iteration limits
- evidence → required artifact paths + hashes
- stop reasons → ReasonCodes taxonomy
- DecisionTrace → required 5–10 lines artifact

**Outputs**
- Packet contract template + schema
- Evidence bundle manifest format
- Promotion gate checklist (mechanical)

---

### L8 — Release & distribution (OSS expectations)
**Goal**: make “what shipped” unambiguous and reproducible.

- Versioning policy (e.g., SemVer-like or repo-specific)
- Changelog/release notes conventions
- Artifact immutability (hashes, tags)
- Compatibility statements (public API, config schema)

**Signals**
- release artifact hash
- changelog entry present
- compatibility checks (if applicable)

**Outputs**
- Release spec + checklist
- Release evidence record

---

### L9 — Operate, observe, reliability (DevOps/SRE alignment)
**Goal**: close the loop post-merge.

- Minimal observability conventions (logs/metrics/traces) for the system
- Incident loop: detection → mitigate → postmortem
- Supervisory control: stability mode when reliability degrades
- Regression prevention: add sensors/tests/probes for incidents

**Signals**
- runtime error rates, latency, saturation indicators
- alert summaries (if applicable)
- postmortem actions tracked as new PlantSpecs/TransitionSpecs

**Outputs**
- Observability standard (keys/spans)
- Reliability mode policy
- Postmortem template (bounded, evidence-backed)

---

## Minimum signals (per packet; default gate set)

Always required:
- **Correctness**: tests + targeted regression test
- **Integrity**: lint/format/type checks (as applicable)
- **Change scope**: diffstat + touched files list
- **DecisionTrace**: 5–10 lines (“why” + “why safe”)

Conditionally required (when relevant):
- **Performance**: before/after benchmark (same harness)
- **Runtime behavior**: logs/tracing summary (OTel only if already in stack)

---

## ReasonCodes v0 (SSOT) — seed set
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

## EvidenceCapsule v0 (SSOT) — minimum fields
Required fields (minimum):
- id, packet_id, base_ref, commit, timestamp
- status (PASS|FAIL|BLOCKED)
- reason_codes[]
- commands_run[]
- checks[] (tests/lint/type/bench results)
- diffstat (files, insertions, deletions) + touched_files[]
- artifacts[] (path + hash)
- decision_trace (path + line_count)

---

## Open items (next edits)
1. Finalize **Observability standard** (log keys, span naming, correlation propagation).
2. Finalize **Benchmarking standard** (baseline format, variance handling, thresholds).
3. Finalize **Dependency rule enforcement** (imports/deps constraints + harness).
4. Finalize **Promotion protocol** (WORK → PROMOTE) as a mechanical gate.

