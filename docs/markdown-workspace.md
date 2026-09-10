# Markdown Workspace — PoC

The smallest complete loop from the national product vision:

```
Markdown         human-edited files are the durable source of truth
  ↓ parse        headings/sections/lines → candidate claims (SVO)
  ↓ extraction   existing mumblewrap Decomposer → nodes + edges
  ↓ graph        existing Graph, persisted as JSON
  ↓ provenance   file / section / line / version on every node + edge
  ↓ edit         user edits a .md file
  ↓ sync         hash-based incremental update (only changed files)
  ↓ report       what changed, why, and where each claim came from
```

## Usage

```python
from speculoop.markdown_workspace import MarkdownWorkspace

mw = MarkdownWorkspace("path/to/knowledge-folder")
mw.ingest()                     # build the graph from all *.md files
mw.sync()                       # incremental; skip unchanged files

# Where did this relationship come from?
mw.relationship_source("Good tooling", "increases", "quality")

# Why does this concept exist?
mw.explain_node("quality")
```

Derived state (graph + sync metadata) lives in `<workspace>/.speculoop/`.
The Markdown tree itself stays git-friendly and human-readable.

## What a sync reports

Every change is reported as a `SyncEvent` with a human-readable reason:

- `claim_added` — extracted a new relationship, with file/line/section/version
- `claim_removed` — source line gone; edges detached, private nodes removed,
  shared nodes/edges kept
- `file_added` / `file_deleted` — whole-file lifecycle events

Claims are identified by content hash, so moving a line does not count as a
delete + add. Repeating the same claim in another file strengthens provenance
(an edge can carry provenance from multiple sources) without duplicating it.

## What is deliberately NOT built yet

- No LLM is involved: extraction uses the existing pattern-based Decomposer
  (simple subject–verb–object sentences). Harder prose is reported as
  `unresolved` rather than silently dropped.
- No UI. The PoC exposes `sync()` reports and provenance queries as the
  foundation for a future "Why?" experience.
- Semantic provenance (where knowledge came from) exists; execution
  provenance (what the agent did) is a separate model for later.
- Human corrections are not yet aggregated into revision patterns (the
  long-term learning loop from the brief).

## Tests

```bash
python3 tests/test_markdown_workspace.py
```

Covers: ingest with provenance, incremental edit (add + remove), unchanged
file skipping, shared claims surviving partial removal, private node
detachment, and `explain_node`.
