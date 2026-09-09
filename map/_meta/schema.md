# Schema

Card types: `object` (noun) and `process` (verb).

## Object card

```yaml
type: object
name: slug
implementation: relative/path.py
summary: one sentence
```

Fields:
- `name` — kebab-case slug, matches the card filename.
- `implementation` — the code that owns this noun.
- `summary` — what it is, in one sentence.
- `described_in` — any spec/design doc that describes it (optional).

## Process card

```yaml
type: process
name: slug
entrypoint: file:function or file:class.method
inputs: [things it reads]
outputs: [things it writes/returns]
```

Fields:
- `name` — kebab-case slug, matches the card filename.
- `entrypoint` — the code a later agent edits to change this behavior.
- `inputs` / `outputs` — exact module-level dependencies.

## Effects index

Format: one line per process → objects it mutates or reads.

`process-slug → object-slug (read | write)`

Hits = the card actually changes. Does-not-hit = the obvious next noun that is wrong.
