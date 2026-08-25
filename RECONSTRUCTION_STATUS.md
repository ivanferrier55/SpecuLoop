# Reconstruction Status

**Date**: 2026-08-25
**Phase**: 1 — Core Kernel Implemented

---

## 1. What Exists

- Python 3.12 + Node.js 22 environment
- Clean workspace (rebuilt from scratch)

## 2. What Is Missing

- The original WRAP implementation (lost)
- The original syntax/format (unknown)
- Original algorithms (especially backprop scoring)
- Original node/edge type definitions
- Original persistence mechanism
- Any test cases or examples from the original system
- The Obsidian vault that motivated the system

## 3. Assumptions Being Made

| Assumption | Confidence | Basis |
|---|---|---|
| WRAP is a graph of nodes and edges | FOUNDATIONAL | Core design principle |
| Edges have numeric weights/forces | MEMORY | Remembered from original |
| Multiple relationship types exist | MEMORY | Remembered from original |
| Lenses modify edge importance | MEDIUM_CONFIDENCE | Concept remembered, details unknown |
| Backprop adjusts edge weights | HYPOTHESIS | "Backprop" word remembered, mechanism unknown |
| Nodes have a concept/primitive distinction | HYPOTHESIS | Logical requirement, not directly remembered |
| Semantic zoom compresses via graph structure | MEMORY | Concept remembered |
| Provenance tracks WRAP→Mumble mapping | HIGH_CONFIDENCE | Core requirement |

## 4. Implemented Kernel

### File Structure

```
SpecuLoop/
├── RECONSTRUCTION_STATUS.md    # This file
├── WRAP_CORE_SPEC.md           # Node, Edge, Graph, Primitive specification
├── INTERLOCKED_TRANSLATION.md  # Mumble ↔ WRAP translation spec
├── DRAG_CORE.md                # Graph selection/scoring spec
├── SELF_EXTENSION.md           # New primitive proposal spec
├── demo.py                     # Interactive demo
└── wrap/
    ├── __init__.py
    ├── api.py                  # SpecuLoop — main interface
    ├── core/
    │   ├── node.py             # Node dataclass
    │   ├── edge.py             # Edge dataclass + relation forces
    │   ├── graph.py            # Graph with persistence
    │   └── lens.py             # Lens dataclass
    ├── translation/
    │   ├── translator.py       # Orchestrates Mumble ↔ WRAP
    │   ├── decomposer.py       # Text → graph structures
    │   └── composer.py         # Graph → Mumble Markdown
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
        └── test_core_loop.py   # End-to-end test (9 tests, all passing)
```

### Component Status

| Component | Status | Notes |
|---|---|---|
| Node | ✅ Implemented | With kind, label, content, metadata, lenses |
| Edge | ✅ Implemented | With relation forces, weight, metadata |
| Graph | ✅ Implemented | Add/remove/find, JSON persistence |
| Lens | ✅ Implemented | Weight modifiers for nodes/edges/kinds |
| Decomposer | ✅ Implemented | Pattern-matching (keyword/phrase → relation) |
| Composer | ✅ Implemented | Template-based Mumble Markdown generation |
| Translator | ✅ Implemented | Orchestrates ingest/emit |
| DRAG Selector | ✅ Implemented | Score-based with propagation |
| Scorer | ✅ Implemented | Text match + edge density + usage |
| Self-Extender | ✅ Implemented | Proposes new primitives |
| Feedback | ✅ Implemented | Provenance-based edit propagation |
| Persistence | ✅ Implemented | JSON save/load |

## 5. Verified Vertical Slice

The following loop demonstrably works:

```
"Speed and quality are in tension."
    ↓ ingest
WRAP: Speed --[opposes]--> quality
    ↓ emit
"Speed opposes quality." (with provenance metadata)
    ↓ human edit
"Speed opposes quality, but good tooling reduces this tension."
    ↓ propagate
WRAP updated (new concepts detected, edges adjusted)
```

### Test Results

```
✓ test_node_creation
✓ test_edge_creation
✓ test_graph_persistence
✓ test_ingest_simple
✓ test_emit_markdown
✓ test_full_vertical_slice
✓ test_drag_query
✓ test_self_extension
✓ test_lens
9/9 passed
```

## 6. Known Limitations

1. **Decomposer is pattern-based** — only handles known verb/phrase patterns. Needs LLM integration for arbitrary text.
2. **Edit propagation is heuristic** — uses keyword matching, not semantic understanding.
3. **DRAG scoring is simple** — text overlap + edge density. Needs embedding-based scoring.
4. **No backprop yet** — `process_feedback` exists but isn't wired into the main loop.
5. **Duplicate sentences in DRAG output** — propagation can emit the same edge multiple times (needs deduplication).
6. **No semantic zoom compression** — `compress()` exists but isn't integrated into emit.
7. **No visual/graph output** — only text-based Markdown.

## 7. Next Steps

1. **LLM integration for decomposer** — replace pattern matching with semantic understanding
2. **Embedding-based scoring** — replace text overlap with vector similarity
3. **Backprop integration** — wire `process_feedback` into the main loop
4. **Semantic zoom in emit** — use `compress()` to control detail level
5. **Graph visualization** — export to dot/graphviz or interactive format
6. **Obsidian integration** — bidirectional sync with vault files
7. **Multi-agent support** — concurrent graph access with locking
8. **Self-improvement loop** — system proposes and tests its own improvements
