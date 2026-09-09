# map/ — SpecuLoop system map

Catalog of every noun and verb in the SpecuLoop codebase. A later agent reads this file to know what exists, then follows one card to do its work.

## What is SpecuLoop?

A semantic reasoning environment that preserves meaning across translations. Three layers: mumbleWRAP (semantic substrate), DRAG (retrieval + reasoning), SpecuLoop (orchestration + feedback).

## Where am I?

| Path | Role |
|---|---|
| `map/CLAUDE.md` | This file — you are here |
| `map/objects/` | Object cards (nouns): the modules and types |
| `map/processes/` | Process cards (verbs): the operations |
| `map/effects/CONTEXT.md` | Effects index: what moves if you change X |
| `map/_meta/schema.md` | Card format definitions |
| `../mumblewrap/` | mumbleWRAP source code |
| `../drag/` | DRAG source code |
| `../speculoop/` | SpecuLoop orchestration source |
| `../demo.py` | Live demo of the full loop |

## How to change something

1. Find the object you want to change in `map/objects/`.
2. Open `map/effects/CONTEXT.md` — what else moves if you change it?
3. Read the object card for the exact file path.
4. Read any process card that lists this object as output.
5. Edit the code. Run `python3 tests/test_core_loop.py` to verify.

## Quick reference

| Layer | Modules | Card directory |
|---|---|---|
| mumbleWRAP | `mumblewrap/core/`, `mumblewrap/translation/`, `mumblewrap/persistence/` | `objects/` |
| DRAG | `drag/` | `objects/` |
| SpecuLoop | `speculoop/` | `objects/` |
| Interface | `mumblewrap/api.py` | `objects/speculoop-api.md` |
