# Graph Coarsening for Semantic Retrieval

Graph coarsening is the process of merging highly related nodes into higher-level abstractions, reducing graph size while preserving semantic structure.

## How It Works in SpecuLoop

Coarsening is driven by semantic lenses:

1. Score nodes by relevance to query under active lens
2. Cluster nodes by relationship strength and lens weight
3. Merge clusters into representative nodes
4. Summarize inter-cluster edges
5. Return compressed subgraph

The compression ratio is controlled by a target token budget.

## Lens-Dependent Coarsening

Different lenses produce different coarsened views:

- **Architecture lens**: merges by system component
- **Temporal lens**: merges by time period
- **Next-steps lens**: merges by action chain
- **Causal lens**: merges by cause-effect path

## Related Technical Concepts

- graph coarsening (Karypis & Kumar, 1998)
- hierarchical clustering
- multiscale graph representation
- graph summarization
- semantic compression

**Related to**: [Semantic Zoom](semantic-zoom.md), [Semantic Lenses](semantic-lenses.md)

**Implementation**: `wrap/drag/selector.py` — `compress()` method

**Status**: Basic node removal implemented. Full cluster merging planned.

## Questions This Project Addresses

- How can graph coarsening be driven by semantic lenses?
- How can compression preserve the most relevant relationships?
- How can coarsening adapt to different query types?
