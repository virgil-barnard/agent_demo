# Context Atlas architecture

## Overview

The repository contains two products: a deterministic Python build pipeline and a
static browser application. The pipeline consumes tracked content and checked-in
site assets, validates an explicit provenance model, and writes a Pages artifact.
The browser consumes only that artifact.

```text
docs/ + src/ + tests/ + checked-in site assets
                  |
                  v
        Python standard-library builder
                  |
                  v
  generated graph JSON + copied HTML/CSS/JS
                  |
                  v
          GitHub Pages static hosting
```

## Input contract

Issue drafts are Markdown files with a constrained metadata block. The finalized
schema will record an issue ID, title, GitHub state and optional URL/number,
implementation state, requirement IDs, dependencies, implementation paths, and
test paths. Requirements are Markdown headings whose identifiers match
`REQ-CA-<number>`.

The analyzer scans approved tracked Markdown and Python inputs, excluding build
output, virtual environments, caches, `.git`, and third-party directories. Python
imports are parsed through `ast`; no code is imported or executed.

## Graph data contract

The versioned JSON document has these top-level keys:

- `schema_version` — integer format version;
- `nodes` — stable node records with `id`, `kind`, `label`, `path`, optional
  `line_start`/`line_end`, state fields, excerpt, content hash, and estimated cost;
- `edges` — sorted records with `source`, `target`, `kind`, and an `evidence`
  object containing path and line range;
- `artifacts` — loadable document sections or whole source/test files;
- `context_profiles` — deterministic candidate rankings for each issue.

Node IDs are derived from normalized repository-relative paths and stable declared
IDs. Edge evidence points to the source that caused the relationship; UI links use
these paths and lines rather than mutable rendered locations.

## Context-budget policy

An artifact has a deterministic cost of `ceil(UTF-8 byte count / 4)`, labelled
"estimated tokens" in the UI. This deliberately simple estimate is stable across
machines and makes no claim to represent a provider tokenizer.

For an issue, the ranker emits a sorted candidate list:

1. the selected issue draft (mandatory);
2. directly declared requirement sections;
3. declared implementation and test artifacts;
4. declared dependency issue drafts and their requirements;
5. architecture and supporting documents reached by declared provenance.

Each candidate records score components: policy tier (the numbered order above),
artifact kind, normalized path, and line anchor, plus an evidence route. Ties are
resolved by those components in that order. The browser greedily packs this
immutable order without exceeding the selected budget and reports the first
excluded item's threshold at the current packed total. If mandatory context cannot
fit, it reports the minimum viable budget.

## Static application

Checked-in `web/` assets render an SVG graph with a deterministic layout, filters,
state legend, selection detail panel, and context explorer. JavaScript reads the
generated JSON through a relative URL only. It performs no API call and relies on
no external CDN.

## Build and deployment

A module entry point will accept a repository root and output directory, validate
the input contract, generate graph data, and copy static assets. The deployment
workflow will invoke the same build command, upload only its output directory, and
deploy it with GitHub Pages actions.

The provenance-index entry point is:

```bat
.venv\Scripts\python.exe -m agent_demo.context_atlas.build --repository-root . --output-dir build
```

Issue drafts may include a UTF-8 metadata block immediately after their heading to
override their tracked snapshot states. Its only accepted keys are
`github_state` (`draft`, `open`, or `closed`) and `implementation_state`
(`planned`, `in_progress`, or `complete`); absent values default to `draft` and
`planned`. Planned issue artifacts are prospective and omitted until their issue
is in progress; otherwise the builder rejects invalid values, duplicate requirement
or issue IDs, missing declared paths, and graph references to missing nodes.

See [DEC-CA-001](decisions/DEC-CA-001-reproducible-issue-source.md) and
[DEC-CA-002](decisions/DEC-CA-002-static-site-and-build.md).
