Correct. The primary interface should be:

```text id="68ofam"
ACP = editor / Neovim-facing agent session protocol
MCP = tools / resources / context protocol
Marimo = MCP-backed context and notebook surface
nvim headless = MCP tool or ACP-adjacent workspace adapter
```

ACP is the right top-level framing because it standardizes communication between code editors and coding agents, while MCP is the right lower-level framing for resources and tools exposed to the agent. ([GitHub][1]) MCP resources are explicitly for exposing context like files, schemas, or application-specific information via URIs, and MCP tools expose executable functions with schemas and structured results. ([Model Context Protocol][2])

## Corrected control plane

```text id="2jk803"
Neovim / ACP client
  -> Codex ACP agent
    -> MCP client
      -> marimo-context MCP server
      -> nvim-headless MCP server/tool
      -> exercism-bash MCP resources
      -> bash-test-runner MCP tool
      -> bash-analyzer MCP tool
      -> shellcheck/shfmt/bash-lsp MCP tools
```

## Role split

| Layer             | Role                                | Owns                                                                                                   |
| ----------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **ACP**           | editor ↔ agent session              | chat/session, current workspace mediation, user-visible edits, single-question lifecycle               |
| **MCP resources** | bounded context                     | syllabus refs, local Bash manual, Wooledge, ShellCheck corpus, Google Bash guide, Marimo session notes |
| **MCP tools**     | bounded execution                   | context slicing, headless nvim probes, lint, format diff, test runner, analyzer                        |
| **Marimo**        | persistent notebook/resource engine | indexes, slice history, linear session state, promotion candidates                                     |
| **Codex**         | agent logic                         | normalize question, request MCP resources/tools, synthesize one answer                                 |

## Updated surface manifest

Codex should see an ACP session plus a small MCP registry.

```json id="k5ed28"
{
  "version": "bash-track-agent-surfaces.v1",
  "primary_protocols": {
    "session": "ACP",
    "resources_and_tools": "MCP"
  },
  "mcp_servers": {
    "marimo.context": {
      "resources": [
        "marimo://session/current",
        "marimo://refs/exercism/bash/{kind}/{slug}",
        "marimo://refs/bash-manual/{topic}",
        "marimo://refs/wooledge/{topic}",
        "marimo://refs/shellcheck/{query}",
        "marimo://refs/google-bash-guide/{topic}"
      ],
      "tools": [
        "context.slice",
        "context.scaffold",
        "session.summarize"
      ]
    },
    "workspace.nvim": {
      "tools": [
        "nvim.current_buffer",
        "nvim.selection",
        "nvim.diagnostics",
        "nvim.lsp_symbols",
        "nvim.headless_eval"
      ]
    },
    "exercism.bash": {
      "resources": [
        "exercism://bash/config",
        "exercism://bash/docs/{topic}",
        "exercism://bash/exercise/{slug}/metadata",
        "exercism://bash/exercise/{slug}/tests",
        "exercism://bash/exercise/{slug}/instructions"
      ],
      "tools": [
        "exercism.test_run",
        "exercism.analyze"
      ]
    },
    "bash.tooling": {
      "tools": [
        "bash.syntax_check",
        "shellcheck.run",
        "shfmt.diff",
        "bats.run"
      ]
    }
  }
}
```

## Refined Codex contract

```text id="n81r2c"
Codex over ACP:
  - receives one user question from Neovim/editor
  - reads active workspace through ACP/MCP bridge
  - requests MCP resources only by URI/template
  - invokes MCP tools only under caps
  - returns one solution response

Codex does not:
  - crawl repos directly
  - search the web
  - read whole corpora
  - own notebook state
  - bypass MCP for tests/lints/context
```

## Marimo’s corrected position

Marimo is not “the broker” for everything. It is one MCP server:

```text id="qpksuh"
marimo-context MCP server:
  resources:
    indexed reference slices
    notebook session summaries
    static local corpus views

  tools:
    context.slice
    context.scaffold
    session.summarize
    maybe: registry.promote_candidate
```

So the agent does not call arbitrary notebook functions. It calls MCP tools/resources whose implementation happens to live in Marimo.

## `nvim headless` position

`nvim --headless` should be exposed as an MCP tool surface, probably separate from Marimo:

```json id="4fnhto"
{
  "server": "workspace.nvim",
  "tools": {
    "nvim.current_buffer": {
      "description": "Return active buffer path, filetype, content hash, and bounded visible content."
    },
    "nvim.diagnostics": {
      "description": "Return current diagnostics from LSP and linters."
    },
    "nvim.headless_eval": {
      "description": "Run bounded headless Neovim Lua/Vimscript probes."
    }
  }
}
```

This keeps editor/workspace introspection aligned with ACP, while execution remains explicitly tool-shaped.

## Single-question lifecycle

```text id="qygbyf"
1. ACP session starts from Neovim.
2. User asks one Bash-track question.
3. Codex normalizes the question.
4. Codex asks MCP:
   - workspace.nvim for current buffer/diagnostics
   - marimo.context for syllabus/ref slices
   - exercism.bash for exercise metadata/tests if needed
5. Codex invokes MCP validation tools if useful:
   - shellcheck
   - shfmt
   - bash -n
   - bash-test-runner
   - bash-analyzer
6. Codex returns one response through ACP.
7. Marimo persists compact linear context.
```

## Better naming

Avoid saying “Codex inspects workspace” directly. More precise:

```text id="v24wob"
Codex requests workspace facts over ACP/MCP.
```

Avoid saying “Codex runs validation” directly. More precise:

```text id="bmqq9h"
Codex requests validation via MCP tools.
```

## Initial iteration target

```text id="4tw3pd"
Build an ACP-first, MCP-backed Bash-track assistant.

Primary:
  - ACP session through Neovim / agent client
  - MCP resource server for Exercism Bash and local refs
  - MCP tool server for nvim headless, ShellCheck, shfmt, Bats, analyzer, test-runner

Secondary:
  - Marimo notebook as implementation/runtime for context slicing and session continuity
```

That preserves the architecture: **ACP is the agent session surface; MCP is the controlled tool/resource plane; Marimo is a persistent implementation surface behind MCP, not the protocol boundary itself.**

[1]: https://github.com/agentclientprotocol/agent-client-protocol "GitHub - agentclientprotocol/agent-client-protocol: A protocol for connecting any editor to any agent · GitHub"
[2]: https://modelcontextprotocol.io/docs/concepts/resources "Resources - Model Context Protocol"
