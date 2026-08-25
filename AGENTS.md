# AI Agent Instructions

This repository contains SpecuLoop — a self-updating reasoning environment built on two layers: mumbleWRAP (semantic inertia) and DRAG (dynamic RAG / semantic reasoning).

---

## What Problem Does This Project Solve?

Semantic drift across translations. When information moves between human language, semantic structures, code, and execution, meaning drifts at each step. SpecuLoop preserves meaning through interlocked translations.

---

## Architecture: Three Layers

```
Human / Agent Swarm
    ↕
SpecuLoop (orchestration + feedback)
    ↕
DRAG (reasoning + retrieval)
    ↕
mumbleWRAP (semantic inertia)
    ↕
Translations / Implementations / Tools
    ↕
Observed Reality
```

| Layer | Directory | Purpose |
|---|---|---|
| mumbleWRAP | `mumblewrap/` | Persistent semantic substrate |
| DRAG | `drag/` | Retrieval, lenses, zoom, forces |
| SpecuLoop | `speculoop/` | Orchestration, feedback, agents |

---

## Where to Look

| What | File |
|---|---|
| Main interface | `mumblewrap/api.py` — `SpecuLoop` class |
| Graph model | `mumblewrap/core/graph.py` |
| Node | `mumblewrap/core/node.py` |
| Edge with forces | `mumblewrap/core/edge.py` |
| Lens | `mumblewrap/core/lens.py` |
| Text → graph | `mumblewrap/translation/decomposer.py` |
| Graph → text | `mumblewrap/translation/composer.py` |
| Subgraph selection | `drag/selector.py` |
| Scoring | `drag/scorer.py` |
| Self-extension | `speculoop/self_extender.py` |
| Edit propagation | `speculoop/propagator.py` |
| Persistence | `mumblewrap/persistence/store.py` |
| Tests | `tests/test_core_loop.py` |
| Demo | `demo.py` |

---

## Key Concepts

- **mumbleWRAP**: persistent semantic substrate (semantic inertia)
- **DRAG**: dynamic retrieval and semantic reasoning
- **Interlocked translation**: bidirectional links between representations
- **Semantic zoom**: lens-dependent graph compression
- **Semantic forces**: numeric edge weights (attraction/repulsion)
- **Provenance**: trace from output to source structures

---

## What Is Hypothesis?

| Topic | Confidence |
|---|---|
| Edge force model | HYPOTHESIS |
| Lens propagation | MEDIUM |
| Pattern decomposition | MEDIUM |
| Text overlap scoring | LOW |
| Edit propagation | MEDIUM |
| Execution grounding | LOW |
