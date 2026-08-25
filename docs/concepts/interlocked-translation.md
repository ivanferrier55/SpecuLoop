# Interlocked Translation

**Search terms**: bidirectional programming, natural language code synchronization, bidirectional natural language representation, program synthesis

## What Is Interlocked Translation?

Interlocked translation is the bidirectional mapping between natural language and semantic structures:

```
Natural language (Mumble)
    ↕
Semantic graph (WRAP)
    ↕
Materialized views (Markdown)
    ↕
Code / tools / execution
```

The "interlocked" property means that changes in one representation propagate to the others.

## How It Works

### WRAP → Mumble (Emission)

The graph generates natural language with provenance metadata:

```markdown
<!-- provenance: nodes=[speed,quality] edges=[opposes] lens=default -->
Speed opposes quality.
<!-- /provenance -->
```

### Mumble → WRAP (Ingestion)

Natural language is decomposed into graph structures:

```
"Speed and quality are in tension"
    ↓
Node[speed] --opposes--> Node[quality]
```

### Edited Mumble → WRAP (Feedback)

Human edits propagate back:

```
Original:  "Speed opposes quality."
Edited:    "Speed opposes quality, but good tooling reduces this tension."
    ↓
New nodes: [tooling]
New edges: tooling --decreases--> (speed-opposes-quality tension)
```

## Natural Language ↔ Code

The intended long-term relationship:

```
English specification
    ↕ interlocked translation
Semantic graph (WRAP)
    ↕ code generation
Executable code
    ↕ execution feedback
Results → semantic update
```

Changes in the specification propagate to code. Execution failures propagate back to the specification as constraints.

**Implementation status**: Mumble ↔ WRAP translation works. Code translation is planned.

## Questions This Project Addresses

- How can generated natural language remain linked to semantic structures?
- How can human edits propagate back into a knowledge graph?
- How can specifications, code, and execution results remain synchronized?

## Related Technical Concepts

- bidirectional programming
- natural language code synchronization
- program synthesis
- bidirectional transformations
- source-target synchronization
