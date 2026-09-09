---
type: object
name: self-extender
implementation: speculoop/self_extender.py
summary: Proposes new semantic primitives for unrecognized concepts.
---

# SelfExtender

When the system encounters a concept it can't represent with existing primitives, SelfExtender proposes a new node. The proposal is provisional until confirmed.

**Mutated by:** propose (creates proposal), confirm (adds to graph).
**Read by:** SpecuLoop API (propose, confirm_proposal).
