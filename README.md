# Model Run Notebook

Summarize recorded model runs, supplied usage, latency, and assertion-pass counts.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external service, or network access is required.

## Run

```console
python -m runs_tool --help
python -m runs_tool examples/sample.json
python -m runs_tool --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Requires recorded runs {id,model,input_tokens,output_tokens,latency_ms,passed}, up to 1000. Unique IDs and boolean assertion outcomes are required. Groups supplied usage, latency totals/averages, and pass rates by model label. Usage is not measured by this tool; pass flags are not independent model-quality judgments. No current pricing, cost estimate, recommendation, provider call, or external benchmark is included.

## Learning focus

User-directed personal AI/LLM/agent exploration. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `runs_tool/core.py`: validated parsing, storage, or state transitions.
- `runs_tool/cli.py`: JSON command interface.
- `runs_tool/generate_fixtures.py`: original deterministic validation cases.
- `runs_tool/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 259 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
