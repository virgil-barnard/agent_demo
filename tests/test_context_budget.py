from agent_demo.context_atlas.context_budget import (
    ContextCandidate,
    pack_candidates,
    rank_candidates,
)
from agent_demo.context_atlas.model import Artifact


def _artifact(identifier: str, kind: str, path: str, cost: int, line_start: int = 1) -> Artifact:
    return Artifact(
        identifier, identifier.removeprefix("artifact:"), kind, path, line_start, line_start, cost
    )


def test_ranking_uses_tier_then_kind_path_and_anchor() -> None:
    candidates = [
        ContextCandidate(
            _artifact("artifact:z", "test", "tests/z.py", 1), 3, "test", ("issue:CA-1",)
        ),
        ContextCandidate(
            _artifact("artifact:b", "source", "src/a.py", 1, 2), 3, "source", ("issue:CA-1",)
        ),
        ContextCandidate(
            _artifact("artifact:a", "source", "src/a.py", 1, 1), 3, "source", ("issue:CA-1",)
        ),
        ContextCandidate(
            _artifact("artifact:issue", "issue", "docs/issues/a.md", 1),
            1,
            "issue",
            ("issue:CA-1",),
            True,
        ),
    ]

    ranked = rank_candidates(candidates)

    assert [candidate.artifact.id for candidate in ranked] == [
        "artifact:issue",
        "artifact:a",
        "artifact:b",
        "artifact:z",
    ]
    assert ranked[1].to_dict()["score"] == {
        "tier": 3,
        "kind": "source",
        "path": "src/a.py",
        "anchor": 1,
    }


def test_pack_includes_an_exact_fit_and_exposes_next_item_threshold() -> None:
    ranked = rank_candidates(
        [
            ContextCandidate(
                _artifact("artifact:issue", "issue", "docs/issue.md", 4), 1, "issue", (), True
            ),
            ContextCandidate(
                _artifact("artifact:requirement", "requirement", "docs/req.md", 6),
                2,
                "requirement",
                (),
            ),
        ]
    )

    exact_fit = pack_candidates(ranked, 10)
    below_threshold = pack_candidates(ranked, 9)

    assert [candidate.artifact.id for candidate in exact_fit.included] == [
        "artifact:issue",
        "artifact:requirement",
    ]
    assert exact_fit.total_cost == 10
    assert exact_fit.next_useful_threshold is None
    assert [candidate.artifact.id for candidate in below_threshold.included] == ["artifact:issue"]
    assert [candidate.artifact.id for candidate in below_threshold.excluded] == [
        "artifact:requirement"
    ]
    assert below_threshold.next_useful_threshold == 10


def test_pack_reports_the_minimum_when_mandatory_context_does_not_fit() -> None:
    ranked = rank_candidates(
        [
            ContextCandidate(
                _artifact("artifact:issue", "issue", "docs/issue.md", 4), 1, "issue", (), True
            )
        ]
    )

    plan = pack_candidates(ranked, 3)

    assert not plan.mandatory_fits
    assert plan.included == ()
    assert plan.minimum_viable_budget == 4
    assert plan.next_useful_threshold == 4
