---
type: object
name: edge
implementation: mumblewrap/core/edge.py
summary: Typed relationship between nodes with numeric force (attraction/repulsion).
---

# Edge

A directed, typed relationship between two nodes. Carries a relation type, numeric force (attraction or repulsion), and reuse count.

**Mutated by:** ingest (new edges), edit (propagation), accept_refactor (rewiring).
**Read by:** Scorer (force-based scoring), Translator (emit), DRAGSelector (subgraph traversal).
