# Context Atlas delivery plan

The plan is intentionally dependency-ordered so an implementation agent can take
one bounded issue at a time. Local drafts mirror the published GitHub issues.

| Planning ID | GitHub issue | Outcome | Depends on |
|---|---|---|---|
| CA-001 | [#1](https://github.com/virgil-barnard/agent_demo/issues/1) | Durable contracts, metadata schema, and planning baseline | — |
| CA-002 | [#2](https://github.com/virgil-barnard/agent_demo/issues/2) | Deterministic provenance index and graph-data generator | [#1](https://github.com/virgil-barnard/agent_demo/issues/1) |
| CA-003 | [#3](https://github.com/virgil-barnard/agent_demo/issues/3) | Static interactive graph application | [#2](https://github.com/virgil-barnard/agent_demo/issues/2) |
| CA-004 | [#4](https://github.com/virgil-barnard/agent_demo/issues/4) | Deterministic context-budget explorer | [#2](https://github.com/virgil-barnard/agent_demo/issues/2), [#3](https://github.com/virgil-barnard/agent_demo/issues/3) |
| CA-005 | [#5](https://github.com/virgil-barnard/agent_demo/issues/5) | Reproducible packaging and GitHub Pages delivery | [#2](https://github.com/virgil-barnard/agent_demo/issues/2), [#3](https://github.com/virgil-barnard/agent_demo/issues/3), [#4](https://github.com/virgil-barnard/agent_demo/issues/4) |

## Delivery rules

- Publish only after explicit user authorization.
- Replace planning IDs with GitHub issue numbers and URLs at publication time.
- Keep the issue metadata mirrored in its local draft as work progresses.
- Each implementation issue creates `docs/evidence/issue-N.md` only after it has a
  published GitHub number.
- Run the issue validation and the complete [`scripts/check.cmd`](../scripts/check.cmd)
  gate before completing any issue.

## Planned validation strategy

Unit tests cover metadata parsing, ID validation, AST relationships, ordering,
budget boundaries, and browser-independent JSON contracts. Integration tests build
two independent output directories and compare their relative file names and bytes.
The release issue validates the static artifact and deployment workflow structure.
