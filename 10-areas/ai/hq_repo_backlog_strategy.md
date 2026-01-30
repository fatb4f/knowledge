# HQ Repo Strategy for Multi-Repo Backlogs

## Recommendation (Summary)
Use a hub-and-spoke model:
- Each repo keeps its own canonical `backlog.md` at repo root.
- The HQ repo maintains a lightweight index that links to each repo backlog and summarizes top priorities.
- HQ owns cross-repo initiatives and coordination, not per-repo implementation tasks.

This respects the “backlog.md must be at repo root” constraint without duplication or drift.

---

# Proposed Resource (HQ repo)

## File: `backlog-index.md`
Purpose: a single page to see status and priorities across repos.

Recommended structure:
- Overview (current P0/P1 across repos)
- Repo backlogs (links + short summary)
- Cross-repo epics (owned by HQ)
- Change log (optional)

Example outline:

- Overview
  - P0 focus (one-line summary)
  - P1 follow-ups
- Repo Backlogs
  - ctrlr: link + top 3 items
  - plant-a: link + top 3 items
  - external-observer: link + top 3 items
- Cross-Repo Epics
  - Epic name -> links to component issues

---

# Plan

## Phase 1 — HQ Setup
- Create HQ repo (if not already created).
- Add `README.md` with purpose + repo index.
- Add `backlog-index.md` in HQ.

## Phase 2 — Repo Alignment
- Ensure each repo has a canonical `backlog.md` at root.
- Add a short “backlog pointer” line in each repo README:
  - “Backlog: see `backlog.md`.”

## Phase 3 — Coordination Workflow
- Maintain per-repo backlog locally.
- HQ updates `backlog-index.md` weekly or on milestone changes.
- HQ epics are links to component issues in repo backlogs.

## Phase 4 — Optional Automation
- Add a small script to update HQ index from repo backlogs.
- Keep it as a manual step unless drift becomes a real problem.

---

# Risks and Mitigations

- Drift between HQ index and repo backlogs
  - Mitigation: keep HQ index minimal and link-heavy.

- Over-centralization
  - Mitigation: do not move implementation issues into HQ.

- Duplicate priorities
  - Mitigation: HQ index only summarizes top items, never full backlogs.

---

# Decision Record (Suggested)

Decision: Adopt hub-and-spoke backlogs (local canonical + HQ index)
Date: 2026-01-30
Rationale: Respects repo-root backlog requirement while enabling cross-repo visibility.
