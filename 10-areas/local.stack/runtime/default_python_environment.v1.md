# Default Python Environment v1

## Purpose

This note locks the default Python runtime expected by the Codex operational substrate.

It is a runtime realization note.
It does not redefine kernel-owned semantic contract meaning.

## Default Interpreter

The default interpreter for this Codex runtime is:

- CPython `3.12.12`

This is the interpreter currently used by the project-local `.venv` and should remain the default until the environment is intentionally upgraded.

## Authority Surfaces

The environment lock is expressed through:

- [pyproject.toml](/home/chronos/src/dotfiles/chezmoi/dot_config/codex/pyproject.toml)
- [\.python-version](/home/chronos/src/dotfiles/chezmoi/dot_config/codex/.python-version)
- project-local `.venv` resolution through `uv`

## Rules

- Keep the default interpreter on Python `3.12.x`.
- Do not silently float to Python `3.13+`.
- Align notebook `requires-python` headers with the project interpreter range when those notebooks are part of the default runtime surface.
- Treat interpreter upgrades as explicit runtime changes that require re-lock, test revalidation, and note updates.

## Practical Meaning

For this repo:

- `uv run ...` should resolve against the project `.venv`
- the project `.venv` should be based on CPython `3.12.12`
- notebook, CLI, replay, and binding surfaces should all execute under the same interpreter family

## Current Runtime Scope

This environment lock applies directly to:

- Marimo host notebooks under `runtime/`
- runtime bindings such as CLI, MCP, ACP, and replay helpers
- proposal/runtime tests executed through `uv`

## Upgrade Gate

Before changing the default Python version:

- update `pyproject.toml`
- update `.python-version`
- refresh `uv.lock`
- rerun the state/runtime test slice
- update this note if the default interpreter changes
