from pathlib import Path

from agent_demo.context_atlas.build import build_graph


def _write(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _repository(root: Path) -> None:
    _write(root, "web/index.html", '<!doctype html>\n<link rel="stylesheet" href="styles.css">\n')
    _write(root, "web/styles.css", "body { color: black; }\n")
    _write(root, "web/app.js", 'const GRAPH_DATA_URL = "graph.json";\n')
    _write(root, "web/assets/logo.txt", "Context Atlas\n")
    _write(root, "docs/requirements.md", "### REQ-CA-001 — Static graph\n\nStatic files.\n")


def test_build_creates_reproducible_self_contained_pages_artifact(tmp_path: Path) -> None:
    _repository(tmp_path)

    first = tmp_path / "first"
    second = tmp_path / "second"
    build_graph(tmp_path, first)
    build_graph(tmp_path, second)

    expected_paths = ["app.js", "assets/logo.txt", "graph.json", "index.html", "styles.css"]
    for output in (first, second):
        paths = sorted(
            path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()
        )
        assert paths == expected_paths
    assert {
        path.relative_to(first).as_posix(): path.read_bytes()
        for path in first.rglob("*")
        if path.is_file()
    } == {
        path.relative_to(second).as_posix(): path.read_bytes()
        for path in second.rglob("*")
        if path.is_file()
    }
    assert str(tmp_path).encode() not in (first / "graph.json").read_bytes()
