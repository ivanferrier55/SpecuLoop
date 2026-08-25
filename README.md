# SpecuLoop

**Three layers. One repository. Shared semantic model.**

```
SpecuLoop
    ├── mumbleWRAP: semantic inertia
    ├── DRAG: dynamic RAG / semantic reasoning
    └── SpecuLoop: complete self-updating reasoning environment
```

---

## The Problem: Semantic Drift Across Representations

A human describes an intention. An AI translates that into a semantic structure. That structure becomes code. The code executes. Reality produces an observation.

At each translation, meaning can drift:

```
human intention
    → AI interpretation     (drift)
    → semantic structure     (drift)
    → code                  (drift)
    → execution             (drift)
    → observation
```

Traditional systems lose the relationship between these representations. Corrections in one layer do not propagate to others.

**The core problem is semantic drift across translations.**

---

## The Goal: Preserve Meaning Across Translations

> **Preservation and propagation of meaning across translations.**

When information moves between human language, semantic structures, code, and execution, the system should preserve semantic intent. Changes and observations should propagate bidirectionally.

Success means:

- Meaning survives translation
- Changes propagate correctly
- Observations propagate backward
- Semantic drift is reduced
- Representations remain mutually consistent

---

## The Architecture: Three Layers

### mumbleWRAP — Semantic Inertia

The persistent semantic substrate. mumbleWRAP increases semantic inertia by preserving, connecting, and accumulating meaning across incoming inputs and translations.

- Tracks incoming semantic inputs
- Decomposes new inputs into existing structures
- Records reuse and strengthens repeated patterns
- Preserves provenance through all translations
- Identifies confusion and contradictions
- Allows new primitives when needed

**[mumbleWRAP docs](mumblewrap/README.md)** · [Core](mumblewrap/core/) · [Translation](mumblewrap/translation/) · [Persistence](mumblewrap/persistence/)

### DRAG — Dynamic RAG / Semantic Reasoning

The retrieval and reasoning layer. DRAG dynamically retrieves, compresses, and reasons over mumbleWRAP's semantic structures.

- Dynamic subgraph selection
- Semantic zoom (lens-dependent compression)
- Semantic lenses (different views over the same graph)
- Numerical force calculations (attraction/repulsion)
- Graph-based visual and mathematical reasoning

**[DRAG docs](drag/README.md)** · [Selector](drag/selector.py) · [Scorer](drag/scorer.py)

### SpecuLoop — Complete Reasoning Environment

The operational layer. SpecuLoop combines mumbleWRAP, DRAG, agent orchestration, human feedback, and execution into a continuous reasoning system.

- Agent orchestration and swarm coordination
- Human feedback propagation
- Self-extension (new primitive proposals)
- Execution grounding (failures become constraints)
- Persistent system state

**[SpecuLoop docs](speculoop/README.md)** · [Self-Extension](speculoop/self_extender.py) · [Feedback](speculoop/propagator.py)

---

## The Full Translation Chain

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

Each layer retains provenance to the layer that produced it. Changes in any layer propagate through the chain.

---

## Onboarding

New contributors and AI agents should start with [INTERACTION.md](INTERACTION.md) — it defines how the system responds to users and how corrections propagate as persistent knowledge.

Then read [AGENTS.md](AGENTS.md) for architecture, file locations, and current hypotheses.

---

## Quick Start

```bash
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop
python3 demo.py
python3 tests/test_core_loop.py
```

### Example

```python
from mumblewrap.api import SpecuLoop

loop = SpecuLoop("knowledge.json")

# Ingest: human language → mumbleWRAP
loop.ingest("Speed and quality are in tension.")

# Retrieve: mumbleWRAP → human language (via DRAG)
result = loop.query("What affects quality?")

# Feedback: human edit → mumbleWRAP update
loop.edit(result.markdown,
    "Speed opposes quality, but good tooling reduces this tension.")
```

---

## Repository Structure

```
SpecuLoop/
├── README.md              # This file
├── ARCHITECTURE.md        # System architecture
├── WHY.md                 # Engineering history
├── mumblewrap/            # Semantic inertia layer
│   ├── README.md
│   ├── core/              # Node, Edge, Graph, Lens
│   ├── translation/       # Mumble ↔ mumbleWRAP
│   ├── persistence/       # JSON storage
│   ├── inertia/           # (planned)
│   └── primitives/        # (planned)
├── drag/                  # Dynamic RAG / semantic reasoning
│   ├── README.md
│   ├── selector.py        # Subgraph selection
│   ├── scorer.py          # Relevance scoring
│   ├── lenses/            # (planned)
│   ├── zoom/              # (planned)
│   ├── forces/            # (planned)
│   └── viewer/            # (planned)
├── speculoop/             # Complete reasoning environment
│   ├── README.md
│   ├── self_extender.py   # New primitive proposals
│   ├── propagator.py      # Edit propagation
│   ├── agents/            # (planned)
│   ├── swarm/             # (planned)
│   └── orchestration/     # (planned)
├── tests/                 # End-to-end tests
├── docs/                  # Documentation
├── examples/              # Problem-oriented examples
└── demo.py                # Interactive demo
```

---

## Status

This is an experimental reconstruction of a lost system. All components are designed to be replaceable. The goal is to find the smallest core that can build the rest.

See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for current status.

---

## License

MIT
