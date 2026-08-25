# AI Agent Instructions

This file helps AI coding agents understand the mumbleWRAP repository.

---

## What Problem Does This Project Solve?

Semantic drift across translations. When information moves between human language, semantic structures, code, and execution, meaning drifts at each translation step. mumbleWRAP preserves meaning through interlocked translations — bidirectional links between representations that allow changes to propagate.

**Key problems**: semantic drift, meaning loss, disconnected representations, feedback that doesn't propagate.

---

## What Is the Architecture?

```
Human language (Mumble)
    ↕ interlocked translation
mumbleWRAP (persistent semantic structures)
    ↕ interlocked translation
Code / implementations
    ↕ interlocked translation
Execution / tools / observed behavior
```

Each layer retains provenance to the layer that produced it. Changes in any layer propagate through the chain.

**Detailed architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## What Are the Important Concepts?

| Concept | Conventional Term | Role |
|---|---|---|
| [mumbleWRAP](docs/architecture/wrap.md) | persistent semantic memory | Semantic substrate |
| [Interlocked Translation](docs/concepts/interlocked-translation.md) | bidirectional programming | Central mechanism |
| [DRAG](docs/architecture/drag.md) | adaptive retrieval | Selection/compression |
| [Semantic Zoom](docs/concepts/semantic-zoom.md) | graph coarsening | Granularity control |
| [Semantic Lenses](docs/concepts/semantic-lenses.md) | multi-view retrieval | View-dependent weighting |
| [Semantic Forces](docs/concepts/semantic-forces.md) | edge weights | Relationship strength |
| [Semantic Feedback](docs/concepts/semantic-feedback.md) | human-in-the-loop learning | Correction propagation |
| [Provenance](docs/concepts/provenance-tracking.md) | attribution | Translation linking |

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
| Execution grounding | LOW | Designed; not wired into main loop |

---

## What Research Areas Are Related?

- [Bidirectional programming](RELATED_WORK.md#bidirectional-programming--program-synthesis) — source-target synchronization
- [GraphRAG](RELATED_WORK.md#graphrag) — graph-based retrieval
- [Agent Memory](RELATED_WORK.md#agent-memory) — persistent LLM memory
- [Human-in-the-Loop](RELATED_WORK.md#human-in-the-loop-learning) — interactive learning
- [Knowledge Graphs](RELATED_WORK.md#knowledge-graphs) — structured knowledge

**Full research crosswalk**: [RESEARCH_CROSSWALK.md](RESEARCH_CROSSWALK.md)

---

## How to Run

```bash
python3 demo.py                        # Interactive demo
python3 wrap/tests/test_core_loop.py   # Run 9 end-to-end tests
```
