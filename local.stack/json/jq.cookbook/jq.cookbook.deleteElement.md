## Delete elements from objects recursively

A straightforward and general way to delete key/value pairs from all objects, no matter where they occur, is to use `walk/1`. (If your jq does not have `walk/1`, then you can copy its definition from https://github.com/jqlang/jq/blob/master/src/builtin.jq)

For example, to delete all "foo" keys, you could use the filter: 

```jq
walk(if type == "object" then del(.foo) else . end)
```

It may also be possible to use the `recurse` builtin, as shown in the following example.

Let's take the [`recurse` example](http://jqlang.github.io/jq/manual/#recurse) from the manual, and add a bunch of useless `{"foo": "bar"}` to it:

```jsonc
{"name": "/", "foo": "bar", "children": [
  {"name": "/bin", "foo": "bar", "children": [
    {"name": "/bin/ls", "foo": "bar", "children": []},
    {"name": "/bin/sh", "foo": "bar", "children": []}]},
  {"name": "/home", "foo": "bar", "children": [
    {"name": "/home/stephen", "foo": "bar", "children": [
      {"name": "/home/stephen/jq", "foo": "bar", "children": []}]}]}]}
```

`recurse(.children[]) | .name` will give me all the `name`s, but destroy the structure of the JSON in the process.

Is there a way to get that information, but preserve the structure?

That is, with the JSON above as input, the desired output would be:

```jsonc
{"name": "/", "children": [
  {"name": "/bin", "children": [
    {"name": "/bin/ls", "children": []},
    {"name": "/bin/sh", "children": []}]},
  {"name": "/home", "children": [
    {"name": "/home/stephen", "children": [
      {"name": "/home/stephen/jq", "children": []}]}]}]}
```

**Explanation**

In order to remove the "foo" attribute from each element of the structure, you want to recurse through the structure and set each element to the result of deleting the `foo` attribute from itself. This translates to jq as:

```jq
recurse(.children[]) |= del(.foo)
```

If, instead of blacklisting `foo`, you'd rather whitelist `name` and `children`, you could do something like:

```jq
recurse(.children[]) |= {name, children}
```

_(This recipe is from [#263](https://github.com/jqlang/jq/issues/263).)_

