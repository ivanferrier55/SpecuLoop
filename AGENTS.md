# AI Agent Instructions

This file helps AI coding agents understand the SpecuLoop repository.

---

## What Problem Does This Project Solve?

AI agents working with large knowledge bases face context-window pressure, token waste, shallow retrieval, and disconnected specifications. SpecuLoop implements a persistent semantic knowledge graph that compresses knowledge through semantic zoom, retrieves through lens-dependent subgraph selection, and translates bidirectionally between natural language and semantic structures.

**Key problems addressed**:
- [Large context](docs/problems/large-context.md)
- [Token waste](docs/problems/token-waste.md)
- [Shallow retrieval](docs/concepts/dynamic-rag.md)
- [Semantic relationships](docs/concepts/semantic-forces.md)
- [Multiple perspectives](docs/concepts/semantic-lenses.md)
- [Provenance](docs/concepts/interlocked-translation.md)
- [Code-language disconnect](docs/concepts/interlocked-translation.md)
- [Agent misunderstanding](docs/problems/agent-misunderstanding.md)

---

## What Is the Architecture?

```
Natural language (Mumble)
    ↕ decompose / compose
Semantic graph (WRAP) — persistent, authoritative
    ↕ DRAG select / score
Relevant subgraph — lens-dependent
    ↕ compose
Materialized views (Markdown with provenance)
    ↕ human edit
Updated graph — interlocked translation
    ↕ tools / code
Reality — execution feedback becomes constraints
```

**Detailed architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## What Are the Important Concepts?

| Concept | Conventional Term | Status |
|---|---|---|
| [WRAP](docs/architecture/wrap.md) | persistent semantic memory | implemented |
| [DRAG](docs/architecture/drag.md) | dynamic adaptive RAG | implemented |
| [Semantic Zoom](docs/concepts/semantic-zoom.md) | graph coarsening, multiscale retrieval | mechanism exists |
| [Semantic Lenses](docs/concepts/semantic-lenses.md) | multi-view retrieval | implemented |
| [Semantic Forces](docs/concepts/semantic-forces.md) | edge weights, attraction-repulsion | implemented |
| [Interlocked Translation](docs/concepts/interlocked-translation.md) | bidirectional programming | partial |
| [Semantic Feedback](docs/concepts/semantic-feedback.md) | human-in-the-loop learning | partial |
| [Persistent Memory](docs/concepts/persistent-semantic-memory.md) | agent memory | implemented |

**Full terminology map**: [docs/concepts/TERMINOLOGY_MAP.md](docs/concepts/TERMINOLOGY_MAP.md)

---

## Where Should I Look for Implementation?

| What | File |
|---|---|
| Main interface | `wrap/api.py` — `SpecuLoop` class |
| Graph model | `wrap/core/graph.py` |
| Node | `wrap/core/node.py` |
| Edge with forces | `wrap/core/edge.py` |
| Lens | `wrap/core/lens.py` |
| Text → graph | `wrap/translation/decomposer.py` |
| Graph → text | `wrap/translation/composer.py` |
| Subgraph selection | `wrap/drag/selector.py` |
| Scoring | `wrap/drag/scorer.py` |
| New primitive proposals | `wrap/extension/self_extender.py` |
| Edit propagation | `wrap/feedback/propagator.py` |
| Persistence | `wrap/persistence/store.py` |
| Tests | `wrap/tests/test_core_loop.py` |
| Demo | `demo.py` |

---

## What Is Still Hypothesis?

| Topic | Confidence | Notes |
|---|---|---|
| Edge force model | HYPOTHESIS | Base forces implemented; formula is provisional |
| Lens propagation | MEDIUM | Weights work; full propagation untested |
| Pattern decomposition | MEDIUM | Works for known patterns; needs LLM upgrade |
| Text overlap scoring | LOW | Starting point; needs embeddings |
| Edit propagation | MEDIUM | Heuristic; needs semantic understanding |
| Self-extension | MEDIUM | Basic proposals; needs evaluation |
| Backprop integration | HYPOTHESIS | Designed; not wired into main loop |

**Labeled hypotheses**: See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for confidence levels on all design decisions.

---

## What Research Areas Are Related?

- [GraphRAG](RELATED_WORK.md#graphrag) — graph-based retrieval
- [Agent Memory](RELATED_WORK.md#agent-memory) — persistent LLM memory
- [Knowledge Graphs](RELATED_WORK.md#knowledge-graphs) — structured knowledge
- [Graph Embeddings](RELATED_WORK.md#graph-embeddings) — vector representations of graphs
- [Graph Coarsening](RELATED_WORK.md#graph-coarsening--multiscale-graphs) — multiscale compression
- [Hierarchical Retrieval](RELATED_WORK.md#hierarchical-retrieval) — multi-level search
- [Causal Reasoning](RELATED_WORK.md#causal-reasoning) — cause-effect modeling
- [Human-in-the-Loop](RELATED_WORK.md#human-in-the-loop-learning) — interactive learning
- [Program Synthesis](RELATED_WORK.md#bidirectional-programming--program-synthesis) — code from specs

**Full research crosswalk**: [RESEARCH_CROSSWALK.md](RESEARCH_CROSSWALK.md)

---

## How to Run

```bash
python3 demo.py                        # Interactive demo
python3 wrap/tests/test_core_loop.py   # Run 9 end-to-end tests
```
