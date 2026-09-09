---
type: process
name: edit
entrypoint: mumblewrap/api.py:SpecuLoop.edit
inputs: [propagator, graph, store]
outputs: [EditResult, graph (new nodes/edges)]
---

# edit

Human edits markdown, propagator diffs original vs edited, changes flow back into mumbleWRAP.

**Flow:** original_markdown + edited_markdown → FeedbackPropagator.process_edit → diff → new Node/Edge → Graph → Store.save.
**Human gate:** the human provides the edit itself.
**Does not hit:** emit (but depends on prior emit output).
