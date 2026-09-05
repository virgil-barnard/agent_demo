# CA-001 — Establish Context Atlas planning contracts

<!-- context-atlas
github_state: closed
implementation_state: complete
-->

**Proposed labels:** `agent-task`, `type:documentation`, `type:architecture`,
`priority:P1`  
**GitHub issue:** [#1](https://github.com/virgil-barnard/agent_demo/issues/1)

## Motivation

Context Atlas needs stable, reviewable contracts before analysis and UI work can be
independently implemented.

## Scope

Create the vision, requirements, architecture, decisions, delivery plan, evidence
convention, and complete local issue drafts. Define the issue-draft metadata
schema, graph schema, state vocabulary, relationship evidence contract, and
determinism rules.

## Non-goals

- Implementing the analyzer, generated graph, browser application, or workflow.
- Publishing GitHub issues.

## Dependencies

None.

## Acceptance criteria

- Documents define and link `REQ-CA-001` through `REQ-CA-009`.
- The source of GitHub issue data, static delivery approach, and deterministic
  generation rules are recorded as decisions.
- Issue drafts CA-002 through CA-005 are independently executable and dependency
  ordered.
- The metadata and graph contracts state validation/failure behavior.

## Validation

```bat
scripts\check.cmd
```

Review all Markdown links and planning-ID references manually.

## Expected artifacts

- `docs/vision.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/decisions/DEC-CA-001-reproducible-issue-source.md`
- `docs/decisions/DEC-CA-002-static-site-and-build.md`
- `docs/plan.md`
- `docs/evidence/README.md`
- `docs/issues/CA-001-planning-baseline.md` through `docs/issues/CA-005-pages-release.md`

## Context manifest

| Role | Path or URL | Why it matters |
|---|---|---|
| Read | `AGENTS.md` | Environment, validation, and deterministic-output rules. |
| Read | `.opencode/prompts/plan.md` | Required planning and issue-draft format. |
| Read | `README.md` | Establishes the bootstrap baseline. |
| Read | `pyproject.toml` | Existing package and dependency policy. |
| Create | `docs/vision.md` | Product purpose and non-goals. |
| Create | `docs/requirements.md` | Stable acceptance requirements. |
| Create | `docs/architecture.md` | Data, build, and UI contract. |
| Create | `docs/decisions/DEC-CA-001-reproducible-issue-source.md` | Issue-source decision. |
| Create | `docs/decisions/DEC-CA-002-static-site-and-build.md` | Technology and deployment decision. |
| Create | `docs/plan.md` | Dependency-ordered work queue. |
| Create | `docs/issues/CA-002-provenance-index.md` | Next implementation unit. |
| Test | `scripts/check.cmd` | Complete repository gate. |
| Reference | `docs/requirements.md` | Authoritative requirements. |

## Planning references

- [Vision](../vision.md)
- [Requirements](../requirements.md)
- [Architecture](../architecture.md)
- [Delivery plan](../plan.md)
