# mumbleWRAP: Preserving Meaning Across Translations

**Interlocked translation between natural language, semantic graph nodes, code, and executable tools — a persistent semantic substrate where meaning survives translation and changes propagate bidirectionally.**

---

## The Problem: Semantic Drift Across Representations

A human describes an intention. An AI translates that into a semantic representation. That representation becomes code. The code executes. Reality produces an observation.

At each translation, meaning can drift:

```
human intention
    → AI interpretation     (drift)
    → semantic structure     (drift)
    → code                  (drift)
    → execution             (drift)
    → observation
```

By the time the observation reaches the human, the original intention may be unrecognizable. Traditional systems lose the relationship between these representations. Corrections in one layer do not propagate to others.

This is the core problem: **semantic drift across translations**.

---

## The Goal: Preserve Meaning Across Translations

The primary optimization target is:

> **Preservation and propagation of meaning across translations.**

When information moves between human language, semantic structures, code, and execution, the system should attempt to preserve semantic intent. Changes and observations should propagate bidirectionally through interlocked representations.

Success is defined as:

- Meaning survives translation
- Changes propagate correctly
- Observations propagate backward
- Semantic drift is reduced
- Representations remain mutually consistent

Token efficiency, graph compression, and retrieval speed are valuable because they help achieve these objectives — not as ends in themselves.

---

## The Solution: Interlocked Translation

An **interlocked translation** is a translation whose output remains linked to the semantic structures from which it was produced.

Therefore:

```
source changes
    → semantic representation updates
    → downstream translations can update

downstream observations
    → semantic structures update
    → upstream representations can update
```

mumbleWRAP implements interlocked translation between:

- **Human language** ↔ **mumbleWRAP** (semantic structures)
- **mumbleWRAP** ↔ **code** (implementations)
- **Code** ↔ **execution** (tools, behavior)
- **Execution** ↔ **mumbleWRAP** (feedback, constraints)

Each layer retains provenance to the layer that produced it. A change in any layer can propagate through the chain.

---

## The Semantic Layer: mumbleWRAP

mumbleWRAP is the persistent semantic substrate connecting different representations. It is not merely an encoding of sentences. It represents reusable semantic structures and the relationships between them.

```
mumbleWRAP
    ├── nodes: concepts, actions, entities, properties, constraints
    ├── edges: typed relationships with numeric forces
    ├── lenses: weight modifiers for different views
    └── persistence: survives across sessions, grows incrementally
```

When new information arrives, it is decomposed into existing semantic structures when possible. New primitives are constructed only when necessary.

### Key Properties

- **Persistent**: survives across sessions
- **Incremental**: grows as new information arrives
- **Decomposable**: new inputs reuse existing structures
- **Self-extending**: proposes new primitives when needed
- **Grounded**: connected to execution and observation

---

## The Semantic Layer in Context

mumbleWRAP sits in the middle of the translation chain:

```
Human language (Mumble)
    ↕ interlocked translation
mumbleWRAP (persistent semantic structures)
    ↕ interlocked translation
Code / implementations
    ↕ interlocked translation
Execution / tools / observed behavior
```

### What Each Layer Does

| Layer | Role |
|---|---|
| **Human language** | Intention, description, correction |
| **mumbleWRAP** | Semantic structures, relationships, forces |
| **Code** | Implementation of semantic intent |
| **Execution** | Reality, observation, constraint |

### What Flows Through

- **Downstream**: intention → structure → code → execution
- **Upstream**: observation → constraint → structure → understanding

Both directions are interlocked. Both directions preserve meaning.

---

## Reasoning Infrastructure: DRAG

DRAG (Dynamic RAG) is infrastructure for selecting, weighting, composing, and compressing semantic structures according to the active lens and context.

DRAG is not the objective. DRAG is the mechanism that allows mumbleWRAP to present the appropriate granularity of semantic structure for a given question.

### How DRAG Works

1. **Score** nodes and edges by relevance to the query
2. **Select** a relevant subgraph from mumbleWRAP
3. **Compress** the subgraph using semantic zoom
4. **Compose** the result as human-readable text with provenance

### Semantic Zoom

Semantic zoom is a mechanism for presenting the appropriate granularity of the underlying semantic structure. It is not the ultimate objective.

- **Zoomed in**: detailed nodes and relationships
- **Zoomed out**: highly related structures merge and compress
- **Lens-dependent**: different lenses produce different compressed views

---

## Semantic Lenses

A semantic lens determines which relationships and structures are important for a particular question.

```
same mumbleWRAP graph
    × different lens
    = different representation
```

Examples:

| Lens | Emphasis |
|---|---|
| `implementation` | Code-related structures, dependencies |
| `architecture` | System components, containment |
| `time` | Temporal relationships, sequences |
| `next-steps` | Action chains, priorities |
| `onboarding` | Core concepts, explanations |
| `causality` | Cause-effect relationships |

Lenses are data, not hardcoded. The system can extend its lens vocabulary.

---

## Execution: Grounding in Reality

Execution is part of the semantic loop. If generated code behaves unexpectedly, the observation becomes semantic information.

```
intended behavior
    ↓
mumbleWRAP
    ↓
implementation
    ↓
execution
    ↓
observed behavior
    ↓
semantic feedback
    ↓
mumbleWRAP (updated)
```

This grounds the semantic system in reality. Failures and constraints are not discarded — they become persistent information about what the system can and cannot do.

---

## Human Feedback: Semantic Corrections

Human edits are semantic observations. When a human changes a generated description, the system attempts to determine which underlying semantic structures were being corrected.

That correction propagates through the interlocked translation relationships.

The objective is to discover what the human was pointing toward — not merely record the literal sentence.

**Example**:

```
System:  "The main issue is context-window size."
Human:   "No, the underlying issue is token waste."
```

The system propagates this correction:
- Weakens "context-window" relevance for this context
- Strengthens "token waste" node
- Records the correction as a semantic observation

---

## Secondary Optimization Targets

The architecture also optimizes for:

- **Semantic fidelity**: meaning is preserved, not just words
- **Translation consistency**: translations remain coherent
- **Bidirectional propagation**: changes flow in both directions
- **Grounding**: connected to executable reality
- **Alignment**: human intent stays connected to system behavior
- **Token efficiency**: avoid unnecessary context
- **Retrieval efficiency**: find relevant structures quickly

These support the primary goal: preserving meaning across translations.

---

## Quick Start

```bash
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop
python3 demo.py
python3 wrap/tests/test_core_loop.py
```

### Example

```python
from wrap.api import SpecuLoop

loop = SpecuLoop("knowledge.json")

# Ingest: human language → mumbleWRAP
loop.ingest("Speed and quality are in tension.")
loop.ingest("Good tooling improves quality.")

# Retrieve: mumbleWRAP → human language (with provenance)
result = loop.query("What affects quality?")
print(result.markdown)
# → "Speed opposes quality."
# → "Good tooling increases quality."

# Feedback: human edit → mumbleWRAP update
loop.edit(result.markdown,
    "Speed opposes quality, but good tooling reduces this tension.")

# Self-extension: propose new semantic structures
proposal = loop.propose("creativity")
loop.confirm_proposal(proposal)
```

---

## Architecture

```
Human language (Mumble)
    ↕ decompose / compose
mumbleWRAP (persistent semantic structures)
    ↕ DRAG select / score / compress
Relevant subgraph (lens-dependent)
    ↕ compose
Materialized views (Markdown with provenance)
    ↕ human edit
Updated mumbleWRAP (interlocked translation)
    ↕ code generation
Implementations
    ↕ execution
Observed behavior → semantic feedback → mumbleWRAP
```

### Components

| Component | Role | Status |
|---|---|---|
| mumbleWRAP graph | Persistent semantic substrate | Implemented |
| Translation layer | Mumble ↔ mumbleWRAP | Implemented |
| DRAG | Select / compress subgraphs | Implemented |
| Lenses | View-dependent weighting | Implemented |
| Self-extension | Propose new primitives | Implemented |
| Feedback | Human edit propagation | Partial |
| Execution grounding | Tool failure → constraint | Designed |

---

## Repository Structure

```
SpecuLoop/
├── README.md
├── WHY.md                  # Engineering history
├── GLOSSARY.md             # Term definitions
├── ARCHITECTURE.md         # System overview
├── AGENTS.md               # AI agent instructions
├── RELATED_PROBLEMS.md     # Problem index
├── RESEARCH_CROSSWALK.md   # Research mappings
├── RELATED_WORK.md         # Papers and projects
├── CITATION.cff
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── demo.py
├── docs/
│   ├── problems/           # Engineering problems
│   ├── concepts/           # Core technical concepts
│   ├── architecture/       # Component documentation
│   ├── comparisons/        # Related systems
│   └── discovery/          # External research tracking
├── examples/               # Problem-oriented examples
└── wrap/                   # Implementation
    ├── api.py              # SpecuLoop interface
    ├── core/               # Node, Edge, Graph, Lens
    ├── translation/        # Mumble ↔ mumbleWRAP
    ├── drag/               # Subgraph selection
    ├── extension/          # Self-extension
    ├── feedback/           # Edit propagation
    ├── persistence/        # JSON storage
    └── tests/              # End-to-end tests
```

---

## Status

This is an experimental reconstruction of a lost system. The current implementation is a minimal kernel demonstrating the core loop: mumbleWRAP ↔ human language ↔ execution.

All components are designed to be replaceable. The goal is to find the smallest core that can build the rest.

See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for current status and known limitations.

---

## License

MIT
