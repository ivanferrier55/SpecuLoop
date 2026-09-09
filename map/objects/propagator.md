---
type: object
name: propagator
implementation: speculoop/propagator.py
summary: Propagates human edits back into the semantic graph.
---

# FeedbackPropagator

Compares original and edited markdown to detect what changed, then propagates those changes back into mumbleWRAP as new nodes or modified edges.

**Mutated by:** edit (adds nodes/edges from diff).
**Read by:** SpecuLoop API (edit).
