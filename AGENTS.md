# AI Agent Instructions

This file helps AI coding agents understand the SpecuLoop repository.

---

## Project Purpose

SpecuLoop implements WRAP — a persistent semantic state engine for AI agents. It provides:

- A semantic knowledge graph (nodes + edges + numeric forces)
- Bidirectional translation between natural language and graph structures
- Dynamic RAG with semantic zoom and lens-dependent retrieval
- Human-in-the-loop feedback propagation
- Self-extending knowledge structures

---

## Architecture

```
Mumble ←→ WRAP ←→ DRAG ←→ Materialized Views
             ↕
         Lenses
             ↕
    Tools / Code / Reality
```

- **Mumble**: natural language (input/output)
- **WRAP**: persistent semantic graph (authoritative store)
- **DRAG**: dynamic RAG — selects and compresses subgraphs
- **Lenses**: weight modifiers that change graph emphasis
- **Materialized Views**: Markdown with provenance metadata

---

## Important Files

| File | Purpose |
|---|---|
| `wrap/api.py` | Main interface — `SpecuLoop` class |
| `wrap/core/graph.py` | Graph with add/remove/find/persist |
| `wrap/core/node.py` | Node dataclass |
| `wrap/core/edge.py` | Edge with relation forces |
| `wrap/core/lens.py` | Lens weight modifiers |
| `wrap/translation/decomposer.py` | Text → graph (pattern-based, replaceable) |
| `wrap/translation/composer.py` | Graph → text with provenance |
| `wrap/drag/selector.py` | Subgraph selection |
| `wrap/drag/scorer.py` | Node/edge scoring (replaceable) |
| `wrap/extension/self_extender.py` | New primitive proposals |
| `wrap/feedback/propagator.py` | Edit → graph update |
| `wrap/persistence/store.py` | JSON persistence |
| `wrap/tests/test_core_loop.py` | End-to-end tests (9 passing) |

---

## Terminology

- **WRAP**: persistent semantic state (the graph)
- **Mumble**: natural language representation
- **DRAG**: dynamic RAG (subgraph selection)
- **Semantic zoom**: graph coarsening via lenses
- **Semantic force**: numeric edge weight
- **Lens**: weight modifier for graph views
- **Provenance**: trace from output to source structures
- **Primitive**: atomic, non-decomposable node
- **Interlocked translation**: bidirectional natural language ↔ graph mapping

---

## How to Run

```bash
python3 demo.py                    # Run the demo
python3 wrap/tests/test_core_loop.py  # Run tests
```

---

## Current Hypotheses

1. Edge types map to numeric forces (causes, opposes, supports, etc.) — HYPOTHESIS
2. Lenses modify edge weights to produce different views — MEDIUM_CONFIDENCE
3. Pattern-based decomposition is a reasonable starting point — MEDIUM_CONFIDENCE
4. Text overlap scoring captures enough relevance for initial DRAG — LOW_CONFIDENCE

---

## Known Limitations

- Decomposer uses pattern matching, not LLM — needs upgrade for arbitrary text
- Scoring uses text overlap, not embeddings — needs vector similarity
- Edit propagation is heuristic — needs semantic understanding
- No backprop wired into main loop yet
- No graph visualization output
- No SQLite or graph DB persistence yet
