# Semantic Forces

**Search terms**: semantic relationship forces, attraction repulsion graph, knowledge graph reasoning

## What Are Semantic Forces?

Semantic forces are the numeric strengths and directions of relationships in the WRAP graph. They determine how nodes attract or repel each other.

## The Conceptual Model

```
force(edge, lens, context) → numeric magnitude
```

Each edge type has a base force:

| Relation | Direction | Sign | Example |
|---|---|---|---|
| `causes` | forward | +1.0 | A → B |
| `increases` | forward | +1.0 | speed → quality_loss |
| `decreases` | forward | -1.0 | speed → quality |
| `supports` | bidirectional | +1.0 | A ↔ B |
| `opposes` | bidirectional | -1.0 | A ↔ B |
| `requires` | backward | +1.0 | B requires A |
| `demonstrates` | forward | +0.5 | evidence → claim |
| `clarifies` | forward | +0.3 | explanation → concept |

## Force Examples

### Problem ↔ Solution

The `opposes` relationship creates repulsion — the graph separates problem and solution nodes, with intermediate concepts forming paths between them.

### Speed ↑ → Quality ↓

The `increases` and `decreases` relationship creates a tradeoff loop — increasing speed pushes quality down, and vice versa.

### Evidence → Hypothesis

The `demonstrates` relationship creates a directional pull — evidence nodes attract hypothesis nodes.

## Lens Modification

Forces are modified by the active lens:

```
effective_force(edge, lens) = base_force(edge) × lens_weight(edge, lens)
```

A `causal` lens might double the weight of `causes` edges while halving `supports` edges.

**Implementation status**: Base forces are implemented in `wrap/core/edge.py`. Lens modification is implemented in scoring. Full force-directed layout is planned.
