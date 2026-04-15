## Filter objects based on tags in an array

In this section, we discuss how to select items from an array of objects each of which has an array of tags, where the selection is based on the presence or absence of a given tag in the array of tags.

For the sake of illustration, suppose the following sample JSON is in a file named `input.json`:

```jsonc
[ { "name": "Item 1",
    "tags": [{ "name": "TAG" },  { "name": "TAG" }, { "name": "Not-TAG" } ] },
  { "name": "Item 2",
    "tags": [ { "name": "Not-TAG" } ] } ]
```

Notice that the first item is tagged twice with the tag "`TAG`".

Here is a jq filter that will select the objects with the tag "`TAG`":

```jsonc
map(select( any(.tags[]; .name == "TAG" )))
```

In words: select an item if any of its tags matches "`TAG`".

Using the `-c` command-line option would result in the following output:

```jsonc
[{"name":"Item 1","tags":[{"name":"TAG"},{"name":"TAG"},{"name":"Not-TAG"}]}]
```

Using `any/2` here is recommended because it allows the search for the matching tag to stop once a match is found.

A less efficient approach would be to use `any/0`:

```jq
map(select([ .tags[] | .name == "TAG" ] | any))
```

The subexpression `[ .tags[] | .name == "TAG" ]` creates an array of boolean values, where `true` means the corresponding tag matched; this array is then passed as input to the `any` filter to determine whether there is a match.

If the tags are distinct, the subexpression could be written as `select(.tags[] | .name == "TAG")` with the same results; however if this subexpression is used, then the same item will appear as many times as there is a matching tag, as illustrated here:

```shell
$ jq 'map(select(.tags[] | .name == "TAG"))[] | .name'  input.json
"Item 1"
"Item 1"
```

### Selecting all items that do _NOT_ have a specific tag

To select items that do _NOT_ have the "TAG" tag, we could use `all/2` or `all/0` with the same results:

```shell
$ jq -c 'map(select( all( .tags[]; .name != "TAG") ))'  input.json
[{"name":"Item 2","tags":[{"name":"Not-TAG"}]}]
```

```shell
$ jq -c 'map(select([ .tags[] | .name != "TAG" ] | all))'  input.json
[{"name":"Item 2","tags":[{"name":"Not-TAG"}]}]
```

Using `all/2` would be more efficient if only because it avoids the intermediate array.

