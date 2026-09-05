# Issue 3 evidence — Implement static provenance graph application

- **Issue:** [#3 — Implement static provenance graph application](https://github.com/virgil-barnard/agent_demo/issues/3)
- **Requirements addressed:** REQ-CA-004 (distinct progress states) and REQ-CA-005
  (interactive traceability).

## Decisions and implementation

- Added a dependency-free static application that fetches only the relative
  `graph.json` artifact and renders its nodes and relationships in SVG.
- The deterministic layout groups a stable, fixed kind order and sorts each group
  by node ID. Filters constrain visible types and issue state values.
- The legend uses separate GitHub-state borders and implementation-state stroke
  widths. Selecting a node shows its stable identity, repository path, line range,
  states, adjacent edges, and each edge's evidence path and range.
- No dependencies changed; the checked-in HTML, CSS, and JavaScript follow
  DEC-CA-002's vanilla static-site decision.

## Context consulted

- `AGENTS.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/decisions/DEC-CA-002-static-site-and-build.md`
- `src/agent_demo/context_atlas/model.py`
- `src/agent_demo/context_atlas/build.py`
- `tests/test_context_atlas_index.py`
- `pyproject.toml` and `scripts/check.cmd`

## Files

- Created `web/index.html`, `web/styles.css`, and `web/app.js`.
- Created `tests/test_context_atlas_web_contract.py` for relative-asset, graph-data,
  filtering, state-encoding, and evidence-rendering contracts.
- Created this evidence record.

## Validation

- `.venv\Scripts\python.exe -m pytest tests/test_context_atlas_web_contract.py tests/test_context_atlas_index.py` — 9 passed.
- `.venv\Scripts\python.exe -m pytest` — passed.
- `scripts\check.cmd` — passed.

## Publication

- **Implementation commit:**
  [`19fb404e26b3c34161004a263527c5e6ecfb2402`](https://github.com/virgil-barnard/agent_demo/commit/19fb404e26b3c34161004a263527c5e6ecfb2402).
- **Artifacts:** [static application](https://github.com/virgil-barnard/agent_demo/tree/19fb404e26b3c34161004a263527c5e6ecfb2402/web),
  [contract tests](https://github.com/virgil-barnard/agent_demo/blob/19fb404e26b3c34161004a263527c5e6ecfb2402/tests/test_context_atlas_web_contract.py),
  and this evidence record.

## Limitations

- Browser interaction is implemented in vanilla JavaScript; repository validation
  checks its static contract but does not include a browser automation harness.
