---
type: object
name: semantic-learner
implementation: mumblewrap/semantic.py
summary: Observes clues, measures basis adequacy, and proposes/prunes semantic primitives.
---

# SemanticLearner

The experimental core of SpecuLoop. Observes incoming text, measures how well the current basis explains it, proposes provisional primitives when the basis is inadequate, and manages the accept/refactor lifecycle.

**Mutated by:** observe (scores + potential candidate), accept_candidate (adds primitive), accept_refactor (replaces nodes).
**Read by:** SpecuLoop API (learn, accept_candidate, propose_refactor, accept_refactor).
