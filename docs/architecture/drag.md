# DRAG: Dynamic RAG

DRAG is the retrieval layer of SpecuLoop. It selects and compresses knowledge from the WRAP graph.

## Scoring

Nodes and edges are scored by relevance to a query:

```
score(node, query, lens) = 
    text_match(node, query) × lens_weight(node, lens)
    + edge_density_bonus(node)
    + usage_bonus(node)
```

The scoring mechanism is explicitly replaceable.

## Selection

1. Score all nodes
2. Select top-K seeds
3. Propagate through connected edges (priority by edge weight × lens weight)
4. Collect the subgraph

## Compression

The subgraph is compressed to fit a token budget by removing lowest-scored nodes and their connected edges.

See [DRAG_CORE.md](../../DRAG_CORE.md) for the full specification.
