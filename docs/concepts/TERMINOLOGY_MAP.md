# Terminology Map

Proprietary terms mapped to conventional technical terminology. Use this to find the project from any standard search term.

---

## WRAP (Persistent Semantic State)

**What it is**: A graph of nodes and edges representing semantic meaning, persisted across sessions.

**Conventional terms** (search for these):
- semantic knowledge graph
- persistent semantic memory
- structured agent memory
- symbolic-semantic representation
- graph-based reasoning
- knowledge representation
- semantic network

**Related systems**:
- ConceptNet (common-sense knowledge graph)
- Wikidata (collaborative knowledge graph)
- Neo4j (graph database)
- RDF / SPARQL (semantic web standards)

**What's different**: WRAP adds numeric forces on edges, lens-dependent weights, provenance tracking, and self-extension proposals. Most knowledge graphs use binary relationships without numeric strength.

**Status**: Experimental implementation of persistent semantic memory.

---

## DRAG (Dynamic RAG)

**What it is**: Retrieval that dynamically selects and compresses a subgraph based on query, lens, and graph state.

**Conventional terms**:
- adaptive retrieval
- dynamic knowledge graph RAG
- graph-based retrieval
- query-dependent subgraph selection
- lens-dependent retrieval

**Related systems**:
- GraphRAG (Microsoft) — per-query graph construction
- Agentic RAG — agent-driven retrieval decisions
- RAPTOR — hierarchical retrieval with tree summarization

**What's different**: DRAG uses a persistent, incrementally updated graph with lens-dependent scoring, not per-query graph construction.

**Status**: Scoring and selection implemented. Compression and feedback learning planned.

---

## Semantic Zoom

**What it is**: Compressing or expanding a knowledge graph at different levels of abstraction, depending on the active lens.

**Conventional terms**:
- graph coarsening
- multiscale graph representation
- hierarchical clustering
- semantic compression
- context reduction
- hierarchical retrieval
- progressive disclosure

**Related systems**:
- Graph coarsening algorithms (Karypis & Kumar)
- Multiscale graph neural networks
- Hierarchical clustering

**What's different**: Semantic zoom is lens-dependent — different lenses produce different compressed views of the same graph.

**Status**: Compression mechanism exists. Not yet integrated into emit pipeline.

---

## Semantic Lens

**What it is**: A weight modifier that changes how a graph is viewed, scored, and compressed.

**Conventional terms**:
- multi-view knowledge graph
- context-dependent retrieval
- adaptive retrieval
- query-dependent ranking
- view-dependent graph projection

**Related systems**:
- Multi-head attention (different heads = different views)
- Topic-aware retrieval

**What's different**: Lenses are explicit, user-definable data structures that modify edge and node weights globally.

**Status**: Weight modification implemented. Dynamic propagation planned.

---

## Semantic Force

**What it is**: The numeric strength and direction of a relationship edge.

**Conventional terms**:
- edge weight
- attraction-repulsion model
- force-directed graph
- signed graph
- weighted relation

**Related systems**:
- Force-directed graph layout (Fruchterman-Reingold)
- Signed social networks
- Attraction/repulsion in agent swarms

**What's different**: Forces are modified by lenses and represent semantic relationships (causes, opposes, supports), not just spatial layout.

**Status**: Base forces implemented. Full force-directed layout planned.

---

## Interlocked Translation

**What it is**: Bidirectional mapping between natural language and semantic structures, where changes in one propagate to the other.

**Conventional terms**:
- bidirectional programming
- natural language code synchronization
- program synthesis
- bidirectional transformation
- source-target synchronization

**Related systems**:
- Bidirectional lenses (Foster et al., 2007)
- Boomerang /颠倒 (bidirectional programming languages)
- Natural language to code systems

**What's different**: Interlocked translation operates through a semantic graph intermediary, not direct text-to-text transformation.

**Status**: Natural language ↔ graph implemented. Code translation planned.

---

## Semantic Feedback

**What it is**: Human corrections propagated as semantic updates to the knowledge graph.

**Conventional terms**:
- interactive graph learning
- human-in-the-loop knowledge graph
- persistent correction
- semantic belief update
- interactive machine learning

**Related systems**:
- Active learning
- RLHF (reinforcement learning from human feedback)
- Interactive machine learning

**What's different**: Feedback modifies graph structure (nodes, edges, weights), not model parameters.

**Status**: Edit propagation implemented. Full feedback integration planned.

---

## Persistent Semantic Memory

**What it is**: Knowledge stored as a semantic graph that survives across sessions and grows incrementally.

**Conventional terms**:
- lifelong agent memory
- AI agent persistent memory
- long-term LLM memory
- persistent knowledge graph
- agent memory system

**Related systems**:
- MemGPT / Letta (tiered text memory)
- Generative Agents (memory streams with reflection)
- MemoryBank (long-term agent memory)

**What's different**: Memory is stored as a semantic graph with typed relationships and numeric forces, not flat text summaries.

**Status**: Core graph with persistence implemented.

---

## Dynamic RAG

**What it is**: Retrieval that changes over time — both the retrieval scope and the knowledge graph itself update.

**Conventional terms**:
- adaptive retrieval
- incremental graph learning
- lifelong retrieval
- knowledge graph updating
- persistent retrieval

**Related systems**:
- Adaptive RAG
- Online learning for retrieval
- Incremental knowledge graph construction

**What's different**: Both the retrieval mechanism and the knowledge graph are dynamic. Retrieval quality improves as the graph learns.

**Status**: Graph updates implemented. Feedback-driven retrieval improvement planned.

---

## Graph Coarsening

**What it is**: Merging highly related nodes into higher-level abstractions to reduce graph size while preserving structure.

**Conventional terms**:
- graph summarization
- hierarchical aggregation
- multiscale reduction
- graph compression

**Related systems**:
- Graph coarsening (Karypis & Kumar, 1998)
- Graph summarization
- Clique compression

**What's different**: Coarsening is driven by semantic lenses, not just structural similarity.

**Status**: Basic node removal implemented. Full cluster merging planned.
