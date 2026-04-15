## `check-jsonschema`: minimal config

This tool is worth configuring at the repo level. Its main interfaces are CLI flags and pre-commit hook config. It expects exactly one schema-selection mode such as `--schemafile`, `--builtin-schema`, or `--check-metaschema`. It also supports JSON output, color control, caching, and format-check tuning. ([Check JSON Schema][2])

### Best minimal config: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.37.1
    hooks:
      - id: check-metaschema
        files: ^schemas/.*\.json$

      - id: check-jsonschema
        name: validate examples against app schema
        files: ^examples/.*\.(json|ya?ml)$
        args: ["--schemafile", "schemas/app.schema.json"]
```

This is the cleanest place to keep repo policy, and the docs show both `check-jsonschema` and `check-metaschema` as first-class pre-commit hooks. ([Check JSON Schema][3])

### CLI defaults I would standardize on

For manual runs:

```bash
check-jsonschema --check-metaschema schemas/app.schema.json
check-jsonschema --schemafile schemas/app.schema.json examples/*.json
```

For CI:

```bash
check-jsonschema -o JSON --schemafile schemas/app.schema.json examples/*.json
```

Those usage forms are directly supported by the CLI docs. ([Check JSON Schema][2])

### Optional hardening

Only add these if needed:

```bash
# disable strict format checks if tool disagreement becomes noisy
check-jsonschema --disable-formats "*" --schemafile schemas/app.schema.json examples/*.json

# disable remote caching in highly controlled CI
check-jsonschema --no-cache --schemafile schemas/app.schema.json examples/*.json
```

`check-jsonschema` supports disabling format checks and remote-schema caching. ([Check JSON Schema][2])

### Optional parser add-ons

Out of the box it supports JSON and YAML. JSON5 needs an extra dependency; TOML support is documented as available in current versions. ([Check JSON Schema][4])

---

## Minimal working config I would actually use

### Shell

```bash
alias jqfmt='jq -S .'
alias jqc='jq -c'
alias jqr='jq -r'
export NO_COLOR=1
```

### Repo

```text
schemas/
examples/
tools/jq/
.pre-commit-config.yaml
```

### Pre-commit

```yaml
repos:
  - repo: https://github.com/python-jsonschema/check-jsonschema
    rev: 0.37.1
    hooks:
      - id: check-metaschema
        files: ^schemas/.*\.json$
      - id: check-jsonschema
        files: ^examples/.*\.json$
        args: ["--schemafile", "schemas/app.schema.json"]
```

