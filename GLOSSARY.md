# Glossary

Proprietary terms and their conventional technical equivalents.

---

## Mumble

**Related to**: natural language representation, human-readable format

Mumble is the human/LLM-readable representation of meaning in SpecuLoop. It is not a specific syntax — it is any readable form that expresses semantic content. In practice, Mumble appears as plain English input and structured Markdown output.

Mumble ↔ WRAP translation is bidirectional. Generated Mumble retains provenance to the semantic structures that produced it.

---

## WRAP

**Related to**: persistent semantic state, knowledge graph, semantic memory

WRAP is the persistent semantic state of SpecuLoop. It is a graph of nodes (concepts, actions, entities) and edges (relationships with numeric forces) that serves as the authoritative knowledge store.

All other representations — Mumble, Markdown, visual views — are materialized views of WRAP. WRAP is the source of truth.

---

## DRAG

**Related to**: dynamic RAG, adaptive retrieval, graph-based retrieval

DRAG (Dynamic RAG) selects and compresses knowledge from the WRAP graph for a given query. It is dynamic because:

1. Retrieval is dynamically compressed through semantic zoom.
2. The knowledge graph itself changes as new information arrives.

DRAG replaces static vector-similarity retrieval with lens-dependent graph traversal and scoring.

---

## SpecuLoop

**Related to**: AI agent memory system, persistent agent memory, lifelong agent memory

SpecuLoop is the overall system built on top of WRAP. It includes persistent semantic memory, dynamic RAG, semantic zoom, interlocked translation, and self-extending knowledge graphs. The goal is a system that agents can use to maintain persistent understanding across sessions.

---

## Semantic Zoom

**Related to**: graph coarsening, hierarchical clustering, multiscale graphs, semantic compression

Semantic zoom is the process of compressing or expanding knowledge at different levels of abstraction. When zoomed in, detailed nodes and relationships are visible. When zoomed out, highly related structures merge and compress.

The compression depends on the active semantic lens. This is described as **lens-dependent multiscale semantic graph representation** or **semantic graph coarsening for context-efficient reasoning**.

---

## Semantic Lens

**Related to**: multi-view knowledge graph, context-dependent retrieval, adaptive retrieval

A semantic lens modifies how the graph is viewed and scored. Different lenses emphasize different relationship types and node kinds. For example, a `temporal` lens emphasizes time relationships, while an `architecture` lens emphasizes structural relationships.

The same graph produces different views under different lenses, allowing the same knowledge to answer structurally different questions.

---

## Semantic Force

**Related to**: graph edge weight, attraction-repulsion model, force-directed graph

A semantic force is the numeric strength and direction of an edge in the WRAP graph. Forces can be:

- **Attraction** (positive): `supports`, `causes`, `increases`, `demonstrates`
- **Repulsion** (negative): `opposes`, `decreases`, `conflicts`

Forces are modified by the active semantic lens. The conceptual model is:

```
force(edge, lens, context) → numeric magnitude
```

---

## Interlocked Translation

**Related to**: bidirectional programming, natural language-code synchronization, program synthesis

Interlocked translation is the bidirectional mapping between natural language and semantic structures. Generated text retains provenance to the graph nodes and edges that produced it. Human edits propagate back into the graph.

This creates a linked chain:

```
natural language → semantic graph → materialized views → code / tools
```

Where changes in any layer can propagate to the others.

---

## Dynamic RAG

**Related to**: adaptive retrieval, incremental graph learning, lifelong retrieval

Dynamic RAG differs from static RAG in two ways:

1. **Retrieval is dynamically compressed** through semantic zoom, not fixed at a single granularity.
2. **The knowledge graph updates** as new information, feedback, and execution results arrive. Retrieval quality improves over time.

---

## Semantic Node

**Related to**: knowledge graph entity, concept node, graph vertex

A semantic node represents a unit of meaning — a concept, action, entity, property, state, or constraint. Nodes carry metadata, usage counts, and lens-specific weights.

---

## Semantic Edge

**Related to**: knowledge graph relation, typed edge, predicate

A semantic edge represents a relationship between two nodes. Edges have a relation type (e.g., `causes`, `opposes`, `supports`), a numeric weight, and lens-specific modifiers. Edges produce semantic forces.

---

## Primitive

**Related to**: atomic concept, indivisible unit, base element

A primitive is a node that cannot be decomposed further. It is the atomic unit of meaning in WRAP. When new input cannot be expressed using existing primitives, the system proposes new ones.

---

## Materialized View

**Related to**: derived view, projection, computed output

A materialized view is any output derived from the WRAP graph — Markdown, visualizations, summaries, or code. Materialized views are not authoritative; the graph is. Changes to a materialized view propagate back to the graph through interlocked translation.

---

## Provenance

**Related to**: traceability, attribution, source tracking

Provenance is the mapping from generated output back to the specific WRAP nodes and edges that produced it. Every generated sentence carries metadata identifying its source structures. This enables:

- Verification of generated output
- Propagation of human edits back to the graph
- Debugging of retrieval and generation

---

## Semantic Feedback

**Related to**: interactive learning, human-in-the-loop correction, belief update

Semantic feedback is the process of incorporating human corrections into the graph. When a human edits generated text or corrects a system's understanding, the correction is propagated as a semantic update — not just a text edit.

---

## Constraint

**Related to**: system limitation, environmental restriction, failure mode

A constraint is a limitation that prevents a desired operation. In SpecuLoop, constraints are recorded as semantic information rather than discarded as errors. This enables constraint-aware planning and prevents repeated failures.

---

## Graph Coarsening

**Related to**: graph summarization, hierarchical aggregation, multiscale reduction

Graph coarsening is the process of merging highly related nodes and edges into higher-level abstractions. In SpecuLoop, coarsening is driven by semantic lenses and is the mechanism behind semantic zoom. Different lenses produce different coarsened views of the same graph.
