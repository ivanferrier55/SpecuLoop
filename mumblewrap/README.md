# mumbleWRAP: Semantic Inertia Layer

mumbleWRAP is the persistent semantic substrate that increases semantic inertia by preserving, connecting, and accumulating meaning across incoming inputs and translations.

---

## Purpose

mumbleWRAP tracks incoming semantic inputs, decomposes new inputs into existing structures, records reuse, creates translation relationships, preserves provenance, identifies confusion, and allows the system to grow its semantic vocabulary.

---

## What mumbleWRAP Does

- **Tracks** incoming semantic inputs
- **Decomposes** new inputs into existing nodes when possible
- **Records** reuse of existing nodes
- **Creates** translation relationships
- **Supports** bidirectional translation
- **Preserves** provenance
- **Identifies** confusion and contradictions
- **Strengthens** semantic structures that repeatedly explain inputs
- **Allows** new primitives when existing structures are insufficient

---

## What mumbleWRAP Is NOT

- Not a RAG system (that's DRAG)
- Not a visualization system
- Not a token optimization system

Those may be implementation aspects, but semantic inertia is the primary purpose.

---

## Components

| Component | Purpose |
|---|---|
| `core/` | Node, Edge, Graph, Lens — the semantic data model |
| `translation/` | Mumble ↔ mumbleWRAP bidirectional translation |
| `persistence/` | JSON graph persistence |
| `inertia/` | Semantic inertia tracking (planned) |
| `primitives/` | Primitive management (planned) |
| `provenance/` | Provenance tracking (planned) |

---

## Key Concepts

- **Nodes**: concepts, actions, entities, properties, constraints
- **Edges**: typed relationships with numeric forces
- **Lenses**: weight modifiers for different views
- **Primitives**: atomic, non-decomposable semantic units
- **Reuse tracking**: frequency-based importance signals

---

## Status

Core graph model and translation implemented. Inertia tracking and provenance modules planned.

**Related**: [ARCHITECTURE.md](../ARCHITECTURE.md), [DRAG](../drag/README.md), [SpecuLoop](../speculoop/README.md)
