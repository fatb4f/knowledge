Below is a **courseware-style map** of the stack you are actually sitting on with a near-vanilla LazyVim setup. The most useful way to study it is in **two layers**:

1. **Core platform**: Neovim itself as an editor runtime, API host, UI server, and structured text engine.
2. **Foundational plugins**: the subsystem plugins that LazyVim wires together to turn that runtime into an IDE-shaped environment.

LazyVim itself autoloads `lua/config/{autocmds,keymaps,lazy,options}.lua`, loads plugin specs from `lua/plugins/*.lua`, and configures included plugins using the same `lazy.nvim` spec model you would use in a scratch setup. Its docs also expose picker/completion switching knobs such as `vim.g.lazyvim_picker` and `vim.g.lazyvim_cmp`, so treat “vanilla LazyVim” as a curated distribution over a stable architecture rather than one frozen manifest. ([LazyVim][1])

---

# Guide 1: Core platform

## 1. What Neovim is, architecturally

The right mental model is **not** “a terminal editor with plugins.” Neovim’s own architecture docs describe the UI as **decoupled from the core editor**: the builtin TUI is just one client, external UIs can connect to the same editor server, and external plugins run in separate processes. Neovim also builds its platform and I/O layer on **libuv**, which is why async jobs, timers, subprocesses, RPC, and filesystem/event integration feel native rather than bolted on. ([Neovim][2])

For an advanced LazyVim user, this matters because most of the modern “magic” you experience is just structured composition on top of that architecture:

* the editor core owns buffers, windows, diagnostics, extmarks, folds, and the RPC/API boundary;
* UIs render state from that core;
* plugins orchestrate behavior by calling APIs and responding to events. ([Neovim][2])

## 2. Startup and initialization pipeline

Neovim’s startup order is worth learning because many “why did this option/plugin/keymap win?” questions reduce to load order. The `starting` docs say Neovim processes command-line arguments, starts a server unless `--listen` was given, waits for a UI if started with `--embed`, sets up default mappings/autocmds, enables filetype and indent plugins, and then loads user config. If you start with `-u NONE`, plugins and syntax highlighting are skipped; if you start with `-u NORC`, config loading is skipped without disabling as much built-in behavior. ([Neovim][3])

LazyVim then adds its own second-stage structure on top of that. Its docs say files under `lua/config` are loaded automatically at the appropriate time, and plugin specs under `lua/plugins/` are loaded automatically by `lazy.nvim`. This is why a LazyVim config feels “sparse”: much of the orchestration is delegated to the distro’s autoload structure rather than explicit `require()` chains in your `init.lua`. ([LazyVim][1])

### Practical implication

When debugging startup:

* use `nvim -V1log` when you need core startup tracing;
* use `:Lazy`, `:Lazy profile`, and `:Lazy debug` for the plugin layer;
* use `:checkhealth` for environment/runtime breakage. ([Neovim][3])

## 3. The three API layers you actually program against

Neovim’s Lua guide explicitly describes **three API layers**:

* the inherited **Vim API**: Ex commands and Vimscript functions, accessed from Lua via `vim.cmd()` and `vim.fn`;
* the **Nvim API**: low-level C/RPC APIs accessed as `vim.api`;
* the **Lua API / stdlib**: higher-level Lua-first functions under `vim.*`. ([Neovim][4])

That separation is foundational. In practice:

* use `vim.api` for exact editor state manipulation;
* use `vim.lsp`, `vim.diagnostic`, `vim.fs`, `vim.uv`, `vim.iter`, etc. when the stdlib already exposes the abstraction you need;
* fall back to `vim.fn` or `vim.cmd` mainly for legacy/editor command surfaces that do not yet have a better Lua wrapper. ([Neovim][4])

### Rule of thumb

A clean Neovim config moves **upward** in abstraction:

* `vim.cmd("set number")` is legacy-compatible;
* `vim.opt.number = true` is standard Lua config style;
* `vim.api.nvim_set_option_value(...)` is precise and explicit when you need buffer/window scope control. ([Neovim][4])

## 4. Runtime model: runtimepath, packpath, built-in packages

Core Neovim still has a package/runtime model independent of third-party managers. The `health` docs note that Neovim depends on `$VIMRUNTIME`, `'runtimepath'`, and `'packpath'` to find syntax files, filetype behavior, and standard plugins. The `plugins` docs also note that some bundled plugins/modules are loaded by default while others are activated with `:packadd`. ([Neovim][5])

This is important for two reasons.

First, **not everything is “third-party plugin land.”** Neovim ships built-ins like `editorconfig`, `matchparen`, `netrw`, `man.lua`, `tohtml`, `undotree`, and others. Some are always on, some are on-demand package plugins. That means your baseline editing environment already has a plugin architecture before LazyVim or `lazy.nvim` ever enter the picture. ([Neovim][6])

Second, it explains why package-manager choices are mostly about **distribution and orchestration**, not fundamental capability. Whether you use `vim.pack`, `lazy.nvim`, or something else, the core runtime still resolves files and modules through Neovim’s runtime mechanisms. ([Neovim][6])

## 5. Text model: buffers, windows, tabpages, namespaces, extmarks

One of the most important under-the-hood concepts is that Neovim’s visible UI is mostly just a projection over structured state. Buffers hold text, windows view buffers, tabpages group windows, and many plugin features are anchored using **extmarks** and namespaces. The API docs show extmarks can carry virtual text, signs, highlight groups, conceal behavior, priorities, and even UI-watched rendering hints. They are the backbone for diagnostics, inline annotations, code lenses, sign columns, git hunks, and many custom overlays. ([Neovim][7])

If you want to understand why good plugins coexist while bad ones fight, this is the answer: plugins that cooperate with Neovim’s text model usually express themselves as **piecewise edits plus extmark/decorations**, rather than overwriting whole buffers or faking screen state. That same philosophy is why Conform’s minimal-diff behavior matters later in the plugin layer. ([Neovim][7])

### What to internalize

* Extmarks are not just “marks.”
* They are the universal attachment point for editor metadata.
* Diagnostics, Treesitter highlights, signs, virtual text, and many UI decorations all compete or compose here through priorities and namespaces. ([Neovim][7])

## 6. UI protocol: why Neovim can have GUIs and experimental UI layers

The `api-ui-events` docs describe external UIs as client processes that communicate with Neovim over the RPC API. A UI calls `nvim_ui_attach()` and then renders grids and optional externalized widgets. The UI can choose a grid model, RGB behavior, and extension capabilities. ([Neovim][8])

That is why features like:

* Neovide,
* remote UI clients,
* `noice.nvim`,
* 0.12’s `ui2`,
* externalized cmdline/messages/popupmenu

all sit on the same conceptual foundation. Neovim is not redrawing “a terminal app” in the old sense; it is emitting structured UI events that can be rendered by the builtin TUI or by an external client. ([Neovim][8])

For a LazyVim user, the practical lesson is that UI plugins are not merely cosmetic. They are often **adapters** or **policy layers** over real editor subsystems:

* statusline and tabline plugins render state;
* message/cmdline plugins intercept or restyle UI events;
* diagnostics/gitsigns/pickers often depend on structured editor data rather than raw text scraping. ([Neovim][8])

## 7. LSP as a core subsystem, not just a plugin feature

Neovim’s LSP docs define a real core API for creating/managing clients and for buffer-level operations. LSP methods are handled by Lua handlers, with explicit request/response/notification signatures. In 0.12, Neovim further expanded built-in LSP with better diagnostics, health checking, and more first-party surfaces. ([Neovim][9])

This means that in a modern LazyVim setup, `nvim-lspconfig` is not “the LSP engine.” The engine is **Neovim itself**. `nvim-lspconfig` is the configuration catalog and adapter layer that feeds per-server configs into the core client. That distinction matters when you customize behavior:

* `vim.lsp.*` = core runtime behavior;
* `nvim-lspconfig` = server registry/config composition;
* LazyVim = orchestration and defaults around both. ([Neovim][9])

## 8. Diagnostics are a first-class framework

Neovim’s diagnostic docs describe diagnostics as a general framework for displaying warnings/errors from LSP servers and non-LSP tools, extending existing quickfix/location-list workflows. This is the bridge that lets LSP, linters, formatters, git surfaces, and UI plugins converge on a shared representation of problems in your code. ([Neovim][10])

The key lesson is that diagnostics are **not owned by LSP**. LSP is just one producer. `nvim-lint`, external tools, or your own custom tooling can publish diagnostics into the same system. Once you understand that, plugins like Trouble stop looking like isolated tools and start looking like alternate renderers over a shared diagnostic/event graph. ([Neovim][10])

## 9. Treesitter in core Neovim

Neovim’s Treesitter docs describe parsed syntax trees (`TSTree`) and nodes (`TSNode`) as structured representations of buffer content that can be traversed and queried. Core features and plugins use those trees for highlighting, textobjects, motions, and semantic structure. ([Neovim][11])

This is one of the biggest conceptual upgrades over classic regex syntax systems. Once you think in syntax trees rather than line-oriented regex rules, a lot of plugin behavior becomes easier to explain:

* syntax highlighting is more precise;
* motions can target function/class/parameter objects;
* comment behavior can vary by embedded language region;
* rename/select/jump features become syntax-aware rather than text-pattern-aware. ([Neovim][11])

## 10. Core platform study checklist

If you want to truly understand the platform under LazyVim, study these in order:

1. `:help lua-guide`
2. `:help api`
3. `:help api-ui-events`
4. `:help lsp`
5. `:help diagnostic`
6. `:help treesitter`
7. `:help starting`
8. `:checkhealth` and `:checkhealth vim.lsp` ([Neovim][4])

### Lab work for the core platform

Use these drills:

* start `nvim -u NORC` and inspect what disappears versus your LazyVim session;
* run `:lua vim.print(vim)` and then inspect `vim.api`, `vim.lsp`, `vim.diagnostic`;
* open `:checkhealth`, then `:checkhealth vim.lsp`;
* use `:lua` to place an extmark with virtual text in a scratch buffer;
* attach to a file with LSP and inspect buffer-local keymaps and diagnostics producers. ([Neovim][12])

---

# Guide 2: Foundational plugins

## 1. What “foundational” means in a LazyVim setup

For a vanilla LazyVim user, foundational plugins are the ones that establish the **control plane** of the editor, not just extra features. LazyVim’s docs group them into coding, editor, formatting, linting, LSP, Treesitter, UI, and util categories, and the distro’s README presents it as a Neovim setup powered by `lazy.nvim`. ([LazyVim][13])

The right way to study these is **by subsystem**, not alphabetical plugin list. In practice, the core subsystems are:

* plugin/package orchestration,
* language intelligence,
* syntax/structural editing,
* formatting and linting,
* navigation and problem lists,
* git/workspace state,
* UI composition and session/runtime utilities. ([LazyVim][13])

## 2. The orchestration layer: `lazy.nvim` + LazyVim’s spec model

`lazy.nvim` is the package/orchestration substrate. Its spec model defines source, dependencies, setup hooks, lazy-loading triggers, versioning, and advanced composition via `specs`/`optional`/`import`. It also explicitly recommends using `opts` instead of `config` whenever possible, because `opts` participates in spec merging and automatic setup heuristics. ([lazy.folke.io][14])

LazyVim sits on top of that model. Its plugin docs say customization is the same as building with `lazy.nvim` directly; `cmd`, `event`, `ft`, `keys`, `opts`, and `dependencies` are merged according to predictable rules; other properties override defaults. This is the most important operational habit in a distro setup: **override the spec, not the world**. ([LazyVim][15])

### Operational rule

For included plugins:

* prefer `opts = { ... }` or `opts = function(_, opts) ... end`;
* use `enabled = false` to disable;
* add new lazy triggers or keymaps by extending the spec;
* avoid replacing `config` unless you intentionally want to take over plugin setup. ([LazyVim][15])

### Why this matters

If you bypass the spec model, you break LazyVim’s composition. Its formatting docs explicitly warn not to override `plugin.config` for `conform.nvim`, because that breaks LazyVim formatting integration. The same design logic applies more broadly: LazyVim wants to remain the orchestrator, while you customize through merged options. ([LazyVim][16])

## 3. Language intelligence layer

## A. `nvim-lspconfig`

In current LazyVim, LSP is anchored by `neovim/nvim-lspconfig` plus Mason integration. LazyVim’s LSP config shows it using:

* global and server-specific keymaps,
* built-in Neovim inlay hints,
* built-in code lens wiring,
* built-in folds via `vim.lsp.foldexpr()`,
* diagnostics config via `vim.diagnostic.config()`,
* `vim.lsp.config(server, opts)` and `vim.lsp.enable(server)` for actual client setup. ([LazyVim][17])

The big lesson is that `lspconfig` is the **server config catalog** and LazyVim is the **policy layer**. LazyVim adds capability-based keymaps, automatic registration, file-operation capabilities, and server setup hooks; Neovim itself owns the active clients and editor semantics. ([LazyVim][17])

### What to study

* how LazyVim declares `servers = { ... }`;
* the special `["*"]` default server entry;
* the `setup` hook table for custom server wiring;
* the handoff between Mason-managed installs and direct `vim.lsp.enable()`. ([LazyVim][17])

## B. `mason.nvim` and `mason-lspconfig.nvim`

LazyVim uses Mason in two roles:

* package installer for tools/servers,
* bridge to server enablement. ([LazyVim][17])

Its docs show `mason.nvim` being given an `ensure_installed` list, invoking `:MasonUpdate` as a build step, refreshing the Mason registry, and auto-installing missing tools. `mason-lspconfig.nvim` is then used to map lspconfig server names to Mason packages and to auto-enable installed servers, excluding any that LazyVim intentionally manages differently. ([LazyVim][17])

### Mental model

* `mason.nvim` manages external binaries.
* `mason-lspconfig.nvim` maps binaries to server configs.
* `nvim-lspconfig` defines those server configs.
* Neovim core runs the LSP clients.
* LazyVim composes the policy across all four. ([LazyVim][17])

## C. `lazydev.nvim`

LazyVim includes `lazydev.nvim` in its coding stack for Lua/Neovim-config development. Its docs say it configures LuaLS to support completion and type checking while editing your Neovim config, and the default library includes `luv`, `LazyVim`, `snacks.nvim`, `lazy.nvim`, and `nvim-lspconfig`. ([LazyVim][18])

This is an unusually important plugin for distro users because it makes your configuration itself a first-class codebase. Without it, editing your own Neovim Lua tends to feel much more weakly typed and less discoverable. ([LazyVim][18])

## D. Completion engine: `blink.cmp` / auto completion engine selection

LazyVim’s current docs expose `vim.g.lazyvim_cmp` with `auto` and list supported completion-engine choices including `nvim-cmp` and `blink.cmp`. Its installation page also lists `curl` for `blink.cmp`, and the `blink.cmp` project itself describes the plugin as a batteries-included completion engine for LSP, cmdline, signature help, and snippets, with pluggable sources and an optional custom fuzzy matcher. ([LazyVim][1])

For study purposes, completion should be understood as a pipeline:

* source gathering,
* filtering/fuzzy ranking,
* presentation/rendering,
* acceptance/commit behavior,
* snippet expansion / signature help interaction. ([GitHub][19])

The practical takeaway is that completion is **not** the same subsystem as LSP even when LSP is the most important source. Completion sits at the interaction boundary between editor state, source providers, and UI. ([GitHub][19])

## 4. Structural editing layer

## A. `nvim-treesitter`

LazyVim includes `nvim-treesitter` as its main structure engine and sets up highlighting, indentation, folding, and parser installation via `ensure_installed`. The upstream `nvim-treesitter` project describes itself as providing parser install/update/remove functions, query collections that enable Treesitter-based Neovim features, and a staging ground for Treesitter features considered for upstreaming. It also warns that the current mainline is an incompatible rewrite relative to older setups. ([LazyVim][20])

This plugin is foundational because it sits between syntax trees and user-facing editing semantics. Everything that says “syntax-aware” is probably touching Treesitter:

* structural textobjects,
* language-aware comments,
* better highlighting,
* tag insertion,
* some motion and selection tools. ([GitHub][21])

## B. `nvim-treesitter-textobjects`

LazyVim enables `nvim-treesitter-textobjects` with motions such as next/previous function, class, and parameter boundaries, and it dynamically attaches buffer-local mappings only when the relevant textobject queries exist. ([LazyVim][20])

This is an ideal example of plugin architecture done correctly:

* Treesitter provides syntax nodes and queries,
* the textobjects plugin maps those queries into semantic motions,
* LazyVim adds capability-aware buffer-local bindings. ([LazyVim][20])

## C. `mini.ai`, `ts-comments.nvim`, `nvim-ts-autotag`

LazyVim’s coding and Treesitter pages show a strong structural-editing bias:

* `mini.ai` extends textobjects with Treesitter-backed “function,” “class,” “block,” and other semantic selections;
* `ts-comments.nvim` improves comment syntax for mixed-language buffers;
* `nvim-ts-autotag` auto-manages closing tags for HTML/JSX-like grammars. ([LazyVim][18])

The important thing to study here is **division of labor**:

* Treesitter supplies structure;
* small focused plugins map that structure into editing actions. ([GitHub][21])

## 5. Formatting and linting layer

## A. `conform.nvim`

LazyVim uses `conform.nvim` for formatting. Its docs emphasize that formatter config belongs in `opts.formatters`, `opts.formatters_by_ft`, and format options passed through the plugin’s setup model. Upstream, Conform’s README highlights two design points that matter technically: it preserves extmarks and folds by calculating minimal diffs, and it repairs bad-behaving LSP formatters by converting whole-buffer replacements into proper piecewise edits using built-in LSP format utilities. ([LazyVim][16])

That makes Conform more than a “run prettier/black/shfmt” wrapper. It is a **text-edit application layer** tuned to cooperate with Neovim’s buffer model. That matters a lot in a heavily decorated editor where Treesitter highlights, folds, diagnostics, signs, and virtual text are all attached to buffer state. ([GitHub][22])

## B. `nvim-lint`

LazyVim uses `nvim-lint` to asynchronously invoke linters and publish their output into `vim.diagnostic`. Its linting docs show event-driven triggering, filetype-to-linter mappings, optional global or fallback linters, and a resolution path that handles full filetypes, split filetypes, and conditional linter activation. ([LazyVim][23])

This is the cleanest example of Neovim’s “diagnostics are a shared framework” philosophy:

* `nvim-lint` is not part of LSP;
* it still feeds the same diagnostic surfaces used by LSP;
* UIs such as Trouble or sign/virtual-text renderers do not need to care which producer generated the problem. ([LazyVim][23])

## C. `trouble.nvim`

LazyVim includes `trouble.nvim` as a problem-list/navigation layer for diagnostics, symbols, LSP references/definitions, location list, quickfix list, and TODO integration. In the docs, its default mappings expose separate entry points for diagnostics, symbols, LSP mode, loclist, qflist, and previous/next item traversal. ([LazyVim][24])

Treat Trouble as a **diagnostic/query browser**, not merely a prettier quickfix window. It is foundational because it turns the editor’s various problem streams into a structured navigation interface. ([LazyVim][24])

## 6. Navigation and editing ergonomics

## A. `flash.nvim`

LazyVim includes `flash.nvim` for fast labeled jumps, Treesitter-backed jumps, remote operations, and search toggling. Its default mappings wire it into normal, visual, operator-pending, and command-line modes, including a Treesitter-based selection flow that can stand in for incremental selection. ([LazyVim][24])

This is worth studying because it shows a very Neovim-native pattern: enrich built-in motions instead of replacing the editing model wholesale. Flash does not invent a separate editor; it plugs into search, operator-pending mode, and Treesitter. ([LazyVim][24])

## B. `which-key.nvim`

LazyVim includes `which-key.nvim` and uses it as the discoverability layer for its large keymap surface. Its defaults register grouped prefixes like tabs, code, debug, file/find, git, search, and quit/session. ([LazyVim][24])

Conceptually, which-key is foundational because it is how a large compositional config remains learnable. In a distribution, keymaps are not just bindings; they are a discoverable command taxonomy. ([LazyVim][24])

## C. `grug-far.nvim`, `todo-comments.nvim`

LazyVim includes `grug-far.nvim` for multi-file search/replace and `todo-comments.nvim` for indexed comment markers like TODO/FIX/HACK. Both integrate into the broader problem/search surfaces, and TODOs can be routed through Trouble or search commands. ([LazyVim][24])

These are good examples of **domain-specific indexers**: they harvest structured project information and expose it through Neovim-native navigation surfaces rather than acting as separate applications. ([LazyVim][24])

## 7. Git, workspace, and runtime utility layer

## A. `gitsigns.nvim`

LazyVim includes `gitsigns.nvim` and exposes toggles for git signs in its editor stack. Upstream, Gitsigns centers much of its setup on an `on_attach` callback for buffer-local mappings and behavior. That is the right mental model: git hunks are attached to specific buffers and rendered as signs/decorations in the editor surface. ([LazyVim][24])

Study Gitsigns as a composition of:

* repo state detection,
* per-buffer diffing,
* sign/extmark rendering,
* staged/reset/preview actions. ([GitHub][25])

## B. `snacks.nvim`

`snacks.nvim` is now one of the most strategically important plugins in the LazyVim ecosystem. Upstream it describes itself as a collection of small QoL plugins, but the feature list is broad: bigfile handling, buffer deletion, dashboard, explorer, git utilities, notifier, picker, quickfile, scope, terminal, words, and more. It also notes that some components must be set up early and that setup itself creates autocmds without eagerly loading the whole world. ([GitHub][26])

LazyVim uses Snacks across multiple categories:

* UI: indent, input, notifier, scope, scroll, words, dashboard;
* util: bigfile, quickfile, terminal, scratch/profiler scratch;
* LSP: picker integrations, rename-file action, document-highlight jumps. ([LazyVim][27])

This makes Snacks a **meta-foundational** plugin in modern LazyVim. It is not one feature; it is an umbrella layer that absorbs a lot of formerly separate “small utility plugin” space. ([GitHub][26])

## C. `persistence.nvim` and `plenary.nvim`

LazyVim includes `persistence.nvim` for automatic session management and `plenary.nvim` as a shared Lua utility library used by other plugins. Persistence is workflow state; Plenary is ecosystem infrastructure. ([LazyVim][28])

You rarely “study Plenary” for user-visible behavior, but you should recognize it as one of the common dependency layers in the Neovim plugin ecosystem. ([LazyVim][28])

## 8. UI composition layer

## A. `lualine.nvim` and `bufferline.nvim`

LazyVim’s UI stack includes `lualine.nvim` and `bufferline.nvim`. Upstream, Lualine supports statusline, tabline, and winbar composition, including buffer and tab components; LazyVim uses Bufferline to render tab/buffer-like UI with diagnostics and delete-buffer callbacks routed through Snacks. ([LazyVim][27])

These plugins are best understood as **state renderers**:

* they do not own project/file/problem state;
* they render state produced elsewhere by diagnostics, git plugins, sessions, buffers, and editor options. ([LazyVim][27])

## B. `noice.nvim`

LazyVim includes `noice.nvim`, while upstream Noice describes itself as a highly experimental replacement for messages, cmdline, and popupmenu UI. That places it directly in the part of the stack closest to Neovim’s UI-event protocol and 0.12’s evolving message/cmdline story. ([GitHub][29])

For you, the practical lesson is that Noice is powerful precisely because it is near the **UI protocol boundary**. That also makes it more sensitive than, say, a file explorer or statusline plugin. ([GitHub][29])

## 9. How to customize this stack safely

The safest pattern in vanilla LazyVim is to treat each plugin as a **spec extension point**, not an object you reinitialize manually. Use `lua/plugins/*.lua` and merge `opts`, `keys`, `ft`, `event`, `cmd`, or `dependencies` into the existing spec. LazyVim’s docs state those merge rules explicitly, and the distro auto-loads every spec file in that directory. ([LazyVim][15])

A minimal customization pattern looks like this:

```lua
-- lua/plugins/my_lsp.lua
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        pyright = {
          settings = {
            python = {
              analysis = {
                typeCheckingMode = "basic",
              },
            },
          },
        },
      },
    },
  },
}
```

That style composes with LazyVim’s defaults instead of replacing them. The same pattern applies to Snacks, Trouble, Treesitter, Gitsigns, and most other included plugins. ([LazyVim][15])

## 10. Suggested learning order for a vanilla LazyVim user

Study the plugin layer in this order:

1. `lazy.nvim` spec model and `:Lazy` UI
2. LazyVim merge rules and file layout
3. `nvim-lspconfig` + Mason + diagnostics
4. `nvim-treesitter` + textobjects
5. Conform + `nvim-lint` + Trouble
6. Snacks as the modern utility/meta layer
7. Gitsigns + persistence
8. Lualine / Bufferline / Noice as UI renderers/adapters ([lazy.folke.io][14])

## 11. Lab sequence for foundational plugins

Use this progression:

* `:Lazy` → inspect one plugin at a time, note triggers and dependencies.
* `:checkhealth lazy`, `:checkhealth vim.lsp`, `:checkhealth snacks`.
* Open a Lua file and inspect how `lazydev.nvim` changes completion/type help.
* Add one LSP server override under `lua/plugins/`.
* Add one Treesitter parser and one textobject motion.
* Add one Conform formatter and one `nvim-lint` linter.
* Change one Snacks module setting and one Trouble mode setting.
* Disable one default keymap by setting it to `false` in a plugin spec. ([lazy.folke.io][30])

---

## Bottom line

For a vanilla LazyVim setup, the shortest correct model is:

* **Neovim core** is the editor runtime, API host, UI server, structured text engine, diagnostic framework, and LSP client. ([Neovim][2])
* **LazyVim foundational plugins** are the orchestration and policy layer that turn those primitives into a cohesive developer environment. `lazy.nvim` manages the package/spec graph; `nvim-lspconfig`/Mason manage language tooling; Treesitter and small structural plugins manage syntax-aware editing; Conform and `nvim-lint` manage code hygiene; Trouble, Gitsigns, Snacks, Lualine, Bufferline, and Noice render or navigate shared editor state. ([lazy.folke.io][14])

A strong next step would be to turn this into a **vanilla LazyVim reverse-engineering syllabus**, with one lesson per subsystem and concrete exercises against your live config.

[1]: https://lazyvim.github.io/configuration/general "General Settings | LazyVim"
[2]: https://neovim.io/doc/user/vim_diff/ " Vim_diff - Neovim
      docs"
[3]: https://neovim.io/doc/user/starting/ " Starting - Neovim
      docs"
[4]: https://neovim.io/doc/user/lua-guide/ " Lua-guide - Neovim
      docs"
[5]: https://neovim.io/doc/user/health/ " Health - Neovim
      docs"
[6]: https://neovim.io/doc/user/plugins/ " Plugins - Neovim
      docs"
[7]: https://neovim.io/doc/user/api/ " Api - Neovim
      docs"
[8]: https://neovim.io/doc/user/api-ui-events/ " Api-ui-events - Neovim
      docs"
[9]: https://neovim.io/doc/user/lsp/ " Lsp - Neovim
      docs"
[10]: https://neovim.io/doc/user/diagnostic/?utm_source=chatgpt.com "Diagnostic - Neovim docs"
[11]: https://neovim.io/doc/user/treesitter/ " Treesitter - Neovim
      docs"
[12]: https://neovim.io/doc/user/lua/ " Lua - Neovim
      docs"
[13]: https://lazyvim.github.io/plugins "Core Plugins | LazyVim"
[14]: https://lazy.folke.io/spec?utm_source=chatgpt.com "Plugin Spec | lazy.nvim"
[15]: https://lazyvim.github.io/configuration/plugins "Plugins | LazyVim"
[16]: https://www.lazyvim.org/plugins/formatting "Formatting | LazyVim"
[17]: https://www.lazyvim.org/plugins/lsp "LSP | LazyVim"
[18]: https://www.lazyvim.org/plugins/coding "Coding | LazyVim"
[19]: https://github.com/Saghen/blink.cmp/blob/main/README.md "blink.cmp/README.md at main · saghen/blink.cmp · GitHub"
[20]: https://www.lazyvim.org/plugins/treesitter "TreeSitter | LazyVim"
[21]: https://github.com/nvim-treesitter/nvim-treesitter "GitHub - nvim-treesitter/nvim-treesitter: Nvim Treesitter configurations and abstraction layer · GitHub"
[22]: https://github.com/stevearc/conform.nvim/blob/master/README.md "conform.nvim/README.md at master · stevearc/conform.nvim · GitHub"
[23]: https://www.lazyvim.org/plugins/linting "Linting | LazyVim"
[24]: https://www.lazyvim.org/plugins/editor "Editor | LazyVim"
[25]: https://github.com/lewis6991/gitsigns.nvim "GitHub - lewis6991/gitsigns.nvim: Git integration for buffers · GitHub"
[26]: https://github.com/folke/snacks.nvim/blob/main/README.md "snacks.nvim/README.md at main · folke/snacks.nvim · GitHub"
[27]: https://www.lazyvim.org/plugins/ui "UI | LazyVim"
[28]: https://www.lazyvim.org/plugins/util "Util | LazyVim"
[29]: https://github.com/folke/noice.nvim "GitHub - folke/noice.nvim:  Highly experimental plugin that completely replaces the UI for messages, cmdline and the popupmenu. · GitHub"
[30]: https://lazy.folke.io/usage " Usage | lazy.nvim"

