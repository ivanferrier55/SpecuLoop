# Self-Extension Specification

**Status**: Provisional — reconstructed from memory
**Date**: 2026-08-26
**Confidence**: See per-section labels

---

## 1. Overview

Self-extension is the ability of the semantic basis to change when existing structures cannot adequately compress or reconstruct new evidence.

The key distinction is **proposal versus acceptance**: an unresolved clue can generate a candidate primitive without immediately making that candidate authoritative.

---

## 2. Core Flow

```text
new clue
  ↓
attempt decomposition into existing primitives
  ↓
adequate?
 ├─ yes → reuse + strengthen usage
 └─ no  → uncertainty
             ↓
       generate hypotheses
             ↓
       generate examples/tests
             ↓
       evaluate candidate bases
             ↓
       choose minimum sufficient basis
             ↓
       accept / modify / reject
```

This replaces a simple "unknown word → create node" strategy with semantic model selection.

---

## 3. Candidate Primitive

A candidate records:

- unresolved clue/evidence;
- proposed primitive;
- alternative decompositions;
- supporting examples/tests;
- predicted reconstruction;
- observed reconstruction;
- compression score;
- decoder score when available;
- uncertainty;
- status: `pending`, `accepted`, `modified`, or `rejected`.

Candidates remain provisional until accepted.

---

## 4. Active Testing

Uncertainty can cause the system to construct its own examples rather than immediately asking the human.

An example may:

- test a primitive;
- distinguish two candidate interpretations;
- demonstrate a relationship;
- expose a contradiction;
- provide a regression test for a previously learned structure.

Agents can generate and execute such tests when they have the required capabilities.

---

## 5. Decoder Reconstruction Test

A candidate primitive or basis can be isolated and supplied to a decoder. The decoder attempts to reconstruct the clue set that motivated the primitive.

```text
candidate basis
      ↓
    decoder
      ↓
predicted clue set
      ↕
observed clue set
      ↓
reconstruction score
```

Different decoders may require different representation granularity. Therefore decoder capability is part of the compression context.

This mechanism is currently a **hypothesis**, but the kernel exposes an optional decoder callback so it can be tested experimentally.

---

## 6. Basis Selection

The current provisional objective is:

```text
basis score = reconstruction error + complexity penalty
```

The desired behavior is to prefer the smallest basis that adequately explains the evidence. This permits semantic refactoring:

```text
old: P1 + P2 + P3
          ↓
new:       P4
```

when P4 captures the same evidence with better reconstruction and lower complexity.

The exact historical objective function is unknown.

---

## 7. Learning from Feedback

Evidence comes from multiple sources:

- human feedback;
- agent-generated tests;
- tool results;
- execution failures;
- constraints;
- future observations.

All should be represented as evidence rather than as a separate memory system.

Repeated confirmation strengthens a semantic structure. Contradictory evidence increases uncertainty and may trigger basis revision.

---

## 8. Guardrails

- Never hide provisional status.
- Preserve the evidence trail for every primitive change.
- Prefer reuse before creating a new primitive.
- Do not equate graph degree with semantic importance.
- Prevent uncontrolled primitive explosion.
- Allow rollback/refactoring when a later basis explains earlier evidence better.
- Keep historical claims separate from reconstruction hypotheses.
