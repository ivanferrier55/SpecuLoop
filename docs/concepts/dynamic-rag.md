# Dynamic RAG: Infrastructure for Semantic Retrieval

DRAG (Dynamic RAG) is infrastructure for selecting, weighting, composing, and compressing mumbleWRAP structures according to the active lens and context.

DRAG is a mechanism that supports the central objective (meaning preservation), not the objective itself.

## What DRAG Does

1. **Score** nodes and edges by relevance to the query
2. **Select** a relevant subgraph from mumbleWRAP
3. **Compress** using semantic zoom (lens-dependent)
4. **Compose** as human-readable text with provenance

## How It Differs from Static RAG

| Aspect | Static RAG | DRAG |
|---|---|---|
| Retrieval basis | Vector similarity | Graph traversal + scoring |
| Scope | Fixed document set | Dynamic subgraph |
| Compression | Truncation | Semantic zoom |
| Learning | None | Graph updates from feedback |
| Provenance | None | Full traceability |
| View | Single ranking | Lens-dependent |

## Dynamic in Two Senses

1. **Retrieval is dynamically compressed** through semantic zoom — the scope adapts to the query and active lens
2. **The knowledge graph itself changes** — new information, feedback, and execution results update mumbleWRAP incrementally

## Related Technical Concepts

- adaptive retrieval
- incremental graph learning
- lifelong retrieval
- knowledge graph updating
- online learning for retrieval

**Related problems**: [shallow retrieval](../problems/shallow-retrieval.md), [context overload](../problems/large-context.md)

**Implementation**: `wrap/drag/selector.py`, `wrap/drag/scorer.py`

**Status**: Scoring and selection implemented. Compression and feedback learning planned.
