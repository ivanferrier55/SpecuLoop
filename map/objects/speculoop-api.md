---
type: object
name: speculoop-api
implementation: mumblewrap/api.py
summary: Public interface class that wires all layers together.
---

# SpecuLoop (API class)

The single entry point that wires mumbleWRAP, DRAG, SpecuLoop layers, and persistence into a cohesive interface. Exposes: ingest, learn, emit, query, edit, propose, confirm_proposal, accept_candidate, propose_refactor, accept_refactor.

**Mutated by:** all mutation methods delegate to inner components then call store.save().
**Read by:** demo.py, tests, user code.
