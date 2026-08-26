# SpecuLoop — Grounded Semantic Reasoning for AI Agents

**An experimental semantic system for letting AI generate, test, and refine knowledge without letting generated volume become semantic authority.**

SpecuLoop explores a different approach to AI memory and reasoning: instead of treating memory as an undifferentiated collection of information, it represents knowledge as reusable semantic structures and tests whether those structures remain useful against new evidence.

> **Core idea:** AI can generate knowledge faster than it can be grounded. Generation explores; grounding constrains; the semantic basis records what currently survives.

### At a glance

```text
SpecuLoop
    ├── Grounding: objectives, observations, experiments, tools, evidence
    ├── mumbleWRAP: persistent semantic state / primitive basis
    ├── DRAG: lens-dependent retrieval, forces, and semantic zoom
    └── SpecuLoop: agents, tests, tools, feedback, and execution
```

### Explore

- [Grounded Semantic Reasoning](GROUNDING.md)
- [Quick Start](#quick-start)
- [Core Research Question](#the-core-research-question)
- [Semantic Compression](#why-semantic-compression)
- [Evidence and Self-Refactoring](#evidence-and-self-refactoring)
- [Architecture](ARCHITECTURE.md)
- [Semantic Solve](SEMANTIC_SOLVE.md)
- [Reconstruction Status](RECONSTRUCTION_STATUS.md)
- [Glossary](GLOSSARY.md)

---

## What Makes SpecuLoop Different?

Many AI systems can generate enormous amounts of information. SpecuLoop investigates what happens when generated information must remain distinguishable from the evidence that grounds the system's semantic representation.

```text
Generation
    propose → explain → plan → hypothesize

Grounding
    observe → test → measure → execute → constrain

Semantic basis
    represent → reconstruct → evaluate → refactor
```

The goal is not to slow AI generation or make humans approve every generation. A fully autonomous research system is compatible with this architecture: the AI can generate hypotheses and design experiments while the experiment provides the grounding signal.

The current reconstruction records primitive reuse, unresolved evidence, uncertainty, provenance, and the tests that support changes to the semantic basis. This is an experimental direction, not a claim that the system is already a fully autonomous grounded reasoning system.

---

## The Core Research Question

> **Can an AI generate and accumulate knowledge at machine speed while keeping its semantic representation grounded in objectives, observations, experiments, and other evidence?**

A related hypothesis is that **semantic inertia** emerges when generated information becomes recursively influential simply because it has accumulated or is easy to retrieve. Separating candidate generation from evidence-based basis updates may reduce this effect.

The current reconstruction treats incoming information as a clue and attempts to express it using existing primitives. If that representation is inadequate, the mismatch becomes uncertainty that can drive human questions, agent-generated hypotheses, tool execution, decoder tests, experiments, and candidate primitive discovery.

This is broader than AI memory. Memory is the persistent substrate; the research target is a grounded semantic representation that can improve its ability to represent, retrieve, test, and translate information.

---

## The Core Loop

```text
                 OBJECTIVE / QUESTION
                         │
                         ▼
                  SEMANTIC BASIS
                         │
                         ▼
                    AI GENERATION
                         │
              hypotheses / plans / candidates
                         │
                         ▼
                    TEST / EXECUTE
                         │
                         ▼
                 OBSERVATION / EVIDENCE
                         │
                         ▼
                  BASIS EVALUATION
                    ┌────┴────┐
                    ▼         ▼
                 adequate  inadequate
                    │         │
                    ▼         ▼
              retain/update  investigate
                              │
                              ▼
                        basis refactor
                              │
                              └──────→ next cycle
```

The system is intended to improve its **representation without allowing generation volume to become semantic authority**.

See [Grounded Semantic Reasoning](GROUNDING.md) and [Semantic Solve](SEMANTIC_SOLVE.md).

---

## Why Semantic Compression?

Ordinary retrieval asks:

> Which documents should I retrieve?

SpecuLoop explores a different question:

> **What reusable semantic basis allows the relevant information to be represented and reconstructed without repeatedly carrying every underlying document?**

The system records primitive reuse, unresolved evidence, uncertainty, and the tests that justify changes to the basis. A good compression is therefore not just a short summary: it should preserve enough structure for the intended decoder, task, and lens to recover useful meaning.

### Decoder-aware representation

Different AI systems may require different amounts of explicit information to reconstruct the same semantic structure:

```text
R* = f(semantic structure, decoder capability, lens, task)
```

This is a design hypothesis, not a recovered historical equation. The kernel exposes an optional decoder callback so the hypothesis can be tested without committing to a particular LLM provider.

---

## Evidence and Self-Refactoring

Semantic changes are not supposed to become unexplained permanent facts. The system records evidence associated with compression decisions:

```text
clue
primitive hypothesis
test / prediction
observed result
compression score
uncertainty
lens / task / decoder
basis decision
```

A candidate primitive can be evaluated against an existing basis before it is accepted. When a candidate materially improves the explanatory score, the old primitives can be marked **superseded** rather than deleted. This preserves provenance and allows later evidence to revisit the decision.

That makes primitive discovery closer to an experimental/scientific loop than to ordinary automatic summarization.

---

## Preserving Meaning Across Translations

The broader system is designed around interlocked representations:

```text
objective / human intention
    ↕
Mumble
    ↕
WRAP semantic state
    ↕
code / tools / experiments
    ↕
observed reality
```

When information moves between representations, provenance should be retained so that a human edit, code change, tool failure, or execution result can propagate back to the semantic state rather than becoming a disconnected document.

---

## mumbleWRAP — Semantic State and Primitive Basis

mumbleWRAP is the persistent semantic substrate. The current memory-based expansion of WRAP is **Words Reconstructed As Primitives**; this remains a hypothesis about the original naming.

The reconstructed invariants are:

- reuse existing structures before creating new ones;
- record how often structures are reused;
- represent multiple relationship types, not only causality;
- support attraction/repulsion and numeric edge weights;
- preserve provenance between generated views and source nodes;
- allow provisional primitives and later refactoring;
- retain uncertainty when the current basis cannot explain evidence;
- treat examples as potential tests of semantic hypotheses, not automatically as causes.

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

The historical DRAG equations are deliberately **not** hard-coded as recovered fact.

---

## Existing-Solution Incorporation

A major application under investigation is using the same semantic basis to compare existing solutions rather than treating retrieved documents as isolated answers:

```text
problem
   ↓
semantic decomposition
   ↓
search existing solutions
   ↓
translate candidates into common semantic structure
   ↓
compare reusable primitives / contradictions / gaps
   ↓
reuse → combine → test
              │
              └──→ invent only when existing structure is insufficient
```

This allows the system to ask not only **"What exists?"**, but **"Which existing pieces already solve parts of this problem, how can they be combined, and what is genuinely missing?"**

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

# Contextual semantic solve
solve = loop.learn(
    "Semantic zoom should compress related information.",
    lens="onboarding",
    task="understand_system",
    decoder_name="my-model",
)
print(solve.compression.coverage)
print(solve.compression.uncertainty)
print(solve.evidence_id)

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
├── GROUNDING.md
├── GLOSSARY.md
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

The current implementation now has a concrete experimental center:

1. observe a clue;
2. score it against the existing basis;
3. record uncertainty and evidence;
4. propose a provisional primitive when necessary;
5. optionally test decoder reconstruction;
6. compare candidate bases against existing ones;
7. refactor without deleting provenance.

The original primitive vocabulary, exact WRAP syntax, historical DRAG equations, and remembered backpropagation behavior remain open reconstruction questions.

See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for the evidence and implementation status.

## License

MIT
