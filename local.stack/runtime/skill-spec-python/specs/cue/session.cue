package specpython

import "time"

#Staleness: {
	mode: "fresh" | "stale" | "unknown"
	observed_at?: time.Time
}

#SessionV1: {
	artifact_type:    "session"
	artifact_version: "v1"
	session_id:       #NonEmptyString
	host:             "marimo"
	transport:        "direct" | "mcp" | "acp"
	staleness:        #Staleness
	lineage_refs?:    [...string]
}
