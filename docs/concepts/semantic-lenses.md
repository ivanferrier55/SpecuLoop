# Lens-Based Knowledge Graph Retrieval

**Search terms**: multi-view knowledge graph, lens-based retrieval, adaptive retrieval, context-dependent search

## What Are Semantic Lenses?

A semantic lens modifies how the graph is viewed and scored. The same graph produces different views under different lenses.

### How Lenses Work

Each lens specifies:

- **Node weights**: which nodes to emphasize or de-emphasize
- **Edge weights**: which relationships to emphasize or de-emphasize
- **Kind weights**: which node types to emphasize (e.g., actions vs. concepts)
- **Relation weights**: which relationship types to emphasize (e.g., causal vs. structural)

### Example Lenses

**Architecture Lens**
- Emphasizes: `contains`, `part_of`, `requires`
- De-emphasizes: `motivates`, `clarifies`
- Result: system structure view

**Temporal Lens**
- Emphasizes: time-related nodes and edges
- De-emphasizes: structural relationships
- Result: timeline view

**Next-Steps Lens**
- Emphasizes: `requires`, `depends_on`, action nodes
- De-emphasizes: historical relationships
- Result: action/dependency chain view

**Problem-Solution Lens**
- Emphasizes: `opposes`, `solves`, problem/solution nodes
- De-emphasizes: unrelated structural details
- Result: problem resolution view

## Dynamic Lens Propagation

When a new lens is introduced, it should propagate through the existing graph — updating edge weights and node relevance based on the lens's emphasis rules.

**Implementation status**: Lenses modify weights during scoring and selection. Dynamic propagation through the full graph is planned.
