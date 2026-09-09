---
type: object
name: node
implementation: mumblewrap/core/node.py
summary: Semantic unit with label, content, reuse count, and provenance.
---

# Node

A labeled semantic unit in the graph. Carries content, reuse count, metadata (evidence, uncertainty, provisional flag), and provenance.

**Mutated by:** ingest (new nodes), accept_candidate, accept_refactor, edit (propagation).
**Read by:** Translator (emit), Scorer (scoring), Decomposer (matching).
