### Shell config

Put this in your shell rc:

```bash
# stable, machine-friendly defaults
alias jqc='jq -c'
alias jqr='jq -r'
alias jqS='jq -S'

# useful combo for deterministic JSON output
alias jqfmt='jq -S .'
```

### Repo layout

Use files, not giant one-liners:

```text
tools/
  jq/
    lib/
      shape.jq
      keys.jq
    filters/
      strip_noise.jq
      inspect_keys.jq
```

Then call them like this:

```bash
jq -f tools/jq/filters/inspect_keys.jq sample.json
jq -L tools/jq/lib -f tools/jq/filters/strip_noise.jq sample.json
```

Using `-f` reads filters from files, and `-L` sets the module search path. ([Jq][1])

### Optional env

Only set these if you care:

```bash
export NO_COLOR=1
# or customize colors instead of disabling them
# export JQ_COLORS="0;90:0;39:0;39:0;39:0;32:1;39:1;39:1;34"
```

`jq` respects `NO_COLOR`, and color output can be customized with `JQ_COLORS`. ([Jq][1])


