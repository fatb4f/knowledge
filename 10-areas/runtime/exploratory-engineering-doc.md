# Exploratory Engineering Document
## Gate-First Packet Lifecycle with Hof, CUE, Kernel Contracts, and Marimo Evidence

## Status
Exploratory.

This document captures a proposed architectural direction for refactoring plan, implement, and packet generation around promotion gates, contract-defined packet requirements, and reproducible evidence bundles.

---

## 1. Summary

The current direction replaces a step-oriented execution model with a gate-oriented packet lifecycle.

Instead of treating plan and implement as sequences of prescribed steps, the system defines:

- artifact states
- promotion requirements
- gate results
- evidence requirements
- promotion edges

Under this model:

- **Kernel** defines the required schemas, manifests, evidence classes, and promotion requirements for each phase.
- **CUE** defines admissible artifact state, local invariants, and promotion legality.
- **Hof** becomes the main control-plane tool for generating plan and packet artifacts, routing targets, executing gates, and packaging evidence.
- **Python** remains a thin task implementation layer.
- **Just** remains an operator-facing command surface.
- **marimo** becomes the default execution and replay environment, and potentially part of the evidence itself.

This shifts the execution DAG from a chain of tasks to a chain of promotion states.

---

## 2. Problem Statement

Several tensions motivate this refactor:

1. **Step chains are too brittle.**
   They encode one expected route through a problem, even when multiple valid routes exist.

2. **Plan artifacts are too procedural.**
   A plan should define admissible target state and required proof, not a brittle sequence of actions.

3. **Registries and inventories drift.**
   Hand-maintained projections such as skill registries are prone to surface drift and should be generated.

4. **Evidence is under-modeled.**
   Logs and outputs are not sufficient. The packet should capture the execution environment, replay recipe, and introspection state.

5. **Runtime and semantic authority are blurred.**
   Contracts and promotion rules should live in kernel/CUE, while runtime orchestration should live in Hof.

---

## 3. Architectural Thesis

### 3.1 Control-plane split

The stable split is:

- **Kernel**: semantic authority
- **CUE**: admissibility plane
- **Hof**: orchestration and generation plane
- **Python**: execution substrate
- **Just**: operator shell
- **marimo**: execution, replay, and evidence surface

### 3.2 Promotion-first model

The system should no longer be centered on:

```text
prepare -> build -> validate -> review -> implement -> test -> evidence
```

It should instead center on:

```text
candidate artifact -> gate results -> promotable artifact -> promoted artifact -> next phase
```

### 3.3 Packet-first execution

The packet is not a side effect of execution.
It is a first-class artifact family.

Each phase produces:

- a constrained artifact
- a packet describing the artifact and required proof
- gate results
- execution evidence
- promotion state

---

## 4. Kernel as Promotion Authority

Kernel should define a set of schemas and manifests required for each phase of the packet lifecycle.

These kernel definitions can be migrated into CUE and bundled as promotion requirements.

### 4.1 Kernel responsibilities

Kernel should define:

- phase schemas
- manifest schemas
- evidence requirements
- allowed promotion edges
- packet completeness rules
- gate result schemas
- replay requirements
- introspection requirements

### 4.2 Proposed kernel families

```text
kernel/
  schemas/
    plan.cue
    implement.cue
    packet.cue
    gate_result.cue
    evidence_bundle.cue
    execution_envelope.cue
    replay_recipe.cue
    introspection_snapshot.cue
  manifests/
    phase_requirements.cue
    promotion_edges.cue
  policy/
    admissibility.cue
    evidence_requirements.cue
    packet_completeness.cue
```

### 4.3 Phase-oriented definitions

A likely shape is:

```text
#PlanCandidate
#PlanPacket
#PlanPromotable
#PlanPromoted

#ImplementCandidate
#ImplementPacket
#ImplementPromotable
#ImplementPromoted
```

This supports promotion as a chain of admissible states rather than a checklist of tasks.

---

## 5. Plan and Implement as Constrained Artifacts

### 5.1 Shift in meaning

Plan and implement should be modeled as constrained artifacts with embedded local invariants.

A plan is no longer primarily:

- step 1
- step 2
- step 3

A plan becomes:

- declared scope
- target state
- required evidence
- expected gates
- promotion legality

### 5.2 Constraint placement

Each artifact should embed:

- artifact-local invariants
- field relationships
- required evidence slots
- completeness rules for its own phase

Each artifact should import:

- kernel-level policy
- cross-artifact legality
- phase transition rules
- evidence class requirements

### 5.3 Promotion ladder

A useful modeling pattern is:

```text
#Base
#Candidate
#Reviewable
#Promotable
#Promoted
```

Promotion is then represented as successful unification plus deterministic gate results.

---

## 6. Hof as the Main Tool for Plan and Packet Generation

For generating plan files and packet files, Hof should be the main tool.

### 6.1 Hof responsibilities

Hof should own:

- git delta discovery
- surface impact routing
- target fan-out
- gate execution ordering
- candidate artifact generation
- packet generation
- evidence packaging
- retry loop orchestration
- replay-oriented execution wiring

### 6.2 CUE vs Hof

The clean formulation is:

- **Hof runs the loop**
- **CUE defines what passing means**
- **Python performs the work**

### 6.3 Why Hof fits

The control-plane patterns identified include:

- shared runtime context
- conditional task materialization
- changed-file routing
- selected-target fan-out
- ordered stage dependencies
- watch and rebuild loops

These make Hof a good fit for materializing plan, implement, and packet artifacts.

---

## 7. Surface Routing and Generated Inventories

### 7.1 Replace hand-maintained registries

Surface inventories and skill registries should be generated projections, not manually maintained truth.

The canonical authority should be a kernel- or control-defined surface inventory.

### 7.2 Surface routing model

Routing should not rely only on raw file globs.

Instead, it should model:

- `surface_id`
- `owned_paths`
- `derived_paths`
- `deps`
- `changed_files`
- `impacted_surfaces`
- `reasons`

This improves:

- explainability
- target selection
- transitive expansion
- packet scope derivation

### 7.3 Generated outputs

Generated projections may include:

- skill registry
- runtime routing tables
- inventory views
- packet manifests
- docs

---

## 8. Execution DAG Becomes a Chain of Promotion Gates

This is one of the major paradigm shifts.

### 8.1 Old model

Nodes are mostly actions.

### 8.2 New model

Nodes are mostly:

- candidate artifact states
- gate result objects
- promotion edges
- promoted artifact states

Tasks still exist, but they become subordinate to gates.

### 8.3 Example progression

```text
PlanCandidate
  -> ScopeGate
  -> ManifestGate
  -> EvidenceGate
  -> ReviewGate
  -> PlanPromoted
  -> ImplementCandidate
  -> MutationGate
  -> ValidationGate
  -> TestGate
  -> EvidenceBundleGate
  -> ImplementPromoted
```

This gives a cleaner basis for retry loops and promotion logic.

---

## 9. Evidence Bundle as a First-Class Packet

The packet should include both outputs and the environment that produced them.

### 9.1 Core rule

> The environment that produced the packet is part of the packet.

This evolves further into:

> Introspection of that environment is also evidence.

### 9.2 Evidence classes

The evidence bundle should include at least three classes:

#### Execution evidence

- structured outputs
- logs
- ndjson/jsonl event streams
- gate results
- task timings
- stdout/stderr records

#### Environment evidence

- runtime profile
- package lock / dependency fingerprint
- git state
- tool/runtime versions
- protocol metadata
- selected targets and flow inputs

#### Introspection evidence

- loaded packet/artifact state
- flow expansion state
- active gate set
- resolved targets/surfaces
- marimo graph snapshot
- notebook or graph lineage state
- replay inputs and recipe

### 9.3 Proposed evidence layout

```text
packet/
  artifact.json
  gate-results.jsonl
  execution.json
  runtime.json
  protocol/
    mcp.ndjson
    acp.ndjson
  logs/
    events.ndjson
    stderr.log
  marimo/
    notebook.py
    notebook-state.json
    graph-attestation.json
  replay/
    replay.just
    replay.hof.cue
    inputs.lock.json
  outputs/
    structured-output.json
    evidence-set.json
  hashes/
    manifest.json
```

---

## 10. marimo as Default Execution, Replay, and Evidence Surface

marimo fits especially well now that it is the default code-mode environment.

### 10.1 Roles for marimo

marimo can serve as:

- packet workbench
- implementation environment
- replay harness
- evidence surface
- graph/state attestation witness

### 10.2 Why it fits

marimo strengthens:

- reproducible execution
- Python-native artifacts
- replay via source
- notebook and graph introspection
- structured workbench-style evidence

### 10.3 Important boundary

marimo is not the semantic authority.

Kernel contracts, manifests, and policy remain authoritative.
marimo is a runtime and evidence surface.

---

## 11. Protocols, Structured Outputs, and Runtime Records

The runtime model benefits from:

- MCP and ACP-style protocol traces
- structured outputs
- ndjson/jsonl event streams
- typed runtime records

### 11.1 Packet implications

This allows the packet to capture:

- protocol traces
- structured message flows
- event logs
- deterministic envelopes
- replayable execution records

### 11.2 Runtime typing

A useful pattern is:

- CUE for admissibility and promotion legality
- typed Python runtime models for event records
- NDJSON/JSONL as append-only evidence streams

This gives a clean boundary between semantic policy and runtime telemetry.

---

## 12. Replay as Primary Proof, Semantic Diff as Optional Enrichment

### 12.1 Replay as the stronger proof

Once replay is high confidence, replay becomes the primary proof of execution validity.

It answers:

- can this packet be rerun
- under the captured environment
- with materially consistent outputs

### 12.2 Semantic diff becomes secondary

AST and incremental diff then become mostly:

- diagnostic instrumentation
- bug localization support
- semantic-risk classification
- review compression

rather than core promotion evidence.

### 12.3 Optional semantic evidence stack

A useful optional stack is:

- **tree-sitter** for structural parsing and incremental diff
- **ast-grep** for semantic classification and rule-based matching
- **LSP** for optional symbol/tokens/diagnostic enrichment

These should enrich packet evidence rather than replace promotion gates.

---

## 13. Semantic Evidence and Potential Logic-Bug Tracing

Even after replay matures, semantic diff can still provide value.

### 13.1 High-signal use cases

- changed signatures
- import surface changes
- side-effect introduction
- control-flow changes
- notebook dependency graph changes
- diagnostics regressions

### 13.2 Correct role

Semantic evidence should be:

- optional
- typed
- attached to packet evidence
- used for debugging, triage, and review
- not the primary source of promotion legality

---

## 14. Worktree-Mounted Execution and Cell-Scoped Lineage

A more speculative pattern was discussed:

- implementation occurs on a git worktree
- the worktree is mounted into marimo
- each cell may produce a replayable checkpoint
- semantic evidence may be attached per cell

### 14.1 Current assessment

This is plausible, but should be deferred until the system reaches greater maturity.

### 14.2 Why defer it

It depends on stabilizing:

- packet schema family
- replay fidelity
- marimo graph/state capture
- evidence bundle completeness
- semantic evidence quality
- worktree execution discipline

### 14.3 Recommended future framing

Treat cell-scoped commits or checkpoints as:

- an evidence-lineage enhancement
- a maturity-gated feature
- not a current architectural requirement

---

## 15. Suggested Contract Families

The following contract families look like the strongest next units to define.

### 15.1 Core promotion contracts

```text
#GateResult
#PromotionEdge
#PromotionPacket
```

### 15.2 Plan contracts

```text
#PlanCandidate
#PlanPacket
#PlanPromotable
#PlanPromoted
```

### 15.3 Implement contracts

```text
#ImplementCandidate
#ImplementPacket
#ImplementPromotable
#ImplementPromoted
```

### 15.4 Evidence contracts

```text
#ExecutionEnvelope
#EnvironmentFingerprint
#IntrospectionSnapshot
#GraphAttestation
#ReplayRecipe
#EvidenceBundle
```

### 15.5 Surface and routing contracts

```text
#Surface
#SurfaceInventory
#SurfaceImpact
#TargetExpansion
```

---

## 16. Proposed Hof/CUE Flow Layout

### 16.1 Shared flow base

A common `flow-base.cue` should provide:

- shared runtime tags
- repo/delta context
- changed-file discovery
- surface impact resolution
- selected targets
- conditional execution wrappers

### 16.2 Plan flow

`plan.flow.cue` should orchestrate:

- delta collection
- impacted surface resolution
- transitive expansion
- candidate plan generation
- gate execution
- packet generation
- promotion

### 16.3 Implement flow

`implement.flow.cue` should orchestrate:

- accepted plan intake
- selected target resolution
- candidate implementation generation
- validation/test/evidence gates
- packet generation
- promotion

### 16.4 Evidence flow

A dedicated evidence or packet flow may also be warranted for:

- bundle assembly
- hash and manifest generation
- replay material generation
- introspection capture
- final promotion packet generation

---

## 17. Near-Term Recommendations

### 17.1 Highest-priority moves

1. Define the kernel phase and promotion contract families in CUE.
2. Move packet and phase requirements into kernel-managed CUE definitions.
3. Make plan and implement constrained artifact families.
4. Land a shared `flow-base.cue`.
5. Generate packet files and evidence bundles from Hof.
6. Make evidence bundles first-class promotion artifacts.
7. Add replay recipe and execution envelope to every implement packet.

### 17.2 Medium-priority moves

1. Generate surface inventory and skill registry projections.
2. Add structured result envelopes to every stage.
3. Add introspection snapshots to implement packets.
4. Add risk-triggered semantic evidence support.

### 17.3 Deferred moves

1. Cell-scoped VCS lineage.
2. Full semantic-diff-per-cell evidence.
3. Strong LSP-enriched packet traces everywhere.

---

## 18. Open Questions

1. What is the minimal viable kernel contract family for the first promotion-oriented packet lifecycle?
2. How much of packet generation should be in Hof templates versus Python emitters?
3. What exact evidence classes are required for plan promotion versus implement promotion?
4. How should graph attestation be represented for marimo-backed execution?
5. When does semantic evidence become worth the operational cost?
6. What is the minimal stable replay recipe required for promotion?
7. How should promotion failures be encoded for re-entry into the loop?

---

## 19. Working Thesis

The most stable formulation from this exploration is:

> **Kernel defines what must be true for promotion.**  
> **CUE expresses the admissible state and packet requirements.**  
> **Hof drives artifacts through the promotion gates and generates the plan and packet files.**  
> **Python performs the concrete work.**  
> **marimo hosts execution, replay, and evidence.**  
> **The packet contains the outputs, the environment, and introspection of the executor.**

---

## 20. Closing Position

This direction is promising because it unifies:

- contract-first design
- promotion-first execution
- reproducible runtime evidence
- generated packet artifacts
- replay-based trust
- Hof/CUE as a thorough control-plane substrate

The clearest next step is to turn this into concrete kernel contract skeletons and a shared Hof flow base.
