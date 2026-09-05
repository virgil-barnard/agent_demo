# DEC-CA-001 — Tracked issue drafts are the issue source

## Status

Accepted for the planned implementation.

## Context

The graph must represent GitHub issues but must run as a reproducible static site.
Fetching the GitHub API during browsing requires network access and makes a build
depend on mutable external state.

## Decision

Issue drafts in `docs/issues/` are the build input. Their metadata mirrors the
published issue number, URL, GitHub state, and implementation state when known.
The builder uses only this tracked metadata.

## Consequences

- The output can be regenerated offline from a checkout.
- Issue metadata changes are explicit, reviewable repository changes.
- The site is a controlled snapshot, not a live GitHub dashboard.
- The publication process must update the corresponding draft after GitHub creates
  an issue.
