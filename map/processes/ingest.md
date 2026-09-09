---
type: process
name: ingest
entrypoint: mumblewrap/api.py:SpecuLoop.ingest
inputs: [translator, decomposer, graph]
outputs: [graph (new nodes/edges), store]
---

# ingest

Human text → semantic nodes and edges. The translator delegates to the decomposer, which reuses existing nodes or creates new ones.

**Flow:** text → Translator.ingest → Decomposer → new Node/Edge → Graph → Store.save.
**Human gate:** none (automatic).
**Does not hit:** emit (separate direction).
