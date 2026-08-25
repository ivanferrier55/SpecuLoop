# Related Problems

Semantic index of engineering problems this project addresses. Each entry maps conventional terminology to project concepts.

---

## Problem: Large Knowledge Bases Exceed Agent Context

### Problem

AI agents must inspect many files before understanding a large knowledge base. As the knowledge base grows, agents face increasing context-window pressure and token waste.

### Conventional Terminology

- long-context reasoning
- agent memory
- persistent memory
- context-window limitation
- hierarchical retrieval
- knowledge compression
- semantic retrieval

### Existing Approaches

- RAG (retrieve-then-read)
- GraphRAG (graph-based retrieval with community detection)
- hierarchical RAG (tree-based document organization)
- summarization (pre-computed summaries)
- vector retrieval (embedding similarity)

### Limitations of Existing Approaches

- RAG retrieves by similarity, not by semantic relationship
- GraphRAG rebuilds graphs per query, does not persist
- Hierarchical RAG uses fixed document trees, not dynamic compression
- Summarization loses structure and relationships

### WRAP Approach

Persistent semantic representation with lens-dependent multiscale graph compression. The graph compresses differently depending on the query and active lens.

### Related WRAP Concepts

- semantic zoom
- semantic lenses
- DRAG
- persistent semantic memory

### Relevant Files

- `docs/concepts/semantic-zoom.md`
- `docs/concepts/dynamic-rag.md`
- `docs/problems/large-context.md`
- `docs/problems/token-waste.md`

### Status

Experimental

### Confidence

MEDIUM — the mechanism exists but has not been tested at scale.

---

## Problem: Shallow Retrieval Without Learning

### Problem

Traditional RAG retrieves documents by vector similarity but does not strengthen or weaken relationships based on retrieval success. Each query starts fresh.

### Conventional Terminology

- stateless retrieval
- retrieval without feedback
- non-adaptive RAG
- static knowledge retrieval

### Existing Approaches

- Vector similarity search
- BM25 keyword search
- Hybrid retrieval (vector + keyword)

### Limitations

- No memory of which retrievals were useful
- No relationship strengthening between co-retrieved concepts
- No learning from user feedback on retrieval quality

### WRAP Approach

Dynamic RAG (DRAG) that updates the knowledge graph based on retrieval success, human feedback, and usage patterns. Retrieval quality improves as the graph learns.

### Related WRAP Concepts

- dynamic RAG
- semantic feedback
- persistent semantic memory

### Relevant Files

- `docs/concepts/dynamic-rag.md`
- `wrap/drag/selector.py`
- `wrap/feedback/propagator.py`

### Status

Scoring and selection implemented. Feedback-driven learning planned.

### Confidence

MEDIUM — the mechanism is designed but feedback integration is incomplete.

---

## Problem: Semantic Relationships Beyond Similarity

### Problem

Vector similarity does not represent relationships like causation, opposition, support, or dependency. Two concepts can be similar but oppositional.

### Conventional Terminology

- semantic relationships
- knowledge graph relations
- typed edges
- relational reasoning
- causal graphs

### Existing Approaches

- Knowledge graphs with typed edges (RDF, OWL)
- Causal graphs (structural causal models)
- Graph embeddings (TransE, Node2Vec)

### Limitations

- Most knowledge graphs use binary relationships without numeric strength
- Causal graphs represent only causation, not other relationship types
- Graph embeddings lose explicit relationship semantics

### WRAP Approach

Edges have typed relationships AND numeric forces. Forces are modified by lenses. The graph represents causation, opposition, support, dependency, and other relationships with numeric strength.

### Related WRAP Concepts

- semantic forces
- semantic edges
- semantic lenses

### Relevant Files

- `wrap/core/edge.py`
- `docs/concepts/semantic-forces.md`
- `docs/concepts/semantic-lenses.md`

### Status

Base forces implemented. Lens modification implemented in scoring.

### Confidence

MEDIUM — the force model is a hypothesis about the original system.

---

## Problem: One-Size-Fits-All Retrieval

### Problem

Different questions require different views of the same knowledge. A question about architecture needs different relationships than a question about timeline.

### Conventional Terminology

- multi-view knowledge graph
- context-dependent retrieval
- adaptive retrieval
- query-dependent ranking

### Existing Approaches

- Multi-head attention (different heads capture different relationships)
- Query-specific reranking
- Topic-aware retrieval

### Limitations

- Most systems apply a single ranking strategy
- No explicit mechanism for switching between semantic views
- No lens-based compression

### WRAP Approach

Semantic lenses modify how the graph is viewed and scored. The same graph produces different compressed views under different lenses.

### Related WRAP Concepts

- semantic lenses
- semantic zoom
- multi-view retrieval

### Relevant Files

- `wrap/core/lens.py`
- `docs/concepts/semantic-lenses.md`
- `docs/concepts/semantic-zoom.md`

### Status

Lens weights implemented in scoring. Dynamic lens propagation planned.

### Confidence

MEDIUM — the concept is remembered; exact mechanism is provisional.

---

## Problem: AI-Generated Text Without Provenance

### Problem

AI-generated explanations cannot be traced back to specific knowledge structures. This makes verification, correction, and updating impossible.

### Conventional Terminology

- provenance tracking
- attribution
- source tracing
- interpretable AI reasoning
- verifiable AI outputs

### Existing Approaches

- Citation-based attribution
- Attention visualization
- Chain-of-thought reasoning

### Limitations

- Citations point to documents, not semantic structures
- Attention is not interpretable as provenance
- Chain-of-thought is not linked to persistent knowledge

### WRAP Approach

Every generated sentence carries provenance metadata linking it to specific graph nodes and edges. Human edits propagate back through provenance.

### Related WRAP Concepts

- provenance
- interlocked translation
- semantic feedback

### Relevant Files

- `wrap/translation/composer.py`
- `wrap/feedback/propagator.py`
- `docs/concepts/interlocked-translation.md`

### Status

Provenance metadata generated and parsed. Edit propagation partially implemented.

### Confidence

HIGH — provenance tracking is well-understood.

---

## Problem: Disconnected Specifications and Code

### Problem

Natural-language specifications, executable code, and shell commands are often disconnected. Changes in one do not propagate to others.

### Conventional Terminology

- bidirectional programming
- natural language code synchronization
- specification-code alignment
- program synthesis
- live programming

### Existing Approaches

- Bidirectional lenses (Foster et al.)
- Program synthesis from specifications
- Live programming environments

### Limitations

- Bidirectional lenses require formal specifications
- Program synthesis is limited to small programs
- Live programming does not handle natural language

### WRAP Approach

Interlocked translation maintains bidirectional links between natural language, semantic structures, and code. The semantic graph is the intermediary.

### Related WRAP Concepts

- interlocked translation
- provenance
- semantic feedback

### Relevant Files

- `docs/concepts/interlocked-translation.md`
- `INTERLOCKED_TRANSLATION.md`

### Status

Natural language ↔ graph translation implemented. Code translation planned.

### Confidence

MEDIUM — the concept is clear; code translation is unimplemented.

---

## Problem: Agent Misunderstanding

### Problem

AI agents may fail to recognize when they have misunderstood an instruction. Errors compound silently.

### Conventional Terminology

- agent misunderstanding detection
- human-in-the-loop reasoning
- semantic belief update
- interactive learning
- clarification questions

### Existing Approaches

- Confidence calibration
- Active learning (ask when uncertain)
- Human-in-the-loop pipelines

### Limitations

- Confidence calibration is often miscalibrated
- Active learning asks about data, not understanding
- Human-in-the-loop pipelines are task-specific

### WRAP Approach

Gaps in decomposition become semantic information. The system flags ambiguity and proposes clarification questions based on detected gaps.

### Related WRAP Concepts

- self-extension
- semantic feedback
- constraints

### Relevant Files

- `wrap/extension/self_extender.py`
- `wrap/feedback/propagator.py`
- `docs/problems/agent-misunderstanding.md`

### Status

Gap detection and proposal generation implemented. Clarification question generation planned.

### Confidence

MEDIUM — the mechanism exists; quality of proposals needs evaluation.

---

## Problem: Tool Failures Discarded

### Problem

Tool failures and environmental constraints are discarded as transient errors rather than incorporated into persistent reasoning state.

### Conventional Terminology

- grounded agent reasoning
- execution feedback
- tool-aware reasoning
- environment-aware AI
- constraint-aware planning

### Existing Approaches

- Retry with backoff
- Error logging
- Tool selection based on success rate

### Limitations

- Retries do not learn from failure patterns
- Error logs are not semantic
- Tool selection does not represent constraints

### WRAP Approach

Failures are translated back into the semantic graph as constraints. The system learns what it cannot do and avoids repeated failures.

### Related WRAP Concepts

- constraints
- reality-constrained reasoning
- semantic feedback

### Relevant Files

- `wrap/feedback/propagator.py`
- `docs/problems/constraints.md` (planned)

### Status

`process_feedback()` exists but is not wired into the main loop.

### Confidence

LOW — the mechanism is designed but untested.

---

## Problem: Knowledge Graph Ambiguity

### Problem

Link count is mistaken for importance. Generic nodes with many connections appear important; critical nodes with few connections are overlooked.

### Conventional Terminology

- graph centrality limitations
- knowledge graph importance metrics
- semantic importance
- PageRank limitations

### Existing Approaches

- PageRank / betweenness centrality
- Degree-based ranking
- HITS (hubs and authorities)

### Limitations

- Centrality metrics are global, not query-dependent
- Generic nodes dominate rankings
- No mechanism for context-dependent importance

### WRAP Approach

Importance is a function of the query, the lens, and the graph structure. No single metric determines importance globally.

### Related WRAP Concepts

- semantic lenses
- semantic forces
- DRAG scoring

### Relevant Files

- `wrap/drag/scorer.py`
- `docs/problems/knowledge-graph-ambiguity.md`

### Status

Query-dependent scoring implemented. Lens-dependent scoring implemented.

### Confidence

HIGH — this is a well-understood problem with a reasonable solution.
