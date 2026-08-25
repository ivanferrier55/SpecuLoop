# Interlocked Translation: Preserving Meaning Across Representations

Interlocked translation is the central architectural idea of mumbleWRAP. An interlocked translation is a translation whose output remains linked to the semantic structures from which it was produced.

## The Core Property

```
source changes
    → semantic representation updates
    → downstream translations can update

downstream observations
    → semantic structures update
    → upstream representations can update
```

This bidirectional linking means meaning can survive translation between human language, semantic structures, code, and execution.

## The Translation Chain

mumbleWRAP interlocks four representations:

- **Human language** ↔ mumbleWRAP (decompose / compose with provenance)
- **mumbleWRAP** ↔ **Code** (semantic structures → implementation)
- **Code** ↔ **Execution** (implementation → observed behavior)
- **Execution** ↔ **mumbleWRAP** (feedback → semantic update)

## How It Works

### mumbleWRAP → Human Language (Emission)

The graph generates text with provenance metadata:

```markdown
<!-- provenance: nodes=[speed,quality] edges=[opposes] lens=default -->
Speed opposes quality.
<!-- /provenance -->
```

### Human Language → mumbleWRAP (Ingestion)

Text is decomposed into graph structures:

```
"Speed and quality are in tension"
    ↓
Node[speed] --opposes--> Node[quality]
```

### Edited Language → mumbleWRAP (Feedback)

Human edits propagate back:

```
Original:  "Speed opposes quality."
Edited:    "Speed opposes quality, but good tooling reduces this tension."
    ↓
New nodes: [tooling]
New edges: tooling --decreases--> (speed-opposes-quality tension)
```

### Execution → mumbleWRAP (Grounding)

Tool failures and constraints become semantic information:

```
intended behavior → mumbleWRAP → code → execution → observation
    → semantic feedback → mumbleWRAP (updated)
```

## Why It Matters

Without interlocked translation:
- Generated text cannot be traced to source knowledge
- Human edits do not update the knowledge base
- Execution failures disappear as transient errors
- Specifications and implementations drift apart

With interlocked translation:
- Every output has provenance
- Every correction propagates
- Every failure becomes knowledge
- Representations stay mutually consistent

## Related Technical Concepts

- bidirectional programming
- natural language code synchronization
- program synthesis
- bidirectional transformations
- source-target synchronization

**Related problems**: [code-language disconnect](../problems/code-language-disconnect.md), [provenance](provenance-tracking.md)

**Implementation**: `wrap/translation/`, `wrap/feedback/propagator.py`

**Status**: Natural language ↔ mumbleWRAP implemented. Code and execution translation planned.
