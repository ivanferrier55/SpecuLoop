# DRAG Core Specification

**Status**: Provisional — reconstructed from memory
**Date**: 2026-08-25
**Confidence**: See per-section labels

---

## 1. Overview

DRAG (Dynamic RAG) selects and compresses knowledge from the WRAP graph for a given query or context. It is "dynamic" because:

1. It dynamically selects relevant subgraphs based on the query and active lens
2. It dynamically updates the knowledge graph as new information arrives

DRAG is explicitly designed to be replaceable. The initial implementation uses simple scoring. Better algorithms (embedding-based, graph neural networks, linear algebra) can replace it without changing the rest of the system.

**Confidence**: HIGH_CONFIDENCE

---

## 2. Interface

```python
class DRAG:
    def __init__(self, graph: Graph):
        self.graph = graph
    
    def select(self, query: str, lens: Lens = None, max_nodes: int = 50) -> Subgraph:
        """
        Select the most relevant subgraph for a query.
        Returns a Subgraph (subset of the full graph).
        """
    
    def score(self, node_id: str, query: str, lens: Lens = None) -> float:
        """
        Score a node's relevance to a query under a given lens.
        This is the REPLACEABLE scoring mechanism.
        """
    
    def compress(self, subgraph: Subgraph, target_tokens: int) -> Subgraph:
        """
        Compress a subgraph to fit within a token budget.
        Merges highly-related structures, drops low-relevance nodes.
        """
    
    def propagate(self, node_id: str, depth: int = 2) -> list[str]:
        """
        Propagate from a node through the graph to find connected context.
        Returns ordered list of node IDs by relevance.
        """
```

**Confidence**: HIGH_CONFIDENCE — the interface is clear; implementation is provisional.

---

## 3. Initial Scoring Algorithm

The initial scoring is intentionally simple and replaceable.

### Node Relevance Score

```
score(node, query, lens) = 
    text_match(node.label, query) * lens_weight(node, lens) 
    + edge_density_bonus(node) 
    + usage_bonus(node)
```

Where:
- `text_match`: simple substring/keyword overlap (0.0 to 1.0)
- `lens_weight`: node's weight under the active lens (from node.lenses)
- `edge_density_bonus`: bonus for nodes with many connections (small)
- `usage_bonus`: bonus for frequently reused nodes (small)

### Edge Propagation

When propagating from a seed node, edge weights influence traversal priority:

```
priority(edge) = edge.weight * lens_weight(edge, lens) * direction_bonus(edge)
```

Edges with negative weights (opposition) are traversed but with reduced priority.

**Confidence**: HYPOTHESIS — this is a reasonable starting point, not the original algorithm.

---

## 4. Subgraph

```python
@dataclass
class Subgraph:
    nodes: dict[str, Node]     # selected nodes
    edges: dict[str, Edge]     # selected edges
    root_ids: list[str]        # seed nodes that started the selection
    scores: dict[str, float]   # node_id → relevance score
    lens: str                  # active lens id
    token_estimate: int        # estimated token count when rendered
```

**Confidence**: HIGH_CONFIDENCE

---

## 5. Semantic Zoom via DRAG

Semantic zoom is implemented through DRAG's compression:

| Zoom Level | Behavior |
|---|---|
| Fine (zoomed in) | All nodes and edges visible, detailed labels |
| Medium | Merge highly-connected node clusters, show summary |
| Coarse (zoomed out) | Only major concepts and their direct relationships |

The lens determines what "highly connected" means in context.

**Confidence**: MEDIUM_CONFIDENCE — the concept is remembered; exact compression heuristics are provisional.

---

## 6. Backprop / Feedback Propagation

The term "backprop" in the original system likely refers to semantic feedback propagation:

When a query is answered (or fails), the result propagates back through the graph to adjust edge weights and node relevance:

1. **Successful answer**: edges involved get weight boost
2. **Failed answer**: edges involved get weight reduction
3. **Partial answer**: mixed adjustment

This creates a learning signal that improves future DRAG selections.

```
result → propagate_feedback(graph, involved_structures, success_score)
```

The `success_score` is a float from -1.0 (total failure) to 1.0 (perfect answer).

**Confidence**: MEMORY — backprop is remembered. Exact mechanism is HYPOTHESIS.

---

## 7. Replacement Strategy

The scoring mechanism is explicitly designed to be swapped:

1. **Phase 1** (current): Text match + simple heuristics
2. **Phase 2**: Embedding-based similarity (requires vector store)
3. **Phase 3**: Graph neural network or attention-based scoring
4. **Phase N**: Whatever works best

To replace, implement the same interface with a different `score()` method.

**Confidence**: FOUNDATIONAL

---

## 8. Open Questions

- What was the original backprop formula?
- Did the original system use embeddings for node similarity?
- How was token counting done (model-specific)?
- Was there a specific graph traversal algorithm (BFS, DFS, priority-based)?
