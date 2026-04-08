package specpython

#OutputV1: {
	artifact_type:    "output"
	artifact_version: "v1"
	encoding:         "json" | "ndjson" | "jsonl"
	schema_ref:       #NonEmptyString
	streaming?:       bool
	notes?:           [...string]
}
