# CA-004 — Add deterministic context-budget explorer

<!-- context-atlas
github_state: open
implementation_state: in_progress
-->

**Proposed labels:** `agent-task`, `type:feature`, `type:test`, `priority:P1`  
**GitHub issue:** [#4](https://github.com/virgil-barnard/agent_demo/issues/4)

## Motivation

The live demonstration must make bounded context selection tangible: viewers need
to see what an agent should load for a task, why it ranks there, and what a budget
change excludes.

## Scope

Implement the documented deterministic ranking/cost policy in the generated data
and a browser explorer for selecting an issue and changing a numeric budget. Show
mandatory context, included/excluded artifact slices, total estimate, rationale,
evidence route, minimum viable budget, and next useful threshold. Add boundary and
ordering tests.

## Non-goals

- Provider-specific tokenizer integration.
- Optimizing arbitrary knapsack combinations contrary to the documented greedy
  provenance-first policy.
- Live task creation or GitHub API queries.

## Dependencies

- [#2 — CA-002](https://github.com/virgil-barnard/agent_demo/issues/2)
- [#3 — CA-003](https://github.com/virgil-barnard/agent_demo/issues/3)

## Acceptance criteria

- Costs use `ceil(UTF-8 byte count / 4)` and are labelled as estimates.
- Candidate order and score explanation match the architecture contract and are
  stable across runs.
- The UI updates included/excluded artifacts, cost, and threshold when a budget
  changes.
- Each candidate exposes its path/section, cost, rationale, and provenance route.
- Insufficient mandatory budget produces an explicit minimum-budget explanation.
- Tests cover tie-breaking, exact fit, insufficient mandatory budget, and changes
  at the next-item threshold.

## Validation

```bat
.venv\Scripts\python.exe -m pytest tests/test_context_atlas_index.py tests/test_context_budget.py
.venv\Scripts\python.exe -m pytest
scripts\check.cmd
```

## Expected artifacts

- `src/agent_demo/context_atlas/context_budget.py`
- `tests/test_context_budget.py`
- `web/app.js`
- `web/styles.css`
- `docs/architecture.md` (only if implementation exposes a needed contract clarification)

## Context manifest

| Role | Path or URL | Why it matters |
|---|---|---|
| Read | `AGENTS.md` | Deterministic test requirements. |
| Read | `docs/requirements.md` | REQ-CA-006 and REQ-CA-007. |
| Read | `docs/architecture.md#context-budget-policy` | Authoritative cost, rank, and packing policy. |
| Read | `src/agent_demo/context_atlas/build.py` | Existing data-generation integration point. |
| Read | `web/app.js` | Existing selection interface. |
| Read | `web/index.html` | Existing semantic details panel that hosts the explorer. |
| Create | `src/agent_demo/context_atlas/context_budget.py` | Deterministic rank and pack logic. |
| Create | `tests/test_context_budget.py` | Ranking and budget-boundary tests. |
| Edit | `web/app.js` | Context explorer controls and rendering. |
| Edit | `web/styles.css` | Explorer state and threshold visuals. |
| Test | `scripts/check.cmd` | Complete repository gate. |
| Reference | `docs/architecture.md#context-budget-policy` | Required algorithm contract. |

## Planning references

- [REQ-CA-006](../requirements.md)
- [REQ-CA-007](../requirements.md)
- [Architecture](../architecture.md)
