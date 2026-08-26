# Grounding

Grounding is the source-agnostic input layer for SpecuLoop.

A grounding is evidence that can constrain the semantic model. Human input is
one grounding source, but it is not the only one. Other sources can include
artifacts, code, tool results, execution results, experiments, agent reports,
constraints, and historical evidence.

## Core rule

```text
source → grounding → semantic compression → mumbleWRAP → lens/DRAG
```

The storage backend is deliberately separate from the semantic representation.
A future implementation may replace the current graph persistence without
changing the meaning of a grounding.

## Type and strength

Each grounding has:

- `kind`: provenance/source category
- `strength`: a normalized 0..1 influence/confidence value
- `provenance`: information about where it came from
- `metadata`: additional source-specific information

Type and strength are separate. A human statement can be strong evidence about
intent while a tool result can be strong evidence about execution.

## API

```python
from mumblewrap.api import SpecuLoop

loop = SpecuLoop()
result = loop.ground(
    "The tool rejects files above the configured limit.",
    kind="tool",
    strength=0.95,
    provenance={"tool": "example"},
)
```

Groundings are evaluated before a new primitive is accepted. Low compression
produces a provisional candidate and uncertainty; it does not silently turn
the observation into a permanent primitive.

`learn(text)` remains as a compatibility alias for a human grounding.

## Historical reconstruction rule

When reconstructing the original system, preserve raw grounding and provenance
rather than converting hypotheses into facts. The semantic basis may change;
the evidence that caused the change must remain inspectable.
