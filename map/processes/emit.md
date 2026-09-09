---
type: process
name: emit
entrypoint: mumblewrap/api.py:SpecuLoop.emit
inputs: [graph, translator, composer, lens]
outputs: [CompositionResult (markdown)]
---

# emit

Graph → human-readable text. Optionally filtered by a lens.

**Flow:** node_ids + lens → Translator.emit → Composer → markdown.
**Human gate:** the output is an edit surface (humans can edit, then call edit() to propagate).
**Does not hit:** ingest (separate direction).
