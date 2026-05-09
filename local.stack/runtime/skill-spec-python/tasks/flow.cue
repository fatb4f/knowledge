package specpython

specToPython: {
	@flow(specToPython)

	steps: {
		validateCue: {
			@task(os.Exec)
			cmd: [
				"bash",
				"-lc",
				"env -u CUE_EXPERIMENT cue vet ./specs/fixtures/*.json ./specs/cue/*.cue",
			]
		}

		validateReport: {
			@task(os.Exec)
			cmd: ["uv", "run", "python", "./scripts/write_validation_report.py"]
		}

		generatePython: {
			@task(os.Exec)
			cmd: ["uv", "run", "python", "./scripts/generate_python.py"]
		}

		generateSchemas: {
			@task(os.Exec)
			cmd: ["uv", "run", "python", "./scripts/generate_schemas.py"]
		}

		runtimeIngressCheck: {
			@task(os.Exec)
			cmd: [
				"bash",
				"-lc",
				"PYTHONPATH=. uv run python -m runtime.jsonargparse_adapter --mode validate --config ./runtime/examples/state.valid.yaml",
			]
		}

		verifyReviewNotebook: {
			@task(os.Exec)
			cmd: [
				"bash",
				"-lc",
				"uv run python -m py_compile ./review/inspect_generated.py",
			]
		}

		verifyGeneratedPython: {
			@task(os.Exec)
			cmd: [
				"bash",
				"-lc",
				"uv run python -m py_compile ./generated/python/*.py",
			]
		}

		verifyReport: {
			@task(os.Exec)
			cmd: ["uv", "run", "python", "./scripts/write_verify_report.py"]
		}
	}
}
