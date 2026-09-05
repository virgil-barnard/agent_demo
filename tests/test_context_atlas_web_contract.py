from pathlib import Path

WEB_ROOT = Path(__file__).parents[1] / "web"


def test_static_application_uses_only_relative_checked_in_assets() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")

    assert 'href="styles.css"' in html
    assert 'src="app.js"' in html
    assert "http://" not in html
    assert "https://" not in html


def test_application_contract_covers_graph_filters_states_and_evidence() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    javascript = (WEB_ROOT / "app.js").read_text(encoding="utf-8")
    css = (WEB_ROOT / "styles.css").read_text(encoding="utf-8")

    assert 'id="graph"' in html
    assert 'id="kind-filters"' in html
    assert 'id="github-filter"' in html
    assert 'id="implementation-filter"' in html
    assert 'const GRAPH_DATA_URL = "graph.json"' in javascript
    assert "fetch(GRAPH_DATA_URL)" in javascript
    assert "edge.evidence.path" in javascript
    assert "edge.evidence.line_start" in javascript
    assert "Context budget explorer" in javascript
    assert "estimated tokens" in javascript
    assert "Next useful threshold" in javascript
    assert "KIND_ORDER" in javascript
    for github_state in ("draft", "open", "closed"):
        assert f"github-{github_state}" in css
    for implementation_state in ("planned", "in_progress", "complete"):
        assert f"implementation-{implementation_state}" in css
