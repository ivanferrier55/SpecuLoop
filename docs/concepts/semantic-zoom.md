# Semantic Zoom for Knowledge Graphs

**Search terms**: semantic zoom, graph coarsening, multiscale graphs, semantic compression, context-efficient reasoning

## What Is Semantic Zoom?

Semantic zoom is the process of compressing or expanding knowledge at different levels of abstraction. It is **not** visual zoom — it changes the semantic content, not the display.

### Zoomed In

Detailed nodes and relationships are visible. Every edge is shown with its full label and weight.

### Zoomed Out

Highly related structures merge. Clusters of nodes compress into single representative nodes. Edges between clusters are summarized.

## Lens-Dependent Compression

The compression depends on the active semantic lens. Different lenses produce different compressed views of the same graph.

| Lens | Compression Strategy |
|---|---|
| `temporal` | Merge nodes by time period, show temporal sequence |
| `architecture` | Merge by system component, show structural dependencies |
| `next-steps` | Merge by action chain, show dependency order |
| `causal` | Merge by cause-effect path, show causal chains |
| `problem-solution` | Merge by problem-solution pairs, show resolution paths |

## Technical Description

Semantic zoom is described as:

- **Lens-dependent multiscale semantic graph representation**
- **Semantic graph coarsening for context-efficient reasoning**

The coarsening algorithm:

1. Score all nodes by relevance to the query under the active lens
2. Cluster nodes by relationship strength and lens weight
3. Merge clusters into representative nodes
4. Summarize inter-cluster edges
5. Return the compressed subgraph

The compression ratio is controlled by a target token budget.

**Implementation status**: The `compress()` method exists in `wrap/drag/selector.py` but is not yet integrated into the main emit pipeline. Current implementation removes lowest-scored nodes. Full coarsening with cluster merging is planned.
