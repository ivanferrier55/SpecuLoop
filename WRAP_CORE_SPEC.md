# WRAP Core Specification

**Status**: Provisional — reconstructed from memory, not original source
**Date**: 2026-08-25
**Confidence**: See per-section labels

---

## 1. Overview

WRAP is persistent semantic state. It is a graph of nodes and edges representing meaning. WRAP is the authoritative knowledge store; all other representations (Mumble, Markdown, visual views) are materialized views of it.

**Confidence**: FOUNDATIONAL

---

## 2. Node

A node represents a semantic unit — a concept, entity, action, property, or relation.

```python
@dataclass
class Node:
    id: str                    # unique identifier (UUID or content-hash)
    kind: str                  # type: concept, action, entity, property, state, constraint, etc.
    label: str                 # human-readable name
    content: str               # semantic content (free text / structured)
    created_at: float          # timestamp
    updated_at: float          # timestamp
    usage_count: int = 0       # how often this node is reused
    metadata: dict = field(default_factory=dict)
    lenses: dict = field(default_factory=dict)  # lens_id → {weight, relevance}
```

### Node Kinds (provisional)
- `concept` — abstract idea (e.g., "speed", "quality")
- `action` — verb-like (e.g., "increase", "decrease", "implement")
- `entity` — concrete thing (e.g., "WRAP", "Obsidian vault")
- `property` — attribute of something (e.g., "fast", "reliable")
- `state` — condition or situation
- `constraint` — limitation or requirement
- `primitive` — foundational building block, never decomposed further

**Confidence**: HYPOTHESIS — node kinds are provisional. The original system may have used different categories or no categories at all.

---

## 3. Edge

An edge represents a semantic relationship between two nodes.

```python
@dataclass
class Edge:
    id: str                    # unique identifier
    source: str                # source node id
    target: str                # target node id
    relation: str              # relationship type
    weight: float = 1.0        # numeric strength / force
    created_at: float = 0.0
    updated_at: float = 0.0
    metadata: dict = field(default_factory=dict)
    lenses: dict = field(default_factory=dict)  # lens_id → {weight, relevance}
```

### Relation Types (provisional)
| Relation | Semantic Force | Example |
|---|---|---|
| `causes` | directed, positive | A → B |
| `increases` | directed, positive magnitude | speed → quality_loss |
| `decreases` | directed, negative magnitude | speed → quality |
| `supports` | bidirectional, positive | A ↔ B |
| `opposes` | bidirectional, negative | A ↔ B |
| `requires` | directed, hard constraint | B requires A |
| `demonstrates` | directed, evidential | A demonstrates B |
| `clarifies` | directed, reductive | A clarifies B |
| `motivates` | directed, directional | A motivates B |
| `solves` | directed, directional | A solves B |
| `contains` | directed, structural | A contains B |
| `part_of` | directed, structural | B part_of A |

**Confidence**: HYPOTHESIS — these are reconstructed guesses. Original relation names unknown.

### Numeric Forces

Each edge produces numeric forces used by DRAG and semantic zoom:

- `causes(A→B)`: A pushes B forward in time/causality
- `increases(A→B)`: positive magnitude, increases weight
- `decreases(A→B)`: negative magnitude
- `opposes(A↔B)`: repulsion force between nodes
- `supports(A↔B)`: attraction force between nodes

Force magnitude is a function of `edge.weight` and the active `lens`.

**Confidence**: MEMORY — numeric forces are remembered. Exact formulas unknown.

---

## 4. Graph

The graph is the persistent, authoritative store of all WRAP state.

```python
@dataclass
class Graph:
    nodes: dict[str, Node]     # id → Node
    edges: dict[str, Edge]     # id → Edge
    edge_index: dict[str, list[str]]  # node_id → [edge_ids] (adjacency)
    lenses: dict[str, "Lens"]  # id → Lens
    created_at: float = 0.0
    updated_at: float = 0.0
```

### Operations
- `add_node(node) → Node`
- `add_edge(edge) → Edge`
- `get_node(id) → Node | None`
- `get_edges(node_id, direction) → list[Edge]`
- `remove_node(id)` — also removes connected edges
- `remove_edge(id)`
- `find_nodes(query) → list[Node]` — label/content search
- `find_similar(node_id) → list[(node_id, score)]` — based on shared edges
- `save(path)` / `load(path)` — JSON persistence

**Confidence**: HIGH_CONFIDENCE — basic graph operations are well-understood.

---

## 5. Primitive

A primitive is a node that cannot be decomposed further. It is the atomic unit of meaning in WRAP.

When a new input arrives and cannot be expressed using existing primitives, a new primitive is proposed (see SELF_EXTENSION.md).

```python
@dataclass
class Primitive:
    node: Node                 # the node itself
    decomposition: list = field(default_factory=list)  # empty = atomic
    synonyms: list[str] = field(default_factory=list)
```

**Confidence**: HYPOTHESIS — the distinction between primitives and composites is assumed.

---

## 6. Usage and Reuse

When existing nodes are reused to construct a new composite meaning, usage is tracked:

```python
@dataclass
class UsageRecord:
    composite_id: str          # what was built
    component_ids: list[str]   # what was reused
    context: str               # what triggered this use
    timestamp: float
```

Usage count on nodes provides a simple frequency signal for importance/pruning.

**Confidence**: MEDIUM_CONFIDENCE — usage tracking is remembered, exact mechanism unknown.

---

## 7. Metadata

Nodes and edges carry arbitrary metadata for extensibility:

```python
metadata: {
    "source_text": "...",      # original input that created this
    "provenance": [...],       # list of contributing node/edge ids
    "confidence": float,       # system's confidence in this structure
    "human_verified": bool,    # has a human confirmed this?
    ...
}
```

**Confidence**: HIGH_CONFIDENCE — metadata is a standard extensibility pattern.

---

## 8. Persistence

The graph is persisted as a JSON file. This is intentional for inspectability and simplicity.

Future options (if needed):
- SQLite for larger graphs
- Binary format for speed
- Network graph format for visualization

**Confidence**: FOUNDATIONAL — persistence is required. JSON is provisional.

---

## 9. Open Questions

- Did the original system use a specific graph database or file format?
- Were nodes always typed, or was typing emergent?
- How were primitive vs. composite nodes distinguished in the original?
- Was there a specific serialization format?

Each of these is marked UNKNOWN.
