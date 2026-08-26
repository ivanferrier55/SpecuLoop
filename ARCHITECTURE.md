# Architecture

The SpecuLoop system — three layers, one semantic model, shared history, and an explicit grounding loop.

---

## The Full Translation Chain

```text
Human / Agent Swarm
    ↕
SpecuLoop (objectives + orchestration + feedback)
    ↕
DRAG (reasoning + retrieval)
    ↕
mumbleWRAP (semantic basis)
    ↕
Translations / Implementations / Tools / Experiments
    ↕
Observed Reality
```

The important architectural distinction is not human versus AI. It is **generation versus grounding**.

AI systems may generate hypotheses, plans, explanations, and candidate structures at enormous scale. Those generations should not automatically acquire the same semantic authority as observations, constraints, experiments, or other evidence.

### Information Flows

**Downstream** (objective → action):

```text
objective / question
    → SpecuLoop receives and orchestrates
    → DRAG selects and compresses relevant structures
    → mumbleWRAP provides semantic substrate
    → Translation layer produces code/implementation
    → Tools / experiments execute
    → Reality produces observation
```

**Upstream** (evidence → understanding):

```text
observed behavior / experiment / external evidence
    → grounding signal reaches SpecuLoop
    → evidence and constraints recorded in mumbleWRAP
    → DRAG updates retrieval/reasoning state
    → semantic basis is evaluated
    → human or autonomous system receives updated understanding
```

### Grounding Loop

```text
                 OBJECTIVE / QUESTION
                         │
                         ▼
                  SEMANTIC BASIS
                         │
                         ▼
                    AI GENERATION
                         │
                   hypotheses
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

The system is intended to let generation run quickly while making **evidence, rather than generation volume, the source of semantic authority**.

---

## Layer: mumbleWRAP (Semantic Basis)

The persistent semantic substrate. It maintains the current semantic basis and its history rather than serving as an undifferentiated store of generated information.

**Responsibilities**:

- Track incoming semantic inputs and evidence
- Decompose new inputs into existing structures
- Record reuse of existing nodes
- Create translation relationships
- Preserve provenance
- Identify confusion and contradictions
- Strengthen structures that repeatedly explain grounded inputs
- Allow provisional primitives when needed
- Support later semantic refactoring

**Contains**:

- `core/` — Node, Edge, Graph, Lens
- `translation/` — Mumble ↔ mumbleWRAP
- `persistence/` — JSON graph storage
- `inertia/` — (planned) semantic inertia tracking
- `primitives/` — (planned) primitive management

**Does NOT contain**: retrieval, visualization, agent orchestration

### Semantic inertia

The repository's original architectural notes used “semantic inertia” to describe accumulation. The current research direction treats inertia as a **problem to manage**: generated representations can become disproportionately influential merely because they accumulate or are repeatedly retrieved.

The semantic basis is intended to reduce this effect by distinguishing provisional generated candidates from evidence-supported structures.

---

## Layer: DRAG (Dynamic RAG / Semantic Reasoning)

The retrieval and reasoning layer. Dynamically retrieves, compresses, and reasons over mumbleWRAP.

**Responsibilities**:

- Dynamic subgraph selection for queries
- Semantic zoom (lens-dependent compression)
- Semantic lenses (different views over the same graph)
- Numerical force calculations
- Graph-based visual and mathematical reasoning
- Preserve the provenance and status of retrieved structures

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

The operational layer. Combines mumbleWRAP, DRAG, agents, tools, experiments, and humans into a continuous reasoning system.

**Responsibilities**:

- Agent orchestration and swarm coordination
- Human feedback propagation
- Self-extension (new primitive proposals)
- Execution grounding (failures → constraints)
- Experiment/tool feedback
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

### Grounding

Grounding signals may come from humans or from the world. Relevant sources can include:

- objectives and constraints;
- observations;
- experiments and measurements;
- execution results;
- external evidence;
- validated simulations.

Generated hypotheses are candidates for grounding rather than automatic replacements for it.

See [GROUNDING.md](GROUNDING.md).

### Provenance

Provenance links generated output to the specific mumbleWRAP structures and evidence that produced or supported it. It flows through all layers:

- mumbleWRAP stores provenance metadata
- DRAG preserves provenance during selection
- SpecuLoop uses provenance for feedback propagation

A future epistemic layer may additionally distinguish source type and evidential status; this remains an open research question.

### Lenses

Lenses modify how the graph is viewed and scored. They are data structures, not hardcoded logic:

- mumbleWRAP stores lens configurations
- DRAG applies lenses during scoring and compression
- SpecuLoop allows humans to define and switch lenses

### Persistence

The graph persists as JSON. All layers read from and write to the same persistent store.

---

## Design Principles

1. **Grounding constrains semantic authority**
2. **Meaning preservation** is the primary optimization target
3. **Interlocked translation** is the central mechanism
4. **mumbleWRAP** is the semantic substrate, not the objective
5. **Generation is exploratory; evidence can change the basis**
6. **Every component is replaceable**
7. **One repository** until components are independently useful
8. **Shared history** and experiments across all layers
