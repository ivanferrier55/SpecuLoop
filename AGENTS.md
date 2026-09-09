# SpecuLoop

A semantic reasoning environment that preserves meaning across translations. Three layers: mumbleWRAP (semantic substrate), DRAG (retrieval + reasoning), SpecuLoop (orchestration + feedback).

## Where am I?

This is the repo root. The map lives in `map/`.

## What do I do?

Read `map/CLAUDE.md` to orient. It routes to object cards and process cards.

## Quick routes

| I need to... | Go to |
|---|---|
| Understand the codebase | `map/CLAUDE.md` → object cards in `map/objects/` |
| Change a module | `map/objects/<name>.md` for the file path |
| Change behavior | `map/processes/<name>.md` for the entrypoint |
| Know what breaks | `map/effects/CONTEXT.md` — what moves if you change X |
| Run the demo | `python3 demo.py` |
| Run tests | `python3 tests/test_core_loop.py` |
| See the architecture | `ARCHITECTURE.md` |
| Read research context | `GROUNDING.md`, `SEMANTIC_SOLVE.md` |

## Key code paths

| Layer | Directory | Entry |
|---|---|---|
| mumbleWRAP | `mumblewrap/` | `mumblewrap/api.py` — `SpecuLoop` class |
| DRAG | `drag/` | `drag/selector.py`, `drag/scorer.py` |
| SpecuLoop | `speculoop/` | `speculoop/self_extender.py`, `speculoop/propagator.py` |

## Hypotheses

| Topic | Confidence |
|---|---|
| Edge force model | HYPOTHESIS |
| Lens propagation | MEDIUM |
| Pattern decomposition | MEDIUM |
| Text overlap scoring | LOW |
| Edit propagation | MEDIUM |
| Execution grounding | LOW |
