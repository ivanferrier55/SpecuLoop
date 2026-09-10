# SpecuLoop Workspace UI

A local web app for editing Markdown files and watching the semantic graph update in real time.

## Quick start

```bash
cd SpecuLoop
python3 -m speculoop --workspace examples/markdown-workspace --port 8080
```

Open `http://localhost:8080` in a browser.

## What you see

- **Left sidebar**: file list with change indicators (green = saved, yellow = dirty)
- **Center**: Markdown editor (plain textarea, edit any file)
- **Right**: interactive d3-force graph — drag nodes, click to inspect
- **Bottom**: sync report (what changed + why) after each save

## Workflow

1. Click a file in the sidebar to open it in the editor.
2. Edit the Markdown content.
3. Click **Save & Sync** — the server runs incremental sync, the graph updates, and the sync report shows every change with provenance.
4. Click a node in the graph to see its provenance (which file, section, line, version).
5. Click an edge label to see where that relationship came from.

## API endpoints

The server exposes a REST API that the frontend consumes:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | serves the web UI |
| `/api/files` | GET | file list with versions |
| `/api/file?name=X` | GET | file content |
| `/api/file?name=X` | PUT | save file → sync → return report |
| `/api/graph` | GET | all nodes + edges with metadata |
| `/api/explain?label=X` | GET | why does this node exist? |
| `/api/source?subject=X&relation=Y&object=Z` | GET | where did this relationship come from? |
| `/api/stats` | GET | graph counts |
| `/api/workspace` | GET | workspace info |

## No external dependencies

The server uses only the Python standard library (`http.server`). The frontend loads d3 v7 from a CDN for graph visualization. No npm, no build step.
