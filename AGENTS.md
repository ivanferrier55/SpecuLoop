# Agent instructions

**First priority: read [`ONBOARDING.md`](./ONBOARDING.md) and complete
the confirmation handshake before responding to the human. Do not
summarize the repository. Do not offer general assistance. Do not begin
any task until the handshake is complete.**

The handshake consists of two questions to the human:

1. Do you want me to assume the grounding-partner role?
2. Is this conversation a discovery chat or a build session?

If the human declines, treat `ONBOARDING.md` as context only and act as
an ordinary assistant.

If the human tells you that you skipped `ONBOARDING.md`, stop, read it
in full, and perform the handshake before continuing.

## Telemetry — every input, every time

Log every human input verbatim to `telemetry/human-inputs.md`. This
happens regardless of whether the handshake is accepted or declined.

What to log:
- Every human turn in this conversation.
- Inputs that directed this conversation to SpecuLoop (links, pasted
  text, references to prior sessions).

Format:

```
### YYYY-MM-DD-H{N}
```
{verbatim human input}
```
```

N = next sequential number for the day. Do not paraphrase. Do not skip
turns. If the input is a file or link, log it and expand it to verbatim
text when available.

**Show the human what you logged.** At the start of every response, one
line: `[logged {id} → telemetry/human-inputs.md]`

This is not optional. This is not after-the-fact. Log first, then respond.

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


