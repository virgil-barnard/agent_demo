# Context Atlas vision

## Purpose

Context Atlas is a static GitHub Pages demonstration of issue-driven autonomous
development. It turns this repository's tracked planning documents, requirements,
issue drafts, source files, and tests into an interactive provenance-aware graph.

Visitors can follow a requirement to its planned issue, implementation, and tests;
see the difference between GitHub issue state and implementation state; and explore
the bounded context an agent should load for a selected task.

## User outcomes

- A viewer can inspect meaningful repository relationships without a server or a
  live GitHub API call.
- A viewer can answer "why does this file exist?" using evidence-backed graph
  edges.
- A viewer can select an issue and see a deterministic, explainable, budget-bounded
  context recommendation.
- A contributor can regenerate the same site artifact from the same tracked inputs.

## Principles

1. **Tracked inputs are authoritative.** Issue drafts mirror published GitHub
   metadata so the site is reproducible without network access.
2. **Evidence over inference.** Relationships originate in explicit metadata,
   Markdown identifiers, or Python AST imports; the tool does not invent links from
   arbitrary prose similarity.
3. **Determinism is observable.** Stable sorting, normalized paths, and byte-stable
   serialization allow an automated two-build comparison.
4. **Progress is legible.** GitHub lifecycle state and implementation lifecycle
   state remain distinct visual concepts.
5. **Small, inspectable technology.** Analysis uses the Python standard library;
   the application uses vanilla HTML, CSS, and JavaScript.

## Non-goals

- A general-purpose code intelligence platform or semantic search engine.
- Runtime GitHub API access, authentication, or a server component.
- Exact tokenizer emulation for every model provider.
- Automatic extraction of relationships from arbitrary natural-language text.

See [requirements](requirements.md) and [architecture](architecture.md) for the
testable product contract.
