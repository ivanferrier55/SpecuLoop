---
type: object
name: store
implementation: mumblewrap/persistence/store.py
summary: JSON persistence for the semantic graph.
---

# Store

Serializes and deserializes the full graph to/from a JSON file. Called after every mutation.

**Mutated by:** save (writes JSON).
**Read by:** SpecuLoop API (init loads graph), SpecuLoop methods (save after mutation).
