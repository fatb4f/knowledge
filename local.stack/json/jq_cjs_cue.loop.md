# 1. inspect data shape
jq '[.. | objects | keys[]] | unique' sample.json

# 2. validate schema itself
check-jsonschema --check-metaschema schema.json

# 3. validate instances
check-jsonschema --schemafile schema.json sample.json

# 4. then import/refine in CUE
cue import schema.json
