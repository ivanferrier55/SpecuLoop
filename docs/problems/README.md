# Problems

## Primary Problem: Semantic Solving

**Semantic solving** is the central problem SpecuLoop is exploring:

> How can an AI solve problems while preserving and evolving the meaning, relationships, context, provenance, uncertainty, and lessons that make its reasoning useful across time and transformations?

This is intentionally broader than AI memory. Memory is one substrate for solving the problem; the objective is meaningful semantic continuity and better problem solving.

The repository currently provides evidence for a narrower and more established observation: **semantic drift across translations**. A human intention can be interpreted by an AI, represented semantically, translated into implementation, executed, and observed, with meaning potentially changing at each step. SpecuLoop is an experimental attempt to preserve and propagate meaning through that chain.

The broader framing of semantic solving is an **organizing hypothesis**, not an experimentally proven result.

## Problem Map

### P0 — Foundational

1. **Preserve semantic continuity across time and transformations**
   - Meaning, relationships, context, provenance, and applicability can be preserved as experience moves between representations and across time.
2. **Determine what knowledge should be retained and how it should evolve**
   - The system must decide what becomes durable knowledge, how strongly it should be believed, and how new experience modifies existing knowledge without destroying useful history.

### P1 — Very High

3. **Retrieve the right semantic context without overwhelming the agent**
   - Select the relevant portion of persistent semantic structure for a particular reasoning task.
4. **Preserve provenance and uncertainty through reasoning**
   - Keep claims traceable to origins, evidence, assumptions, and confidence as they are reused and transformed.
5. **Turn failures and observations into reusable knowledge**
   - Convert corrections, experiments, failures, and execution observations into persistent knowledge that improves future behavior.

### P2 — High

6. **Propagate changes through interconnected knowledge safely**
   - Propagate relevant consequences when semantic knowledge changes without causing uncontrolled or incorrect updates.
7. **Prevent semantic drift and contradiction as knowledge evolves**
   - Represent competing, outdated, conditional, and superseded knowledge without silently collapsing it into a misleading truth.
8. **Ground semantic representations in execution**
   - Connect semantic understanding to actual implementation and observed execution so the system can test whether its understanding matches reality.

### P3 — Exploratory

9. **Enable controlled self-extension of the semantic substrate**
   - Allow semantic structures and capabilities to extend while preserving coherence, provenance, safety, and human interpretability.

## Existing Problem Documentation

The existing pages are narrower observations and problem-oriented explorations that feed into this map:

- [Semantic drift](semantic-drift.md)
- [Agent misunderstanding](agent-misunderstanding.md)
- [Code-language disconnect](code-language-disconnect.md)
- [Knowledge graph ambiguity](knowledge-graph-ambiguity.md)
- [Large context](large-context.md)
- [Token waste](token-waste.md)

These pages should be treated as evidence and exploratory framing, not as proof that the proposed solutions work.

## Evidence Discipline

For every problem, distinguish:

- **Established observation** — directly supported by repository behavior, tests, or explicit documentation.
- **Inference** — a reasonable interpretation of the evidence.
- **Hypothesis** — an unverified mechanism or expected outcome.

Importance is provisional and should change as evidence accumulates.

## Ultimate Direction

The long-term objective is not simply to build persistent AI memory. It is to determine whether an AI can maintain **meaningful semantic continuity while solving problems over time** — learning from experience without losing the relationships, context, provenance, uncertainty, and lessons that made that experience useful.
