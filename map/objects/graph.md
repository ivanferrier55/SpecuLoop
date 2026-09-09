---
type: object
name: graph
implementation: mumblewrap/core/graph.py
summary: Central semantic graph holding nodes, edges, lenses, and statistics.
---

# Graph

The persistent semantic substrate. Stores all nodes, edges, and lenses. Supports add/get/remove operations and statistics.

**Mutated by:** ingest (new nodes/edges), accept_candidate (new primitive), accept_refactor (replaces nodes), edit (propagation), store (save/load).
**Read by:** DRAGSelector (query), Scorer (scoring), Translator (emit), SemanticLearner (compression).
