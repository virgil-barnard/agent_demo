# CA-002 — Build deterministic repository provenance index

**Proposed labels:** `agent-task`, `type:feature`, `type:architecture`, `priority:P1`  
**GitHub issue:** [#2](https://github.com/virgil-barnard/agent_demo/issues/2)

## Motivation

The static application needs validated, deterministic graph data derived from
tracked repository inputs rather than runtime GitHub or filesystem access.

## Scope

Implement a standard-library package module and CLI that scans the approved
Markdown/Python inputs, parses requirements and issue-draft metadata, parses Python
imports with `ast`, validates all references, and emits the versioned graph JSON.
Emit loadable artifact records and deterministic context-profile candidates as
specified by the architecture. Add focused unit and reproducibility tests.

## Non-goals

- Rendering the graph or context explorer in a browser.
- GitHub Pages workflow configuration.
- Fuzzy relationship extraction or executing repository Python code.

## Dependencies

- [#1 — CA-001](https://github.com/virgil-barnard/agent_demo/issues/1)

## Acceptance criteria

- A documented module entry point accepts explicit repository-root and output
  directory arguments and returns nonzero with clear diagnostics for invalid input.
- It emits schema-versioned, sorted UTF-8 JSON with normalized `/` paths and no
  host-specific or timestamp values.
- It creates nodes for documents, requirements, issue drafts, source, and tests;
  edges have evidence paths and line ranges.
- It validates duplicate/missing IDs, invalid state values, and missing referenced
  files or nodes.
- Python imports are determined using `ast` without importing target modules.
- Tests prove output ordering, validation failures, import edges, and byte-identical
  generation into two output directories.

## Validation

```bat
.venv\Scripts\python.exe -m pytest tests/test_context_atlas_index.py
.venv\Scripts\python.exe -m pytest
scripts\check.cmd
```

## Expected artifacts

- `src/agent_demo/context_atlas/__init__.py`
- `src/agent_demo/context_atlas/build.py`
- `src/agent_demo/context_atlas/model.py`
- `src/agent_demo/context_atlas/parse.py`
- `tests/test_context_atlas_index.py`
- `tests/fixtures/context_atlas/` (only deterministic, minimal fixture inputs)

## Context manifest

| Role | Path or URL | Why it matters |
|---|---|---|
| Read | `AGENTS.md` | Standard-library and deterministic-output obligations. |
| Read | `pyproject.toml` | Package layout and test configuration. |
| Read | `docs/requirements.md` | REQ-CA-001, 002, 003, 008, and 009. |
| Read | `docs/architecture.md` | Input, JSON, and ranking contracts. |
| Read | `docs/decisions/DEC-CA-001-reproducible-issue-source.md` | Authoritative issue source. |
| Read | `docs/issues/CA-002-provenance-index.md` | Metadata format to parse. |
| Create | `src/agent_demo/context_atlas/build.py` | Deterministic builder entry point. |
| Create | `src/agent_demo/context_atlas/model.py` | Typed graph and validation model. |
| Create | `src/agent_demo/context_atlas/parse.py` | Markdown and AST analysis. |
| Create | `tests/test_context_atlas_index.py` | Index and determinism contract tests. |
| Test | `scripts/check.cmd` | Complete repository gate. |
| Reference | `docs/architecture.md#graph-data-contract` | Output schema authority. |

## Planning references

- [REQ-CA-001 through REQ-CA-003](../requirements.md)
- [REQ-CA-008 and REQ-CA-009](../requirements.md)
- [Architecture](../architecture.md)
