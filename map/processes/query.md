---
type: process
name: query
entrypoint: mumblewrap/api.py:SpecuLoop.query
inputs: [drag-selector, scorer, translator, composer]
outputs: [CompositionResult (markdown)]
---

# query

DRAG selects relevant subgraph, then composer generates text. The core retrieval-reasoning path.

**Flow:** query_text → DRAGSelector.select (scores all nodes, takes top-N) → Translator.emit → markdown.
**Human gate:** output is an edit surface.
**Does not hit:** ingest.
