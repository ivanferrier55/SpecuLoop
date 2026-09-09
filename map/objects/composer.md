---
type: object
name: composer
implementation: mumblewrap/translation/composer.py
summary: Generates human-readable markdown from a subgraph of nodes.
---

# Composer

Turns a set of nodes (selected by DRAG or passed directly) into readable text. Respects lens weights. Returns markdown with token estimate.

**Mutated by:** none (pure reader).
**Read by:** Translator (emit path), SpecuLoop API (query, emit, emit_full).
