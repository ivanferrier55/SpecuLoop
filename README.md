# SpecuLoop — WRAP: Persistent Semantic State for AI Agents

**WRAP is a graph-based semantic memory engine that enables AI agents to maintain persistent knowledge, perform dynamic RAG with semantic zoom, and translate bidirectionally between natural language and structured meaning.**

> Built as the core kernel of [SpecuLoop](https://github.com/ivanferrier55/SpecuLoop) — a system for persistent AI agent memory, semantic knowledge graphs, and interlocked natural language translation.

---

## What Problem Does This Solve?

AI agents lose context between sessions. RAG helps retrieve relevant documents, but it doesn't solve the underlying problem: **agents need persistent semantic memory** — a structured, queryable knowledge graph that grows over time, understands relationships, and translates between human language and machine-readable meaning.

SpecuLoop's WRAP engine is that semantic memory layer. It provides:

- **Persistent semantic graph** — nodes, edges, and numeric forces that survive across sessions
- **Bidirectional Mumble ↔ WRAP translation** — natural language in, structured knowledge out, and back again
- **Dynamic RAG (DRAG)** — subgraph selection with replaceable scoring (text match → embeddings → GNN)
- **Semantic zoom** — compress or expand knowledge at different levels of abstraction
- **Provenance tracking** — every generated sentence traces back to the WRAP structures that produced it
- **Interlocked translation** — human edits to generated text propagate semantic changes back into the graph
- **Self-extension** — proposes new primitives when existing structures can't represent an input
- **Lens system** — different views over the same graph (architecture, timeline, next steps)

---

## Core Architecture

```
┌─────────────────────────────────────────────────┐
│                  Human / Agent                    │
│         reads or edits Mumble Markdown            │
└──────────────────────┬──────────────────────────┘
                       │
              ┌────────▼────────┐
              │    Mumble       │  ← natural language
              │   (Markdown)    │
              └────────┬────────┘
                       │
           ┌───────────▼───────────┐
           │   Interlocked         │  ← bidirectional
           │   Translation         │     semantic translation
           └───────────┬───────────┘
                       │
              ┌────────▼────────┐
              │   WRAP Graph    │  ← persistent semantic state
              │  (nodes + edges │     with numeric forces
              │   + forces)     │
              └────────┬────────┘
                       │
           ┌───────────▼───────────┐
           │      DRAG             │  ← Dynamic RAG
           │  (subgraph selection  │     with semantic zoom
           │   + scoring)          │
           └───────────┬───────────┘
                       │
              ┌────────▼────────┐
              │  Mumble Output   │  ← generated with
              │  (with provenance)│     provenance metadata
              └─────────────────┘
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop

# Run the demo
python3 demo.py

# Run tests (9/9 passing)
python3 mumblewrap/tests/test_core_loop.py
```

### Example: Ingest → Query → Edit → Update

```python
from wrap.api import SpecuLoop

loop = SpecuLoop("my_knowledge.json")

# Ingest knowledge
loop.ingest("Speed and quality are in tension.")
loop.ingest("Good tooling improves quality.")

# Query the graph (DRAG selects relevant subgraph)
result = loop.query("What affects quality?")
print(result.markdown)
# → "Speed opposes quality."
# → "Good tooling increases quality."

# Human edits the output
loop.edit(result.markdown, "Speed opposes quality, but good tooling reduces this tension.")
# → WRAP graph updated with new concepts and relationships

# Propose new primitives for unrecognized concepts
proposal = loop.propose("creativity")
loop.confirm_proposal(proposal)
```

---

## Key Concepts

### WRAP (Persistent Semantic State)
The authoritative knowledge store. A graph of nodes (concepts, actions, entities) and edges (relationships with numeric forces). All other representations are materialized views.

### Mumble ↔ WRAP Translation
Bidirectional mapping between human-readable text and structured semantic state. Supports:
- **Ingestion**: plain text → graph structures (decomposition)
- **Emission**: graph → natural language with provenance metadata
- **Feedback propagation**: human edits → semantic graph updates

### DRAG (Dynamic RAG)
Unlike static RAG, DRAG dynamically selects and compresses knowledge:
- **Subgraph selection**: score nodes by relevance to a query
- **Semantic zoom**: compress highly-related structures at different abstraction levels
- **Replaceable scoring**: start with text match, upgrade to embeddings or GNNs

### Interlocked Translation
Generated Markdown retains provenance to the WRAP nodes and edges that produced each sentence. When a human edits the text, the system determines which underlying semantic structures the edit refers to and propagates the change back.

### Self-Extension
When input cannot be decomposed into existing structures, the system proposes new primitives for human confirmation. The graph grows organically.

### Lenses
Different views over the same graph. A lens modifies edge weights and node relevance:
- `architecture` — emphasizes system structure
- `timeline` — emphasizes temporal relationships
- `next-steps` — emphasizes action/dependency chains

---

## Architecture

```
mumblewrap/
├── api.py                  # SpecuLoop — main interface
├── core/
│   ├── node.py             # Node (concept, action, entity, property, state, constraint)
│   ├── edge.py             # Edge with relation forces (causes, increases, opposes, etc.)
│   ├── graph.py            # Graph with persistence (JSON)
│   └── lens.py             # Lens (weight modifiers)
├── translation/
│   ├── translator.py       # Orchestrates Mumble ↔ WRAP
│   ├── decomposer.py       # Text → graph structures (replaceable)
│   └── composer.py         # Graph → Mumble Markdown (replaceable)
├── drag/
│   ├── selector.py         # Subgraph selection (replaceable)
│   └── scorer.py           # Node/edge scoring (replaceable)
├── extension/
│   └── self_extender.py    # New primitive proposals
├── feedback/
│   └── propagator.py       # Edit feedback → WRAP update
├── persistence/
│   └── store.py            # JSON graph persistence
└── tests/
    └── test_core_loop.py   # 9 end-to-end tests
```

---

## Specifications

| Document | Description |
|---|---|
| [WRAP_CORE_SPEC.md](WRAP_CORE_SPEC.md) | Node, Edge, Graph, Primitive data model |
| [INTERLOCKED_TRANSLATION.md](INTERLOCKED_TRANSLATION.md) | Mumble ↔ WRAP translation design |
| [DRAG_CORE.md](DRAG_CORE.md) | Graph selection/scoring algorithm |
| [SELF_EXTENSION.md](SELF_EXTENSION.md) | New primitive proposal mechanism |
| [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) | Current status and known limitations |

---

## Design Principles

1. **Every component is replaceable** — pattern matching → LLM, text overlap → embeddings, JSON → graph DB
2. **Hypotheses are labeled** — confidence levels (FOUNDATIONAL / HIGH / MEDIUM / HYPOTHESIS / UNKNOWN) prevent false certainty
3. **Semantic reversibility** — meaning ↔ representation, not characters ↔ characters
4. **Reality pushes back** — failures and constraints become semantic information
5. **Self-improvement** — the system proposes, tests, and extends its own structures

---

## Roadmap

- [ ] LLM-based decomposition (replace pattern matching)
- [ ] Embedding-based scoring (replace text overlap)
- [ ] Graph visualization (interactive + static)
- [ ] Obsidian vault integration (bidirectional sync)
- [ ] Backprop integration (execution feedback → graph weights)
- [ ] Semantic zoom compression in emit
- [ ] Multi-agent concurrent access
- [ ] Self-improvement loop (system proposes its own improvements)

---

## License

MIT

---

## Keywords

semantic memory, persistent memory, AI agent memory, knowledge graph, semantic graph, dynamic RAG, retrieval augmented generation, graph-based RAG, semantic zoom, provenance tracking, bidirectional translation, natural language to graph, graph to natural language, interlocked translation, agent context management, semantic knowledge representation, WRAP, SpecuLoop, Mumble, DRAG, self-extending knowledge graph, AI agent memory system, persistent semantic state
