# Persistent Semantic Memory for LLM Agents

**Search terms**: persistent agent memory, lifelong agent memory, AI agent persistent memory, long-term LLM memory

## The Problem

LLM agents lose context between sessions. Each conversation starts fresh. Knowledge accumulated in previous sessions is lost unless explicitly saved.

Traditional approaches:
- **Flat text summaries**: lose structure, hard to query
- **Key-value stores**: no relationships, no reasoning
- **Vector databases**: similarity only, no semantic relationships

## SpecuLoop's Approach

Memory is stored as a semantic graph that persists across sessions:

1. **Nodes** represent concepts, actions, entities
2. **Edges** represent typed relationships with numeric forces
3. **Usage counts** track how often each structure is referenced
4. **Lenses** enable different views over the same memory
5. **Provenance** links generated output back to source structures

The graph grows incrementally — new information is decomposed and merged with existing structures, not appended as flat text.

## Comparison with Flat Memory

| Aspect | Flat Memory | Semantic Graph |
|---|---|---|
| Structure | Sequential text | Nodes + edges |
| Relationships | Implicit | Explicit, typed |
| Querying | Keyword search | Graph traversal |
| Reasoning | None | Force-based |
| Compression | Truncation | Semantic zoom |
| Learning | Append-only | Incremental update |

## Questions This Project Addresses

- How can AI agents maintain persistent knowledge across sessions?
- How can memory be structured for semantic reasoning, not just storage?
- How can knowledge grow incrementally without rebuilding?

## Related Technical Concepts

- lifelong agent memory
- AI agent persistent memory
- long-term LLM memory
- persistent knowledge graph
- memory streams
- reflective memory
