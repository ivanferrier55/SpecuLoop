---
type: object
name: lens
implementation: mumblewrap/core/lens.py
summary: Named view over the graph that reweights edges by relation type.
---

# Lens

A named projection that modifies how the graph is scored and compressed. Contains relation weights that scale edge forces during DRAG selection.

**Mutated by:** add_lens (graph stores it).
**Read by:** DRAGSelector (scoring), Translator (emit with lens), SemanticLearner (lens-aware compression).
