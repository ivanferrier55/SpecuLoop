# Persistent Semantic Memory for LLM Agents

mumbleWRAP is the persistent semantic substrate for AI agent memory. It stores meaning as reusable semantic structures, not flat text summaries.

## Why Semantic Memory, Not Text Memory

When an agent stores knowledge as flat text:
- Relationships between concepts are implicit
- Querying requires scanning all text
- Compression means truncation
- No mechanism for bidirectional translation

When an agent stores knowledge as mumbleWRAP:
- Relationships are explicit (typed edges with forces)
- Querying uses graph traversal
- Compression is semantic (zoom)
- Bidirectional translation preserves meaning

## How mumbleWRAP Memory Works

1. **Ingest**: human language → semantic structures
2. **Decompose**: new inputs reuse existing nodes when possible
3. **Extend**: propose new primitives when needed
4. **Retrieve**: lens-dependent subgraph selection
5. **Feedback**: human corrections propagate into the graph
6. **Persist**: graph survives across sessions

## Comparison with Flat Memory

| Aspect | Flat Memory | mumbleWRAP |
|---|---|---|
| Structure | Sequential text | Semantic graph |
| Relationships | Implicit | Explicit, typed |
| Querying | Keyword search | Graph traversal |
| Compression | Truncation | Semantic zoom |
| Translation | None | Interlocked |
| Learning | Append-only | Incremental update |

## Related Technical Concepts

- lifelong agent memory
- AI agent persistent memory
- long-term LLM memory
- persistent knowledge graph
- memory streams
- reflective memory

**Related to**: [Interlocked Translation](interlocked-translation.md), [Semantic Feedback](semantic-feedback.md)

**Implementation**: `wrap/core/graph.py`, `wrap/persistence/store.py`

**Status**: Core graph with persistence implemented.
