# Issue #2 evidence — Build deterministic repository provenance index

- **Issue:** [#2 — Build deterministic repository provenance index](https://github.com/virgil-barnard/agent_demo/issues/2)
- **Requirements addressed:** REQ-CA-001, REQ-CA-002, REQ-CA-003, REQ-CA-008, and REQ-CA-009.
- **Decision followed:** [DEC-CA-001](../decisions/DEC-CA-001-reproducible-issue-source.md) and the standard-library constraint in [DEC-CA-002](../decisions/DEC-CA-002-static-site-and-build.md).

## Implementation

The `agent_demo.context_atlas.build` module accepts explicit `--repository-root`
and `--output-dir` arguments. It reads approved UTF-8 Markdown and Python files,
uses `ast` for imports without importing target code, validates declared metadata
and graph references, and writes sorted schema-versioned `graph.json` output.
The implementation uses no new dependencies. Issue drafts now record their tracked
GitHub and implementation state snapshots in the documented metadata block.

## Context consulted

`AGENTS.md`, `pyproject.toml`, `docs/requirements.md`, `docs/architecture.md`,
`docs/decisions/DEC-CA-001-reproducible-issue-source.md`,
`docs/decisions/DEC-CA-002-static-site-and-build.md`, all tracked issue drafts,
`README.md`, and `scripts/check.cmd`.

## Changed files

- Added `src/agent_demo/context_atlas/__init__.py`, `build.py`, `model.py`, and
  `parse.py`.
- Added `tests/test_context_atlas_index.py`.
- Updated `docs/architecture.md` and the issue-draft state metadata under
  `docs/issues/`.
- This evidence record is `docs/evidence/issue-2.md`.

## Tests and validation

- Added focused tests for output ordering, AST import edges, deterministic bytes,
  invalid states, duplicate requirement IDs, missing paths, missing node
  references, and CLI diagnostics.
- `.venv\Scripts\python.exe -m pytest tests/test_context_atlas_index.py` — 7 passed.
- `.venv\Scripts\python.exe -m pytest` — 8 passed.
- `scripts\check.cmd` — passed (environment integrity, dependency check,
  formatting, linting, tests, and compilation).
- The publication commit SHA is recorded in the issue completion comment after it
  reaches `main`.

## Limitations

Context profiles provide deterministic declared-provenance candidates. Budget
scoring and greedy packing are intentionally deferred to issue #4. The generated
graph is a tracked-input snapshot; it does not query GitHub at build or browser
runtime.
