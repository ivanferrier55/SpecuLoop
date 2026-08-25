# Semantic Solve and Self-Update

**Status:** Provisional reconstruction
**Date:** 2026-08-26

This document records the newest reconstruction of the core loop. It is deliberately separated from historical claims: the lost implementation is not available, so mathematical details and exact primitive names remain hypotheses.

## Core invariant

A new statement is treated as a **clue**. The system first tries to express it using the existing semantic basis. The important question is not simply whether the text can be summarized, but whether the current basis preserves enough structure for the intended decoder and task to reconstruct the meaning.

```text
clue
  ↓
existing basis
  ↓
compression / decomposition
  ├─ adequate → reuse + strengthen
  └─ inadequate → uncertainty
                    ↓
              hypotheses / tests
                    ↓
             candidate primitives
                    ↓
          reconstruction evaluation
                    ↓
            extend or refactor basis
```

## Decoder-aware compression

Compression is relative to the decoder and lens. A strong model may reconstruct a clue from a smaller representation than a weaker model. Therefore the target representation is better described as:

```text
R* = f(semantic structure, decoder capability, lens, task)
```

This is a design hypothesis, not a recovered historical equation.

## Generative primitive test

A candidate primitive can be isolated and supplied to a decoder (for example, an LLM adapter). The decoder attempts to reconstruct the existing clue set. The generated output is compared with the observations.

```text
primitive basis
      ↓
   decoder
      ↓
predicted clues
      ↕
actual clues
      ↓
reconstruction error
```

A primitive is therefore valuable when it is not merely a compact label, but captures structure that allows useful prediction or reconstruction.

The current Python kernel supports an optional decoder callback. It uses deterministic token overlap for the baseline score so the mechanism can be tested without selecting an LLM provider.

## Primitive discovery

Candidate bases should trade explanatory power against complexity. A provisional objective is:

```text
basis score = reconstruction error + complexity penalty
```

The intended behavior is minimum sufficient semantic basis: if a new primitive explains the evidence better than several existing primitives, the system can eventually refactor toward it rather than accumulating nodes indefinitely.

## Uncertainty is actionable

Uncertainty means that the current representation cannot adequately compress or reconstruct the clue. It should trigger investigation rather than a generic clarification request.

Possible evidence sources include:

- human clarification;
- agent-generated examples and test cases;
- tool execution;
- constraints and failures from reality;
- alternative primitive hypotheses;
- decoder reconstruction tests.

Examples can therefore be **tests** rather than causes. A test example may distinguish competing semantic interpretations or demonstrate whether a primitive actually explains a problem.

## Persistent self-update

The system should retain the evidence used to change its semantic basis:

```text
clue
primitive hypothesis
supporting evidence
test case
prediction
observed result
compression score
uncertainty
basis decision
```

This makes the reconstruction process itself persistent and auditable. Future evidence can revisit an earlier primitive decision instead of treating it as immutable truth.

## Relationship to WRAP, DRAG, and SpecuLoop

```text
Mumble
  ↕
WRAP: semantic representation / primitives
  ↕
DRAG: lens-specific retrieval, forces, zoom, numerical solve
  ↕
SpecuLoop: agents, tools, feedback, reality constraints
```

The same semantic state can be projected through different lenses. Zoom is therefore not just a visual hide/show operation: it is a task- and decoder-dependent projection of the graph.

## Historical confidence

**Strongly supported by the conversation:**

- existing structures should be reused when possible;
- reuse frequency matters;
- semantic uncertainty is meaningful;
- new primitives can be generated;
- a smaller sufficient primitive basis is desirable;
- old primitives may be replaced by better ones;
- examples can be generated to test hypotheses;
- different AI systems may require different representation granularity;
- semantic lenses alter what information is relevant;
- the system should update from human, agent, tool, and execution feedback.

**Still hypotheses:**

- the exact WRAP syntax;
- the exact primitive vocabulary;
- the historical DRAG equations;
- whether the original system literally used an LLM reconstruction test;
- the exact meaning of remembered backpropagation;
- the original persistence format.

The implementation should preserve these distinctions rather than hard-code guesses as facts.
