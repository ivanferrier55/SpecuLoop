# DRAG: Dynamic RAG / Semantic Reasoning Layer

DRAG dynamically retrieves, compresses, visualizes, and reasons over mumbleWRAP's semantic structures.

---

## Purpose

DRAG provides the infrastructure for selecting, weighting, composing, and compressing semantic structures according to the active lens and context. It is the reasoning and retrieval layer that sits on top of mumbleWRAP.

---

## What DRAG Does

- **Dynamic retrieval**: select relevant subgraphs for queries
- **Semantic zoom**: compress or expand granularity lens-dependently
- **Semantic lenses**: different views over the same graph
- **Graph-based reasoning**: traverse and score semantic structures
- **Numerical force calculations**: attraction and repulsion between concepts
- **Visual reasoning**: graph viewer for humans and LLMs
- **Mathematical reasoning**: force-based relationship modeling

---

## Components

| Component | Purpose |
|---|---|
| `selector.py` | Subgraph selection with propagation |
| `scorer.py` | Node/edge relevance scoring (replaceable) |
| `retrieval/` | Retrieval strategies (planned) |
| `lenses/` | Lens definitions and management (planned) |
| `zoom/` | Semantic zoom compression (planned) |
| `forces/` | Force calculation engine (planned) |
| `viewer/` | Graph visualization (planned) |

---

## Semantic Zoom Is Lens-Dependent

Different lenses produce different compressed views:

| Lens | Compression Strategy |
|---|---|
| `implementation` | Merge by code dependencies |
| `architecture` | Merge by system components |
| `time` | Merge by temporal relationships |
| `next-steps` | Merge by action chains |
| `onboarding` | Merge by concept explanation |
| `causality` | Merge by cause-effect paths |

---

## The Graph Is a Reasoning Space

The graph viewer is not merely a visualization. It is intended to provide a mathematical and visual reasoning space for both humans and LLMs.

Attraction and repulsion between concepts model semantic relationships:

- `problem ↔ solution`: oppositional forces separate them, intermediate concepts form paths
- `speed ↑ → quality ↓`: negative magnitude creates tradeoff structure
- `evidence → hypothesis`: positive directional pull

---

## Status

Scoring and selection implemented. Zoom, lenses, forces, and viewer planned.

**Related**: [mumbleWRAP](../mumblewrap/README.md), [SpecuLoop](../speculoop/README.md), [ARCHITECTURE.md](../ARCHITECTURE.md)
