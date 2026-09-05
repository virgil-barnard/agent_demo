"""CLI for deterministic Context Atlas graph generation.

Run ``python -m agent_demo.context_atlas.build --repository-root . --output-dir build``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from .model import Artifact, Edge, Evidence, Node, ValidationError, validate_graph
from .parse import IssueDraft, parse_issue, parse_requirements, python_imports, read_text

SCHEMA_VERSION = 1


def _cost(text: str) -> int:
    return math.ceil(len(text.encode("utf-8")) / 4)


def _node(
    node_id: str,
    kind: str,
    label: str,
    path: str,
    text: str,
    line_start: int,
    line_end: int,
    **states: str,
) -> Node:
    lines = text.splitlines()
    excerpt = " ".join(lines[line_start - 1 : line_end]).strip()[:240]
    return Node(
        id=node_id,
        kind=kind,
        label=label,
        path=path,
        line_start=line_start,
        line_end=line_end,
        excerpt=excerpt,
        content_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        estimated_cost=_cost("\n".join(lines[line_start - 1 : line_end])),
        **states,
    )


def _files(root: Path, directory: str, suffix: str) -> list[Path]:
    base = root / directory
    return (
        sorted(
            (path for path in base.rglob(f"*{suffix}") if path.is_file()),
            key=lambda path: path.as_posix(),
        )
        if base.exists()
        else []
    )


def _validate_path(root: Path, declared_path: str, issue_path: str) -> None:
    if not (root / declared_path).is_file():
        raise ValidationError(f"{issue_path}: declared path does not exist: {declared_path}")


def _import_target(import_name: str, module_nodes: dict[str, str]) -> str | None:
    parts = import_name.split(".")
    while parts:
        target = module_nodes.get(".".join(parts))
        if target:
            return target
        parts.pop()
    return None


def build_graph(repository_root: Path, output_dir: Path) -> Path:
    """Validate approved repository inputs and write ``graph.json`` to output_dir."""
    root = repository_root.resolve()
    if not (root / "docs").is_dir():
        raise ValidationError(f"repository root has no docs directory: {root}")

    nodes: list[Node] = []
    edges: list[Edge] = []
    artifacts: list[Artifact] = []
    issue_drafts: list[tuple[IssueDraft, str]] = []
    file_text: dict[str, str] = {}

    for path in _files(root, "docs", ".md"):
        text, relative = read_text(path, root)
        file_text[relative] = text
        nodes.append(
            _node(
                f"document:{relative}",
                "document",
                path.stem,
                relative,
                text,
                1,
                len(text.splitlines()),
            )
        )
        for requirement in parse_requirements(text, relative):
            nodes.append(
                _node(
                    f"requirement:{requirement.id}",
                    "requirement",
                    requirement.title,
                    relative,
                    text,
                    requirement.line_start,
                    requirement.line_end,
                )
            )
        if relative.startswith("docs/issues/"):
            issue_drafts.append((parse_issue(text, relative), relative))

    source_paths = _files(root, "src", ".py")
    test_paths = _files(root, "tests", ".py")
    module_nodes: dict[str, str] = {}
    for path in source_paths + test_paths:
        text, relative = read_text(path, root)
        file_text[relative] = text
        kind = "test" if relative.startswith("tests/") else "source"
        node_id = f"{kind}:{relative}"
        nodes.append(_node(node_id, kind, path.stem, relative, text, 1, len(text.splitlines())))
        if relative.startswith("src/"):
            module = (
                relative.removeprefix("src/")
                .removesuffix(".py")
                .replace("/__init__", "")
                .replace("/", ".")
            )
            module_nodes[module] = node_id

    issue_ids: set[str] = set()
    for issue, relative in issue_drafts:
        if issue.id in issue_ids:
            raise ValidationError(f"{relative}: duplicate issue identifier {issue.id}")
        issue_ids.add(issue.id)
        text = file_text[relative]
        issue_id = f"issue:{issue.id}"
        nodes.append(
            _node(
                issue_id,
                "issue",
                issue.title,
                relative,
                text,
                issue.line_number,
                len(text.splitlines()),
                github_state=issue.github_state,
                implementation_state=issue.implementation_state,
            )
        )
        for requirement in issue.requirements:
            edges.append(
                Edge(
                    issue_id,
                    f"requirement:{requirement}",
                    "addresses",
                    Evidence(relative, issue.line_number, issue.line_number),
                )
            )
        for dependency in issue.dependencies:
            edges.append(
                Edge(
                    issue_id,
                    f"issue:{dependency}",
                    "depends_on",
                    Evidence(relative, issue.line_number, issue.line_number),
                )
            )
        for declared_path in issue.implementation_paths:
            if issue.implementation_state == "planned":
                continue
            _validate_path(root, declared_path, relative)
            edges.append(
                Edge(
                    issue_id,
                    f"source:{declared_path}",
                    "implements",
                    Evidence(relative, issue.line_number, issue.line_number),
                )
            )
        for declared_path in issue.test_paths:
            if issue.implementation_state == "planned":
                continue
            _validate_path(root, declared_path, relative)
            edges.append(
                Edge(
                    issue_id,
                    f"test:{declared_path}",
                    "tests",
                    Evidence(relative, issue.line_number, issue.line_number),
                )
            )

    for relative, text in sorted(file_text.items()):
        if not relative.endswith(".py"):
            continue
        source_id = f"test:{relative}" if relative.startswith("tests/") else f"source:{relative}"
        for import_name, line_number in python_imports(text, relative):
            target = _import_target(import_name, module_nodes)
            if target and target != source_id:
                edges.append(
                    Edge(source_id, target, "imports", Evidence(relative, line_number, line_number))
                )

    for node in nodes:
        if node.kind in {"requirement", "issue", "source", "test"}:
            artifacts.append(
                Artifact(
                    f"artifact:{node.id}",
                    node.id,
                    node.kind,
                    node.path,
                    node.line_start,
                    node.line_end,
                    node.estimated_cost,
                )
            )

    artifact_by_node = {artifact.node_id: artifact for artifact in artifacts}
    context_profiles = []
    for issue, _ in sorted(issue_drafts, key=lambda item: item[0].id):
        candidate_nodes = [f"issue:{issue.id}"]
        candidate_nodes.extend(f"requirement:{requirement}" for requirement in issue.requirements)
        candidate_nodes.extend(
            edge.target
            for edge in edges
            if edge.source == f"issue:{issue.id}"
            and edge.kind in {"implements", "tests", "depends_on"}
        )
        candidates = []
        for rank, node_id in enumerate(dict.fromkeys(candidate_nodes), start=1):
            artifact = artifact_by_node.get(node_id)
            if artifact is None:
                continue
            candidates.append(
                {
                    "artifact_id": artifact.id,
                    "mandatory": rank == 1,
                    "rank": rank,
                    "rationale": "selected issue" if rank == 1 else "declared provenance",
                    "evidence_route": [f"issue:{issue.id}", node_id],
                }
            )
        context_profiles.append({"issue_id": f"issue:{issue.id}", "candidates": candidates})

    validate_graph(nodes, edges, artifacts)
    data = {
        "schema_version": SCHEMA_VERSION,
        "nodes": [node.to_dict() for node in sorted(nodes, key=lambda node: node.id)],
        "edges": [
            edge.to_dict()
            for edge in sorted(
                edges,
                key=lambda edge: (
                    edge.source,
                    edge.target,
                    edge.kind,
                    edge.evidence.path,
                    edge.evidence.line_start,
                ),
            )
        ],
        "artifacts": [
            artifact.to_dict() for artifact in sorted(artifacts, key=lambda artifact: artifact.id)
        ],
        "context_profiles": context_profiles,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "graph.json"
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Context Atlas graph data.")
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        build_graph(arguments.repository_root, arguments.output_dir)
    except ValidationError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
