# CUE/Hof Git Workflows — Living Document

## Status

- **State:** exploratory, shaping toward prototype
- **Primary theme:** CUE as authority, hof as projection/orchestration
- **Document type:** living engineering design doc
- **Source basis:** synthesized from the uploaded exploratory output

---

## 1. Purpose

Define a constraint-driven control plane for repo operations centered on:

- Git workflows
- GitHub workflow generation
- commit / PR / issue lifecycle automation
- `pyproject.toml`-based Python repos
- layered `conf.d` and `environment.d` composition
- interactive and non-interactive selection surfaces built on providers like `fd`, `rg`, and picker frontends such as `fzf`

This document shifts the earlier synthesis into an operational living doc:

- clearer authority boundaries
- clearer first implementation slice
- explicit contracts
- explicit rollout phases
- explicit open questions and decisions

---

## 2. Problem Framing

Typical repo automation degrades into:

- shell-script sprawl
- hidden policy in hooks and CI glue
- fragile hand-authored workflow YAML
- inconsistent commit, PR, and issue behavior
- duplicated Python repo configuration
- ad hoc environment setup
- interactive tools that mix search, policy, and execution in one script
- drift between local behavior and CI behavior

The result is low trust, weak reuse, and poor fit for typed or agentic runtime systems.

---

## 3. Core Thesis

### 3.1 Authority split

**CUE owns authority**

- schemas
- constraints
- admissibility rules
- merge legality
- transition legality
- normalized inventories
- override boundaries

**hof owns execution/projection**

- generation
- projection
- flow orchestration
- task wiring
- reconciliation entrypoints
- hook and CI coordination

### 3.2 Design rule

> Generated files are never authority.
>
> Hooks are not authority.
>
> Picker frontends are not authority.
>
> CUE remains the authoritative source of legality and structure.

---

## 4. Desired Outcomes

### 4.1 Operational outcomes

- reproducible workflow generation
- validated commit/PR/issue structures
- path-aware repo policy
- local/CI parity
- reduced config drift
- interchangeable interactive frontends
- stronger support for agent-mediated repo operations

### 4.2 Engineering outcomes

- explicit contracts instead of implicit shell behavior
- stable control surfaces across repos
- typed inventories for selection and generation
- easy-to-explain failures
- deterministic validation before any assistive generation is accepted

---

## 5. Scope

### 5.1 In scope

- commit message generation and validation
- PR generation and validation
- GitHub Actions workflow generation
- issue create/update/close workflows
- hook surfaces
- CI reconciliation
- `pyproject.toml` projection
- `conf.d`-style configuration composition
- `environment.d`-style environment composition
- provider → candidate → picker → action pipelines

### 5.2 Out of scope for first prototype

- full GitHub bot automation platform
- generalized release management
- cross-forge support beyond GitHub
- full secret management system
- rich web UI
- large-scale multi-repo orchestration

---

## 6. Architectural Model

## 6.1 Layers

### Authority layer

Owned by CUE.

Responsibilities:

- schema validity
- cross-document admissibility
- merge semantics
- policy enforcement
- ownership boundaries
- transition legality
- normalized exports

### Projection layer

Owned by hof and deterministic renderers.

Responsibilities:

- render `.github/workflows/*.yml`
- render commit / PR / issue payloads
- render `pyproject.toml`
- render merged config or environment views
- render candidate catalogs

### Execution layer

Owned by hof flows plus Python/shell adapters.

Responsibilities:

- invoke validation
- run generation
- reconcile drift
- dispatch local and CI actions
- coordinate hooks and tasks

### Interaction layer

Owned by replaceable frontends.

Responsibilities:

- display admissible candidates
- preview metadata
- collect selection
- dispatch approved actions

---

## 7. Core Principles

1. **Authority before generation**
2. **Validation before mutation**
3. **Deterministic lane before assistive lane**
4. **Local and CI share the same contracts**
5. **Picker frontends remain replaceable**
6. **Path classification and ownership are explicit**
7. **Rendered files carry provenance and drift is detectable**

---

## 8. Domain Model

## 8.1 Git workflow domain

Primary surfaces:

- commit messages
- pull requests
- issues
- GitHub workflow YAML
- hooks
- CI jobs

## 8.2 Python repo domain

Primary surfaces:

- `pyproject.toml`
- dependency groups
- tool configuration
- package inventories
- monorepo overlays

## 8.3 Layered config domain

Primary surfaces:

- `conf.d` fragments
- `environment.d` fragments
- effective merged views
- precedence and override legality

## 8.4 Selection domain

Primary surfaces:

- structural providers such as `fd`
- semantic providers such as `rg`
- inventory-backed provider outputs
- generic picker adapters
- action dispatchers

---

## 9. First-Class Contracts

The prototype should standardize a small family of contracts.

## 9.1 CommitMessage

Purpose:

- classify the change
- map changed paths to allowed scopes
- enforce required references and trailers

Minimal shape:

```json
{
  "kind": "feat|fix|refactor|docs|chore|test|build|ci",
  "scope": "string",
  "breaking": false,
  "issue_refs": ["..."],
  "summary": "string",
  "body": "string",
  "trailers": ["..."]
}
```

Representative constraints:

- allowed kinds only
- allowed scopes only
- path-to-scope legality
- required issue refs for selected paths
- migration note required for breaking changes
- rationale trailer required for selected control-plane paths

## 9.2 PRPayload

Purpose:

- structure review context
- standardize change summaries
- attach risk and evidence

Minimal shape:

```json
{
  "title": "string",
  "summary": "string",
  "changed_domains": ["control", "runtime", "schemas"],
  "risk_level": "low|medium|high",
  "testing": ["..."],
  "migration_notes": ["..."],
  "checklists": ["..."],
  "linked_issues": ["..."]
}
```

Representative constraints:

- schema changes require compatibility checklist
- workflow changes require projection provenance note
- runtime changes require operational evidence note

## 9.3 WorkflowSpec

Purpose:

- define authoritative CI workflow structure
- generate GitHub Actions YAML from typed inputs

Representative fields:

- workflow id
- triggers
- permissions
- jobs
- matrix strategy
- environment requirements
- generation metadata

Representative constraints:

- approved permissions only
- normalized runner policy
- reusable job fragments only from approved inventory
- generated output must match authority export

## 9.4 IssueLifecycle

Purpose:

- model issue create/update/close transitions as typed state changes

Representative fields:

- type
- state
- labels
- required sections
- allowed transitions

Representative constraints:

- invalid transitions rejected
- label requirements tied to issue type
- close path may require resolution note

## 9.5 EnvironmentFragment

Purpose:

- model environment overlays with legality and precedence

Representative fields:

- fragment id
- profile
- variable set
- required/optional class
- override policy
- secret classification

## 9.6 SelectionCandidate

Purpose:

- normalize structural, semantic, and inventory-backed selection results

Minimal shape:

```json
{
  "id": "string",
  "kind": "file|match|module|workflow|issue|scope|profile",
  "path": "string",
  "line": 0,
  "preview": "string",
  "labels": ["..."],
  "actions": ["open", "edit", "generate", "validate"]
}
```

Representative constraints:

- visibility controlled by policy
- action legality computed before presentation
- picker sees only admissible candidates

---

## 10. Repo Layout Direction

A candidate top-level shape:

```text
control/
  git/
  python/
    pyproject/
  env/
  ui/
    selection/
```

A reusable internal pattern:

```text
contracts/
policy/
inventory/
generator/
projection/
flow/
```

Suggested prototype layout:

```text
control/git/
  contracts/
    commit-message.cue
    pr-payload.cue
    issue-lifecycle.cue
    workflow-spec.cue
  flows/
    local-hooks.cue
    ci-reconcile.cue
  projections/
    github-workflows/
    commit-msg/
    pr/

control/python/pyproject/
  contracts/
  policy/
  flow/

control/env/
  schema.cue
  env.d/
    00-base.cue
    10-python.cue
    20-codex.cue
    30-marimo.cue
    40-ci.cue

control/ui/selection/
  contracts/
  providers/
  frontends/
  actions/
```

---

## 11. Workflow Surface Designs

## 11.1 Commit flow

### Inputs

- staged diff
- changed paths
- branch name
- issue refs
- ownership metadata

### Steps

1. classify changed paths
2. propose allowed scopes and kinds
3. build structured commit object
4. validate object in CUE
5. optionally generate prose assistively
6. revalidate rendered message
7. write draft or block commit

### Hook mapping

- `pre-commit`: cheap validation and metadata prep
- `prepare-commit-msg`: draft generation
- `commit-msg`: validation and normalization
- `post-commit`: event/log emission if needed

## 11.2 PR flow

### Inputs

- change inventory
- diff classification
- tests run
- migration markers
- linked issue refs

### Steps

1. classify changed domains
2. compute required checklists
3. build structured PR payload
4. validate payload
5. optionally synthesize prose
6. validate rendered output
7. emit PR body/template or API payload

## 11.3 Workflow generation flow

### Inputs

- typed workflow specs
- shared job fragments
- policy defaults

### Steps

1. validate workflow authority data
2. render GitHub Actions YAML
3. write generated files
4. run drift check
5. fail CI on uncommitted or invalid projections

## 11.4 Issue lifecycle flow

### Inputs

- current issue state
- requested transition
- labels and body sections

### Steps

1. validate requested transition
2. enrich labels/body if needed
3. emit create/update/close payload
4. reject illegal transitions

---

## 12. Hooks and CI

## 12.1 Local hooks

Recommended behavior:

### `pre-commit`

- validate cheap structural rules
- compute change metadata
- optionally regenerate light projections

### `prepare-commit-msg`

- generate structured draft message

### `commit-msg`

- enforce commit policy
- reject invalid scope/kind/reference/trailer combinations

### `pre-push`

- heavier validation
- workflow drift checks
- PR payload generation

## 12.2 CI jobs

Recommended jobs:

- `validate-control-plane`
- `generate-workflows`
- `check-generated-drift`
- `validate-commit-policy`
- `validate-pr-payload`
- `reconcile-issue-policy`

### CI rule

CI should not invent independent logic.

It should execute the same contract-backed validation used locally.

---

## 13. `pyproject.toml` Strategy

Treat `pyproject.toml` as a projection target, not the final authority.

### CUE should own

- project metadata contracts
- backend policy
- dependency group policy
- tool config baselines
- overlay legality for monorepos

### hof should own

- generation
- projection
- reconciliation
- per-package file emission
- inventory exports

### First-slice use cases

- standardized `[project]` metadata
- normalized `[tool.*]` blocks
- dependency group policy
- minimal new-package scaffolding

---

## 14. `conf.d` and `environment.d` Strategy

## 14.1 `conf.d`

Use layered fragments for repo-local policy:

```text
control/git/conf.d/
  00-base.cue
  10-commit-policy.cue
  20-pr-policy.cue
  30-issue-policy.cue
  40-ci-policy.cue
```

CUE should define:

- fragment schemas
- precedence
- allowed overrides
- ownership boundaries
- conflict detection

## 14.2 `environment.d`

Use layered fragments for runtime activation and profile composition:

```text
control/env/env.d/
  00-base.cue
  10-python.cue
  20-codex.cue
  30-marimo.cue
  40-ci.cue
```

Projection targets can include:

- shell exports
- `.env`
- `environment.d/*.conf`
- CI environment fragments
- wrapper launchers

---

## 15. Picker Architecture

The target abstraction is not “use `fzf`”.

The target abstraction is:

```text
provider -> normalize -> constrain -> rank -> pick -> execute
```

## 15.1 Providers

Structural providers:

- `fd`
- repo inventories
- package catalogs
- fragment inventories

Semantic providers:

- `rg`
- schema/reference matches
- issue references
- path classification matches

## 15.2 Normalization

All providers should map into `SelectionCandidate`.

## 15.3 Constraint application

Policy determines:

- visibility
- ownership
- action legality
- compatibility
- precedence

## 15.4 Frontends

Potential frontends:

- `fzf`
- skim
- shell menus
- TUIs
- notebook/UI adapters
- future web frontends

### Critical rule

Frontends present already-constrained candidates.

They do not decide legality.

## 15.5 Executors

Representative actions:

- open
- edit
- patch
- validate
- generate
- reconcile

---

## 16. Deterministic and Assistive Lanes

## 16.1 Deterministic lane

Always first.

Includes:

- schema validation
- path classification
- transition legality
- merge legality
- candidate filtering
- projection generation
- drift checks

## 16.2 Assistive lane

Optional.

Includes:

- commit wording help
- PR prose generation
- issue synthesis
- summary drafting

### Rule

Assistive output is advisory until revalidated by deterministic contracts.

---

## 17. Initial Implementation Plan

## Phase 0 — contract baseline

Deliver:

- commit message contract
- PR payload contract
- workflow spec contract
- issue lifecycle contract
- selection candidate contract

Exit criteria:

- example inputs validate
- invalid cases fail predictably
- baseline inventories export cleanly

## Phase 1 — Git workflow slice

Deliver:

- commit validation in hooks
- PR payload generation
- GitHub workflow YAML projection
- CI drift checks

Exit criteria:

- one repo can generate workflows from authority files
- commit policy enforced locally and in CI
- PR payload rendered from structured input

## Phase 2 — Python repo slice

Deliver:

- minimal `pyproject.toml` projection
- dependency group policy checks
- package inventory export

Exit criteria:

- one or more packages use projected `pyproject.toml`
- local and CI validation are aligned

## Phase 3 — layered config and selection slice

Deliver:

- `conf.d` merge model
- `environment.d` projection
- provider/normalize/constrain/pick/execute pipeline
- one picker adapter

Exit criteria:

- structural and semantic providers normalize into a shared candidate model
- picker is swappable without policy changes

---

## 18. Acceptance Criteria

The prototype is successful if it demonstrates:

- clear authority boundaries
- reproducible projections
- explainable failures
- local/CI parity
- low-friction hook behavior
- one interchangeable picker frontend
- one inventory-backed selection flow
- one Python repo projection target

---

## 19. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Over-generation hides intent | repo becomes opaque | provenance headers, inventories, effective merged views |
| Policy fragmentation | hard to reason about behavior | precedence model, conflict detection, ownership mapping |
| Heavy hooks | low developer trust | keep local checks fast, move expensive checks to pre-push/CI |
| Picker coupling | brittle UX and policy drift | frontends only present admissible candidates |
| Local/CI divergence | credibility loss | shared contracts and shared flow entrypoints |

---

## 20. Current Decisions

| ID | Decision | Status |
|---|---|---|
| D-001 | CUE is the authority layer | agreed direction |
| D-002 | hof is the execution/projection layer | agreed direction |
| D-003 | generated workflow YAML is not hand-authored authority | agreed direction |
| D-004 | picker logic must not encode business legality | agreed direction |
| D-005 | `pyproject.toml` is a projection target | agreed direction |

---

## 21. Open Questions

| ID | Question | Notes |
|---|---|---|
| Q-001 | What is the minimal contract family needed for a credible first slice? | likely 5 contracts in section 9 |
| Q-002 | Where should shared inventories live relative to repo-local projections? | depends on control-plane boundaries |
| Q-003 | How opinionated should path-to-scope commit policy be? | tension between consistency and friction |
| Q-004 | Should workflow generation be fully monolithic or fragment-composed? | likely fragment-composed with strong provenance |
| Q-005 | How much of issue lifecycle should be local vs API-driven? | keep first slice payload-oriented |
| Q-006 | What is the preferred adapter boundary between hof flows and Python helpers? | important for long-term runtime consistency |

---

## 22. Recommended Immediate Deliverables

### A. `control/git/contracts/*`

- `commit-message.cue`
- `pr-payload.cue`
- `issue-lifecycle.cue`
- `workflow-spec.cue`

### B. `control/git/flows/*`

- `local-hooks.cue`
- `ci-reconcile.cue`

### C. `control/ui/selection/*`

- `selection-candidate.cue`
- provider contracts for `fd` and `rg`
- picker adapter contract
- action dispatch contract

### D. `control/python/pyproject/*`

- minimal `pyproject` projection contract
- validation flow
- package inventory projection

### E. `control/env/*`

- layered env fragments
- effective merged env view
- projection to shell and `.env`

---

## 23. Implementation Notes

### 23.1 Strongest first slice

The most leverage comes from this order:

1. GitHub workflow generation
2. commit message validation
3. PR payload generation
4. issue lifecycle payload validation
5. `pyproject.toml` projection
6. layered env/config composition
7. picker contract pipeline

### 23.2 Why this order

It maximizes:

- early visible payoff
- strong validation value
- drift reduction
- reuse across local and CI entrypoints

---

## 24. Working Summary

This design is best understood as a repo-local control plane:

- **CUE** supplies legality, policy, composition, and typed inventories
- **hof** supplies rendering, orchestration, and operational entrypoints
- **hooks** and **CI** execute shared contracts
- **`pyproject.toml`**, **workflow YAML**, **config fragments**, and **environment fragments** are projections
- **providers** such as `fd` and `rg` feed normalized candidate pipelines
- **pickers** remain interchangeable interaction surfaces

The main architectural win is replacing imperative glue with explicit contracts and reproducible projections.

---

## 25. Change Log

### 2026-03-31

- created living-doc version from uploaded exploratory synthesis
- restructured around contracts, phases, decisions, and open questions
- emphasized first-slice implementation plan and acceptance criteria

---

## 26. Next Editing Targets

Recommended next edits to this document:

1. add a concrete contract appendix with example CUE snippets
2. add an authority/projection map for each repo surface
3. add a first-pass `control/git` file tree with naming conventions
4. add hook timing and failure-mode budgets
5. add CI reconciliation semantics and drift policy

