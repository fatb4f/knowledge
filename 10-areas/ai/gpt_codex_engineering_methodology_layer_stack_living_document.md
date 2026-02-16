# GPT–Codex Engineering Methodology Layer Stack

**Status:** Living document (iterative)

**Purpose**
Define a repeatable methodology for daily work (refactors, features, optimization, testing, content-gen, exploration) using GPT↔Codex exchange patterns, with **code-shape containers**, **signals**, **gates**, **failure prediction**, and translation into **packet contracts**.

---

## Layer stack

### L0 — Foundations (Principles)
- **Loop premise:** iterate until **desired state** is met (measured via gates).
- **3 pillars lens:**
  - *Computation as a System* (budgets, resources, determinism)
  - *Statistics as Inference* (measurement, baselines, verification)
  - *Control & Adaptation* (feedback signals, bounded updates)
- **Evidence-first collaboration:** every meaningful run yields an evidence capsule.

**Outputs**
- Principle checklist (immutable)
- Reason-code taxonomy (shared vocabulary)

---

### L1 — Operational loop (Daily driver)
- **Card → Run → Evidence → Next card**
- Mode selector:
  - GPT-first: unclear “done” / design risk / measurement setup
  - Codex-first: mechanical change / reproduce-fix-verify loops
- Stop rules (default pick 2): 2-strike, iteration cap, diff budget, evidence completeness.

**Outputs**
- Task Card template
- Evidence template

---

### L2 — Coordination patterns (Workflow topologies)
- Linear pipeline
- Contract-first pipeline
- Cyclic rotation
- Adversarial review
- Hypothesis-driven investigation
- Coordinator–specialist (fan-out)
- Adaptive entry point

**Outputs**
- Pattern-specific work methodology (step list + gates + evidence)
- Pattern chooser (decision rules)

---

### L3 — Control containers (Code “containers”)
**Definition**: repeatable code wrappers that enclose variable business logic but always ship:
- signals (logs/metrics/traces/counters)
- gates (tests/invariants/benchmarks/schema)
- failure prediction (detectors + reason codes)
- recovery (rollback/fallback/retry budgets)
- evidence capsule (standard artifact)

**Baseline controls (high ROI)**
- Structured logging + correlation id
- Time/iteration budget guards
- Retry budget (bounded)
- Boundary validation
- Error taxonomy
- Characterization tests for refactors

**Outputs**
- Minimal container API (Budget, Invariant, Signals, EvidenceCapsule, ReasonCodes)
- Container library: controlled_function, pipeline_stage, troubleshoot_probe, refactor_safety, optimization_measure

---

### L4 — Code shape patterns (Structural shapes)
- Functional core / imperative shell
- Ports & adapters
- Pipeline / stage graph
- CQS (command/query separation)
- Orchestrator + workers
- State machine / transition table
- Policy vs mechanism split
- Validation boundary pattern
- Evidence capsule everywhere
- Error taxonomy + recovery channels

**Outputs**
- “Shape spec” checklist enforced by review/tests
- Skeleton module layouts for each shape

---

### L5 — Architecture patterns (System-level)
Boundary/dependency patterns:
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
- Boundary rules (imports, allowed deps)
- Contract tests at boundaries
- Observability standards per boundary (span names, log keys)

---

### L6 — DSAs (Data structures & algorithms) as containers
- DS selection patterns (map/set/deque/heap/tree/graph/union-find/ring buffer)
- Algo shape patterns (two pointers, monotonic structures, BFS/DFS, shortest paths, DP, greedy, divide & conquer, backtracking)

**Container requirements**
- Invariants + validate()
- Budget guard (nodes visited / time / iterations)
- Signals (counts, queue depth, branch hits)
- Property tests where applicable
- Stop reasons (ITER_LIMIT, TIMEOUT, LOOP_DETECTED, NO_SOLUTION)

**Outputs**
- DSA template library (implementation + tests + instrumentation)

---

### L7 — Translation to packet contracts (Execution governance)
**Mapping**
- actuators → allowed_paths/commands
- invariants/gates → required_checks + thresholds
- budgets → diff/time/iteration budgets
- evidence → required artifact paths + hashes
- stop reasons → reason-code taxonomy

**Outputs**
- Packet contract template
- Evidence bundle manifest format
- Promotion gate checklist

---

## Missing layers (detected)
1. **Observability standard (logging/tracing schema)**
   - Stable log keys, span naming, correlation id propagation, minimal required fields.
2. **Benchmarking/measurement standard**
   - Harness conventions, baseline capture format, variance handling, threshold policy.
3. **Boundary enforcement rules (dependency-level)**
   - Mechanical import/dependency constraints beyond path-level scoping.
4. **Promotion protocol (WORK → PROMOTE)**
   - What “promote” means mechanically (CI gate, required evidence, artifact immutability).

---

## Inner-layer gaps

### L1 gaps
- A compact **mode selector** that chooses: refactor/feature/optimization/testing/content-gen/exploration → default pattern + container.

### L2 gaps
- Per-pattern **work methodology** templates (steps, gates, evidence) as reusable blocks.

### L3 gaps
- Implementations of **failure detectors** (loop detection, flake detection, nondeterminism detection) wired into evidence emission.

### L4 gaps
- A “module skeleton” standard (manual or scripted) for each code shape.

### L5 gaps
- A mechanical **dependency rule** mechanism (import/dependency constraints) and test harness.

### L6 gaps
- A standard property-test pattern set (what properties to test per DSA/algo family).

### L7 gaps
- Canonical packet contract schema + evidence manifest schema (if not already locked as SSOT).

---

## ReasonCodes v0 (SSOT)

**Goal:** make failure prediction and troubleshooting first-class via a canonical, machine-checkable taxonomy.

**Artifact:** `control/reason_codes.yaml`

Each entry:
- `code` (stable identifier)
- `class` (budget | determinism | scope | correctness | dependency | environment | unknown)
- `detector` (how it triggers; deterministic rule)
- `default_action` (stop | retry | fallback | split_packet)
- `required_evidence` (fields/artifacts that must be present)
- `notes` (human guidance; short)

**Seed set (minimum):**
- `ITERATION_LIMIT_REACHED`
- `TIME_LIMIT_EXCEEDED`
- `COST_BUDGET_EXCEEDED`
- `LOOP_DETECTED`
- `FLAKY_TEST_DETECTED`
- `NONDETERMINISM_DETECTED`
- `SCHEMA_DRIFT`
- `SCOPE_CREEP_DETECTED`
- `MISSING_EVIDENCE`
- `DEPENDENCY_RULE_VIOLATION`
- `BENCHMARK_REGRESSION`

---

## EvidenceCapsule v0 (SSOT)

**Goal:** standardize what every run emits so debugging and promotion gating are uniform.

**Artifact:** `control/schemas/evidence_capsule.schema.json`

Required fields (minimum):
- `id`, `packet_id`, `base_ref`, `commit`, `timestamp`
- `status` (PASS|FAIL|BLOCKED)
- `reason_codes[]`
- `commands_run[]`
- `checks[]` (tests/lint/type/bench results)
- `diffstat` (files, insertions, deletions)
- `artifacts[]` (path + hash)

---

## ContainerContract v0 (SSOT)

**Goal:** formalize the “how to code this” wrapper as a reusable unit.

**Artifact:** `control/schemas/container_contract.schema.json`

A container declaration must include:
- `name`, `purpose`, `shape` (core/shell | ports/adapters | pipeline_stage | state_machine | etc.)
- `signals` (required log keys, span names, counters)
- `gates` (required tests/invariants/benchmarks)
- `failure_modes` (reason codes + detectors)
- `recovery` (retry budget, fallback, rollback)
- `evidence` (what must be emitted; ties to EvidenceCapsule)

**Note:** pattern choice is not “always code arrays like X”; it is the output of constraints (plant state + risk + budgets + boundary rules).

---

## Packet rendering (contracts)

**Goal:** deterministically render from SSOT policy + container declarations into packet contracts.

Artifacts:
- `control/schemas/packet_contract.schema.json`
- `control/schemas/evidence_manifest.schema.json`

---

## Next smallest deliverables (recommended order)
1. **ReasonCodes v0**: commit `control/reason_codes.yaml` (stable codes + detectors + actions).
2. **EvidenceCapsule v0**: commit schema + require emission per packet.
3. **ContainerContract v0**: commit schema + one reference container declaration.
4. **Packet rendering v0**: deterministic render to packet contracts + evidence manifest.
5. **Pattern methodology blocks v0**: one-page template per coordination pattern.

---

## Maturity model (projection)

**Scale**
- **L0 Ad hoc:** conventions only; no stable artifacts.
- **L1 Documented:** human-readable templates; partial consistency.
- **L2 Contracted:** schemas + required fields; SSOT exists.
- **L3 Mechanically enforced:** CI/preflight denies on violations; evidence audited.
- **L4 Measured:** benchmarks/observability standards enforced; drift + flake detectors active.
- **L5 Adaptive:** policies/budgets tuned using evidence; auto-splitting/routing mature.

**Current state (projected)**
- **Control Kernel + OPA gating:** **L3** (strong allow/deny + audit artifacts).
- **Packet execution discipline (worktrees, evidence paths):** **L3** (mechanically bounded execution).
- **Reason codes:** **L1 → L2 (pending)** (not yet SSOT-enforced; now specified for SSOT).
- **Evidence capsule schema:** **L1 → L2 (pending)** (template-like today; schema needs locking).
- **Container contracts:** **L1 → L2 (pending)** (concept present; needs schema + declarations).
- **Architecture boundary enforcement (dependency rules):** **L1** (path-level exists; dep-level pending).
- **Observability standard:** **L1** (needs log/span key spec + enforcement).
- **Benchmark/measurement standard:** **L1** (needs harness + thresholds).
- **Pattern methodology blocks (work topologies):** **L1** (catalogued; templates pending).

**Overall maturity:** **L2** (contracts emerging) with **L3 strength in execution governance**.

