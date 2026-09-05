"""Parsing helpers that never import or execute repository source files."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

from .model import ValidationError

ISSUE_HEADING = re.compile(r"^# (?P<id>CA-\d+).*?(?P<title>[A-Za-z].*)$", re.MULTILINE)
REQUIREMENT_HEADING = re.compile(r"^### (?P<id>REQ-CA-\d+).*?(?P<title>[A-Za-z].*)$", re.MULTILINE)
METADATA_BLOCK = re.compile(r"<!-- context-atlas\n(?P<body>.*?)-->", re.DOTALL)
STATE_VALUES = {"draft", "open", "closed"}
IMPLEMENTATION_STATE_VALUES = {"planned", "in_progress", "complete"}


@dataclass(frozen=True)
class IssueDraft:
    id: str
    title: str
    github_state: str
    implementation_state: str
    requirements: tuple[str, ...]
    dependencies: tuple[str, ...]
    implementation_paths: tuple[str, ...]
    test_paths: tuple[str, ...]
    line_number: int


@dataclass(frozen=True)
class Requirement:
    id: str
    title: str
    line_start: int
    line_end: int


def parse_requirements(text: str, path: str) -> list[Requirement]:
    """Return requirement sections and reject duplicate declared IDs."""
    matches = list(REQUIREMENT_HEADING.finditer(text))
    requirements: list[Requirement] = []
    seen: set[str] = set()
    lines = text.splitlines()
    for index, match in enumerate(matches):
        requirement_id = match.group("id")
        if requirement_id in seen:
            raise ValidationError(f"{path}: duplicate requirement identifier {requirement_id}")
        seen.add(requirement_id)
        line_start = text[: match.start()].count("\n") + 1
        line_end = (
            len(lines)
            if index + 1 == len(matches)
            else text[: matches[index + 1].start()].count("\n")
        )
        requirements.append(Requirement(requirement_id, match.group("title"), line_start, line_end))
    return requirements


def _metadata(text: str, path: str) -> dict[str, str]:
    match = METADATA_BLOCK.search(text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValidationError(f"{path}: malformed context-atlas metadata line {raw_line!r}")
        key, value = raw_line.split(":", 1)
        values[key.strip()] = value.strip()
    unknown = sorted(set(values) - {"github_state", "implementation_state"})
    if unknown:
        raise ValidationError(f"{path}: unknown context-atlas metadata keys: {', '.join(unknown)}")
    return values


def _section(text: str, name: str) -> tuple[str, int]:
    match = re.search(rf"^## {re.escape(name)}\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    if not match:
        return "", 1
    return match.group(1), text[: match.start(1)].count("\n") + 1


def _references(section: str, prefix: str) -> tuple[str, ...]:
    return tuple(sorted(set(re.findall(rf"\b({re.escape(prefix)}-\d+)\b", section))))


def _paths(section: str) -> tuple[str, ...]:
    return tuple(sorted(set(re.findall(r"`((?:src|tests|docs)/[^`]+)`", section))))


def parse_issue(text: str, path: str) -> IssueDraft:
    """Parse the constrained fields already present in a tracked issue draft."""
    heading = ISSUE_HEADING.search(text)
    if not heading:
        raise ValidationError(f"{path}: expected a CA issue heading")
    metadata = _metadata(text, path)
    github_state = metadata.get("github_state", "draft")
    implementation_state = metadata.get("implementation_state", "planned")
    if github_state not in STATE_VALUES:
        raise ValidationError(f"{path}: invalid github_state {github_state!r}")
    if implementation_state not in IMPLEMENTATION_STATE_VALUES:
        raise ValidationError(f"{path}: invalid implementation_state {implementation_state!r}")

    references, _ = _section(text, "Planning references")
    dependencies, _ = _section(text, "Dependencies")
    artifacts, _ = _section(text, "Expected artifacts")
    all_requirements = _references(references, "REQ-CA")
    if not all_requirements:
        all_requirements = _references(text, "REQ-CA")
    paths = _paths(artifacts)
    line_number = text[: heading.start()].count("\n") + 1
    return IssueDraft(
        id=heading.group("id"),
        title=heading.group("title"),
        github_state=github_state,
        implementation_state=implementation_state,
        requirements=all_requirements,
        dependencies=_references(dependencies, "CA"),
        implementation_paths=tuple(path for path in paths if path.startswith("src/")),
        test_paths=tuple(path for path in paths if path.startswith("tests/")),
        line_number=line_number,
    )


def python_imports(text: str, path: str) -> list[tuple[str, int]]:
    """Return absolute import names and source lines using only ``ast``."""
    try:
        tree = ast.parse(text, filename=path)
    except SyntaxError as error:
        raise ValidationError(
            f"{path}:{error.lineno}: invalid Python syntax: {error.msg}"
        ) from error
    imports: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((alias.name, node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append((node.module, node.lineno))
    return sorted(imports)


def read_text(path: Path, root: Path) -> tuple[str, str]:
    """Read UTF-8 text and return it with its normalized repository path."""
    relative_path = path.relative_to(root).as_posix()
    try:
        return path.read_text(encoding="utf-8"), relative_path
    except UnicodeDecodeError as error:
        raise ValidationError(f"{relative_path}: expected UTF-8 text") from error
