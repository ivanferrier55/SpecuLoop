# Relation Vocabulary and Semantic Forces

Edge relations accepted by `know`. Forces come from `RELATION_FORCES` in
`mumblewrap/core/edge.py` (HYPOTHESIS values — replaceable).

| Relation | Meaning | Direction | Force sign |
|---|---|---|---|
| `causes` | A makes B happen | forward | +1.0 |
| `increases` | A raises B | forward | +1.0 |
| `decreases` | A lowers B | forward | -1.0 |
| `supports` | A backs B | bidirectional | +1.0 |
| `opposes` | A conflicts with B | bidirectional | -1.0 |
| `requires` | A needs B | backward | +1.0 |
| `motivates` | A drives B | forward | +0.7 |
| `solves` | A fixes B | forward | +0.8 |
| `clarifies` | A explains B | forward | +0.3 |
| `demonstrates` | A shows B | forward | +0.5 |
| `contains` | A includes B | forward | 0.0 |
| `part_of` | A belongs to B | backward | 0.0 |

## Choosing a relation

- Improvement/deterioration → `increases` / `decreases`
- Causal claim → `causes`
- Dependency → `requires` (subject needs the object)
- Evidence/backing → `supports`
- Conflict/tradeoff → `opposes`
- Composition → `contains` / `part_of`

## Status lifecycle

`hypothesis` → (tested/verified) → `observed` → (refuted) → `superseded`

Every status change records a source when one is provided. Provenance is the
trace from a claim back to the evidence that grounded it.
