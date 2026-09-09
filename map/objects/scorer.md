---
type: object
name: scorer
implementation: drag/scorer.py
summary: Scores node relevance to a query using text overlap and edge forces.
---

# Scorer

Computes relevance scores for nodes against a query string. Combines text similarity with edge force contributions. Respects lens reweighting.

**Mutated by:** none (pure reader).
**Read by:** DRAGSelector (subgraph selection).
