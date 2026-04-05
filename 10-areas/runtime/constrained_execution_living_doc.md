# Constrained Execution - Living Doc

## Status
Draft baseline for constrained execution runtime and pattern-registry design.

## Purpose
This document captures the current implementation blueprint for a constrained execution system where admissibility, pattern selection, structured execution, and failure promotion are first-class concerns.

---

## 1. System Goal

Build an agent-skill runtime where:

- **CUE** filters admissible patterns, profiles, and routes
- **DSPy** provides high-signal program skeletons
- **Guidance** provides canonical good-op generation helpers
- **Pydantic** defines runtime boundary models
- **Hypothesis** fuzzes the whole pipeline
- **marimo** is the default execution and inspection surface
- **NDJSON/JSONL** captures structured traces
- failures promote into:
  - regressions
  - gotchas
  - tighter constraints
  - stronger good-op helpers

---

## 2. Core Architecture

```text
task request
  -> normalize into Pydantic Task
  -> CUE admissibility filter
  -> choose high-fidelity DSPy pattern
  -> attach Guidance helpers
  -> execute in marimo runtime
  -> stream NDJSON trace
  -> validate outputs/assertions
  -> if fail: structured failure artifact
  -> retry inside constrained envelope
  -> promote interesting failures into corpus/gotchas/regressions
```

---

## 3. Repository Shape

```text
agent_runtime/
  contracts/
    task.schema.json
    failure.schema.json
    task.cue
    profile.cue
    pattern.cue
    route.cue

  models/
    task.py
    profile.py
    pattern.py
    result.py
    failure.py
    trace.py

  registry/
    patterns/
      planner_executor_verifier/
        pattern.yaml
        dspy_program.py
        guidance_helpers.py
        examples/
        negatives/
      typed_extraction/
        pattern.yaml
        dspy_program.py
        guidance_helpers.py
      contract_transform/
        pattern.yaml
        dspy_program.py
        guidance_helpers.py

    corpora/
      design_patterns/
      negative_patterns/
      gotchas/
      regressions/

  runtime/
    selector.py
    planner.py
    executor.py
    retry.py
    promotion.py
    trace_writer.py

  tests/
    unit/
    property/
    fuzz/
      strategies/
      corpus/
      regressions/

  notebooks/
    pattern_workbench.py
    selector_workbench.py
    fuzz_workbench.py
```

---

## 4. Main Runtime Objects

### `Task`

Represents the normalized request.

```python
class Task(BaseModel):
    kind: Literal[
        "extract", "transform", "implement", "summarize",
        "research", "verify", "plan"
    ]
    substrate: Literal["json", "cue", "python", "markdown", "mixed"] | None = None
    inputs: dict
    constraints: dict
    profile: str | None = None
```

### `PatternSpec`

Represents a registry entry for a DSPy-backed pattern family.

```python
class PatternSpec(BaseModel):
    pattern_id: str
    family: str
    task_kinds: list[str]
    substrates: list[str]
    required_guidance_helpers: list[str]
    assertions: list[str]
    supports_retry: bool = True
    fidelity_class: Literal["high", "medium", "low"]
```

### `FailureRecord`

Structured failure explanation.

```python
class FailureRecord(BaseModel):
    code: str
    stage: str
    message: str
    reason_classes: list[str]
    path: str | None = None
    mitigation: str | None = None
    gotcha_candidate: bool = False
```

### `TraceEvent`

NDJSON event stream unit.

```python
class TraceEvent(BaseModel):
    ts: datetime
    run_id: str
    stage: str
    event_type: str
    payload: dict
```

---

## 5. Registry Structure

Each pattern should be a first-class registry object.

### Example `pattern.yaml`

```yaml
pattern_id: contract_transform.v1
family: typed_contract_transform
task_kinds:
  - transform
  - implement
substrates:
  - json
  - cue
required_guidance_helpers:
  - emit_patch_object
  - emit_failure_reason
assertions:
  - output_parses
  - contract_valid
  - targets_exist
fidelity_class: high
retry_policy:
  max_attempts: 2
  mutable_stages:
    - draft
    - verify
  immutable_constraints:
    - output_format=json
    - stage_topology=fixed
corpora:
  positive:
    - examples/valid_patch_01.json
  negative:
    - negatives/missing_path_01.json
```

---

## 6. CUE’s Role

CUE should filter:

- task ↔ pattern compatibility
- pattern ↔ profile compatibility
- task ↔ Guidance helper requirements
- retry envelope legality
- downstream consumer requirements

### Example responsibilities

#### `task.cue`
Defines admissible task fields and cross-field constraints.

#### `pattern.cue`
Defines which pattern families are legal for which task shapes.

#### `profile.cue`
Defines runtime profiles:

- `strict_contracts`
- `offline_local`
- `research_heavy`
- `patch_safe`

#### `route.cue`
Defines admissible combinations:

- task
- profile
- pattern
- required helpers
- output constraints

This is what reduces retries up front.

---

## 7. DSPy Role

DSPy should provide reusable program skeletons, not one-off prompts.

### High-signal pattern families

#### `typed_extraction`
Stages:
- draft extraction
- schema verify
- repair extraction

#### `planner_executor_verifier`
Stages:
- plan
- execute
- verify
- summarize

#### `contract_transform`
Stages:
- inspect contract
- draft transform
- validate transform
- repair transform

#### `retrieval_synthesis_verify`
Stages:
- retrieve
- synthesize
- evidence check
- structured output

#### `draft_critique_repair`
Stages:
- produce initial artifact
- critique against assertions
- repair inside same pattern family

These become registry-backed skill patterns.

---

## 8. Guidance Role

Guidance helpers should be canonical good-op functions.

These are not generic prompts. They are reusable local emitters and scaffolds.

### Good-op helper examples

#### Output helpers
- `emit_json_object`
- `emit_patch_object`
- `emit_validation_report`
- `emit_contract_violation`
- `emit_structured_summary`

#### Behavior helpers
- `stay_within_schema`
- `omit_prose_when_json_required`
- `require_evidence_block`
- `use_compact_reasoning_surface`

#### Gotcha-aware helpers
- `include_required_target_path`
- `preserve_enum_values`
- `never_mix_rationale_with_payload`
- `emit_only_allowed_patch_ops`

These should be attached to patterns by registry metadata.

---

## 9. marimo Role

marimo should be the default workbench and runtime host.

Each pattern should have a marimo notebook or workbench that exposes:

- pattern metadata
- DSPy stages
- Guidance helpers
- Pydantic models
- CUE admissibility result
- streamed NDJSON trace
- assertion results
- fuzz replay controls
- gotcha inventory
- regression examples

That makes every skill pattern:

- runnable
- inspectable
- debuggable
- teachable

---

## 10. NDJSON/JSONL Event Model

Every run should emit events like:

```json
{"stage":"selection","event_type":"task_normalized","payload":{"task_kind":"transform"}}
{"stage":"selection","event_type":"cue_filter_pass","payload":{"pattern_id":"contract_transform.v1"}}
{"stage":"execution","event_type":"guidance_helpers_attached","payload":{"helpers":["emit_patch_object"]}}
{"stage":"execution","event_type":"assertion_failed","payload":{"assertion":"targets_exist"}}
{"stage":"retry","event_type":"retry_narrowed","payload":{"reason_code":"missing_target_path"}}
{"stage":"promotion","event_type":"gotcha_promoted","payload":{"code":"missing_target_path"}}
```

That gives structured observability.

---

## 11. Hypothesis Fuzz Pipeline

### Objectives

Fuzz:

- Pydantic model boundaries
- CUE route combinations
- DSPy pattern selection
- Guidance helper correctness
- retry narrowing behavior
- failure artifact completeness

### Test families

#### A. Boundary model fuzz
Test:
- parsing
- validation
- normalization
- serialization round-trips

Properties:
- no crashes
- normalized objects remain stable
- invalid objects produce structured errors

#### B. Selector fuzz
Generate tasks and profiles.

Properties:
- selected pattern must be admissible
- inadmissible patterns must be rejected with normalized reasons
- stricter profiles do not widen admissible set

#### C. Guidance fuzz
Generate near-miss cases around helper expectations.

Properties:
- helper-constrained output remains parseable
- helpers prevent known gotcha classes
- helpers do not leak prose into JSON-only channels

#### D. Retry fuzz
Inject stage failures.

Properties:
- retry remains inside immutable constraints
- retry does not switch pattern family illegally
- retry narrows rather than broadens search

#### E. Promotion fuzz
Feed repeated failure classes.

Properties:
- repeated failures can be promoted into gotchas
- shrunk failures persist as regression seeds
- mitigation field is populated for promotable classes

---

## 12. Hypothesis Strategy Layout

```text
tests/fuzz/strategies/
  task_strategies.py
  profile_strategies.py
  pattern_strategies.py
  failure_strategies.py
  mutation_strategies.py
```

### Strategy classes

#### Valid generators
Generate admissible:
- task
- profile
- pattern combinations

#### Contradiction generators
Generate cases like:
- `needs_files=true` with no files
- JSON-only output plus prose-heavy helper
- offline profile with web-only pattern

#### Mutation generators
Take real seeds and mutate:
- field removal
- enum corruption
- path corruption
- oversized collections
- weird unicode
- empty structured payloads

#### Corpus-driven generators
Replay:
- known regressions
- gotcha examples
- RefactoringGuru-derived examples
- negative corpus examples

---

## 13. Design-Pattern Corpus Seeding

Use `RefactoringGuru/design-patterns-python` as a seed corpus for pattern priors.

Not as “copy this code.” Use it as:

- decomposition examples
- canonical role separation
- architecture exemplars
- naming conventions
- “which pattern fits which problem” priors

### Good uses

#### Positive seeds
- command-like task dispatch patterns
- strategy-like pattern selection
- builder-like structured artifact assembly
- adapter-like surface bridging
- template method-like stage pipelines

#### Negative seeds
Add anti-pattern corpus for:
- unnecessary abstraction
- wrong pattern selection
- overengineered hierarchy
- pattern misuse for trivial tasks

This lets DSPy and Guidance learn both:
- proper form
- pattern misuse avoidance

---

## 14. Promotion Pipeline

Every interesting failure should be promotable.

### Promotion outputs

#### Regression
Minimal replay case in `tests/fuzz/corpus/regressions/`

#### Gotcha
Human-readable operator warning in skill docs and registry

#### Guidance helper improvement
Example:
- add `include_required_target_path`

#### CUE tightening
Example:
- forbid a pattern under a stricter profile
- require helper X when output format is patch

#### DSPy assertion strengthening
Example:
- add `all_patch_ops_have_target_path`

---

## 15. Retry Model

Retries should be constrained repair, not broad resampling.

### Retry envelope should preserve
- selected pattern family
- output contract
- profile
- immutable Guidance helper set where required
- CUE-admissible route

### Retry envelope may vary
- stage-local prompt params
- stage-local examples
- specific helper variant
- one failing field or assertion context

### Retry artifact

```yaml
retry_policy:
  max_attempts: 2
  immutable:
    - pattern_family=contract_transform
    - output_format=json
    - profile=strict_contracts
  mutable:
    - draft_stage_examples
    - helper_variant
    - local assertion hint
```

---

## 16. Suggested First Implementation Slice

### Phase 1: foundational contracts
Build:
- `Task`
- `Profile`
- `PatternSpec`
- `FailureRecord`
- `TraceEvent`

Add:
- JSON Schema
- Pydantic models
- initial CUE admissibility definitions

### Phase 2: one real pattern family
Implement one high-signal pattern:
- `contract_transform.v1`

Include:
- DSPy program skeleton
- 3–5 Guidance helpers
- marimo workbench
- NDJSON trace

### Phase 3: fuzz layer
Add Hypothesis tests for:
- selector admissibility
- structured failure completeness
- retry immutability
- helper correctness

### Phase 4: promotion loop
Persist:
- shrunk failures
- gotchas
- regression seeds

### Phase 5: broaden registry
Add:
- `typed_extraction`
- `planner_executor_verifier`
- `retrieval_synthesis_verify`

---

## 17. Success Criteria

This is working when:

- pattern selection is explainable
- retries are rare and local
- failures are structured and classifiable
- gotchas are generated from actual evidence
- helpers reduce repeat failure classes
- fuzz testing regularly produces useful shrunk cases
- marimo workbenches make patterns easy to inspect and refine

---

## 18. Concrete Minimal Deliverables

Start with these files:

```text
contracts/task.cue
contracts/profile.cue
contracts/pattern.cue
models/task.py
models/profile.py
models/pattern.py
models/failure.py
runtime/selector.py
runtime/retry.py
registry/patterns/contract_transform/pattern.yaml
registry/patterns/contract_transform/dspy_program.py
registry/patterns/contract_transform/guidance_helpers.py
tests/property/test_selector.py
tests/fuzz/test_retry_properties.py
notebooks/pattern_workbench.py
```

---

## 19. Recommended Pattern Priorities

Implement in this order:

1. **contract_transform**
2. **typed_extraction**
3. **planner_executor_verifier**
4. **retrieval_synthesis_verify**
5. **draft_critique_repair**

This keeps the first slice close to the JSON/CUE/Python-heavy workflow.

---

## 20. Bottom Line

The high-confidence stack is:

- **CUE** for admissibility and route narrowing
- **DSPy** for high-fidelity program patterns
- **Guidance** for canonical good-op helpers
- **Pydantic** for runtime contracts
- **Hypothesis** for adversarial pressure and shrunk regressions
- **marimo** for execution and workbench inspection
- **NDJSON/JSONL** for observable structured traces

That gives a system that is:

- constrained before execution
- structured during execution
- testable under adversarial inputs
- repairable on failure
- continuously improved by promotion of failures into assets

## Immediate Next Move

Draft the actual `pattern.yaml`, `task.cue`, `selector.py`, and `guidance_helpers.py` skeleton for `contract_transform.v1`.

