## List keys used in any object in a list

If you have an array of JSON objects and want to obtain a listing of the top-level keys in these objects, consider:

```jq
add | keys
```

If you want to obtain a listing of all the keys in all the objects, no matter how deeply nested, you can use this filter:

```jq
[.. | objects | keys[]] | unique
```

For example, given the array: 

```jsonc
[{"a": {"b":1}}, {"a": {"c":2}}]
```

the previous filter will produce: 

```jsonc
["a", "b", "c"]
```

## Include or import a module and call its functions

Key points:
- If the module, say `M.jq`, is located in `~/.jq/` or `~/.jq/M/` then there should be no need to invoke jq with the -L option unless there is a file M.jq in the pwd;
- The search path can be specified using the command-line option: `-L <path>` 
-- the path may be relative or absolute, and may begin with `~/`
- `include "filename";` 
-- a reference to filename.jq
- `include "filename" {"search": "PATH"};`
-- e.g. `jq -n 'include "sigma" {search: "~/jq"}; sigma(inputs)'`
- `import "filename" as symbol;` 
-- a reference to `filename.jq`
- `::` is the scope resolution operator, e.g. `builtin::walk`

### Example 1: `~/.jq/library/library.jq`

1. Copy the definition of `walk/1` to `$HOME/.jq/library/library.jq` (see e.g. https://github.com/jqlang/jq/blob/master/src/builtin.jq)

2. Invoke jq:

```shell
jq 'include "library"; walk(if type == "object" then del(.foo) else . end)' <<< '{"a":1, "foo": 2}'
```

### Example 2: `~/jq/library.jq`

1. Copy the definition of `walk/1` to `$HOME/jq/library.jq` (see e.g. https://github.com/jqlang/jq/blob/master/src/builtin.jq)

2. Invoke jq with the `-L` option:

```shell
jq -L $HOME/jq 'import "library" as lib;
   lib::walk(if type == "object" then del(.foo) else . end)' <<< '{"a":1, "foo": 2}'
```

