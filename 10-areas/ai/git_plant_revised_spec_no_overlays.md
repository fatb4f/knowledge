# Git Plant — Revised Spec (No Overlays)

Status: Draft → Active
Last updated: 2026-02-02
Owner: baf

## 0. Purpose
Define a **worktree-driven, branchless-by-default Git plant** for **xtrl** that yields:

- deterministic, audit-friendly execution
- sharp trunk history (single promoted commit per packet)
- promotion by patch application onto a clean trunk checkout
- strict denial of risky diffs (binaries, submodules)

This document is the **canonical GitPlant spec**. Per-task/per-packet “overlays” are out of scope.

---

## 1. Locked constraints
1. **State dirs** (global):
   - `$CODEX_STATE/xtrl/{out,worktrees,logs,cache}`
2. **Isolation primitive:** Git worktrees (branches are **not** an invariant).
3. **Promotion model:** patch-based
   - (worktree vs `origin/main`) → build patch → apply to clean trunk → create **one** promoted commit → push **FF-only**.
4. **Policy denials:**
   - deny **binary diffs**
   - deny **submodules**
5. **Commit policy (promotion commit only):**
   - Conventional Commits on the promoted commit
   - required trailers:
     - `Packet: packet-<NNN>`
     - `Evidence: $CODEX_STATE/xtrl/out/<packet_id>/...`
6. **Promotion gate:** must run **test + lint** and must block on failure.
7. **Release:** tag-based automation triggered by push to `main`.

---

## 2. Plant model

### 2.1 Modes
- **TRUNK mode**
  - clean checkout at `trunk_ref` (default `origin/main`)
  - no in-progress git operations
- **WORKTREE mode**
  - per-packet worktree under `$CODEX_STATE/xtrl/worktrees/<packet_id>`
  - detached HEAD allowed

### 2.2 State (minimum observable)
- `repo_root` (resolved)
- `trunk_ref` (resolved; default `origin/main`)
- `packet_id` (opaque string; used only for paths + commit trailers)
- `worktree_path` (derived from packet_id)
- `git_status_trunk` / `git_status_wt`
- `merge_rebase_in_progress` (boolean)
- `diff_numstat` (used for binary detection)
- `submodule_indicators` (gitlinks / .gitmodules)

### 2.3 Sensors (how the plant is observed)
- `git status --porcelain=v1`
- `git rev-parse` / `git symbolic-ref`
- `git diff --numstat <base>...HEAD` (binary detection)
- `git diff --name-only <base>...HEAD` + gitlink detection (submodule detection)
- `git fetch origin` (reachability)

### 2.4 Actuators (allowed actions)
- fetch
- create/ensure worktree
- rebase worktree onto trunk_ref
- build patch and diffstat
- apply patch to trunk
- create promoted commit
- run checks (test + lint)
- push FF-only

---

## 3. Control surface (xtrl CLI)
A dedicated module (suggested): `xtrl/gitplant/`.

### 3.1 Commands
1. `xtrl git doctor`
   - prints resolved paths (`repo_root`, `trunk_ref`, `worktrees_root`, `out_root`)
   - prints detected mode (TRUNK / WORKTREE)

2. `xtrl git wt create <packet_id>`
   - ensures worktree exists at `$CODEX_STATE/xtrl/worktrees/<packet_id>`
   - defaults to detached worktree

3. `xtrl git wt status <packet_id>`
   - reports gate status (ordered) for trunk + worktree
   - indicates whether promotion is admissible

4. `xtrl git promote <packet_id>`
   - executes the full promotion ruleset (S0–S9)
   - emits EvidenceCapsule
   - returns allow/deny with reason codes

---

## 4. Ruleset (Promotion DAG)
Inputs:
- `packet_id`
- `repo_root`
- `trunk_ref` (default `origin/main`)
- derived `worktree_path := $CODEX_STATE/xtrl/worktrees/<packet_id>`

### S0 — TRUNK preflight
Actions:
- `git fetch origin`

Gates:
- `TRUNK_CLEAN`
- `NO_GIT_OP_IN_PROGRESS`
- `FETCH_OK`

### S1 — WORKTREE preflight
Gates:
- `WORKTREE_REGISTERED`
- `WORKTREE_PATH_OK`
- `WT_CLEAN_POLICY`

### S2 — Rebase (worktree)
Actions:
- `git fetch origin`
- `git -C <wt> rebase <trunk_ref>`

Gate:
- `REBASE_CLEAN`

### S3 — Deny binaries and submodules
Binary gate (canonical):
- deny if `git -C <wt> diff --numstat <trunk_ref>...HEAD` contains `-\t-`

Submodule gate:
- deny if `.gitmodules` is touched
- deny if any gitlink entries are present (mode `160000`)

Gates:
- `BINARY_DIFF_DENY`
- `SUBMODULE_DENY`

### S4 — Patch build
Actions:
- `git -C <wt> diff --patch <trunk_ref>...HEAD > $OUT/patch.diff`
- `git -C <wt> diff --stat  <trunk_ref>...HEAD > $OUT/diffstat.txt`

Gate:
- `PATCH_BUILD_OK`

### S5 — Apply patch on clean trunk
Actions:
- ensure trunk checkout is clean and at `<trunk_ref>`
- `git apply --index $OUT/patch.diff`

Gate:
- `PATCH_APPLY_CLEAN`

### S6 — Create promoted commit
Commit message requirements:
- Subject: `<type>(<scope>): <summary> (packet-<NNN>)`
- Trailers:
  - `Packet: packet-<NNN>`
  - `Evidence: $CODEX_STATE/xtrl/out/<packet_id>/...`

Gate:
- `PROMOTION_MSG_VALID`

### S7 — Checks (test + lint)
Actions:
- run `test` command
- run `lint` command

Gates:
- `TESTS_PASS`
- `LINT_PASS`

### S8 — Push (FF-only)
Actions:
- `git push --ff-only origin main` (or equivalent enforcement)

Gate:
- `PUSH_OK`

### S9 — Cleanup (optional)
Action:
- optionally remove worktree after successful promote

---

## 5. EvidenceCapsule
Emit to: `$CODEX_STATE/xtrl/out/<packet_id>/git/`

Required outputs:
- `patch.diff`
- `diffstat.txt`
- `gates.json` (ordered gate results + reason codes)
- `promotion_commit.txt` (SHA + subject + trailers)
- `test.log`
- `lint.log`
- `env.json` (resolved paths + tool versions)

Evidence rules:
- Evidence emission is mandatory even on denial.
- `gates.json` must include the **first failing gate** plus all prior pass gates.

---

## 6. Reason codes (deny-fast taxonomy)
- `CONTRACT_INVALID` (invalid or missing packet_id / path resolution failure)
- `TRUNK_NOT_CLEAN`
- `GIT_OP_IN_PROGRESS`
- `FETCH_FAIL`
- `WORKTREE_INVALID`
- `REBASE_CONFLICT`
- `BINARY_DIFF_DENY`
- `SUBMODULE_DENY`
- `PATCH_BUILD_FAIL`
- `PATCH_APPLY_FAIL`
- `PROMOTION_MSG_INVALID`
- `TESTS_FAIL`
- `LINT_FAIL`
- `PUSH_FAIL`

---

## 7. Implementation sequence (minimal)
1. **Packet A — Docs + ruleset harness**
   - land this spec
   - add a small harness that can execute gates and emit `gates.json` in a dry-run mode

2. **Packet B — Worktree control**
   - implement `doctor`, `wt create`, `wt status`
   - offline tests using a fixture repo

3. **Packet C — Promote actuator**
   - implement S0–S9
   - enforce deny binaries/submodules
   - always emit EvidenceCapsule

4. **Packet D — Commit + checks integration**
   - enforce commit message + trailers
   - wire test/lint commands (repo-defined; not per-packet)

5. **Packet E — CI release hook**
   - configure tag-based release automation triggered by pushes to `main`

---

## 8. Stability notes
- v1 stays strict: no exceptions for binary/submodule denials.
- keep gates deterministic and local; CI is for release automation, not promotion.
- prefer one entrypoint for promotion: `xtrl git promote <packet_id>`.

