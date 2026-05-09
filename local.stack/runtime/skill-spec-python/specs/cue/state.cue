package specpython

import "time"

#RepoRef: {
	root:   #NonEmptyString
	head?:  string
	branch?: string
}

#Freshness: {
	mode: "cached" | "fresh" | "hydrated"
	source_snapshot_id?: string
}

#StateV1: {
	schema_version: "state.v1"
	snapshot_id:    #NonEmptyString
	repo_ref:       #RepoRef
	observed_at:    time.Time
	freshness:      #Freshness
	state: {
		git:       _
		semantic:  _
		workspace: _
	}
	provenance: {
		backend: "gix" | "sem" | "combined"
		inputs:  [...string]
		warnings: [...string]
	}
}
