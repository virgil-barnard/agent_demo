# Context Atlas requirements

## Product requirements

### REQ-CA-001 — Static provenance graph

The build shall produce a static GitHub-Pages-compatible application and a
versioned graph-data file from tracked repository inputs. It shall work after being
served as static files and shall make no runtime network request.

### REQ-CA-002 — Repository artifact coverage

The graph shall represent repository documents, identified requirement sections,
tracked issue drafts, Python source files, and Python test files. Nodes shall have
stable identifiers and repository-relative paths where applicable.

### REQ-CA-003 — Meaningful, inspectable relationships

The graph shall represent declared requirement, issue, dependency,
implementation, and test relationships, plus Python import relationships where
available. Every edge shall include provenance evidence identifying its input path
and source line range.

### REQ-CA-004 — Distinct progress states

Issue nodes shall expose GitHub state (`draft`, `open`, or `closed`) separately
from implementation state (`planned`, `in_progress`, or `complete`). The interface
shall use a legend and visually distinct encodings for both.

### REQ-CA-005 — Interactive traceability

The application shall let a viewer filter node types and states, select a node,
inspect its metadata and adjacent relationships, and navigate to provenance
evidence sufficient to trace an implementation or test back to its issue and
requirement.

### REQ-CA-006 — Deterministic context-budget explorer

For a selected issue/task and configurable budget, the application shall show a
deterministic ranked set of loadable artifact slices. Each recommendation shall
state its estimated cost, rank rationale, provenance route, and whether it fits.

### REQ-CA-007 — Visible budget effects

Changing the budget shall visibly update the included and excluded context, total
estimated cost, and the next useful threshold. A budget too small for mandatory
context shall yield an explicit explanation rather than silently overflowing.

### REQ-CA-008 — Input validation

The builder shall reject malformed metadata, duplicate identifiers, invalid state
values, missing referenced paths, and missing referenced node identifiers with
actionable diagnostics.

### REQ-CA-009 — Reproducible generation

Generated files shall use UTF-8, `/` repository-relative paths, stable IDs, sorted
records and JSON keys, and no wall-clock or host-specific data. A test shall prove
identical inputs yield byte-identical output.

## Constraints

- Python 3.11+ standard library is preferred for analysis and generation.
- The site uses vanilla HTML, CSS, and JavaScript; no browser package manager is
  required.
- The generated Pages site must be deployable by GitHub Actions.
- The cost shown by the explorer is a documented deterministic estimate, not a
  claim of exact model-token counts.

## Acceptance evidence

Each delivered requirement is linked from an issue draft under
[`docs/issues/`](issues/) and later recorded in an issue evidence file under
[`docs/evidence/`](evidence/).
