---
type: process
name: propose
entrypoint: mumblewrap/api.py:SpecuLoop.propose
inputs: [self-extender]
outputs: [Proposal]
---

# propose

Generates a candidate primitive for an unrecognized concept. The proposal is provisional.

**Flow:** text → SelfExtender.propose_primitive → Proposal (not yet in graph).
**Human gate:** confirm_proposal to accept or modify.
**Does not hit:** ingest (separate entry point).
