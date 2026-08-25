# Comparison with Related Systems

Honest comparison of SpecuLoop with existing approaches.

---

## vs. Vector RAG

| Aspect | Vector RAG | SpecuLoop |
|---|---|---|
| Storage | Vector embeddings | Semantic graph |
| Retrieval | Cosine similarity | Graph traversal + scoring |
| Relationships | Implicit (similarity) | Explicit (typed edges) |
| Learning | None | Graph updates |
| Compression | Truncation | Semantic zoom |
| Provenance | None | Full traceability |

**Shared**: Both retrieve relevant information for a query.
**Different**: SpecuLoop stores explicit relationships and supports lens-dependent retrieval.

---

## vs. GraphRAG (Microsoft)

| Aspect | GraphRAG | SpecuLoop |
|---|---|---|
| Graph type | Entity co-occurrence | Semantic relationships |
| Retrieval | Community summarization | Lens-dependent subgraph selection |
| Forces | None | Numeric attraction/repulsion |
| Lenses | None | Multiple semantic views |
| Update | Rebuilt per query | Incrementally updated |

**Shared**: Both use knowledge graphs for retrieval.
**Different**: GraphRAG builds graphs from documents per query. SpecuLoop maintains a persistent, incrementally updated graph with numeric forces and lenses.

---

## vs. Agentic RAG

| Aspect | Agentic RAG | SpecuLoop |
|---|---|---|
| Agent role | Decides what to retrieve | Retrieves via DRAG + lenses |
| Memory | Session-scoped | Persistent graph |
| Learning | None | Feedback propagation |
| Compression | None | Semantic zoom |

**Shared**: Both use an agent to drive retrieval decisions.
**Different**: SpecuLoop adds persistent memory, semantic zoom, and feedback-driven learning.

---

## vs. Knowledge Graphs

| Aspect | Traditional KG | SpecuLoop |
|---|---|---|
| Relationships | Typed | Typed + numeric forces |
| Weights | None or static | Dynamic, lens-dependent |
| Provenance | None | Full traceability |
| Self-extension | Manual | Automatic proposals |
| Retrieval | SPARQL/cypher | DRAG with scoring |

**Shared**: Both store entities and typed relationships.
**Different**: SpecuLoop adds numeric forces, lenses, provenance, and self-extension.

---

## vs. Hierarchical RAG

| Aspect | Hierarchical RAG | SpecuLoop |
|---|---|---|
| Structure | Fixed document tree | Dynamic graph |
| Compression | Tree level selection | Semantic zoom via lenses |
| Granularity | Predefined levels | Query-dependent |

**Shared**: Both support multi-level retrieval.
**Different**: Hierarchical RAG uses fixed document hierarchies. SpecuLoop's compression is driven by semantic lenses and the query.

---

## vs. Long-term Agent Memory (MemGPT, Letta)

| Aspect | MemGPT/Letta | SpecuLoop |
|---|---|---|
| Memory format | Flat text summaries | Semantic graph |
| Relationships | None | Explicit, typed |
| Querying | Keyword/text search | Graph traversal |
| Reasoning | None | Force-based |

**Shared**: Both provide persistent memory across sessions.
**Different**: SpecuLoop stores memory as a semantic graph with relationships and forces, not as flat text.

---

## What Remains Experimental

- Numeric force model (hypothesis, not validated)
- Lens propagation (implemented but not tested at scale)
- Semantic zoom compression (mechanism exists, not integrated into emit)
- Edit propagation (heuristic, needs LLM integration)
- Self-extension proposals (basic, needs evaluation)

SpecuLoop does not claim superiority over these systems. It proposes a different architecture — persistent semantic state with numeric forces, lenses, and interlocked translation — that may complement or improve upon existing approaches for specific use cases.
