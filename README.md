# SpecuLoop: Persistent Semantic Memory for AI Agents

**An experimental semantic knowledge graph engine for persistent agent memory, multiscale semantic retrieval, lens-dependent graph reasoning, and bidirectional natural language translation.**

SpecuLoop implements WRAP (persistent semantic state) — a graph-based architecture where meaning is stored as nodes and edges with numeric forces, viewed through semantic lenses, and translated bidirectionally between natural language and structured representation. The system supports dynamic RAG with semantic zoom, human-in-the-loop feedback propagation, and self-extending knowledge structures.

---

## Problems

AI agents working with large knowledge bases face concrete engineering problems that existing approaches don't fully address.

### A. Context Window Pressure

LLM agents must read many files to understand a large knowledge base. As the knowledge base grows, agents face increasing context-window pressure. Loading everything into context is expensive and often impossible. Token waste compounds with each additional file.

**Search terms**: *context window optimization, token-efficient AI agents, reduce RAG token usage, LLM context window pressure*

### B. Shallow Retrieval

Traditional RAG retrieves documents by vector similarity but does not necessarily strengthen the underlying relationships between concepts. Retrieval is stateless — each query starts fresh, and the system does not learn which retrievals were useful.

**Search terms**: *static RAG limitations, retrieval without learning, stateless RAG*

### C. Semantic Relationships Beyond Similarity

Vector similarity does not adequately represent semantic relationships such as:

- **causes** — A leads to B
- **opposes** — A conflicts with B
- **supports** — A reinforces B
- **increases** / **decreases** — magnitude relationships
- **demonstrates** — evidence for a claim
- **clarifies** — reduces ambiguity
- **requires** — dependency constraint

Two concepts can be semantically close (high vector similarity) but oppositional. Vector RAG cannot distinguish these.

**Search terms**: *semantic relationship types, causal knowledge graphs, oppositional relationships, graph-based reasoning*

### D. Misleading Graph Metrics

Knowledge graphs can become visually misleading when link count is mistaken for semantic importance. A node with many connections is not necessarily important — it may simply be generic. Conversely, a node with few connections may be critically important within a specific context.

**Search terms**: *knowledge graph ambiguity, graph centrality limitations, semantic importance metrics*

### E. One-Size-Fits-All Retrieval

Different questions require different semantic views over the same knowledge. A question about system architecture requires different relationships than a question about timeline or next steps. Most retrieval systems apply a single ranking strategy regardless of the question type.

**Search terms**: *multi-view knowledge graph, lens-based retrieval, adaptive retrieval, context-dependent search*

### F. AI-Generated Text Without Provenance

AI-generated explanations are difficult to connect back to the underlying knowledge structures. When an LLM produces an answer, there is no traceable link between the generated text and the specific knowledge that produced it. This makes it impossible to verify, correct, or update the underlying knowledge through the generated text.

**Search terms**: *provenance tracking, interpretable AI reasoning, verifiable AI outputs, semantic provenance*

### G. Disconnected Specifications and Code

Natural-language specifications, executable code, and shell commands are often disconnected. Changes in one do not propagate to the others. This creates drift between intent and implementation.

**Search terms**: *natural language code synchronization, bidirectional programming, specification-code alignment, program synthesis*

### H. Agent Misunderstanding

AI agents may fail to recognize when they have misunderstood an instruction. Without a mechanism to detect and propagate misunderstandings, errors compound silently.

**Search terms**: *agent misunderstanding detection, human-in-the-loop reasoning, semantic belief update*

### I. Discarded Failures

Tool failures and environmental constraints are often discarded as transient errors rather than incorporated into persistent reasoning state. The system does not learn from what it cannot do.

**Search terms**: *grounded agent reasoning, execution feedback, constraint-aware planning, environment-aware AI*

---

## How SpecuLoop Addresses These Problems

SpecuLoop implements a semantic knowledge graph architecture where:

1. **Knowledge is stored as a persistent graph** of nodes (concepts, actions, entities) and edges (relationships with numeric forces). The graph survives across sessions and grows incrementally.

2. **Retrieval is dynamic and lens-dependent.** Different semantic lenses weight the same graph differently, producing different views for different questions. Semantic zoom compresses highly-related structures at different abstraction levels.

3. **Generated text retains provenance.** Every sentence traces back to the specific nodes and edges that produced it. Human edits propagate back into the graph through interlocked translation.

4. **Failures become knowledge.** Tool failures and constraints are recorded as semantic information, enabling constraint-aware planning.

5. **The graph self-extends.** When input cannot be decomposed into existing structures, the system proposes new primitives for human confirmation.

```
Natural language input
    ↓ decompose
Semantic graph (nodes + edges + forces)
    ↓ select (lens-dependent)
Relevant subgraph (semantic zoom)
    ↓ compose
Natural language output (with provenance)
    ↓ human edit
Semantic update (interlocked translation)
    ↓ persist
Updated knowledge graph
```

---

## Semantic Zoom

Semantic zoom is not visual zoom. It is **lens-dependent multiscale semantic graph representation** — also described as **semantic graph coarsening for context-efficient reasoning**.

When zoomed in, the system shows detailed nodes and relationships. When zoomed out, highly related structures merge and compress. The compression depends on the active semantic lens.

| Lens | Compression Behavior |
|---|---|
| `temporal` | Compresses according to time relationships |
| `architecture` | Compresses according to system structure |
| `next-steps` | Compresses according to action/dependency chains |
| `causal` | Compresses according to cause-effect paths |
| `problem-solution` | Compresses according to problem-solution pairing |

Different lenses on the same graph produce different compressed views. This allows the same knowledge base to answer structurally different questions without loading the entire graph.

**Related concepts**: *graph coarsening, hierarchical clustering, multiscale graphs, semantic compression*

---

## Semantic Forces

Relationships in the graph have numeric strength. The same relationship can have different weights under different semantic lenses.

The conceptual model:

```
force(edge, lens, context) → numeric magnitude
relevance(node, query, lens, scope) → numeric score
```

Attraction and repulsion are expressed through edge weights:

- **Attraction** (positive force): `supports`, `causes`, `increases`, `demonstrates`
- **Repulsion** (negative force): `opposes`, `decreases`, `conflicts`

Examples:

| Structure | Force |
|---|---|
| `problem ↔ solution` | Oppositional — graph separates them, intermediate concepts form paths |
| `speed ↑ → quality ↓` | Negative magnitude — tradeoff loop |
| `evidence → hypothesis` | Positive directional — supports |
| `clarification → confusion` | Negative — reduces ambiguity |

The current model is experimental. The scoring mechanism is explicitly designed to be replaceable — from simple text overlap to embedding-based similarity to graph neural networks.

**Related concepts**: *semantic embeddings, knowledge graph reasoning, graph-based problem solving*

---

## Dynamic RAG

SpecuLoop's retrieval is dynamic in two senses:

1. **Retrieval is dynamically compressed through semantic zoom.** The subgraph selected for a query is shaped by the active lens and the query's semantic content, not by static keyword matching.

2. **The knowledge graph itself changes.** New information, human feedback, usage patterns, and execution results are incorporated into the graph incrementally. Retrieval quality improves as the graph learns.

**Related terms**: *adaptive retrieval, incremental graph learning, persistent semantic memory, knowledge graph updating, lifelong retrieval*

**Related concepts**: *GraphRAG, Agentic RAG, Hierarchical RAG*

---

## Interlocked Translation

Interlocked translation is the bidirectional mapping between natural language and semantic structures:

```
Natural language (Mumble)
    ↕
Semantic graph (WRAP)
    ↕
Materialized views (Markdown)
    ↕
Code / tools / execution
```

Generated natural language retains provenance to the semantic structures that produced each sentence. When a human edits the generated text, the system determines which underlying structures the edit refers to and propagates the semantic change back into the graph.

This means:

- **Semantic representation → natural language**: the graph produces readable text
- **Edited natural language → semantic update**: human corrections update the graph
- **Natural language specification → code**: specifications remain linked to implementation
- **Execution results → semantic update**: successes and failures update the graph

This bidirectional linking between English, code, and semantic structures is a core differentiating feature.

**Related concepts**: *bidirectional programming, program synthesis, natural language to code translation*

---

## Human Feedback

Human corrections are semantic observations, not merely text edits.

**Example**:

```
System:  "The main issue is context-window size."
Human:   "No, the underlying issue is token waste."
```

The system should propagate this correction into the graph: weaken the "context-window" node's relevance for this context, strengthen "token waste," and record the correction as a semantic observation.

Terms: *interactive graph learning, semantic feedback propagation, human-in-the-loop knowledge graph, persistent correction*

---

## Reality-Constrained Reasoning

When a desired operation cannot be executed — because of missing information, tool failure, or environmental constraint — the failure is not discarded. It becomes semantic information:

```
desired operation
    →
attempted execution
    →
success / failure
    →
semantic update
```

A failed tool call records what was attempted, what failed, and why. This enables the system to learn from constraints and avoid repeated failures.

Terms: *grounded agent reasoning, execution feedback, tool-aware reasoning, constraint-aware planning*

---

## Quick Start

```bash
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop

# Run the demo
python3 demo.py

# Run tests (9 passing)
python3 wrap/tests/test_core_loop.py
```

### Example

```python
from wrap.api import SpecuLoop

loop = SpecuLoop("knowledge.json")

# Ingest knowledge
loop.ingest("Speed and quality are in tension.")
loop.ingest("Good tooling improves quality.")

# Query with DRAG
result = loop.query("What affects quality?")
print(result.markdown)
# → "Speed opposes quality."
# → "Good tooling increases quality."

# Human edits propagate back
loop.edit(result.markdown,
    "Speed opposes quality, but good tooling reduces this tension.")

# Self-extension for new concepts
proposal = loop.propose("creativity")
loop.confirm_proposal(proposal)
```

---

## Related Concepts

### GraphRAG

GraphRAG (Microsoft, 2024) builds a knowledge graph from documents and uses community detection to summarize communities of related entities. SpecuLoop shares the goal of graph-based retrieval but differs in that:

- SpecuLoop stores relationships with numeric forces, not just co-occurrence
- Retrieval is lens-dependent, not community-based
- The graph is persistent and incrementally updated, not rebuilt per query

### Agentic RAG

Agentic RAG uses an LLM agent to decide what to retrieve and when. SpecuLoop's DRAG (Dynamic RAG) is similarly agent-driven but adds semantic zoom — the retrieval scope is dynamically compressed based on the active lens and query.

### Knowledge Graphs

Traditional knowledge graphs store entities and typed relationships. SpecuLoop extends this with:

- Numeric forces on edges (attraction/repulsion)
- Lens-dependent edge weights
- Provenance tracking from graph to generated text
- Self-extension proposals for new primitives

### Hierarchical RAG

Hierarchical RAG organizes documents in a tree structure and retrieves at different levels. SpecuLoop's semantic zoom achieves similar compression but through graph coarsening driven by semantic lenses rather than fixed document hierarchies.

### Long-term Agent Memory

Projects like MemGPT and Letta implement persistent memory for LLM agents. SpecuLoop differs by storing memory as a semantic graph with forces and lenses, rather than as flat text summaries or key-value stores.

### Graph Embeddings

Graph embedding methods (TransE, Node2Vec, etc.) map graph structures to vectors. SpecuLoop's scoring mechanism is explicitly designed to eventually incorporate graph embeddings, but starts with simpler heuristics.

### Causal Graphs

Causal graphs represent cause-effect relationships. SpecuLoop includes causal relationships as one of many edge types, alongside oppositional, supportive, and dependency relationships.

### Human-in-the-Loop Learning

Interactive machine learning systems incorporate human feedback to improve models. SpecuLoop applies this to knowledge graphs — human corrections propagate as semantic updates to the graph structure.

### Program Synthesis

Program synthesis generates code from specifications. SpecuLoop's interlocked translation is intended to eventually support bidirectional linking between natural-language specifications and executable code.

---

## Repository Structure

```
SpecuLoop/
├── README.md                  # This file
├── GLOSSARY.md                # Term definitions
├── ARCHITECTURE.md            # System architecture
├── AGENTS.md                  # AI agent instructions
├── RELATED_WORK.md            # Academic and open-source references
├── CITATION.cff               # Citation metadata
├── CONTRIBUTING.md            # Contribution guide
├── LICENSE                    # MIT license
├── CHANGELOG.md               # Version history
├── demo.py                    # Interactive demo
├── docs/
│   ├── problems/              # Engineering problems addressed
│   ├── concepts/              # Core technical concepts
│   ├── architecture/          # Component documentation
│   └── comparisons/           # Comparison with related systems
└── wrap/
    ├── api.py                 # Main interface
    ├── core/                  # Node, Edge, Graph, Lens
    ├── translation/           # Mumble ↔ WRAP
    ├── drag/                  # Subgraph selection
    ├── extension/             # Self-extension
    ├── feedback/              # Edit propagation
    ├── persistence/           # JSON storage
    └── tests/                 # End-to-end tests
```

---

## Status

This is an experimental reconstruction of a lost system. The current implementation is a minimal kernel demonstrating the core loop. All components are designed to be replaceable.

See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for current status and known limitations.

---

## License

MIT
