## Agent-skill extraction matrix

Assumption carried forward from your note: the default agent Python environment is **marimo**, and the runtime should favor **structured outputs** plus **NDJSON/JSONL** event streams. I treat that as a design constraint below.

### Recommended shape of the stack

```text
marimo notebook/runtime
  -> ndjson/jsonl event stream
  -> typed boundary objects (Pydantic)
  -> structured-output backend (Instructor / Outlines / Formatron / etc.)
  -> constraint/admissibility layer (CUE)
  -> fuzz/property tests (Hypothesis)
  -> failure artifacts -> gotchas / regressions / repair hints
```

---

## Matrix

| Library                | Candidate skill                       | Role in stack                                                                | Best first prototype                                                                                   | Likely gotchas                                                                                                                   | Marimo / NDJSON fit                                                                                                                                   |
| ---------------------- | ------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pydantic**           | `typed-boundary-model`                | Canonical runtime models for task, skill, profile, failure, event            | Define `Task`, `SelectionResult`, `FailureRecord`, `StreamEvent`; emit JSON Schema from models         | Silent coercions if not using strict config; unions and defaults can hide ambiguity; version drift across Pydantic features      | Excellent. Use as the schema for notebook cell I/O and NDJSON event records. ([GitHub][1])                                                            |
| **Instructor**         | `structured-output-validator`         | LLM-to-Pydantic extraction and repair-friendly structured output             | A marimo cell that requests a model response and validates directly into `TaskPlan` or `SkillDecision` | Provider behavior differs; “valid JSON” is not the same as “right schema”; retry/repair loops can mask upstream weakness         | Excellent for notebook-centric typed extraction; can stream structured chunks into NDJSON event envelopes. ([GitHub][1])                              |
| **Outlines**           | `grammar-constrained-output`          | Schema/regex/CFG-constrained generation                                      | Compare freeform JSON vs constrained JSON for `FailureRecord` and `ActionSpec`                         | Grammar-constrained output can still encode semantically wrong values; CFG/schema maintenance can become its own contract burden | Strong fit where notebook cells need predictable machine-readable output; good candidate for emitting line-delimited structured events. ([GitHub][1]) |
| **DSPy**               | `typed-program-selector`              | Higher-level typed prompting/program optimization                            | Typed router experiment: `Task -> SkillDecision` with reproducible signatures                          | Can add abstraction before the contract plane is stable; optimization layer may obscure simple failure causes                    | Good later, not first. Better after core marimo event contracts are stable. ([GitHub][1])                                                             |
| **PydanticAI**         | `agent-runtime-typed`                 | Agent framework with typed Python ergonomics                                 | Compare a minimal typed agent loop against your current marimo-first runtime                           | Risk of overlapping with your own control-plane abstractions; framework may fight notebook-native execution flow                 | Worth evaluating as a comparison harness, not as the initial source of truth. ([GitHub][1])                                                           |
| **Formatron**          | `template-constrained-output`         | Constrained decoding with templates, regex, CFG, JSON Schema, Pydantic       | Emit typed NDJSON command/event records from template-backed decoding                                  | Template complexity can grow quickly; f-string templating plus grammar logic needs careful testing                               | Very good fit for structured notebook event emission and constrained task/result packets. ([GitHub][1])                                               |
| **SGLang**             | `fast-json-decoder`                   | High-performance constrained decoding via regex or Pydantic models           | Benchmark constrained decoding of `StreamEvent` payloads                                               | Runtime/backend assumptions may not align with your default environment; optimize later, not first                               | Good for performance-focused local backends if marimo remains the orchestration shell. ([GitHub][1])                                                  |
| **transformers-cfg**   | `local-cfg-output`                    | CFG-constrained decoding for HF Transformers, supports JSON mode/JSON Schema | Local-model constrained generation benchmark for `FailureRecord` and `ToolCall`                        | Best when you already know you want HF-local inference; more backend-specific than control-plane-specific                        | Useful for local experimental lanes, less central to notebook-first runtime control. ([GitHub][1])                                                    |
| **SynCode**            | `multi-format-grammar-output`         | Grammar-guided generation across JSON, YAML, code languages                  | Test whether one grammar system can cover JSON plus config/code artifacts                              | Easy to overgeneralize; JSON success does not imply code/config success                                                          | Interesting if you want the same notebook runtime to emit both JSON events and typed config/code artifacts. ([GitHub][1])                             |
| **guidance**           | `programmatic-constrained-generation` | Interleave Python logic, tools, and constrained generation                   | Build a notebook cell that mixes tool results with structured output constraints                       | Can become prompt-programming-heavy; may duplicate control flow you already want in Python/CUE                                   | Potentially useful in marimo because code cells already provide the Python control layer. ([GitHub][1])                                               |
| **LiteLLM**            | `provider-agnostic-structured-call`   | Provider normalization layer for tool calling / function calling / JSON mode | One adapter that normalizes model calls into a common `ModelResponseEnvelope`                          | Normalized provider API does not normalize provider behavior; still need your own validation layer                               | Strong glue layer for notebook-driven experiments that switch providers while keeping NDJSON envelopes stable. ([GitHub][1])                          |
| **LlamaIndex**         | `structured-retrieval-output`         | Higher-level structured output modules and Pydantic programs                 | Retrieval-to-typed-object prototype                                                                    | Can pull you upward into app-framework concerns too early                                                                        | Better for retrieval-heavy lanes than for the core routing substrate. ([GitHub][1])                                                                   |
| **LangChain**          | `tool-call-normalizer`                | Broad integration/tooling surface with structured outputs                    | Minimal comparison prototype only                                                                      | Too broad for source-of-truth contracts; easy to inherit framework shape accidentally                                            | Treat as adapter/comparison layer, not the control plane. ([GitHub][1])                                                                               |
| **FuzzTypes**          | `input-normalization-repair`          | Pydantic extensions for autocorrecting/normalizing messy values              | Normalize noisy external task/event payloads before strict validation                                  | Autocorrection can hide poor upstream contracts if overused                                                                      | Strong adjunct for notebook ingress points and messy streamed inputs. ([GitHub][1])                                                                   |
| **Mirascope / Marvin** | `ergonomic-structured-extraction`     | Lightweight structured extraction / natural-language interfaces              | Small comparison spike only                                                                            | Convenience-first layers may blur contract boundaries                                                                            | Secondary. Useful if you later want lighter-weight user-facing extraction tools. ([GitHub][1])                                                        |

---

## Best initial skill set

Given your constraints, I would start with six concrete skills.

### 1. `typed-boundary-model`

**Primary libs:** Pydantic
**Purpose:** all notebook/runtime records become typed models.

**Objects to define first**

* `Task`
* `TaskConstraints`
* `SkillDecision`
* `FailureRecord`
* `RepairHint`
* `StreamEvent`
* `NotebookArtifactRef`

**Why first**
Everything else becomes much easier once NDJSON/JSONL lines map to strict models.

---

### 2. `structured-output-validator`

**Primary libs:** Instructor + Pydantic
**Purpose:** get model output into typed objects with explicit validation and repair paths.

**First prototype**

* marimo cell sends a prompt
* response is validated into `TaskPlan`
* success/failure is emitted as NDJSON lines:

  * `generation.started`
  * `generation.completed`
  * `validation.failed`
  * `repair.suggested`

**High-signal gotcha**
Do not treat “parsed successfully” as “decision is admissible.”

---

### 3. `grammar-constrained-output`

**Primary libs:** Outlines
**Purpose:** shift structure enforcement earlier than post-hoc parsing.

**First prototype**
Generate a `FailureRecord` or `ToolCall` as constrained JSON and compare:

* raw prompting
* Instructor validation
* Outlines constrained generation

**What to measure**

* parse success rate
* schema adherence
* semantic error rate
* repair frequency

---

### 4. `template-constrained-output`

**Primary libs:** Formatron
**Purpose:** constrained event generation for notebook-oriented streaming.

**First prototype**
Generate NDJSON `StreamEvent` lines constrained by:

* event type enum
* payload schema
* timestamp format
* status codes

This is especially aligned with your marimo + NDJSON/JSONL runtime.

---

### 5. `provider-agnostic-structured-call`

**Primary libs:** LiteLLM
**Purpose:** swap providers without rewriting notebook orchestration.

**First prototype**
Common response envelope:

```python
class ModelResponseEnvelope(BaseModel):
    provider: str
    model: str
    mode: Literal["json_mode", "tool_call", "freeform", "grammar"]
    raw_text: str | None = None
    parsed: dict | None = None
    usage: dict | None = None
```

Then every cell emits the same NDJSON envelope regardless of provider.

---

### 6. `input-normalization-repair`

**Primary libs:** FuzzTypes + Pydantic
**Purpose:** canonicalize messy inbound data before the strict contract layer.

**First prototype**
Normalize:

* emails
* dates
* paths
* URLs
* custom IDs

before they hit `Task` or `Profile` validators.

---

## Stronger notebook-native event model

Because marimo is the default environment, I would make **structured event streaming** a first-class contract.

### Suggested NDJSON event types

```json
{"type":"task.received","task_id":"t-001","payload":{...}}
{"type":"task.normalized","task_id":"t-001","payload":{...}}
{"type":"selection.started","task_id":"t-001"}
{"type":"selection.rejected","task_id":"t-001","failure":{...}}
{"type":"selection.completed","task_id":"t-001","decision":{...}}
{"type":"generation.started","task_id":"t-001"}
{"type":"generation.completed","task_id":"t-001","artifact":{...}}
{"type":"validation.failed","task_id":"t-001","failure":{...}}
{"type":"repair.suggested","task_id":"t-001","repair":{...}}
```

### Why this matters

It gives you:

* replayable notebook runs
* regression fixtures
* fuzzable event streams
* traceable failure promotion into gotchas

---

## Skill-to-runtime mapping for marimo

| Concern                                  | Best library         | Why                                                        |
| ---------------------------------------- | -------------------- | ---------------------------------------------------------- |
| Typed notebook state and messages        | Pydantic             | Strongest boundary object layer                            |
| Structured extraction into typed objects | Instructor           | Direct path from LLM output to models                      |
| Harder output constraints                | Outlines / Formatron | Best fit for predictable machine-readable notebook outputs |
| Multi-provider experiments               | LiteLLM              | Normalizes call surface                                    |
| Higher-level agent experiments           | PydanticAI / DSPy    | Compare later, do not anchor on them first                 |
| Input cleanup                            | FuzzTypes            | Good ingress normalization before strict validation        |

---

## Suggested first implementation order

### Phase 1 — stabilize the boundary

* Pydantic
* NDJSON `StreamEvent`
* `FailureRecord`
* `SkillDecision`

### Phase 2 — one structured-output path

* Instructor + Pydantic
* marimo cell that emits validated objects and validation failures

### Phase 3 — one constrained-decoding path

* Outlines or Formatron
* same object shape, different generation backend

### Phase 4 — compare and fuzz

* Hypothesis against:

  * `Task`
  * `StreamEvent`
  * `FailureRecord`
  * `SkillDecision`

### Phase 5 — failure promotion

* shrunk failing examples
* gotchas inventory
* regression corpus

---

## Most important design rule

Because the runtime is notebook-first:

> do not make the library the control plane

Instead:

* **marimo** = orchestration surface
* **Pydantic** = runtime contract layer
* **Instructor / Outlines / Formatron** = generation backends
* **CUE** = admissibility and legality
* **Hypothesis** = adversarial testing
* **NDJSON/JSONL** = execution trace

That keeps the substrate clean.

---

## Concrete initial shortlist

If you want the tightest first slice:

1. **Pydantic**
2. **Instructor**
3. **Outlines**
4. **LiteLLM**
5. **FuzzTypes**
6. **Hypothesis** as the test layer
7. **CUE** as the admissibility layer outside the Python library shortlist

That gives you:

* typed objects
* structured extraction
* constrained output
* provider normalization
* ingress normalization
* fuzz/property testing
* constraint routing

---

## Bottom line

For a **marimo + structured outputs + NDJSON/JSONL** default runtime, the highest-signal library extraction is:

* **Pydantic** as the boundary
* **Instructor** as typed extraction
* **Outlines / Formatron** as constrained output backends
* **LiteLLM** as provider glue
* **FuzzTypes** as ingress normalization
* **DSPy / PydanticAI** as later comparison layers, not the initial foundation

The repo’s Python library section directly supports those capabilities: typed Pydantic-backed validation, constrained generation with regex/JSON Schema/Pydantic/CFGs, provider normalization for function calling and JSON mode, and normalization-oriented Pydantic extensions. ([GitHub][1])

I can turn this into a concrete repo skeleton next: `models.py`, `events.py`, `skills/`, `tests/fuzz/`, and a `marimo` notebook layout.

[1]: https://github.com/imaurer/awesome-llm-json?tab=readme-ov-file "GitHub - imaurer/awesome-llm-json: Resource list for generating JSON using LLMs via function calling, tools, CFG. Libraries, Models, Notebooks, etc. · GitHub"
