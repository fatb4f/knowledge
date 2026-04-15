## Exactly

That pattern is **not** “directory traversal from scratch.” It is **prefix rescue**:

* you already know part of the path
* you want completion to take over from that partial prefix
* you want the picker rooted at that prefix, not at `$PWD` or `$HOME`

That is precisely what fzf’s completion path is built for. The docs show forms like `cd ~/github/fzf**<TAB>` and `vim ../fzf**<TAB>`, where the text before `**` becomes the base path/prefix for completion. ([GitHub][1])

## How your two examples map

### `cd ~/.local/share/<TAB>`

What you want semantically is:

* command type: **directory completion**
* base path: `~/.local/share`
* result: pick a directory under that subtree

In stock fzf completion, the documented form is:

```bash
cd ~/.local/share/**<TAB>
```

not bare `cd ~/.local/share/<TAB>`. The docs explicitly show `cd **<TAB>` and `cd ~/github/fzf**<TAB>` for directory completion. ([GitHub][1])

If you override `_fzf_compgen_dir`, fzf passes the base path as `$1`, so your generator can start traversal from `~/.local/share` instead of searching globally. ([GitHub][1])

### `cp ~/.cache/<TAB>`

This is a **path completion** case, not a dir-only traversal case, because `cp` may need a file source or a directory destination depending on position. The corresponding fzf hook is `_fzf_compgen_path`, which also receives the base path as `$1`. If `cp` is not already covered in your enabled command set, you can register it with `_fzf_setup_completion path cp`. ([GitHub][1])

So the fzf-style form is:

```bash
cp ~/.cache/**<TAB>
```

with `_fzf_compgen_path` controlling how candidates are produced from that subtree. ([GitHub][1])

## The key design insight

Your real need is:

> “When I already know the path prefix, let completion continue from there.”

That means the right mechanism is **completion rooted at a partial prefix**, not `ALT-C`.

`ALT-C` is for “I want to jump to some directory.”
Your pattern is “I already typed part of the argument; now finish it fuzzily.” Those are different workflows. fzf separates them the same way: key bindings are one surface, fuzzy completion is another. ([GitHub][1])

## Recommended policy

Use this split:

* `ALT-C` for **open-ended directory jump**
* fzf completion for **partial-path rescue**
* `_fzf_compgen_dir` for dir-only subtree generation
* `_fzf_compgen_path` for file/dir subtree generation
* `_fzf_setup_completion` to classify extra commands like `cp` if needed ([GitHub][1])

## Minimal practical shape

```bash
_fzf_compgen_path() {
  fd --hidden --follow --exclude ".git" . "$1"
}

_fzf_compgen_dir() {
  fd --type d --hidden --follow --exclude ".git" . "$1"
}

_fzf_setup_completion path cp
```

Then the workflow becomes:

```bash
cd ~/.local/share/**<TAB>
cp ~/.cache/**<TAB>
```

That is the clean answer to the pattern you described. ([GitHub][1])

## Bottom line

You were reaching for a catch-all traversal tool, but your recurring case is actually **prefix-aware fuzzy completion**. For that case, completion is the right control surface, and the `compgen` functions are the right place to shape the candidate source. ([GitHub][1])

[1]: https://github.com/junegunn/fzf "GitHub - junegunn/fzf: :cherry_blossom: A command-line fuzzy finder · GitHub"

