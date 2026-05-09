# 1) Architecture outline

## 1.1 System goal
A repo-backed supervisory control system that prevents MRV overshoot by:
- enforcing **mechanical observability tests** (O-tests),
- gating work via **schema-backed time-block contracts**,
- coupling a **Human Plant Supervisor** (fatigue/mode) with an **Execution Ledger Supervisor** (legality/ledger),
- ensuring deterministic **timer-to-timer** state transitions and audit logging.

## 1.2 Components

### A) Human Plant Supervisor (HPS)
**Responsibility:** classify fatigue and enforce mode monotonicity.
- **State:** `(mode ∈ {GREEN,YELLOW,RED}, fatigue_band ∈ {OK,RISING,NEAR_LIMIT}, timer_phase ∈ {WORK,RESET_SHORT,RESET_LONG})`
- **Inputs:** O-tests results, friction triggers, timer events, previous end pointer (mode/band at end)
- **Outputs:** `downgrade_mode`, `force_close_block`, `run_reset_protocol`, `recommend_next_mode`

### B) Execution Ledger Supervisor (ELS)
**Responsibility:** prevent illegal work by requiring a valid active block contract and logging state.
- **State:** `(block_state ∈ {UNDEFINED,DEFINED,CLOSED}, active_block_id?, timer_phase)`
- **Inputs:** plan proposals, schedule gates (Context/Deferred windows), previous end pointer, HPS snapshot
- **Outputs:** `define_block/deny_block`, `enforce_boundary`, `append_event`, `close_block`, `emit_end_pointer`

### C) Scheduler Gate (SG)
**Responsibility:** declare legality windows.
- **Inputs:** weekly schedule template (Deferred Windows, Context Blocks)
- **Outputs:** `is_context_block`, `is_deferred_window`

### D) Policy + Catalog (PC)
**Responsibility:** deterministic mapping from observations to actions.
- O-tests catalog (procedures, pass/fail criteria)
- classifier (FAIL count → fatigue_band)
- action policy (band/mode/window → required outputs)

### E) Artifacts / Ledger
**Responsibility:** auditable SSOT of execution.
- schemas: `time_block`, `end_pointer`, `otest_result`, `preflight_snapshot`
- append-only session log events
- `deferred.md` with tags `[MECH]/[SYL]/[CTX]`

## 1.3 Coupling / dependency
- HPS produces **max allowed intensity** (`recommended_mode`, `band`).
- ELS may only define/continue a block whose `mode_at_start ≤ recommended_mode` and whose pattern legality passes SG.

## 1.4 Work pattern classes
- **SYL (lower MRV risk):** INF* syllabus-aligned work.
- **CTX (high MRV risk):** contextual work around syllabus; legal only in Context Blocks or Deferred Windows.

## 1.5 Control loop sequence

### Preflight (before Plan-Gen)
1. Run O-tests → classify band.
2. Apply monotone mode rule from `prev_end_pointer`.
3. Emit `preflight_snapshot`.

### Plan-Gen (2–3 hours)
- Generate ≤3 blocks, each with a block contract.
- Enforce legality: at most one CTX block/day; CTX only inside scheduled windows.

### Execution (timer-to-timer)
- On each work tick end: reset + O-tests + reclassify + enforce downgrades/close.
- ELS logs each tick and emits end pointers on close.

---

# 2) Tooling selection and scope

## 2.1 Tooling options (repo-backed)

### Option A: Local repo + Python tools (primary)
- `python` scripts provide deterministic gates and logging.
- LLM (ChatGPT/Codex) generates proposals only.

### Option B: Codex CLI + repo (executor)
- Best for applying multi-file changes and maintaining skill-based constraints.
- Works well with existing CBIA/Codex discipline.

### Option C: ChatGPT CLI + repo (planner)
- Best for interactive plan-gen and spec iteration.

## 2.2 Scope boundaries (v0)

### In-scope
- Schema definitions
- Tooling to validate and generate block contracts
- O-test prompts + result logging
- Mode/band policy enforcement
- Deferred windows / context legality gating
- Append-only ledger and end pointers

### Out-of-scope (v0)
- Direct GitHub Projects automation (optional later)
- Full calendar integration (gcal/ifttt) (later)
- ML-based prediction of MRV (not required)
- Fine-grained biometric sensing (optional later)

## 2.3 Recommended split of responsibilities
- **LLM:** propose plans/blocks, draft docs.
- **Repo tools:** decide legality/validity, enforce gates, write logs.

---

# 3) Engineering requirements: coverage + gaps

## 3.1 Requirements (E)

### E1 Deterministic state representation
- All controller-relevant state is serializable: mode, band, timer_phase, block_state.

### E2 Schema-backed contracts
- `time_block` and `end_pointer` must validate with JSON Schema.

### E3 Deterministic policy evaluation
- O-tests → band classifier is deterministic.
- band/mode/window → actions are deterministic.

### E4 Timer-to-timer transitions
- Both supervisors advance state on each timer event.

### E5 Auditability
- Append-only event log with timestamps and summaries.
- Evidence artifacts referenced by path/id.

### E6 Boundary enforcement
- Block contract declares allowed paths + illegal moves.
- Tool denies actions outside the boundary (initially as policy + review; later as repo-level checks).

### E7 Tool ergonomics
- Commands are single-shot, low-friction, minimal prompts.

## 3.2 Current coverage
- Conceptual model defined (HPS/ELS + timer-to-timer).
- O-tests proposed and classifier defined.
- Issue schema drafted and separated from validation tooling.

## 3.3 Gaps (engineering)
- Implement JSON Schemas for `time_block`, `end_pointer`, `otest_result`, `preflight_snapshot`.
- Implement deterministic policy files (`otests.yaml`, `policy.yaml`, `schedule.yaml`).
- Implement toolchain:
  - `preflight_eval.py`
  - `plan_gen.py` (proposal only)
  - `define_block.py` / `validate_block.py`
  - `close_block.py`
  - `append_event.py` (or integrated)
  - `validate_issue.py` (workflow policy)
- Define a canonical log/event format and storage layout.

---

# 4) Operations requirements: coverage + gaps

## 4.1 Requirements (O)

### O1 Simple daily operation
- Start-of-session: `preflight` → `plan-gen` → `define-block`.
- During session: timer rings → reset + (mini) O-tests + log.
- End-of-session: close block → emit end pointer.

### O2 Weekly cadence support
- Deferred Windows 2×/week (60–90m) with triage/execute/stabilize.
- Context Blocks scheduled explicitly; CTX illegal otherwise.

### O3 Failure modes are safe
- If uncertain PASS/FAIL → treat as FAIL.
- If schema invalid or missing block → notes-only.

### O4 Minimal cognitive overhead
- Logging is 1-line.
- O-tests are ≤60s.

### O5 Portability
- Works offline in a local repo.

## 4.2 Current coverage
- Reset oscillator protocol defined.
- Deferred window rules defined.
- Mode monotonicity rule defined.

## 4.3 Gaps (operations)
- Define exact CLI commands and defaults.
- Define the “notes-only” fallback workflow.
- Define weekly schedule template and how it is stored/edited.
- Define how to select ≤2 deferred items and record selection.
- Define housekeeping: archive logs, rotate sessions, backups.

---

# Next deliverable (when ready)

- Convert this document into a living SSOT: `docs/living.md` plus:
  - `control/schemas/*.schema.json`
  - `control/catalog/otests.yaml`
  - `control/catalog/policy.yaml`
  - `control/catalog/schedule.yaml`
  - `tools/*.py` stubs with deterministic interfaces

