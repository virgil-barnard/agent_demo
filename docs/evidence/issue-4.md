# Issue 4 evidence — Add deterministic context-budget explorer

- **Issue:** [#4 — Add deterministic context-budget explorer](https://github.com/virgil-barnard/agent_demo/issues/4)
- **Requirements addressed:** REQ-CA-006 (deterministic context-budget explorer)
  and REQ-CA-007 (visible budget effects).

## Decisions and implementation

- Added dependency-free ranking and greedy packing functions. Costs remain the
  graph's deterministic `ceil(UTF-8 byte count / 4)` estimates.
- Profiles now include stable score components, rationale, and provenance routes
  for selected issues, direct requirements, implementation/tests, dependencies,
  and supporting requirement documents.
- The issue detail panel renders a numeric estimated-token budget, included and
  excluded artifacts, total, threshold, and the explicit mandatory-budget message.
- No dependencies changed; this follows the standard-library and vanilla-browser
  approach in DEC-CA-002.

## Context consulted

- `AGENTS.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/decisions/DEC-CA-002-static-site-and-build.md`
- `src/agent_demo/context_atlas/build.py`, `model.py`, and `parse.py`
- `web/index.html`, `web/app.js`, and `web/styles.css`
- `tests/test_context_atlas_index.py` and `tests/test_context_atlas_web_contract.py`
- `pyproject.toml` and `scripts/check.cmd`

## Files

- Created `src/agent_demo/context_atlas/context_budget.py` and
  `tests/test_context_budget.py`.
- Updated graph-profile generation, the browser explorer, architecture policy,
  issue metadata/context manifest, and relevant contract tests.
- Created this evidence record.

## Validation

- `.venv\Scripts\python.exe -m pytest tests/test_context_atlas_index.py tests/test_context_budget.py` — 10 passed.
- `.venv\Scripts\python.exe -m pytest tests/test_context_atlas_index.py tests/test_context_budget.py tests/test_context_atlas_web_contract.py` — 12 passed.
- `.venv\Scripts\python.exe -m pytest` — 13 passed.
- `scripts\check.cmd` — passed (pip check, format, lint, and 13 tests).

## Publication

- **Implementation commit:** [`fa8010ed93fcfbb8fa094cdbd4179e08170959ef`](https://github.com/virgil-barnard/agent_demo/commit/fa8010ed93fcfbb8fa094cdbd4179e08170959ef).
- **Artifacts:** [budget logic](https://github.com/virgil-barnard/agent_demo/blob/fa8010ed93fcfbb8fa094cdbd4179e08170959ef/src/agent_demo/context_atlas/context_budget.py), [tests](https://github.com/virgil-barnard/agent_demo/blob/fa8010ed93fcfbb8fa094cdbd4179e08170959ef/tests/test_context_budget.py), and [browser explorer](https://github.com/virgil-barnard/agent_demo/blob/fa8010ed93fcfbb8fa094cdbd4179e08170959ef/web/app.js).

## Limitations

- Browser behavior has a static contract test; no browser automation harness is
  configured in this repository.
