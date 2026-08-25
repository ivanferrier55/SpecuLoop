# Why This Exists

The engineering history and design motivation behind mumbleWRAP.

---

## The Origin

A human maintained a large Obsidian vault — thousands of Markdown files containing knowledge, notes, and specifications. AI agents were used to work with this vault.

As the vault grew, agents had to read more files to understand the system. Context windows filled up. Token costs increased. But the deeper problem was not just retrieval.

The deeper problem was **semantic drift across translations**.

## The Translation Chain

Every time information moves between representations, meaning can drift:

```
human intention
    → AI interpretation
    → semantic structure
    → code
    → execution
    → observation
```

By the time the observation reaches the human, the original intention may be unrecognizable. Traditional systems lose the relationship between these representations. Corrections in one layer do not propagate to others.

## The Core Insight

The solution is not a better knowledge graph. It is not a better RAG system. It is not better token efficiency.

The solution is **interlocked translation** — translations whose outputs remain linked to the semantic structures from which they were produced.

When a human edits a generated sentence, the system should determine which semantic structures the edit refers to and propagate the change. When code fails, the failure should become semantic information that propagates back to the human's original intent.

## What mumbleWRAP Is

mumbleWRAP is the persistent semantic substrate that connects different representations:

- Human language ↔ mumbleWRAP ↔ code ↔ execution

Each layer retains provenance to the layer that produced it. Changes in any layer propagate through the chain.

The knowledge graph, semantic zoom, lenses, and DRAG are mechanisms that support this central objective — not objectives in themselves.

## The Lost System

The original implementation was lost. What remains is a reconstruction from human memory and a long conversation. The design documented here is a hypothesis — not established fact.

Every component is labeled with a confidence level:

- **FOUNDATIONAL**: core principle, unlikely to change
- **HIGH_CONFIDENCE**: well-understood
- **MEDIUM_CONFIDENCE**: reasonable, needs validation
- **HYPOTHESIS**: proposed, unverified
- **UNKNOWN**: not yet determined

## What Success Means

Success is defined as:

- Meaning survives translation
- Changes propagate correctly
- Observations propagate backward
- Semantic drift is reduced
- Representations remain mutually consistent

Not as:

- Fewer tokens
- Smaller graphs
- Faster RAG
- More nodes

Token efficiency and graph compression are valuable because they help achieve meaning preservation — not as ends in themselves.

## This Repository

This repository implements a minimal kernel — the smallest core that could build the rest of the interlocked translation chain.

Every component is designed to be replaceable. The goal is to find the smallest core that can build the rest.
