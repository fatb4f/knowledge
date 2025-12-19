# MQT-X Core SSOT Units of Measure (Foundational Standard)

This document defines the eight fundamental units of measure that form the Single Source of Truth (SSOT) for any metadata-driven, schema-first, LLM-expandable system.

These units constitute the conceptual and structural backbone of all future MQT-X, G-CCMS, or pipeline-oriented projects. They encode the **WHAT**, from which all **HOW** can be derived.

---

# 1. Entities
Fundamental domain objects that exist within the system. Each entity must have:
- a clear identity
- a stable definition
- structured fields

Entities map directly to schema constructs.

---

# 2. Relationships
Describes how entities connect to each other.
- parent/child
- one-to-many
- many-to-many

Relationships define the structural integrity of the domain.

---

# 3. Constraints
Rules that must always be true within the system.
- uniqueness
- cardinality
- validation rules
- invariants

Constraints provide guarantees that both humans and machines can rely upon.

---

# 4. Naming Patterns
Deterministic rules that generate IDs, filenames, or symbolic references.
- module_id patterns
- objective_id patterns
- document naming

Naming patterns ensure uniformity and reconstructability.

---

# 5. Valid Transformations
Permissible operations within the domain.
- entity → entity mappings
- schema → artifact mappings
- syllabus → module structure

Transformations describe how data moves and evolves.

---

# 6. Required Outputs
The artifacts that the system must produce.
- study guides
- drills
- indexes
- any additional generated documents

Outputs define the visible, consumable result of the pipeline.

---

# 7. Pipeline Structure
The ordered sequence of stages that apply transformations to yield outputs.
- ingestion
- domain construction
- rendering
- viewing

Pipeline structure describes how the system operates end-to-end.

---

# 8. Rendering Rules
Rules that govern how structured data becomes concrete content.
- layout conventions
- heading levels
- LaTeX formatting
- section ordering

Rendering rules define the final appearance of all artifacts.

---

## Summary
These eight SSOT units – Entities, Relationships, Constraints, Naming Patterns, Valid Transformations, Required Outputs, Pipeline Structure, Rendering Rules – represent the minimal, complete conceptual footprint required to reconstruct any content or pipeline system.

All future standards (Pydantic convergence, G-CCMS development, MQT-X evolution) will extend from this foundation.

