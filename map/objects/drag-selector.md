---
type: object
name: drag-selector
implementation: drag/selector.py
summary: Selects a relevant subgraph from the full graph for a given query.
---

# DRAGSelector

Selects the most relevant subgraph for a query by scoring all nodes, then taking the top-N. Applies lens weights if a lens is provided.

**Mutated by:** none (pure reader).
**Read by:** SpecuLoop API (query).
