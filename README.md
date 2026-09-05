# Context Atlas

Context Atlas is a static, inspectable provenance graph for this repository. Its
browser application uses only generated graph data and checked-in local assets.

## Build the Pages artifact

From the repository root, create a self-contained artifact in `build/` with:

```bat
.venv\Scripts\python.exe -m agent_demo.context_atlas.build --repository-root . --output-dir build
```

Inspect `build/` to find `index.html`, `styles.css`, `app.js`, and `graph.json`.
Serve that directory with any static-file server to use the application; it makes
no runtime network request.

The deployment workflow runs this same build command, uploads only `build/`, and
deploys it using GitHub Pages. A repository administrator must enable GitHub
Pages with **GitHub Actions** as its source if it is not already enabled.
