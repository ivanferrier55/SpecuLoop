# SpecuLoop — WRAP Semantic Engine

**Status**: Phase 1 — Core kernel implemented and tested
**Date**: 2026-08-25

---

## What Is This?

WRAP is persistent semantic state. It's a graph-based knowledge representation that sits between human-readable text (Mumble) and structured knowledge, enabling bidirectional translation.

This is a reconstruction of a lost system, built from memory fragments and design hypotheses.

## Quick Start

```bash
# Run the demo
python3 demo.py

# Run tests
python3 wrap/tests/test_core_loop.py
```

## Core Concept

```
Mumble input (plain text)
    ↓ decompose
WRAP graph (nodes + edges + forces)
    ↓ select (DRAG)
Subgraph (relevant portion)
    ↓ compose
Mumble Markdown (with provenance)
    ↓ human edit
WRAP update (propagate changes back)
```

## Architecture

Every component is replaceable. The initial implementation uses:
- **Pattern matching** for decomposition (replace with LLM)
- **Text overlap** for scoring (replace with embeddings)
- **Template-based** generation (replace with LLM)
- **JSON** for persistence (replace with SQLite/graph DB)

## Key Files

- `wrap/api.py` — Main interface (`SpecuLoop` class)
- `wrap/core/` — Node, Edge, Graph, Lens
- `wrap/translation/` — Mumble ↔ WRAP translation
- `wrap/drag/` — Subgraph selection and scoring
- `wrap/extension/` — Self-extension proposals
- `wrap/feedback/` — Edit propagation

## Specifications

- `WRAP_CORE_SPEC.md` — Data model
- `INTERLOCKED_TRANSLATION.md` — Translation design
- `DRAG_CORE.md` — Selection/scoring design
- `SELF_EXTENSION.md` — Self-extension design
- `RECONSTRUCTION_STATUS.md` — Current status and next steps
