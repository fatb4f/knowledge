# Stdio To WS Transport Bridge v1

## Purpose

This note classifies `marimo-team/stdio-to-ws` as a runtime bridge layer for Codex transport surfaces.

It does not define semantic contract truth.
It does not replace kernel-owned `state.v1`, `session.v1`, or output contracts.

## Source Reference

Upstream repository:

- `https://github.com/marimo-team/stdio-to-ws`

The upstream README describes a small utility that redirects a stdio command to WebSocket and supports:

- `line` framing for line-delimited protocols such as NDJSON
- `raw` framing for chunk-forwarding with optional `Content-Length` stripping

## Runtime Classification

Treat `stdio-to-ws` as:

- a transport bridge
- a runtime exposure shim
- a browser or remote-client compatibility helper

Do not treat it as:

- a semantic authority layer
- a replacement for Python state APIs
- a replacement for MCP or ACP semantics
- a replacement for Marimo host/runtime units

## Intended Fit In The Current Model

The current runtime split remains:

- Marimo is the default host/runtime shell
- Python state APIs are the orchestration boundary
- MCP carries structured request/response reads
- ACP carries direct session execution where boundary crossing is required

`stdio-to-ws` fits beneath that split.

It is useful when a local stdio-oriented process needs a WebSocket-facing surface without changing the semantic contract that process already serves.

## Good Uses

- expose an ACP-over-stdio process to a WebSocket client
- expose an MCP-style stdio process to a browser-facing debug or operator panel
- bridge NDJSON session/event streams to WebSocket while preserving line framing
- keep a local process model while making transport easier for remote consumers

## Non-Goals

- inventing new request/response schema
- redefining session metadata
- changing `json`, `ndjson`, or `jsonl` output meanings
- moving contract authority out of `kernel`

## Framing Guidance

Prefer `line` framing when the underlying protocol already emits line-oriented messages such as NDJSON.

Prefer `raw` framing only when the process expects chunk-level forwarding or header-stripping behavior.

The framing mode is a transport concern, not a contract concern.

## Operational Guidance

If Codex adds a stdio-to-WebSocket bridge in runtime realization work, keep the layering explicit:

```text
WebSocket client
  -> stdio-to-ws
     -> stdio protocol process
        -> Python state API host or ACP/MCP runtime binding
```

The bridge should stay disposable and replaceable.
The state/session/output contracts above it should remain unchanged.
