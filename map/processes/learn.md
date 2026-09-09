---
type: process
name: learn
entrypoint: mumblewrap/api.py:SpecuLoop.learn
inputs: [semantic-learner, translator, graph, store]
outputs: [SemanticSolveResult, graph]
---

# learn

The grounding loop. Observes a clue, measures basis adequacy, optionally proposes a candidate primitive, then commits the ordinary translation.

**Flow:** text → SemanticLearner.observe (scores + candidate) → Translator.ingest → Store.save → SemanticSolveResult.
**Human gate:** candidate remains provisional until accept_candidate is called.
**Does not hit:** emit.
