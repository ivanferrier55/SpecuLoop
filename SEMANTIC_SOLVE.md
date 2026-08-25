# Semantic Solve and Self-Update

**Status:** Provisional reconstruction  
**Date:** 2026-08-26

This document records the current reconstruction of the core loop. Historical facts, strong recollections, and implementation hypotheses are deliberately separated because the original implementation is unavailable.

## Core invariant

A new statement is treated as a **clue**. The system first tries to express it using the existing semantic basis. The important question is not simply whether the text can be summarized, but whether the current basis preserves enough structure for the intended decoder, lens, and task to reconstruct the meaning.

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

This is the experimental heart of SpecuLoop.

## Compression is decoder- and lens-aware

Compression is relative to the decoder, lens, and task. A strong model may reconstruct a clue from a smaller representation than a weaker model. Therefore the target representation is better described as:

```text
R* = f(semantic structure, decoder capability, lens, task)
```

This is a design hypothesis, not a recovered historical equation.

The same graph can therefore have multiple useful projections:

```text
graph
 ├─ onboarding lens
 ├─ time lens
 ├─ next-step lens
 ├─ implementation lens
 └─ system-overview lens
```

Semantic zoom should follow the active projection rather than simply hiding nodes at a fixed visual threshold.

## Generative primitive test

A candidate primitive can be isolated and supplied to a decoder, for example an LLM adapter. The decoder attempts to reconstruct the clue set already represented by that basis.

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

Different decoders can be measured separately. This allows the hypothesis that semantic compression is **decoder-relative** to become an experiment rather than an assumption.

## Primitive discovery and refactoring

Candidate bases should trade explanatory power against complexity. A provisional objective is:

```text
basis score = reconstruction error + complexity penalty
```

The intended behavior is a minimum sufficient semantic basis. If one new primitive explains evidence better than several existing primitives, the system should eventually be able to refactor toward it rather than accumulating nodes indefinitely.

Refactoring is deliberately non-destructive:

```text
P1 ─┐
P2 ─┼──→ candidate P4
P3 ─┘

P1, P2, P3 remain as historical nodes
P4 records that it superseded them
```

This preserves provenance and allows later evidence to challenge the refactor.

## Uncertainty is actionable

Uncertainty means that the current representation cannot adequately compress or reconstruct the clue. It should trigger investigation rather than a generic clarification request.

Possible evidence sources include:

- human clarification;
- agent-generated examples and counterexamples;
- tool execution;
- constraints and failures from reality;
- alternative primitive hypotheses;
- decoder reconstruction tests;
- existing external solutions.

Examples can therefore be **tests** rather than causes. A test example may distinguish competing semantic interpretations or demonstrate whether a primitive actually explains a problem.

## Evidence is part of the semantic state

The system should retain why its representation changed:

```text
clue
primitive hypothesis
test case
prediction
observed result
compression score
uncertainty
lens / task / decoder
basis decision
```

This makes the loop auditable and gives future agents access to failed hypotheses instead of forcing them to rediscover them.

The current kernel stores an evidence node for each semantic compression observation.

## Scientific-method interpretation

The loop is analogous to a scientific method applied to the representation itself:

| Scientific method | SpecuLoop |
|---|---|
| observation | clue |
| hypothesis | candidate primitive / basis |
| prediction | decoder reconstruction / expected clue |
| experiment | generated test case, tool call, or execution |
| measurement | compression / reconstruction score |
| counterexample | unexplained or contradictory evidence |
| theory revision | primitive replacement/refactoring |
| replication | additional clues and tests |

The analogy should not be treated as proof that the system is scientifically valid. It is a useful design model for preventing semantic compression from becoming unchecked speculation.

## Existing-solution incorporation

A major application is searching for and incorporating existing solutions into a new problem rather than treating retrieved documents as isolated answers.

```text
problem
   ↓
semantic decomposition
   ↓
existing primitive search
   ↓
existing solution search
   ↓
translate candidate solutions into common semantic structure
   ↓
compare
   ├─ reusable pieces
   ├─ contradictions
   ├─ missing relationships
   └─ implementation constraints
   ↓
reuse → combine → test
              │
              └──→ invent new primitive only when needed
```

The goal is not merely to retrieve prior art. It is to determine **which existing structures already explain parts of the problem and what genuinely new relationship, integration, or primitive remains**.

## Relationship to WRAP, DRAG, and SpecuLoop

```text
Mumble
  ↕
WRAP: semantic representation / primitives
  ↕
DRAG: lens-specific retrieval, forces, zoom, numerical solve
  ↕
SpecuLoop: agents, tools, feedback, experiments, reality constraints
```

The same semantic state can be projected through different lenses. The numerical DRAG model remains an open reconstruction target rather than something the current implementation claims to have recovered exactly.

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
- the system should update from human, agent, tool, and execution feedback;
- semantic zoom should vary by lens rather than only by visual scale;
- representations should remain interlocked across human language, semantic state, code, and execution.

**Still hypotheses:**

- the exact WRAP syntax;
- the exact primitive vocabulary;
- the historical DRAG equations;
- whether the original system literally used an LLM reconstruction test;
- the exact meaning of remembered backpropagation;
- the original persistence format;
- the exact scoring/force functions used by the lost implementation.

The implementation should preserve these distinctions rather than hard-code guesses as facts.
