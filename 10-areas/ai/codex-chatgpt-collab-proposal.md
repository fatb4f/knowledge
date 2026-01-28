# Codex–ChatGPT Local Collaboration Proposal (v0)

## Purpose
Establish a minimal, reliable local collaboration workflow between the Codex CLI agent and ChatGPT‑style usage, preserving long‑term memory, thread history, and “canvas” equivalents outside the web UI.

## Goals
- Preserve durable context across sessions (memory, threads, summaries).
- Enable two agents to collaborate via shared artifacts (files + DB).
- Keep the system portable (sync via Git or Drive) and auditable.
- Start small and extensible; avoid heavy infrastructure at v0.

## Non‑Goals (v0)
- Full web‑UI parity (canvas, library, saved memories).
- Automatic semantic search across all historical threads.
- Complex multi‑user access control.

## Proposed Architecture (v0)
- **Source of truth**: DuckDB database for threads/messages/memory/events.
- **Human handoff**: `conversation.md` as a compact, editable, diff‑friendly bridge.
- **Prompts**: separate system prompt files for Codex vs ChatGPT workflows.
- **Sync**: Shared folder hosted on a Drive mount or a Git repo (or both).

### Suggested Layout
```
<shared_root>/
  convo/
    conversation.md
    memory.json
    attachments/
  db/
    convo.duckdb
  prompts/
    codex.system.md
    chatgpt.system.md
  scripts/
    import_webui.py
    prompt_bundle.py
```

## Data Model (DuckDB)
Minimal schema to start:
- **threads**(id, title, created_at, updated_at, tags, source)
- **messages**(id, thread_id, role, created_at, content_md, source, meta_json)
- **memory**(id, area, key, value_json, updated_at, source)
- **events**(id, ts, actor, type, payload_json)

## Memory Format (JSON)
Human‑edited, versioned, agent‑injectable:
```json
{
  "version": "v0",
  "defaults": {
    "response_style": "concise",
    "language": "en"
  },
  "areas": {
    "META": { "items": [ {"id":"META-16","text":"concise by default","priority":2} ] },
    "DEV":  { "items": [ {"id":"DEV-68","text":"username src404","priority":1} ] }
  }
}
```
Notes:
- “priority” supports later retrieval/ranking.
- Treat `memory.json` as curated; DB may store snapshots or pointers.

## Shared `conversation.md` (handoff layer)
Compact and human‑readable. Example:
```
# Thread: <title>
- last_updated: <iso8601>
- thread_id: <uuid>

## Codex handoff
- goals:
- constraints:
- next actions:

## Chat history (condensed)
<short running summary>
```

## Workflow (v0)
1) **Agent starts** → loads `memory.json` + latest thread summary.
2) **Work session** → logs to DuckDB; updates `conversation.md` summary.
3) **Handoff** → other agent reads `conversation.md`, pulls context from DB.

## Implementation Plan
Phase 0 (setup)
- Create shared folder structure.
- Initialize `convo.duckdb` with schema.
- Create stub prompts and starter `memory.json`.

Phase 1 (import)
- Export ChatGPT web‑UI history.
- Build `import_webui.py` to ingest export into DuckDB.
- Generate initial `conversation.md` from the most recent thread.

Phase 2 (prompt bundling)
- Build `prompt_bundle.py` to assemble system prompt from memory + recent context.
- Use CLI wrappers to call Codex/ChatGPT with bundled prompts.

Phase 3 (collab)
- Introduce per‑thread Git worktrees.
- Add lightweight scripts for thread creation/rotation.

## Open Decisions
- **Shared root** location (Drive mount vs Git repo vs both).
- **Import format** for ChatGPT web‑UI export (exact files + parser needed).
- **Memory curation** policy (what is machine‑enforced vs human‑only).

## Risks / Mitigations
- **UI‑specific memory** (canvas/library/thread IDs) → map to local files.
- **Drift in summaries** → require manual review checkpoints.
- **Data bloat** → enforce retention policies and summary compression.

## Next Steps (proposed)
1) Choose shared root path and sync strategy.
2) Confirm memory JSON schema (or request a refined one).
3) Author schema + initialize DuckDB.
4) Implement `import_webui.py` and `prompt_bundle.py`.

