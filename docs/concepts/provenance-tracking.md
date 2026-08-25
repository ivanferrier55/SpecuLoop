# Provenance Tracking for AI-Generated Text

Provenance is the mapping from generated output back to the specific semantic structures that produced it. Every generated sentence carries metadata identifying its source nodes and edges.

## How It Works

When the system generates text:

```markdown
<!-- provenance: nodes=[speed,quality] edges=[opposes] lens=default -->
Speed opposes quality.
<!-- /provenance -->
```

The provenance metadata links the sentence to:
- Node `speed`
- Node `quality`
- Edge `opposes`
- Active lens `default`

## Why It Matters

Provenance enables:

1. **Verification**: check which knowledge produced an answer
2. **Correction**: edit the output and propagate changes back
3. **Debugging**: understand why the system produced a particular output
4. **Update**: modify the graph through the generated text

## Semantic Reversibility

Provenance enables semantic reversibility:

```
semantic representation → natural language (meaning preserved)
edited natural language → semantic update (meaning preserved)
```

This is NOT character-level reversal. It is meaning-level reversal.

## Related Technical Concepts

- explainable AI
- attribution
- source tracing
- chain-of-thought reasoning
- interpretable AI outputs

**Related to**: [Interlocked Translation](interlocked-translation.md), [Semantic Feedback](semantic-feedback.md)

**Implementation**: `wrap/translation/composer.py`, `wrap/feedback/propagator.py`

**Status**: Provenance metadata generated and parsed. Edit propagation partially implemented.

## Questions This Project Addresses

- How can AI-generated text be traced back to source knowledge?
- How can provenance survive graph updates?
- How can provenance enable bidirectional translation?
