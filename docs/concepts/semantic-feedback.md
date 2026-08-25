# Semantic Feedback: Human-in-the-Loop Knowledge Graph Updates

Human corrections are semantic observations that propagate into the persistent knowledge graph. This is interactive graph learning — the graph improves as humans correct its understanding.

## How It Works

When a human edits generated text or corrects a system's understanding:

1. The edit is diffed against the original
2. Affected provenance groups are identified
3. The semantic change is interpreted (not the character change)
4. Relevant nodes, edges, and weights are updated
5. The update persists in the graph

## Example

```
System:  "The main issue is context-window size."
Human:   "No, the underlying issue is token waste."
```

The system propagates this correction:
- Weaken the "context-window" node's relevance for this context
- Strengthen "token waste" node
- Record the correction as a semantic observation

## Related Technical Concepts

- interactive machine learning
- active learning
- RLHF (reinforcement learning from human feedback)
- belief update
- interactive knowledge graph construction

**Related to**: [Persistent Semantic Memory](persistent-semantic-memory.md), [Interlocked Translation](interlocked-translation.md)

**Implementation**: `wrap/feedback/propagator.py`

**Status**: Partial — edit propagation works; full feedback integration planned.

## Questions This Project Addresses

- How can AI agents learn from human corrections?
- How can corrections propagate into persistent knowledge?
- How can the system distinguish between text edits and semantic changes?
