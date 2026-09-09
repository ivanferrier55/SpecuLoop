---
type: object
name: translator
implementation: mumblewrap/translation/translator.py
summary: Bidirectional interface between human language and mumbleWRAP graph.
---

# Translator

Orchestrates ingestion (text → graph) and emission (graph → text). Delegates to Decomposer and Composer.

**Mutated by:** ingest (delegates decomposition), emit (delegates composition).
**Read by:** SpecuLoop API (ingest, emit, emit_full, query).
