# DEC-CA-002 — Standard-library build and static Pages delivery

## Status

Accepted for the planned implementation.

## Decision

Use Python's standard library for repository parsing, validation, data generation,
file copying, and hashing. Use checked-in vanilla HTML, CSS, and JavaScript for the
browser interface. Deploy the generated directory with GitHub Actions and GitHub
Pages.

## Rationale

This keeps the demonstration small, inspectable, and reproducible. `ast`,
`pathlib`, `json`, `hashlib`, and `shutil` provide the required build mechanics
without a runtime dependency or JavaScript build chain.

## Consequences

- No dependency change is planned in `pyproject.toml`.
- The graph layout and visual components must be implemented directly rather than
  delegated to a graph library.
- The deployment workflow remains a separate integration concern and must use the
  generated output only.
