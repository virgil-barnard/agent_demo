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

## Publish to GitHub Pages from `/docs`

This repository's Pages source is the `docs/` directory on `main`. Regenerate
the Pages files before committing changes to repository content:

```bat
.venv\Scripts\python.exe -m agent_demo.context_atlas.build --repository-root . --pages-dir docs
```

The command preserves Markdown documentation while writing `docs/index.html`,
`docs/styles.css`, `docs/app.js`, and `docs/graph.json`. A repository
administrator must select the `main` branch and `/docs` folder in GitHub Pages
settings for this source to publish.
