Use this mental model.

## 1. **Core selector layer**

This is the irreducible `fzf` contract:

* **input**: a list on stdin
* **interaction**: fuzzy filter over that list
* **output**: selected line(s) on stdout

That is the base abstraction. `fzf` is a general-purpose interactive Unix filter, not a file manager or file finder by itself. ([GitHub][1])

## 2. **Candidate source layer**

This is where your filesystem semantics come from.

Examples:

* `fd -t d "$prefix"` for directory walk mode
* `fd . "$prefix"` for mixed file/dir mode
* `rg ...` for grep-driven mode
* `find ...` if you need portability

For your use case, this is the layer that decides whether the picker is:

* walker
* file picker
* grep picker
* action target picker

`fzf` itself does not supply those semantics; it consumes whatever list you feed it. ([GitHub][1])

## 3. **Presentation layer**

This is the mostly static UI shell:

* `--height`
* `--layout`
* `--info`
* `--border`
* `--margin`
* `--padding`
* `--tmux`

This layer is about how the picker appears, not what it means. It is the right place for your stable “always use this layout” defaults. The docs explicitly suggest putting recurring display choices in `FZF_DEFAULT_OPTS`. ([GitHub][1])

## 4. **Matching / path-tuning layer**

This is where you tune ranking/filter behavior for the kind of input you are feeding:

* `--scheme=path` for file paths
* optionally `--delimiter`, `--nth`, `--with-nth` for structured lines

For your filesystem picker, `--scheme=path` is the key one to remember. The README explicitly calls out path-oriented schemes for file path input. ([GitHub][2])

## 5. **Preview layer**

This is where `fzf` becomes navigable rather than just selectable.

* `--preview '...'`
* `--preview-window ...`

Important: preview is just an external command run through your shell with the current item substituted in. `fzf` does not have built-in directory preview semantics; whatever your command prints is what appears. That is why branching on candidate type is the key move for your design. ([GitHub][2])

For your case, this layer should do:

* directory → `tree -C -L 2 ...` or `eza`
* file → `bat ...`
* fallback → `file --brief ...`

## 6. **Event/action layer**

This is the real power layer, and the one that matters most for replacing Yazi.

The primitive is:

* `--bind 'key:event-or-action(...)'`

The core actions you care about are:

* **`execute(...)` / `execute-silent(...)`**
  Run an external command and return to `fzf`. Good for quick actions like yank/copy-path/open-preview. ([GitHub][2])

* **`become(...)`**
  Replace `fzf` with another process. Good for `enter -> nvim`, `ctrl-g -> lazygit`, etc. ([GitHub][2])

* **`reload(...)`**
  Replace the candidate list dynamically from another command. This is the critical primitive for your “walk into selected directory” model. It can be bound to keys or events. ([GitHub][2])

This is the layer that turns a picker into a workflow surface.

## 7. **Mode/state layer**

This is not a named `fzf` feature, but it is the design pattern you are building out of bindings.

Your picker will have implicit modes such as:

* **walk mode**

  * source: directories only
  * preview: tree depth 2
  * enter: descend via `reload(...)`

* **pick mode**

  * source: files + dirs
  * preview: branch on type
  * enter: return selection or `become(nvim {})`

* **action mode**

  * source already captured
  * new list is destination candidates
  * accept runs action with `source` and `dest`

`fzf` does not provide “modes” directly; you synthesize them by changing the candidate source and binds, mainly with `reload(...)` and action bindings. The official advanced examples show exactly this pattern when switching data sources and rebuilding the list on keypress or input change. ([GitHub][2])

## 8. **Shell integration layer**

This is separate from your custom picker.

There are two different concerns:

### A. Shell key bindings and built-ins

Examples:

* `CTRL-T`
* `CTRL-R`
* `ALT-C`

These are prepackaged shell integrations. They are useful, but not the right place to define your full custom walker/action tool. ([GitHub][3])

### B. Completion customization

This is where `_fzf_comprun` belongs.

`_fzf_comprun` customizes the `fzf` invocation used by shell completion, and the first parameter is the command being completed; the remaining args are forwarded to `fzf`. That is why the docs show:

```bash
local command=$1
shift
```

This is strictly completion policy, not your general picker/workflow engine. ([GitHub][2])

## 9. **Performance / safety layer**

Two rules matter for your design:

* Do **not** put a file-specific preview into `FZF_DEFAULT_OPTS`, because `fzf` is fed many non-file inputs in other contexts. The README explicitly warns against this. ([GitHub][3])
* Keep expensive preview and tokenization features scoped to the workflows that need them. The README notes that features like `--ansi`, `--nth`, and `--with-nth` carry cost. ([GitHub][3])

## Minimal map for **your** implementation

### Layer A: stable UI defaults

Set only general layout here:

* height
* reverse layout
* border
* maybe tmux popup

### Layer B: candidate generators

Write small shell functions:

* `cand_walk "$prefix"`
* `cand_pick "$prefix"`
* maybe `cand_grep "$prefix" "$query"`

### Layer C: preview dispatcher

One function:

* dir → tree depth 2
* file → bat
* other → file/stat

### Layer D: action table

Bindings for:

* descend
* open in nvim
* launch lazygit
* copy path
* switch mode
* reload

### Layer E: wrapper commands

Build your own scripts/functions:

* `walk_pick`
* `walk_open`
* `walk_action yank`
* `walk_action move`

That is the layer where your real workflow lives.

## If you want the shortest “what do I actually need to learn first?” answer

Only learn these first:

* `--preview`
* `--bind`
* `reload(...)`
* `execute(...)`
* `become(...)`
* `--scheme=path`
* `_fzf_comprun` only for completion customization

Everything else is secondary for your use case. ([GitHub][2])

## Recommended implementation order

1. **Static picker**

   * `fd -t d | fzf --scheme=path --preview ...`

2. **Type-branching preview**

   * directory vs file

3. **Walk mode**

   * bind key to `reload(...)` with selected dir as new prefix

4. **Action binds**

   * `become(nvim {})`
   * `execute-silent(...)`

5. **Two-phase source/destination action**

   * wrapper function around two picks
   * only later try to compress into one clever stateful session

That order matches the official feature surfaces and keeps complexity contained. ([GitHub][2])

If useful, I can reduce this one step further into a **1-page implementation blueprint** with exact function boundaries and no prose.

[1]: https://github.com/junegunn/fzf/blob/master/ADVANCED.md "fzf/ADVANCED.md at master · junegunn/fzf · GitHub"
[2]: https://github.com/junegunn/fzf/blob/master/README.md "fzf/README.md at master · junegunn/fzf · GitHub"
[3]: https://github.com/junegunn/fzf "GitHub - junegunn/fzf: :cherry_blossom: A command-line fuzzy finder · GitHub"

