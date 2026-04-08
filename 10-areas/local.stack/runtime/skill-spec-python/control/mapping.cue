package specpythoncontrol

mapping: {
	state: {
		source: "specs/source/state.schema.json"
		cue:    "specs/cue/state.cue"
		output: "generated/python/state_models.py"
	}
	session: {
		source: "specs/source/session.schema.json"
		cue:    "specs/cue/session.cue"
		output: "generated/python/session_models.py"
	}
	output: {
		source: "specs/source/output.schema.json"
		cue:    "specs/cue/output.cue"
		output: "generated/python/output_models.py"
	}
	runtime_binding: {
		source: "specs/source/runtime.binding.schema.json"
		note:   "tracked locally for runtime alignment, not emitted as a v1 Python target"
	}
}
