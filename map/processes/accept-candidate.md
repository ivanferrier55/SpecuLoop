---
type: process
name: accept-candidate
entrypoint: mumblewrap/api.py:SpecuLoop.accept_candidate
inputs: [semantic-learner, graph, store]
outputs: [Node, graph]
---

# accept_candidate

Promotes a provisional primitive from SemanticLearner into the permanent graph.

**Flow:** candidate Node → SemanticLearner.accept_candidate → added to graph → Store.save.
**Human gate:** only called explicitly after review.
**Does not hit:** propose (that's the prior step).
