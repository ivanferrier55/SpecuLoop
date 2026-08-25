# Architecture

System architecture of SpecuLoop's WRAP semantic engine.

---

## Core Data Flow

```
Natural language input (Mumble)
    ↓
Decomposer (text → semantic structures)
    ↓
WRAP Graph (persistent semantic state)
    ↓
DRAG Selector (lens-dependent subgraph selection)
    ↓
Composer (graph → natural language with provenance)
    ↓
Materialized View (Markdown with provenance metadata)
    ↓
Human reads or edits
    ↓
Feedback Propagator (edit → semantic update)
    ↓
Updated WRAP Graph
```

---

## Component Map

```
Mumble ←→ WRAP ←→ DRAG ←→ Materialized Views
             ↕
         Lenses
             ↕
    Tools / Code / Reality
```

### WRAP (Persistent Semantic State)

The authoritative knowledge store. A graph of:

- **Nodes**: concepts, actions, entities, properties, states, constraints
- **Edges**: relationships with numeric forces (causes, opposes, supports, etc.)
- **Lenses**: weight modifiers that change how the graph is viewed

### DRAG (Dynamic RAG)

Selects and compresses knowledge from the graph:

- **Scorer**: scores node/edge relevance to a query (replaceable)
- **Selector**: traverses the graph to collect relevant subgraphs
- **Compressor**: merges highly-related structures for context efficiency

### Translation Layer

Bidirectional mapping between natural language and semantic structures:

- **Decomposer**: text → graph structures (initially pattern-based, replaceable with LLM)
- **Composer**: graph → text with provenance metadata (initially template-based)
- **Translator**: orchestrates decompose/compose operations

### Extension Layer

- **SelfExtender**: proposes new primitives when decomposition fails

### Feedback Layer

- **FeedbackPropagator**: propagates human edits back into the graph

### Persistence

- **Store**: JSON-based graph serialization (replaceable with SQLite, graph DB, etc.)

---

## Key Design Principles

1. **Graph is authoritative** — all other representations are derived
2. **Every component is replaceable** — pattern matching → LLM, text overlap → embeddings
3. **Provenance is mandatory** — every output traces to its source structures
4. **Constraints are semantic** — failures become persistent knowledge
5. **Lenses are data** — not hardcoded, not fixed, extendable

---

## Confidence Model

All design decisions are labeled with confidence levels:

- **FOUNDATIONAL**: core principle, unlikely to change
- **HIGH_CONFIDENCE**: well-understood, minor adjustments expected
- **MEDIUM_CONFIDENCE**: reasonable approach, needs validation
- **HYPOTHESIS**: proposed mechanism, unverified
- **UNKNOWN**: not yet determined

This prevents false certainty during reconstruction.
