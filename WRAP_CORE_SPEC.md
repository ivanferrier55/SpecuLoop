# WRAP Core Specification

**Status**: Provisional — reconstructed from memory, not original source
**Date**: 2026-08-26
**Confidence**: See per-section labels

---

## 1. Overview

mumbleWRAP (WRAP) is persistent semantic state. It is a graph of nodes and edges representing meaning. WRAP is the authoritative knowledge store; Mumble, Markdown, visual views, and implementation views are materialized representations of it.

A useful current interpretation of WRAP is **Words Reconstructed As Primitives**. This is a memory-based hypothesis, also consistent with the idea of a software wrapper and the mumble-rap wordplay. It is not yet historically verified.

**Confidence**: FOUNDATIONAL for the graph model; HYPOTHESIS for the expansion of WRAP.

---

## 2. Node

A node represents a semantic unit — a concept, entity, action, property, relation, or constraint.

```python
@dataclass
class Node:
    id: str
    kind: str
    label: str
    content: str
    created_at: float
    updated_at: float
    usage_count: int = 0
    metadata: dict = field(default_factory=dict)
    lenses: dict = field(default_factory=dict)
```

### Node Kinds (provisional)

- `concept` — abstract idea
- `action` — verb-like operation
- `entity` — concrete thing
- `property` — attribute
- `state` — condition or situation
- `constraint` — limitation or requirement
- `primitive` — semantic building block that the current basis treats as atomic

**Confidence**: HYPOTHESIS — exact historical categories are unknown.

---

## 3. Edge

An edge represents a semantic relationship between nodes. Relationships are not assumed to be purely causal. Examples, demonstrations, constraints, translations, opposition, and support can require different semantics.

```python
@dataclass
class Edge:
    source: str
    target: str
    relation: str
    weight: float = 1.0
    metadata: dict = field(default_factory=dict)
    lenses: dict = field(default_factory=dict)
```

Candidate relationship families include:

| Relation | Role |
|---|---|
| `causes` | directed causal influence |
| `increases` | directed positive change |
| `decreases` | directed negative change |
| `supports` | positive semantic/evidential connection |
| `opposes` | negative/repulsive connection |
| `requires` | constraint/dependency |
| `demonstrates` | evidence or example |
| `tests` | example/experiment evaluates a hypothesis |
| `clarifies` | reduces ambiguity |
| `motivates` | creates pressure toward an action |
| `solves` | addresses a problem |
| `translates` | links representations |
| `contains` / `part_of` | structural composition |

**Confidence**: relationship families are reconstructed hypotheses. The exact original vocabulary is unknown.

### Numeric forces

Edges can produce numeric attraction/repulsion or directional forces. The same node pair may have different values under different semantic lenses.

The historical force equation is unknown and must remain replaceable.

---

## 4. Graph

The graph is persistent semantic state.

It stores:

- nodes;
- edges;
- lenses;
- provenance and confidence metadata;
- reuse/usage information.

The graph should be treated as a substrate from which other views are generated, rather than as a collection of independent documents.

---

## 5. Primitive and Semantic Basis

A primitive is a reusable semantic building block. The important property is not merely that it is short, but that it allows many clues to be represented and reconstructed.

A **semantic basis** is a set of primitives sufficient to explain the current evidence.

The current reconstruction suggests a minimum-sufficient-basis principle:

```text
prefer the smallest primitive basis that adequately explains
and reconstructs the observed clue set
```

A newly discovered primitive may replace several older primitives when it gives better explanatory compression.

**Confidence**: HYPOTHESIS, strongly motivated by the recovered conversation.

---

## 6. Clues and Compression

Every input can be retained as a clue. Inputs need not be commands or causal statements. A clue can be:

- a problem;
- a desired capability;
- an example;
- a preference;
- a constraint;
- a correction;
- a tool result;
- an execution failure;
- an observation from an agent.

The system first attempts to decompose the clue into existing structures. Reuse is recorded.

```text
clue
 ↓
existing basis
 ↓
compressible?
 ├─ yes → reuse / strengthen
 └─ no  → uncertainty / investigation
```

Unresolved information should not automatically become a permanent node. It can first produce a provisional primitive hypothesis.

---

## 7. Decoder-Aware Compression

The optimal representation may depend on the decoder. Different AI systems can require different levels of explicit information to encode or decode the same semantic structure.

A useful design abstraction is:

```text
R* = f(semantic structure, decoder capability, lens, task)
```

This makes semantic zoom a semantic operation rather than only a visual one.

A candidate primitive can be isolated and passed to a decoder. The decoder attempts to reconstruct the existing clue set. Reconstruction error becomes evidence about the usefulness of the primitive.

```text
primitive basis
      ↓
    decoder
      ↓
predicted clues
      ↕
actual clues
```

The current implementation exposes this through an optional decoder callback and a deterministic lexical baseline.

**Confidence**: HYPOTHESIS — newly reconstructed from the conversation.

---

## 8. Uncertainty

Uncertainty is treated as a property of the current semantic basis:

```text
uncertainty ≈ inability of current representation to compress/reconstruct evidence
```

It should lead to action:

- ask a targeted human question;
- generate an example/test case;
- have agents investigate;
- execute a tool;
- test alternative primitives;
- compare candidate bases.

A useful clarification question is therefore not arbitrary. It should target the missing distinction that would allow the clue to become compressible.

---

## 9. Usage and Reuse

When existing nodes are reused to construct new meaning, usage is tracked. Reuse can become a signal for semantic importance and for deciding which structures deserve persistence.

This is distinct from ordinary graph degree: many links do not necessarily mean semantic importance because links may represent opposition, support, examples, constraints, or other relationships.

**Confidence**: MEDIUM/HIGH — repeated requirement in the recovered design.

---

## 10. Interlocked Representations

Mumble, WRAP, code, commands, tool operations, and observations can be linked as translations of the same semantic state.

```text
Mumble ↔ WRAP ↔ implementation ↔ tool/reality
```

Human edits to a generated Mumble representation should propagate through provenance to the contributing WRAP structures. Implementation or execution feedback should propagate backward as evidence and constraints.

---

## 11. Persistence

JSON is the current implementation format because it is inspectable and easy to replace. The original persistence format is unknown.

The semantic solve loop should additionally preserve its evidence trail: clue, hypothesis, test, prediction, observation, score, uncertainty, and basis decision.

---

## 12. Open Questions

- Exact historical WRAP syntax?
- Exact primitive vocabulary?
- Exact DRAG force equations?
- What did remembered "backprop" actually update?
- Did the original system isolate primitives for LLM reconstruction tests?
- How were candidate primitive sets searched and refactored?
- How were lenses propagated through the graph?
- What was the original persistence format?

These remain explicitly UNKNOWN/HYPOTHESIS and should not be silently promoted to historical fact.
