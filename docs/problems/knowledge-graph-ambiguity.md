# Knowledge Graph Ambiguity

**Search terms**: knowledge graph importance metrics, graph centrality limitations, semantic importance

## The Problem

Knowledge graphs can be misleading when link count is mistaken for semantic importance. A node with many connections may simply be generic (like "system" or "process"), not important.

Conversely, a node with few connections may be critically important within a specific context but overlooked by centrality-based ranking.

## SpecuLoop's Approach

Importance is context-dependent, determined by the active semantic lens. A node's relevance is a function of the query, the lens, and the graph structure — not just its connectivity.

```
relevance(node, query, lens, scope) → numeric score
```
