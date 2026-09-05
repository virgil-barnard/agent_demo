import json
from pathlib import Path

import pytest

from agent_demo.context_atlas.build import build_graph, main
from agent_demo.context_atlas.model import ValidationError


def _write(root: Path, relative_path: str, text: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _repository(root: Path) -> None:
    _write(root, "docs/requirements.md", "# Requirements\n\n### REQ-CA-001 — Graph\n\nA graph.\n")
    _write(
        root,
        "docs/issues/CA-001-graph.md",
        """# CA-001 — Graph\n\n<!-- context-atlas\ngithub_state: open\nimplementation_state: in_progress\n-->\n\n## Dependencies\n\nNone.\n\n## Expected artifacts\n\n- `src/demo.py`\n- `tests/test_demo.py`\n\n## Planning references\n\n- REQ-CA-001\n""",
    )
    _write(root, "src/demo.py", "import agent_demo.helper\n")
    _write(root, "src/agent_demo/helper.py", "VALUE = 1\n")
    _write(root, "tests/test_demo.py", "from agent_demo import helper\n")


def _data(root: Path, output: Path) -> dict[str, object]:
    build_graph(root, output)
    return json.loads((output / "graph.json").read_text(encoding="utf-8"))


def test_builds_sorted_graph_with_ast_import_edges(tmp_path: Path) -> None:
    _repository(tmp_path)
    data = _data(tmp_path, tmp_path / "output")

    assert data["schema_version"] == 1
    nodes = data["nodes"]
    assert [node["id"] for node in nodes] == sorted(node["id"] for node in nodes)
    issue = next(node for node in nodes if node["id"] == "issue:CA-001")
    assert issue["github_state"] == "open"
    assert issue["implementation_state"] == "in_progress"
    assert data["context_profiles"] == [
        {
            "issue_id": "issue:CA-001",
            "candidates": [
                {
                    "artifact_id": "artifact:issue:CA-001",
                    "mandatory": True,
                    "rank": 1,
                    "rationale": "selected issue",
                    "evidence_route": ["issue:CA-001", "issue:CA-001"],
                },
                {
                    "artifact_id": "artifact:requirement:REQ-CA-001",
                    "mandatory": False,
                    "rank": 2,
                    "rationale": "declared provenance",
                    "evidence_route": ["issue:CA-001", "requirement:REQ-CA-001"],
                },
                {
                    "artifact_id": "artifact:source:src/demo.py",
                    "mandatory": False,
                    "rank": 3,
                    "rationale": "declared provenance",
                    "evidence_route": ["issue:CA-001", "source:src/demo.py"],
                },
                {
                    "artifact_id": "artifact:test:tests/test_demo.py",
                    "mandatory": False,
                    "rank": 4,
                    "rationale": "declared provenance",
                    "evidence_route": ["issue:CA-001", "test:tests/test_demo.py"],
                },
            ],
        }
    ]
    assert {edge["kind"] for edge in data["edges"]} == {
        "addresses",
        "implements",
        "imports",
        "tests",
    }
    assert all("\\" not in node["path"] for node in nodes)


def test_build_is_byte_identical(tmp_path: Path) -> None:
    _repository(tmp_path)
    first = build_graph(tmp_path, tmp_path / "first").read_bytes()
    second = build_graph(tmp_path, tmp_path / "second").read_bytes()
    assert first == second


@pytest.mark.parametrize(
    ("relative_path", "replacement", "message"),
    [
        ("docs/requirements.md", "### REQ-CA-001 — Again", "duplicate requirement identifier"),
        ("docs/issues/CA-001-graph.md", "github_state: invalid", "invalid github_state"),
        ("docs/issues/CA-001-graph.md", "`src/missing.py`", "declared path does not exist"),
    ],
)
def test_rejects_invalid_declared_inputs(
    tmp_path: Path, relative_path: str, replacement: str, message: str
) -> None:
    _repository(tmp_path)
    path = tmp_path / relative_path
    original = path.read_text(encoding="utf-8")
    if relative_path == "docs/requirements.md":
        path.write_text(original + replacement + "\n", encoding="utf-8")
    elif "github_state" in replacement:
        path.write_text(original.replace("github_state: open", replacement), encoding="utf-8")
    else:
        path.write_text(original.replace("`src/demo.py`", replacement), encoding="utf-8")

    with pytest.raises(ValidationError, match=message):
        build_graph(tmp_path, tmp_path / "output")


def test_rejects_missing_referenced_issue_node(tmp_path: Path) -> None:
    _repository(tmp_path)
    issue_path = tmp_path / "docs/issues/CA-001-graph.md"
    issue_path.write_text(
        issue_path.read_text(encoding="utf-8").replace("None.", "- CA-999"), encoding="utf-8"
    )

    with pytest.raises(ValidationError, match="references missing node"):
        build_graph(tmp_path, tmp_path / "output")


def test_cli_reports_invalid_input(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["--repository-root", str(tmp_path), "--output-dir", str(tmp_path / "output")])
    assert error.value.code == 2
    assert "repository root has no docs directory" in capsys.readouterr().err
