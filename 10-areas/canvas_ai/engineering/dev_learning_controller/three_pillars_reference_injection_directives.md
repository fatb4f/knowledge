# Three Pillars — Foundational Reference

This document defines the three foundational pillars to be continuously injected into all development, data, and learning work. These pillars are not courses; they are interpretive lenses and reflexive operators applied to existing tasks.

---

## Pillar A — Computation as a System

### Core Idea
Programs are stateful systems governed by invariants and transitions, not merely sequences of instructions.

### Key Concepts
- State and state transitions
- Invariants and constraints
- Failure modes
- Resource ownership and lifetime
- Determinism vs nondeterminism

### Reflex Questions
- What is the state?
- What modifies it?
- What must *always* remain true?
- What breaks first under stress?

### Typical Injection Points
- Variable design
- Function boundaries
- Error handling
- Concurrency / parallelism

---

## Pillar B — Statistics as Inference

### Core Idea
Most outputs are estimates under uncertainty, not facts. Reasoning must account for noise, variability, and bias.

### Key Concepts
- Distributions vs point values
- Variance and uncertainty
- Sampling and estimation
- Bias, overfitting, and generalization

### Reflex Questions
- Is this value measured or inferred?
- What uncertainty am I ignoring?
- How sensitive is the output to noise?
- What happens under repeated trials?

### Typical Injection Points
- Performance measurement
- Data processing
- Model evaluation
- Any numerical output

---

## Pillar C — Control & Adaptation

### Core Idea
Systems evolve over time through feedback. Stability and adaptation depend on how feedback is applied.

### Key Concepts
- Feedback loops
- Stability and instability
- Gain, damping, and delay
- Adaptation vs oscillation

### Reflex Questions
- What is being controlled?
- What feedback signal exists?
- Is the loop stable?
- How does the system adapt over time?

### Typical Injection Points
- Loops and retries
- Learning rate analogies
- Resource management
- Human-in-the-loop systems

---

# Injection Directives (Canonical)

These directives are always in effect unless explicitly overridden.

1. Every non-trivial program is treated as a dynamic system.
2. Every numeric output is assumed uncertain unless proven otherwise.
3. Every loop implies feedback and must be evaluated for stability.
4. At least one pillar lens must be applied consciously per work session.
5. Failures are analyzed as system behavior, not mistakes.

---

# Scope of Application

- Coursework (all programs)
- Side-track development (Python, Rust)
- Tooling and automation
- Data analysis and ML pipelines
- System design and evaluation

This document serves as a stable reference and is intended to remain lightweight, durable, and reusable.

