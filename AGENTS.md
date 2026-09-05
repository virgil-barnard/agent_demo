# Repository Development Guide

## Environment

- Primary development environment: Windows Command Prompt (`cmd.exe`) in VS Code.
- Python requirement: Python 3.11 or newer, as declared in `pyproject.toml`.
- The repository-local virtual environment is `.venv`.
- Agents must never install packages into the base Python environment.
- Agents must not create, delete, clear, or recreate `.venv`. If it is missing or broken, stop and ask the user to run `scripts\\bootstrap.cmd`.
- Do not rely on virtual-environment activation. Invoke the environment interpreter explicitly:

  ```bat
  .venv\Scripts\python.exe
  ```

- Before using Python, verify the interpreter is isolated:

  ```bat
  .venv\Scripts\python.exe -c "import sys; assert sys.prefix != sys.base_prefix; print(sys.executable)"
  ```

## Environment setup

Environment creation is a user/bootstrap operation:

```bat
scripts\bootstrap.cmd
```

The bootstrap installs the project and its `dev` extra into `.venv`.

Agents may synchronize an existing environment after an approved `pyproject.toml` change with:

```bat
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Do not use bare `pip`, `pip3`, `python -m pip`, `py -m pip`, `--user`, or `--system-site-packages`.

## Package configuration

- `pyproject.toml` is authoritative for package metadata, supported Python versions, dependencies, Ruff, pytest, and coverage configuration.
- Runtime dependencies belong in `[project].dependencies`.
- Development-only tools belong in `[project.optional-dependencies].dev`.
- Do not add a dependency when the standard library provides a clear, maintainable solution.
- Any dependency change must include its purpose in the active issue and completion evidence.
- Keep dependency declarations bounded to compatible versions. Maintain any committed lock file when dependency declarations change.
- Never edit files inside `.venv`.

## Repository layout

```text
src/                 importable production code
tests/               automated tests
scripts/             repository automation and validation entry points
docs/                durable requirements, architecture, plans, and evidence
.opencode/            operator-controlled agent prompts and commands
AGENTS.md             this development guide
opencode.json         operator-controlled permissions and agent bindings
pyproject.toml        Python package and tool configuration
```

Preserve the `src/` layout. Tests must exercise the installed package rather than depending on accidental imports from the repository root.

## Canonical quality commands

Run commands from the repository root.

Environment integrity:

```bat
.venv\Scripts\python.exe -c "import sys; assert sys.prefix != sys.base_prefix; print(sys.executable)"
.venv\Scripts\python.exe -m pip check
```

Formatting check:

```bat
.venv\Scripts\python.exe -m ruff format --check .
```

Lint:

```bat
.venv\Scripts\python.exe -m ruff check .
```

Tests:

```bat
.venv\Scripts\python.exe -m pytest
```

Compilation smoke test:

```bat
.venv\Scripts\python.exe -m compileall -q src tests
```

Complete local gate:

```bat
scripts\check.cmd
```

Formatting and safe automated lint repair:

```bat
.venv\Scripts\python.exe -m ruff format .
.venv\Scripts\python.exe -m ruff check --fix .
```

Inspect the resulting diff after any automated repair.

## Testing expectations

- New behavior requires tests.
- A bug fix should begin with a failing regression test when practical.
- Test observable behavior and stable contracts rather than private implementation details.
- Keep unit tests independent of the network, wall-clock time, filesystem ordering, ambient environment variables, and uncontrolled randomness.
- Use fixed seeds and deterministic fixtures when randomness is necessary.
- Use pytest temporary-directory fixtures for filesystem tests.
- Do not make tests order-dependent.
- A skip or expected failure requires a specific documented reason.
- Never weaken, delete, or bypass a test merely to obtain a passing result.
- Run focused tests while iterating, then run `scripts\\check.cmd` before claiming completion.

## Deterministic outputs

Generated artifacts must be reproducible from tracked inputs.

- Sort filesystem traversal, records, nodes, edges, and serialized keys.
- Use stable identifiers derived from normalized inputs.
- Write UTF-8 and use `/` in serialized repository-relative paths.
- Do not serialize absolute paths, credentials, environment values, transient ports, or host-specific state.
- Avoid current timestamps in generated artifacts. If a timestamp is required, accept a controlled value such as `SOURCE_DATE_EPOCH`.
- A deterministic build test should build twice from the same inputs and compare bytes or cryptographic hashes.
- Regenerating committed artifacts at the end of validation must leave `git diff --exit-code` clean.

## Definition of done

A change is complete only when:

- its acceptance criteria are satisfied;
- relevant tests exist and pass;
- `scripts\\check.cmd` passes;
- public behavior and interfaces are documented;
- generated artifacts are current and deterministic where applicable;
- no secrets or machine-local paths were introduced;
- dependency and tool configuration remains accurate;
- limitations are reported rather than hidden.
