# Issue 5 evidence — Package, verify, and deploy the Pages demonstration

- **Issue:** [#5 — Package, verify, and deploy the Pages demonstration](https://github.com/virgil-barnard/agent_demo/issues/5)
- **Requirements addressed:** REQ-CA-001 (static provenance graph) and
  REQ-CA-009 (reproducible generation).

## Decisions and implementation

- The build command now replaces the requested output directory, copies every
  checked-in file under `web/` in sorted order, and writes `graph.json` beside
  those assets. It rejects an output path that could delete the repository or
  source assets.
- The end-to-end test compares complete relative-path-to-byte mappings from two
  builds and confirms the artifact has HTML, CSS, JavaScript, graph data, and a
  nested static asset.
- The Pages workflow builds with the module entry point, uploads only `build/`,
  and uses the supported Pages upload and deployment actions with `contents: read`,
  `pages: write`, and `id-token: write` permissions.
- No dependencies changed; standard-library `shutil.copyfile` implements asset
  copying in accordance with DEC-CA-002.

## Context consulted

- `AGENTS.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/decisions/DEC-CA-002-static-site-and-build.md`
- `src/agent_demo/context_atlas/build.py`
- `web/index.html`
- `README.md`, `pyproject.toml`, and `scripts/check.cmd`
- `tests/test_context_atlas_index.py` and `tests/test_context_atlas_web_contract.py`

## Files

- Updated `src/agent_demo/context_atlas/build.py`,
  `tests/test_context_atlas_index.py`, `docs/architecture.md`,
  `docs/issues/CA-005-pages-release.md`, and `README.md`.
- Created `tests/test_context_atlas_build.py`,
  `.github/workflows/deploy-pages.yml`, and this evidence record.

## Validation

- `.venv\Scripts\python.exe -m pytest tests/test_context_atlas_build.py` — 1 passed.
- `.venv\Scripts\python.exe -m pytest` — 14 passed.
- `scripts\check.cmd` — passed (environment isolation, pip check, formatting,
  lint, 14 tests, and compilation).
- Generated output manifest inspected by `tests/test_context_atlas_build.py`:
  `app.js`, `assets/logo.txt`, `graph.json`, `index.html`, and `styles.css`.

## Publication

- **Local implementation commit:** `252ec99b5fa59ca4a63dfc473210778082a5de3a`.
- **Publishing blocked:** `git push origin main` was rejected because the
  configured Personal Access Token lacks the `workflow` scope required to create
  `.github/workflows/deploy-pages.yml`. No commit reached `main`, so there are no
  commit-specific artifact links or a deployment URL yet.

## Limitations

- Repository Pages settings and the post-merge deployment URL require a
  repository administrator and GitHub Actions; neither is changed by this issue.
