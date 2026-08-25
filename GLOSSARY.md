# Glossary

Proprietary terms and their conventional technical equivalents.

---

## mumbleWRAP

**Related to**: persistent semantic memory, knowledge graph, semantic substrate

mumbleWRAP is the persistent semantic substrate connecting different representations. It is a graph of nodes (concepts, actions, entities) and edges (relationships with numeric forces) that serves as the authoritative semantic layer between human language, code, and execution.

mumbleWRAP is not merely an encoding of sentences. It represents reusable semantic structures and the relationships between them.

All other representations — Mumble, Markdown, visual views — are materialized views of mumbleWRAP.

---

## Mumble

**Related to**: natural language representation, human-readable format

Mumble is the human/LLM-readable representation of meaning. It is not a specific syntax — it is any readable form that expresses semantic content.

Mumble ↔ mumbleWRAP translation is bidirectional. Generated Mumble retains provenance to the semantic structures that produced it.

---

## DRAG

**Related to**: dynamic RAG, adaptive retrieval, graph-based retrieval

DRAG (Dynamic RAG) is infrastructure for selecting, weighting, composing, and compressing semantic structures according to the active lens and context. It is a mechanism, not the objective.

---

## Interlocked Translation

**Related to**: bidirectional programming, natural language-code synchronization, program synthesis

An interlocked translation is a translation whose output remains linked to the semantic structures from which it was produced. This is the central architectural idea.

```
source changes
    → semantic representation updates
    → downstream translations can update

downstream observations
    → semantic structures update
    → upstream representations can update
```

---

## Semantic Zoom

**Related to**: graph coarsening, hierarchical clustering, semantic compression

Semantic zoom is a mechanism for presenting the appropriate granularity of the underlying semantic structure. It is not the ultimate objective.

---

## Semantic Lens

**Related to**: multi-view knowledge graph, context-dependent retrieval

A semantic lens determines which relationships and structures are important for a particular question. The same mumbleWRAP graph produces different representations under different lenses.

---

## Semantic Force

**Related to**: edge weight, attraction-repulsion model

A semantic force is the numeric strength and direction of a relationship edge in the mumbleWRAP graph.

---

## Provenance

**Related to**: traceability, attribution, source tracking

Provenance is the mapping from generated output back to the specific mumbleWRAP nodes and edges that produced it. It enables interlocked translation.

---

## Semantic Feedback

**Related to**: interactive learning, human-in-the-loop correction

Semantic feedback is the process of incorporating human corrections into mumbleWRAP. The objective is to discover what the human was pointing toward, not merely record the literal sentence.

---

## Primitive

**Related to**: atomic concept, indivisible unit

A primitive is a node that cannot be decomposed further. When new input cannot be expressed using existing primitives, the system proposes new ones.

---

## Materialized View

**Related to**: derived view, projection

A materialized view is any output derived from mumbleWRAP — Markdown, visualizations, summaries, or code. Changes to a materialized view propagate back through interlocked translation.

---

## Constraint

**Related to**: system limitation, failure mode

A constraint is a limitation that prevents a desired operation. In mumbleWRAP, constraints are recorded as semantic information rather than discarded as errors.
