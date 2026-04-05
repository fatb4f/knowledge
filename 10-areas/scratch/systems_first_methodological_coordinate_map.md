# Systems‑First Methodological Coordinate Map

## Purpose
This document defines the canonical **Systems‑First Methodological Coordinate Map**. It serves as the top‑level index for reasoning about software development, learning, and operational practices.

The map presents all methodologies, tools, and practices in an **optimized, reduced form** before elaboration, ensuring explicit ecosystem fit and preventing methodological drift.

This document is frozen as a reference unless an axis‑level justification is made.

---

## Canonical Axes (Frozen)

All methods are expressed as a 4‑tuple across the following axes.

### 1. System Lens — *What kind of system exists?*
- **Computational** — Executing programs, algorithms, state transitions
- **Socio‑technical** — Humans + processes + tools
- **Stochastic** — Systems dominated by probabilistic behavior
- **Cyber‑physical** — Coupled software, hardware, and environment

### 2. Control Mode — *How is behavior shaped?*
- **Feedforward** — Planning, anticipation, scaffolding
- **Feedback** — Measurement‑driven correction
- **Robust** — Invariance under disturbance
- **Adaptive** — Learning and parameter update
- **Saturation** — Bounded action, rate and scope limits

### 3. Uncertainty Model — *What is unknown?*
- **Deterministic** — Fully specified behavior
- **Probabilistic** — Modeled uncertainty
- **Adversarial** — Worst‑case or hostile conditions
- **Unknown‑unknowns** — Novel or unmodeled uncertainty

### 4. Operational Surface — *Where does it act?*
- **Code** — Language, structure, invariants
- **Infrastructure** — Runtime, deployment, cloud
- **Process** — Coordination, workflow, planning
- **Learning / Cognition** — Skill acquisition and reasoning

---

## Methodology Definition (Reduced Form)

A methodology is defined as:

```
Methodology := (System Lens, Control Mode, Uncertainty Model, Operational Surface)
```

Examples:
- Agile → (Socio‑technical, Feedback, Unknown‑unknowns, Process)
- CI/CD → (Computational, Feedback, Probabilistic, Infrastructure)
- TDD → (Computational, Feedback, Deterministic, Code)
- Robust typing → (Computational, Robust, Adversarial, Code)

This reduced form is the **required entry point** for all discussions.

---

## Relationship to Existing Constructs

### Control Strategies
Control strategies populate the **Control Mode** axis and are treated as mechanisms, not methodologies.

### Three Pillars
The Three Pillars project into the map as:
- Computation as a System → System Lens: Computational
- Statistics as Inference → Uncertainty Model: Probabilistic
- Control & Adaptation → Entire Control Mode axis

### Tooling and Pipelines
Tools are actuators or sensors acting on one or more operational surfaces and do not define methodology on their own.

---

## Clusters and Traversals

Method families form clusters within the coordinate space. Learning tracks and projects are treated as **paths through the space**, not separate frameworks.

Examples:
- Agile family → Socio‑technical · Feedback · Unknown‑unknowns · Process
- Infrastructure automation → Computational · Feedforward/Robust · Probabilistic · Infrastructure
- Learning systems → Cognitive · Adaptive · Unknown‑unknowns · Learning

---

## Standing Rule (Governing Instruction)

> Any new method, framework, or tool must first be introduced in its reduced coordinate form within this map before elaboration or comparison.

This document functions as the **index layer** for engineering methodology within the ecosystem.

