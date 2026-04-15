## Filter objects based on the contents of a key

E.g., I only want objects whose `genre` key contains `"house"`.

```shell
$ json='[{"genre":"deep house"}, {"genre": "progressive house"}, {"genre": "dubstep"}]'
$ echo "$json" | jq -c '.[] | select(.genre | contains("house"))'
{"genre":"deep house"}
{"genre":"progressive house"}
```

If it is possible that some objects might not contain the key you want to check, and you just want to ignore the objects that don't have it, then the above will need to be modified. For example:

```shell
$ json='[{"genre":"deep house"}, {"genre": "progressive house"}, {"volume": "wubwubwub"}]'
$ echo "$json" | jq -c '.[] | select(.genre | . and contains("house"))'
```

If your version of jq supports `?` then it could also be used:

```shell
$ echo "$json" | jq -c '.[] | select(.genre | contains("house"))?'
```

In jq version 1.4+ (that is, in sufficiently recent versions of jq after 1.4), you can also use regular expressions, e.g. using the "`$json`" variable defined above:

```shell
$ echo "$json" | jq -c 'map( select(.genre | test("HOUSE"; "i")))'
[{"genre":"progressive house"},{"genre":"progressive house"}]
```

Note: use a semi-colon ("`;`") to separate the arguments of `test`.

