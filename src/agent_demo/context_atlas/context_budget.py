"""Deterministic ranking and packing for Context Atlas context profiles."""

from __future__ import annotations

from dataclasses import dataclass

from .model import Artifact


@dataclass(frozen=True)
class ContextCandidate:
    """An artifact recommendation before its stable rank is assigned."""

    artifact: Artifact
    tier: int
    rationale: str
    evidence_route: tuple[str, ...]
    mandatory: bool = False


@dataclass(frozen=True)
class RankedCandidate:
    """A recommendation with its immutable rank and score components."""

    artifact: Artifact
    mandatory: bool
    rank: int
    tier: int
    rationale: str
    evidence_route: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "artifact_id": self.artifact.id,
            "mandatory": self.mandatory,
            "rank": self.rank,
            "score": {
                "tier": self.tier,
                "kind": self.artifact.kind,
                "path": self.artifact.path,
                "anchor": self.artifact.line_start,
            },
            "rationale": self.rationale,
            "evidence_route": list(self.evidence_route),
        }


@dataclass(frozen=True)
class BudgetPlan:
    """The result of greedily packing ranked context into a token estimate budget."""

    included: tuple[RankedCandidate, ...]
    excluded: tuple[RankedCandidate, ...]
    total_cost: int
    minimum_viable_budget: int
    next_useful_threshold: int | None

    @property
    def mandatory_fits(self) -> bool:
        """Whether the supplied budget admitted all mandatory context."""
        return not any(candidate.mandatory for candidate in self.excluded)


def rank_candidates(candidates: list[ContextCandidate]) -> list[RankedCandidate]:
    """Rank candidates by policy tier, artifact kind, normalized path, and anchor."""
    ordered = sorted(
        candidates,
        key=lambda candidate: (
            candidate.tier,
            candidate.artifact.kind,
            candidate.artifact.path,
            candidate.artifact.line_start,
        ),
    )
    return [
        RankedCandidate(
            artifact=candidate.artifact,
            mandatory=candidate.mandatory,
            rank=rank,
            tier=candidate.tier,
            rationale=candidate.rationale,
            evidence_route=candidate.evidence_route,
        )
        for rank, candidate in enumerate(ordered, start=1)
    ]


def pack_candidates(candidates: list[RankedCandidate], budget: int) -> BudgetPlan:
    """Greedily pack immutable candidate order without exceeding ``budget``."""
    if budget < 0:
        raise ValueError("budget must not be negative")

    minimum_viable_budget = sum(
        candidate.artifact.estimated_cost for candidate in candidates if candidate.mandatory
    )
    if budget < minimum_viable_budget:
        return BudgetPlan(
            included=(),
            excluded=tuple(candidates),
            total_cost=0,
            minimum_viable_budget=minimum_viable_budget,
            next_useful_threshold=minimum_viable_budget,
        )

    included: list[RankedCandidate] = []
    excluded: list[RankedCandidate] = []
    total_cost = 0
    next_useful_threshold: int | None = None
    for candidate in candidates:
        cost = candidate.artifact.estimated_cost
        if total_cost + cost <= budget:
            included.append(candidate)
            total_cost += cost
        else:
            excluded.append(candidate)
            if next_useful_threshold is None:
                next_useful_threshold = total_cost + cost
    return BudgetPlan(
        included=tuple(included),
        excluded=tuple(excluded),
        total_cost=total_cost,
        minimum_viable_budget=minimum_viable_budget,
        next_useful_threshold=next_useful_threshold,
    )
