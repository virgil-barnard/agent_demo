# CA-003 — Implement static provenance graph application

<!-- context-atlas
github_state: draft
implementation_state: planned
-->

**Proposed labels:** `agent-task`, `type:feature`, `priority:P1`  
**GitHub issue:** [#3](https://github.com/virgil-barnard/agent_demo/issues/3)

## Motivation

Generated provenance data must be understandable to a viewer as a compelling,
inspectable graph rather than raw JSON.

## Scope

Create checked-in vanilla HTML, CSS, and JavaScript assets that load the generated
graph JSON by relative URL. Render a deterministic SVG graph, filters, legend,
selection details, adjacent relationships, and edge provenance evidence. Style
GitHub state and implementation state as distinct visual encodings.

## Non-goals

- Context-budget controls and ranking display (CA-004).
- Packaging or Pages deployment (CA-005).
- External libraries, CDN assets, or runtime network calls.

## Dependencies

- [#2 — CA-002](https://github.com/virgil-barnard/agent_demo/issues/2)

## Acceptance criteria

- The app works when served solely as static files with the generated JSON.
- It presents nodes and edges for each required artifact category and lets users
  filter and select them.
- A selected node shows stable identity, path, state, adjacent relationships, and
  edge evidence path/line range.
- Legend and styles unambiguously distinguish both state vocabularies.
- Layout and display ordering are deterministic for the same JSON input.
- JavaScript has no dependency-manager or external-network requirement.

## Validation

```bat
.venv\Scripts\python.exe -m pytest tests/test_context_atlas_index.py
.venv\Scripts\python.exe -m pytest
scripts\check.cmd
```

Manually serve a generated artifact with a local static server if available and
exercise selection/filtering without any browser-console network request beyond the
relative graph-data file.

## Expected artifacts

- `web/index.html`
- `web/styles.css`
- `web/app.js`
- `tests/test_context_atlas_web_contract.py`

## Context manifest

| Role | Path or URL | Why it matters |
|---|---|---|
| Read | `AGENTS.md` | Validation and no-unnecessary-dependency policy. |
| Read | `docs/requirements.md` | REQ-CA-004 and REQ-CA-005. |
| Read | `docs/architecture.md` | Static-app and JSON contracts. |
| Read | `src/agent_demo/context_atlas/model.py` | Generated schema consumer contract. |
| Create | `web/index.html` | Static application shell. |
| Create | `web/styles.css` | State and responsive visual design. |
| Create | `web/app.js` | Graph interaction and evidence rendering. |
| Create | `tests/test_context_atlas_web_contract.py` | Static-asset and data-contract checks. |
| Test | `scripts/check.cmd` | Complete repository gate. |
| Reference | `docs/architecture.md#static-application` | UI constraints. |

## Planning references

- [REQ-CA-004](../requirements.md)
- [REQ-CA-005](../requirements.md)
- [DEC-CA-002](../decisions/DEC-CA-002-static-site-and-build.md)
