---
type: object
name: markdown-workspace
implementation: speculoop/markdown_workspace.py
summary: Markdown folder → semantic graph with incremental sync and provenance.
---

# MarkdownWorkspace

Turns a folder of Markdown files into derived semantic state. Files are the
source of truth; the graph and sync metadata live in `<workspace>/.speculoop/`.

**Mutated by:** ingest/sync (parses files, adds/removes nodes and edges),
source edits (hash-based incremental re-sync).
**Read by:** relationship_source, explain_node, graph/stats.
**Depends on:** mumblewrap Graph/Node/Edge, translation Decomposer (SVO patterns).
**Docs:** docs/markdown-workspace.md · demo_markdown.py · tests/test_markdown_workspace.py
