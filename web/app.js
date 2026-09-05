"use strict";

const GRAPH_DATA_URL = "graph.json";
const SVG_NAMESPACE = "http://www.w3.org/2000/svg";
const KIND_ORDER = ["document", "requirement", "issue", "source", "test"];
const KIND_LABELS = {
  document: "Documents",
  requirement: "Requirements",
  issue: "Issues",
  source: "Source files",
  test: "Test files",
};

const state = { data: null, selectedId: null, enabledKinds: new Set(KIND_ORDER) };
const graph = document.querySelector("#graph");
const status = document.querySelector("#graph-status");
const details = document.querySelector("#details");
const githubFilter = document.querySelector("#github-filter");
const implementationFilter = document.querySelector("#implementation-filter");

function element(name, attributes = {}) {
  const node = document.createElementNS(SVG_NAMESPACE, name);
  Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
  return node;
}

function appendText(parent, name, text) {
  const node = document.createElement(name);
  node.textContent = text;
  parent.append(node);
  return node;
}

function visibleNodes() {
  const githubState = githubFilter.value;
  const implementationState = implementationFilter.value;
  return state.data.nodes.filter(
    (node) =>
      state.enabledKinds.has(node.kind) &&
      (githubState === "all" || node.github_state === githubState) &&
      (implementationState === "all" || node.implementation_state === implementationState),
  );
}

function layout(nodes) {
  const columns = new Map(KIND_ORDER.map((kind, index) => [kind, index]));
  const grouped = new Map(KIND_ORDER.map((kind) => [kind, []]));
  nodes.forEach((node) => grouped.get(node.kind).push(node));
  const positions = new Map();
  KIND_ORDER.forEach((kind) => {
    grouped.get(kind).sort((left, right) => left.id.localeCompare(right.id)).forEach((node, index) => {
      positions.set(node.id, { x: 100 + columns.get(kind) * 190, y: 90 + index * 95 });
    });
  });
  const largestGroup = Math.max(...[...grouped.values()].map((group) => group.length), 1);
  return { positions, height: Math.max(640, 140 + largestGroup * 95) };
}

function renderDetails(node) {
  details.replaceChildren();
  appendText(details, "h2", "Selection details");
  if (!node) {
    appendText(details, "p", "Select a visible node to inspect its stable identity, path, state, and evidence.");
    return;
  }
  const list = document.createElement("dl");
  list.className = "detail-list";
  const fields = [
    ["ID", node.id], ["Type", node.kind], ["Path", node.path],
    ["Lines", `${node.line_start}–${node.line_end}`], ["GitHub state", node.github_state || "—"],
    ["Implementation state", node.implementation_state || "—"],
  ];
  fields.forEach(([label, value]) => { appendText(list, "dt", label); appendText(list, "dd", value); });
  details.append(list);
  if (node.excerpt) appendText(details, "p", node.excerpt);

  appendText(details, "h3", "Adjacent relationships");
  const adjacent = state.data.edges
    .filter((edge) => edge.source === node.id || edge.target === node.id)
    .sort((left, right) => `${left.kind}:${left.source}:${left.target}`.localeCompare(`${right.kind}:${right.source}:${right.target}`));
  if (!adjacent.length) { appendText(details, "p", "No adjacent relationships."); return; }
  const edgeList = document.createElement("ul");
  edgeList.className = "edge-list";
  adjacent.forEach((edge) => {
    const item = document.createElement("li");
    item.textContent = `${edge.kind}: ${edge.source} → ${edge.target}; evidence: ${edge.evidence.path}:${edge.evidence.line_start}–${edge.evidence.line_end}`;
    edgeList.append(item);
  });
  details.append(edgeList);
}

function renderGraph() {
  const nodes = visibleNodes();
  const ids = new Set(nodes.map((node) => node.id));
  const { positions, height } = layout(nodes);
  graph.setAttribute("viewBox", `0 0 960 ${height}`);
  graph.replaceChildren();
  const visibleEdges = state.data.edges.filter((edge) => ids.has(edge.source) && ids.has(edge.target));
  visibleEdges.forEach((edge) => {
    const source = positions.get(edge.source); const target = positions.get(edge.target);
    graph.append(element("line", { class: "edge", x1: source.x, y1: source.y, x2: target.x, y2: target.y }));
  });
  nodes.forEach((node) => {
    const position = positions.get(node.id);
    const group = element("g", { class: `node kind-${node.kind}${state.selectedId === node.id ? " selected" : ""}`, tabindex: "0", role: "button", "aria-label": `Select ${node.label}` });
    const circle = element("circle", { cx: position.x, cy: position.y, r: 24, class: `kind-${node.kind} ${node.github_state ? `github-${node.github_state}` : ""} ${node.implementation_state ? `implementation-${node.implementation_state}` : ""}` });
    const label = element("text", { x: position.x, y: position.y + 40, "text-anchor": "middle" });
    label.textContent = node.label;
    const select = () => { state.selectedId = node.id; renderGraph(); renderDetails(node); };
    group.addEventListener("click", select);
    group.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); select(); } });
    group.append(circle, label); graph.append(group);
  });
  if (!ids.has(state.selectedId)) { state.selectedId = null; renderDetails(null); }
  status.textContent = `${nodes.length} visible artifacts and ${visibleEdges.length} visible relationships.`;
}

function configureFilters() {
  const filters = document.querySelector("#kind-filters");
  const legend = document.querySelector("#kind-legend");
  KIND_ORDER.forEach((kind) => {
    const label = document.createElement("label"); const input = document.createElement("input");
    input.type = "checkbox"; input.checked = true; input.value = kind;
    input.addEventListener("change", () => { input.checked ? state.enabledKinds.add(kind) : state.enabledKinds.delete(kind); renderGraph(); });
    label.append(input, ` ${KIND_LABELS[kind]}`); filters.append(label);
    const swatch = document.createElement("span"); swatch.className = `kind-swatch kind-${kind}`; swatch.textContent = KIND_LABELS[kind]; legend.append(swatch);
  });
  githubFilter.addEventListener("change", renderGraph);
  implementationFilter.addEventListener("change", renderGraph);
}

async function loadGraph() {
  try {
    const response = await fetch(GRAPH_DATA_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data.nodes) || !Array.isArray(data.edges)) throw new Error("graph data has no nodes or edges");
    state.data = data;
    configureFilters(); renderGraph();
  } catch (error) {
    status.textContent = `Unable to load ${GRAPH_DATA_URL}: ${error.message}`;
  }
}

loadGraph();
