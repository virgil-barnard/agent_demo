"""Typed graph records and validation for Context Atlas."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


class ValidationError(ValueError):
    """Raised when repository metadata cannot form a valid graph."""


@dataclass(frozen=True)
class Evidence:
    path: str
    line_start: int
    line_end: int


@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    label: str
    path: str
    line_start: int
    line_end: int
    excerpt: str
    content_hash: str
    estimated_cost: int
    github_state: str | None = None
    implementation_state: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    kind: str
    evidence: Evidence

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "kind": self.kind,
            "evidence": asdict(self.evidence),
        }


@dataclass(frozen=True)
class Artifact:
    id: str
    node_id: str
    kind: str
    path: str
    line_start: int
    line_end: int
    estimated_cost: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_graph(nodes: list[Node], edges: list[Edge], artifacts: list[Artifact]) -> None:
    """Ensure every graph record has a unique ID and valid references."""
    node_ids = [node.id for node in nodes]
    duplicates = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    if duplicates:
        raise ValidationError(f"duplicate node identifiers: {', '.join(duplicates)}")

    known_nodes = set(node_ids)
    for edge in edges:
        if edge.source not in known_nodes or edge.target not in known_nodes:
            raise ValidationError(
                f"edge {edge.kind} references missing node: {edge.source} -> {edge.target}"
            )
    for artifact in artifacts:
        if artifact.node_id not in known_nodes:
            raise ValidationError(
                f"artifact {artifact.id} references missing node: {artifact.node_id}"
            )
