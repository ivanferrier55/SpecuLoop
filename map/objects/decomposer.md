---
type: object
name: decomposer
implementation: mumblewrap/translation/decomposer.py
summary: Breaks text into semantic nodes and edges via pattern matching.
---

# Decomposer

Parses human-language input into candidate nodes and edges. Reuses existing nodes when patterns match; creates new ones when they don't.

**Mutated by:** ingest (adds to graph).
**Read by:** Translator (ingest path), SemanticLearner (measures basis adequacy).
