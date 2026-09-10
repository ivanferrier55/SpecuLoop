---
type: object
name: serve-ui
implementation: speculoop/serve.py + speculoop/static/index.html
summary: Local web app — Markdown editor, interactive graph, sync report, provenance inspector.
---

# Serve UI

HTTP server wrapping MarkdownWorkspace for browser-based editing. Python
stdlib only; frontend uses d3-force via CDN for graph visualization.

**Mutated by:** PUT /api/file (saves file, runs sync, returns report).
**Read by:** all GET endpoints (files, graph, explain, source, stats).
**Depends on:** MarkdownWorkspace, static/index.html.
**Docs:** docs/serve-ui.md
