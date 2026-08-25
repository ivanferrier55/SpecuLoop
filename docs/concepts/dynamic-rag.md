# Dynamic RAG

**Search terms**: dynamic RAG, adaptive retrieval, incremental graph learning, lifelong retrieval, adaptive GraphRAG

## What Is Dynamic RAG?

Dynamic RAG (DRAG) is retrieval that changes over time, in two senses:

### 1. Dynamic Retrieval Scope

The subgraph selected for a query is shaped by:

- The query's semantic content
- The active lens
- The graph's current state

This is not static keyword matching or fixed-window retrieval. The scope adapts to the question.

### 2. Dynamic Knowledge Graph

The graph itself changes as:

- New information is ingested
- Human feedback propagates
- Usage patterns shift relevance
- Execution results update constraints

Retrieval quality improves as the graph learns from use.

## How DRAG Works

1. **Score** all nodes by relevance to the query under the active lens
2. **Select** seed nodes (top-K by score)
3. **Propagate** from seeds through connected edges
4. **Collect** the relevant subgraph
5. **Compress** if needed to fit token budget
6. **Return** the subgraph for composition

## Comparison with Static RAG

| Aspect | Static RAG | DRAG |
|---|---|---|
| Retrieval basis | Vector similarity | Graph traversal + scoring |
| Scope | Fixed document set | Dynamic subgraph |
| Learning | None | Graph updates from feedback |
| Compression | Truncation | Semantic zoom |
| Context | Flat | Lens-dependent |

**Implementation status**: Scoring and selection are implemented. Compression and feedback-driven learning are planned.

## Questions This Project Addresses

- How can RAG improve as the knowledge graph grows?
- How can retrieval quality improve from human feedback?
- How can the knowledge graph learn from retrieval success and failure?

## Related Technical Concepts

- adaptive retrieval
- incremental graph learning
- lifelong retrieval
- knowledge graph updating
- online learning for retrieval
