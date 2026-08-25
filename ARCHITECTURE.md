# Architecture

The SpecuLoop system — three layers, one semantic model, shared history.

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

### Information Flows

**Downstream** (intention → reality):

```
human intention
    → SpecuLoop receives and orchestrates
    → DRAG selects and compresses relevant structures
    → mumbleWRAP provides semantic substrate
    → Translation layer produces code/implementation
    → Tools execute
    → Reality produces observation
```

**Upstream** (reality → understanding):

```
observed behavior
    → Execution feedback reaches SpecuLoop
    → Constraints recorded in mumbleWRAP
    → DRAG updates retrieval weights
    → Human receives updated understanding
```

---

## Layer: mumbleWRAP (Semantic Inertia)

The persistent semantic substrate. Increases semantic inertia by preserving, connecting, and accumulating meaning.

**Responsibilities**:

- Track incoming semantic inputs
- Decompose new inputs into existing structures
- Record reuse of existing nodes
- Create translation relationships
- Preserve provenance
- Identify confusion and contradictions
- Strengthen structures that repeatedly explain inputs
- Allow new primitives when needed

**Contains**:

- `core/` — Node, Edge, Graph, Lens
- `translation/` — Mumble ↔ mumbleWRAP
- `persistence/` — JSON graph storage
- `inertia/` — (planned) semantic inertia tracking
- `primitives/` — (planned) primitive management

**Does NOT contain**: retrieval, visualization, agent orchestration

---

## Layer: DRAG (Dynamic RAG / Semantic Reasoning)

The retrieval and reasoning layer. Dynamically retrieves, compresses, and reasons over mumbleWRAP.

**Responsibilities**:

- Dynamic subgraph selection for queries
- Semantic zoom (lens-dependent compression)
- Semantic lenses (different views over the same graph)
- Numerical force calculations
- Graph-based visual and mathematical reasoning

**Contains**:

- `selector.py` — Subgraph selection
- `scorer.py` — Relevance scoring
- `lenses/` — (planned) lens definitions
- `zoom/` — (planned) compression
- `forces/` — (planned) force engine
- `viewer/` — (planned) graph visualization

**Depends on**: mumbleWRAP (core graph model)

**Does NOT contain**: persistence, agent orchestration

---

## Layer: SpecuLoop (Complete Reasoning Environment)

The operational layer. Combines mumbleWRAP, DRAG, agents, and humans into a continuous reasoning system.

**Responsibilities**:

- Agent orchestration and swarm coordination
- Human feedback propagation
- Self-extension (new primitive proposals)
- Execution grounding (failures → constraints)
- Persistent system state

**Contains**:

- `self_extender.py` — New primitive proposals
- `propagator.py` — Edit and feedback propagation
- `agents/` — (planned) agent framework
- `swarm/` — (planned) multi-agent coordination
- `orchestration/` — (planned) task orchestration

**Depends on**: mumbleWRAP, DRAG

---

## Cross-Cutting Concerns

### Provenance

Provenance links generated output to the specific mumbleWRAP structures that produced it. It flows through all layers:

- mumbleWRAP stores provenance metadata
- DRAG preserves provenance during selection
- SpecuLoop uses provenance for feedback propagation

### Lenses

Lenses modify how the graph is viewed and scored. They are data structures, not hardcoded logic:

- mumbleWRAP stores lens configurations
- DRAG applies lenses during scoring and compression
- SpecuLoop allows humans to define and switch lenses

### Persistence

The graph persists as JSON. All layers read from and write to the same persistent store.

---

## Design Principles

1. **Meaning preservation** is the primary optimization target
2. **Interlocked translation** is the central mechanism
3. **mumbleWRAP** is the semantic substrate, not the objective
4. **Every component is replaceable**
5. **One repository** until components are independently useful
6. **Shared history** and experiments across all layers
