# Reconstruction Status

**Date**: 2026-08-26
**Phase**: 2 — Semantic Solve Kernel

---

## 1. What Exists

- Python 3.12 + Node.js 22 environment
- Persistent WRAP graph with nodes, typed relations, numeric forces, lenses, provenance, and JSON persistence
- Mumble ↔ WRAP translation vertical slice
- DRAG selection/scoring kernel
- Provisional self-extension and edit-feedback propagation
- New model-agnostic semantic compression/self-update kernel

## 2. What Is Missing

- The original WRAP implementation (lost)
- The original syntax/format (unknown)
- Original algorithms (especially backprop scoring)
- Original node/edge type definitions
- Original persistence mechanism
- Any test cases or examples from the original system
- The Obsidian vault that motivated the system
- Historical LLM/decoder reconstruction mechanism

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
| Compression quality is decoder-dependent | HYPOTHESIS | Current reconstruction clue |
| Isolated primitives can be tested by LLM reconstruction | HYPOTHESIS | Current reconstruction clue, explicitly uncertain |
| Uncertainty should trigger experiments/questions | HIGH_CONFIDENCE | Repeated system behavior described |

## 4. Implemented Kernel

### File Structure

```
SpecuLoop/
├── RECONSTRUCTION_STATUS.md
├── SEMANTIC_SOLVE.md         # decoder-aware semantic compression loop
├── WRAP_CORE_SPEC.md
├── INTERLOCKED_TRANSLATION.md
├── DRAG_CORE.md
├── SELF_EXTENSION.md
├── demo.py
└── mumblewrap/
    ├── __init__.py
    ├── api.py
    ├── semantic.py            # clue compression + provisional basis testing
    ├── core/
    │   ├── node.py
    │   ├── edge.py
    │   ├── graph.py
    │   └── lens.py
    ├── translation/
    ├── drag/
    ├── extension/
    ├── feedback/
    ├── persistence/
    └── tests/
        ├── test_core_loop.py
        └── test_semantic_reconstruction.py
```

### Component Status

| Component | Status | Notes |
|---|---|---|
| Node | ✅ Implemented | With kind, label, content, metadata, lenses |
| Edge | ✅ Implemented | With relation forces, weight, metadata |
| Graph | ✅ Implemented | Add/remove/find, JSON persistence |
| Lens | ✅ Implemented | Weight modifiers for nodes/edges/kinds |
| Decomposer | ✅ Implemented | Pattern-matching baseline; replaceable by LLM/embedding decomposition |
| Composer | ✅ Implemented | Template-based Mumble Markdown generation |
| Translator | ✅ Implemented | Orchestrates Mumble/WRAP ingest and emit |
| DRAG Selector | ✅ Implemented | Score-based with propagation |
| Scorer | ✅ Implemented | Baseline text match + edge density + usage |
| Self-Extender | ✅ Implemented | Provisional primitive proposals |
| Feedback | ✅ Implemented | Provenance-based edit propagation |
| Persistence | ✅ Implemented | JSON save/load |
| Semantic Learner | 🆕 Implemented | Compression, uncertainty, provisional candidates, decoder callback |
| Basis scoring | 🆕 Implemented | Complexity + reconstruction-error baseline |

## 5. New Core Loop

```text
clue
  ↓
existing semantic basis
  ↓
compress / reconstruct
  ├─ adequate → reuse + strengthen
  └─ inadequate → uncertainty
                    ↓
              candidate primitive
                    ↓
             optional decoder test
                    ↓
             evidence for/refuting basis
                    ↓
              accept / revise / ask
                    ↺
```

The kernel deliberately does **not** auto-accept new primitives. This preserves uncertainty and allows human or agent validation.

## 6. Verified Semantic Slice

The new tests cover:

- existing primitive coverage;
- provisional primitive generation when compression is weak;
- accepting a candidate and reusing it on later clues;
- separating structural coverage from optional decoder reconstruction score.

The decoder interface is provider-neutral. An LLM can be connected later without changing the semantic kernel.

## 7. Known Limitations

1. **Decomposer is pattern-based** — only handles known verb/phrase patterns. Needs LLM integration for arbitrary text.
2. **Edit propagation is heuristic** — uses keyword matching, not semantic understanding.
3. **DRAG scoring is simple** — text overlap + edge density. Needs embedding-based scoring and the recovered force equations.
4. **Backprop is not recovered** — the word is remembered, but its mechanism is unknown.
5. **Semantic zoom is not yet a true lens-dependent graph coarsening algorithm.**
6. **Semantic learner uses lexical overlap as a baseline** — this is intentionally replaceable by embeddings or LLM reconstruction.
7. **Primitive replacement/refactoring is not automated yet.**
8. **Generated test cases and multi-agent experiments are not yet orchestrated.**
9. **No visual/graph output yet.**

## 8. Next Steps

1. Add an LLM adapter for decomposition and decoder reconstruction tests.
2. Replace lexical overlap with embedding/semantic similarity while retaining deterministic fallbacks.
3. Add explicit evidence/test/proposal records to persistent storage.
4. Implement basis search: compare existing primitives against candidate replacements.
5. Implement lens-dependent graph coarsening/semantic zoom.
6. Recover or derive a replaceable numerical DRAG force model.
7. Add generated test cases and agent experiment orchestration.
8. Wire reality/tool failures back into the same semantic evidence loop.
9. Add graph visualization.
10. Integrate Obsidian bidirectional sync when the vault becomes available.
