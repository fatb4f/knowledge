# Bootcamp → CLI → Python → Rust – Execution Plan

## Priority Order (Locked)

### 1) Bootcamp (Tomorrow)
**Goal:** tool fluency + reduced cognitive load.

Rules:
- No architecture work.
- If a side-idea appears: capture a one-line note, do not act.

Deliverables:
- Working command patterns and muscle-memory.

---

### 2) Migrate to OpenAI CLI (Infrastructure Only)
**Goal:** stable, scriptable LLM interface.

Scope:
- CLI-first workflow
- Git-backed config/state (`$APP_DATA` points to a repo)
- Prompts/configs as versioned artifacts

Explicitly excluded:
- Agent loops
- Autonomy frameworks

Deliverables:
- Deterministic prompt templates
- Reusable config profiles

---

### 3) Python (Injection Point #1: Structure)
**Goal:** introduce schema + validation + reproducible pipelines.

Inject:
- Pydantic models / JSON schemas
- Tool wrappers (typed functions)
- Validation-first execution
- Deterministic pipeline stages

Do not inject:
- Planning loops
- Multi-agent orchestration

Deliverables:
- A “compiler/controller” layer that drives workflows predictably.

---

### 4) Rust (Injection Point #2: Control + Hardening)
**Goal:** harden boundaries and enforce capabilities.

Inject:
- Strong typing at interfaces
- Capability/permission enforcement
- Long-lived services where needed
- Event logs + replayability

Deliverables:
- Runtime safety envelope and reliable execution substrate.

---

## Cloud-Hosted Dev Workflows (Rally Everything Up)

### Where Cloud Fits (and where it does not)
Cloud is treated as **execution substrate + reproducibility**, not as a new architecture.

Allowed purposes:
- Identical dev environments across machines
- Remote compute for builds/tests
- CI/CD for deterministic regeneration
- Artifact publishing

Not allowed (for now):
- Always-on autonomous agents
- Background orchestration that bypasses the local pipeline invariants

---

### Cloud Injection Timeline

**A) During Bootcamp:**
- Only lightweight: GitHub repo hygiene, minimal CI awareness.

**B) During OpenAI CLI migration:**
- Store configs in a repo.
- Add CI checks that validate schemas/config files.

**C) During Python injection:**
- GitHub Actions: run validation + build pipeline stages.
- Optional devcontainers to keep environments identical.

**D) During Rust injection:**
- Optional service hardening (self-hosted runners, reproducible builds).
- Stronger artifact provenance (hashes, logs).

---

## Operating Rules
- One active track at a time (no parallel rewrites).
- New ideas get parked as notes until the next phase.
- Portability first: everything rebuildable from repo state.

---

## One-Line Summary
**Bootcamp → OpenAI CLI → Python (structure) → Rust (control).**

Cloud workflows are added only to improve reproducibility and portability, not to expand autonomy.

