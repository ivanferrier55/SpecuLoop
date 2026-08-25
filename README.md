# mumbleWRAP

**Status**: Phase 1 — Core kernel implemented and tested
**Date**: 2026-08-25

---

## What Is This?

mumbleWRAP (WRAP) is persistent semantic state. It's a graph-based knowledge representation that sits between human-readable text (Mumble) and structured knowledge, enabling bidirectional translation.

This is a reconstruction of a lost system, built from memory fragments and design hypotheses.

## Quick Start

```bash
# Install dependencies (Termux)
pkg install git python

# Clone
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop

# Run tests
python mumblewrap/tests/test_core_loop.py

# Run demo
python demo.py
```

## Core Concept

```
Mumble input (plain text)
    ↓ decompose
mumbleWRAP graph (nodes + edges + forces)
    ↓ select (DRAG)
Subgraph (relevant portion)
    ↓ compose
Mumble Markdown (with provenance)
    ↓ human edit
mumbleWRAP update (propagate changes back)
```

## Architecture

Every component is replaceable. The initial implementation uses:
- **Pattern matching** for decomposition (replace with LLM)
- **Text overlap** for scoring (replace with embeddings)
- **Template-based** generation (replace with LLM)
- **JSON** for persistence (replace with SQLite/graph DB)

## Key Files

- `mumblewrap/api.py` — Main interface (`SpecuLoop` class)
- `mumblewrap/core/` — Node, Edge, Graph, Lens
- `mumblewrap/translation/` — Mumble ↔ mumbleWRAP translation
- `mumblewrap/drag/` — Subgraph selection and scoring
- `mumblewrap/extension/` — Self-extension proposals
- `mumblewrap/feedback/` — Edit propagation

## Specifications

- `WRAP_CORE_SPEC.md` — Data model
- `INTERLOCKED_TRANSLATION.md` — Translation design
- `DRAG_CORE.md` — Selection/scoring design
- `SELF_EXTENSION.md` — Self-extension design
- `RECONSTRUCTION_STATUS.md` — Current status and next steps
