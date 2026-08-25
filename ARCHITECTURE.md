# Architecture

The mumbleWRAP system architecture — interlocked translations between representations.

---

## The Translation Chain

```
Human language (Mumble)
    ↕ interlocked translation
mumbleWRAP (persistent semantic structures)
    ↕ interlocked translation
Code / implementations
    ↕ interlocked translation
Execution / tools / observed behavior
```

Each layer retains provenance to the layer that produced it. Changes in any layer propagate through the chain.

---

## Core Data Flow

```
Human language input
    ↓ decompose
mumbleWRAP graph (persistent semantic structures)
    ↓ DRAG select / compress (lens-dependent)
Relevant subgraph
    ↓ compose
Materialized view (Markdown with provenance)
    ↓ human edit
Updated mumbleWRAP (interlocked translation)
    ↓ code generation
Implementation
    ↓ execution
Observed behavior
    ↓ semantic feedback
mumbleWRAP (updated)
```

---

## Components

### mumbleWRAP (Semantic Substrate)

The persistent semantic layer. A graph of:

- **Nodes**: concepts, actions, entities, properties, states, constraints
- **Edges**: relationships with numeric forces
- **Lenses**: weight modifiers that change how the graph is viewed

### Translation Layer

Bidirectional mapping between representations:

- **Decomposer**: text → graph structures
- **Composer**: graph → text with provenance
- **Translator**: orchestrates the bidirectional flow

### DRAG (Selection Infrastructure)

Selects and compresses semantic structures:

- **Scorer**: scores relevance to a query
- **Selector**: traverses the graph
- **Compressor**: merges related structures

### Extension

- **SelfExtender**: proposes new primitives when decomposition fails

### Feedback

- **FeedbackPropagator**: propagates human edits and execution results back into mumbleWRAP

---

## Key Design Principles

1. **Meaning preservation** is the primary optimization target
2. **Interlocked translation** is the central mechanism
3. **mumbleWRAP** is the semantic substrate, not the objective
4. **Every component is replaceable**
5. **Provenance is mandatory** — every output traces to its source
6. **Constraints are semantic** — failures become persistent knowledge
7. **Success** = meaning survives translation, drift is reduced
