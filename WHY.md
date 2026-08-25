# Why This Exists

The engineering history and design motivation behind SpecuLoop.

---

## The Origin

A human maintained a large Obsidian vault — thousands of Markdown files containing knowledge, notes, and specifications. AI agents were used to work with this vault.

As the vault grew:

```
more knowledge
    →
more files
    →
agents must read many files to onboard
    →
context-window pressure
    →
token waste
    →
agent reasoning degrades
```

## RAG Was Considered

Retrieval-Augmented Generation (RAG) appeared to be the obvious solution. But RAG has limitations:

- It retrieves by similarity, not by semantic relationship
- It does not learn which retrievals were useful
- It does not represent causation, opposition, or dependency
- It does not compress knowledge at different abstraction levels

## The Semantic Problem

The underlying problem was not just retrieval. It was **semantic representation**:

- How do you represent that "speed and quality are in tension"?
- How do you represent that "tooling reduces that tension"?
- How do you represent that "testing requires time"?
- How do you represent that a tool call failed because of a missing API key?

These are not document retrieval problems. They are **knowledge representation** problems.

## The Graph Insight

The solution required a graph — not a flat document store, not a vector database, but a graph where:

- Nodes represent concepts, actions, entities
- Edges represent typed relationships with numeric forces
- The graph persists across sessions
- The graph updates incrementally as new information arrives

## Semantic Zoom

A large graph is useless if you have to load it all into context. The graph needs to compress — but not by truncation. By **semantic zoom**:

- Zoomed in: detailed nodes and relationships
- Zoomed out: highly related structures merge
- Different lenses produce different compressed views

A question about architecture compresses differently than a question about timeline.

## Lenses

Different questions need different views. The same graph should answer:

- "What is the system architecture?" → architecture lens
- "What should I do next?" → next-steps lens
- "What happened last week?" → temporal lens
- "What opposes this idea?" → opposition lens

Lenses are not pre-computed views. They are weight modifiers that change how the graph is scored and compressed.

## Interlocked Translation

Humans read and edit Markdown. Agents read and write Markdown. The graph is the source of truth. Therefore:

```
graph → Markdown (with provenance)
human edits Markdown
Markdown → graph update
```

This bidirectional translation — interlocked translation — means humans and agents can collaborate on the same knowledge base without losing semantic structure.

## Constraints and Reality

When an agent tries to do something and fails — the failure should not disappear. It should become semantic information:

```
desired operation
    →
attempted execution
    →
failure
    →
constraint recorded in graph
```

The system learns from what it cannot do.

## Self-Extension

When new input cannot be expressed using existing graph structures, the system should propose new primitives. The graph grows organically, not through manual schema design.

## The Lost System

The original implementation was lost. What remains is a reconstruction from human memory and a long conversation. The design documented here is a hypothesis — not established fact.

Every component is labeled with a confidence level:

- **FOUNDATIONAL**: core principle, unlikely to change
- **HIGH_CONFIDENCE**: well-understood
- **MEDIUM_CONFIDENCE**: reasonable, needs validation
- **HYPOTHESIS**: proposed, unverified
- **UNKNOWN**: not yet determined

## This Repository

This repository implements a minimal kernel — the smallest core that could build the rest:

- Graph model (nodes, edges, lenses)
- Translation (decompose, compose)
- DRAG (score, select, compress)
- Self-extension (propose new primitives)
- Feedback (propagate edits)
- Persistence (JSON save/load)

Every component is designed to be replaceable. Better algorithms, better mathematics, better primitives, or recovered artifacts can replace provisional implementations without destroying the architecture.

The goal is not to build the final system. The goal is to **find the smallest core that can build the rest**.
