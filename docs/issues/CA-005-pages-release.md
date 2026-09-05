# CA-005 — Package, verify, and deploy the Pages demonstration

<!-- context-atlas
github_state: open
implementation_state: complete
-->

**Proposed labels:** `agent-task`, `type:integration`, `priority:P1`  
**GitHub issue:** [#5](https://github.com/virgil-barnard/agent_demo/issues/5)

## Motivation

Context Atlas is complete only when the deterministic graph and browser assets are
assembled into a GitHub Pages artifact and its reproducibility is enforced.

## Scope

Complete the build entry point so it copies checked-in static assets and generated
data into one output directory. Add end-to-end tests comparing two builds byte for
byte. Add a GitHub Actions workflow that builds that directory and deploys it with
the supported GitHub Pages actions. Document local build and artifact inspection.

## Non-goals

- A custom hosting server.
- Runtime deployment secrets or GitHub API access by the application.
- Altering repository branch-protection or GitHub Pages repository settings.

## Dependencies

- [#2 — CA-002](https://github.com/virgil-barnard/agent_demo/issues/2)
- [#3 — CA-003](https://github.com/virgil-barnard/agent_demo/issues/3)
- [#4 — CA-004](https://github.com/virgil-barnard/agent_demo/issues/4)

## Acceptance criteria

- A documented explicit build command creates a self-contained static output
  directory containing HTML, CSS, JavaScript, and graph data.
- Two builds from identical inputs produce identical relative paths and bytes.
- The workflow invokes the repository build command, uploads only generated output,
  and deploys through GitHub Pages actions with least-necessary permissions.
- Documentation states that a repository administrator must enable GitHub Pages
  with GitHub Actions if it is not already enabled.
- No generated artifact contains absolute paths, timestamps, credentials, or
  machine-local data.

## Validation

```bat
.venv\Scripts\python.exe -m pytest tests/test_context_atlas_build.py
.venv\Scripts\python.exe -m pytest
scripts\check.cmd
```

Inspect the workflow and generated output manifest. After merge, confirm the
GitHub Actions deployment and Pages URL in the issue evidence record.

## Expected artifacts

- `src/agent_demo/context_atlas/build.py`
- `tests/test_context_atlas_build.py`
- `.github/workflows/deploy-pages.yml`
- `README.md`
- `docs/evidence/issue-N.md` (after publication and successful completion)

## Context manifest

| Role | Path or URL | Why it matters |
|---|---|---|
| Read | `AGENTS.md` | Required validation and deterministic artifact rules. |
| Read | `docs/requirements.md` | REQ-CA-001 and REQ-CA-009. |
| Read | `docs/architecture.md#build-and-deployment` | Output and deployment design. |
| Read | `src/agent_demo/context_atlas/build.py` | Build entry point to finalize. |
| Read | `web/index.html` | Required static asset. |
| Edit | `src/agent_demo/context_atlas/build.py` | Package assets and graph data. |
| Create | `tests/test_context_atlas_build.py` | End-to-end reproducibility check. |
| Create | `.github/workflows/deploy-pages.yml` | GitHub Pages deployment. |
| Edit | `README.md` | Local build and Pages documentation. |
| Create | `docs/evidence/issue-N.md` | Completion provenance for the published issue. |
| Test | `scripts/check.cmd` | Complete repository gate. |
| Reference | `docs/decisions/DEC-CA-002-static-site-and-build.md` | Technology and deployment decision. |

## Planning references

- [REQ-CA-001](../requirements.md)
- [REQ-CA-009](../requirements.md)
- [DEC-CA-002](../decisions/DEC-CA-002-static-site-and-build.md)
