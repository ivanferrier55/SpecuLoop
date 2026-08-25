# SpecuLoop

**Three layers. One repository. Shared semantic model.**

```text
SpecuLoop
    ├── mumbleWRAP: persistent semantic state
    ├── DRAG: dynamic retrieval / semantic reasoning
    └── SpecuLoop: agents, feedback, tools, and self-update
```

---

## The Primary Problem: Semantic Solving

**Semantic solving** is the central problem SpecuLoop is exploring:

> How can an AI solve problems while preserving and evolving the meaning, relationships, context, provenance, uncertainty, and lessons that make its reasoning useful across time and transformations?

The current reconstruction treats every incoming statement as a **clue**. The system attempts to compress that clue into existing semantic primitives. When it cannot, the failure becomes uncertainty that can drive questions, experiments, and primitive discovery.

This is intentionally broader than AI memory. Memory is one substrate for solving the problem; the objective is meaningful semantic continuity and better problem solving.

---

## The Goal: Preserve Meaning Across Translations

> **Preservation and propagation of meaning across translations.**

When information moves between human language, semantic structures, code, and execution, the system should preserve semantic intent. Changes and observations should propagate bidirectionally.

```text
human intention
    ↕
mumble
    ↕
WRAP semantic state
    ↕
code / tools
    ↕
observed reality
```

Each translation retains provenance so corrections can propagate rather than becoming disconnected documents.

---

## mumbleWRAP — Semantic State and Compression

mumbleWRAP is the persistent semantic substrate. The current memory-based expansion of WRAP is **Words Reconstructed As Primitives**; this remains a hypothesis about the original naming.

The important reconstructed invariant is:

```text
clue → existing primitives → compressed representation
                         ↓
                     uncertainty
                         ↓
                 new evidence/tests
                         ↓
                 new or revised basis
```

Key properties:

- reuse existing structures before creating new ones;
- record how often structures are reused;
- represent multiple relationship types, not only causality;
- support attraction/repulsion and numeric edge weights;
- preserve provenance between generated views and source nodes;
- allow provisional primitives and later refactoring;
- retain uncertainty when the current basis cannot explain evidence.

See [WRAP Core](WRAP_CORE_SPEC.md) and [Semantic Solve](SEMANTIC_SOLVE.md).

---

## DRAG — Dynamic RAG / Semantic Reasoning

DRAG is the retrieval and numerical reasoning layer. The reconstructed design includes:

- dynamic subgraph selection;
- semantic zoom;
- task/lens-dependent projections;
- numerical attraction/repulsion;
- graph-based reasoning;
- propagation/backpropagation as an unresolved historical hypothesis.

Semantic zoom is not assumed to be a simple hide/show threshold. The same graph may compress differently depending on the question, lens, scope, and decoder capability.

See [DRAG Core](DRAG_CORE.md) and `docs/concepts/`.

---

## Semantic Compression Is Decoder-Aware

Different AI systems may need different amounts of explicit information to encode or decode the same semantic structure.

A useful reconstruction abstraction is:

```text
R* = f(semantic structure, decoder capability, lens, task)
```

A candidate primitive can therefore be isolated and given to a decoder to see whether the decoder can reconstruct the clue set that already exists. This tests whether the primitive captures useful predictive structure rather than merely providing a short label.

The current kernel exposes an optional decoder callback and a deterministic lexical baseline. An LLM adapter can be added without changing the semantic data model.

---

## Self-Update Loop

```text
             NEW CLUE
                 │
                 ▼
        TRY EXISTING BASIS
                 │
          ┌──────┴──────┐
          ▼             ▼
      adequate      inadequate
          │             │
          ▼             ▼
    reuse/strengthen  uncertainty
                        │
                ┌───────┼────────┐
                ▼       ▼        ▼
              human   agents    tools
                │       │        │
                └───────┼────────┘
                        ▼
                  test examples
                        ▼
                 candidate bases
                        ▼
               decoder reconstruction
                        ▼
              minimum sufficient basis
                        │
                 ┌──────┴──────┐
                 ▼             ▼
              extend        refactor
                 └──────┬──────┘
                        ▼
                    persistent
                    semantic state
                        ↺
```

The system is intended to improve its **representation**, not merely accumulate more nodes.

---

## Quick Start

```bash
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop
python3 demo.py
python3 mumblewrap/tests/test_core_loop.py
python3 mumblewrap/tests/test_semantic_reconstruction.py
```

### Example

```python
from mumblewrap.api import SpecuLoop

loop = SpecuLoop("knowledge.json")

# Existing vertical slice
loop.ingest("Speed and quality are in tension.")
result = loop.query("What affects quality?")

# Semantic solve
solve = loop.learn("Semantic zoom should compress related information.")
print(solve.compression.coverage)
print(solve.compression.uncertainty)

# Optional decoder/LLM adapter
solve = loop.learn(
    "Semantic zoom should compress related information.",
    decoder=lambda compact: compact,
)
```

---

## Repository Structure

```text
SpecuLoop/
├── README.md
├── ARCHITECTURE.md
├── RECONSTRUCTION_STATUS.md
├── SEMANTIC_SOLVE.md
├── WRAP_CORE_SPEC.md
├── SELF_EXTENSION.md
├── mumblewrap/
│   ├── api.py
│   ├── semantic.py
│   ├── core/
│   ├── translation/
│   ├── persistence/
│   └── tests/
├── drag/
├── speculoop/
└── docs/
```

---

## Status

This is an experimental reconstruction of a lost system. Historical facts, strong recollections, and current implementation hypotheses are deliberately separated. The goal is to find the **smallest core that can rebuild the rest**.

See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for the current evidence and implementation status.

## License

MIT
