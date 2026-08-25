# SpecuLoop: Complete Self-Updating Reasoning Environment

SpecuLoop allows humans and agent swarms to collaboratively think, discover, implement, observe, and update the system over time.

---

## Purpose

SpecuLoop combines mumbleWRAP (semantic inertia), DRAG (dynamic RAG / semantic reasoning), agent orchestration, human feedback, tools/execution, and persistent system state into a continuous reasoning environment.

---

## What SpecuLoop Does

- **Agent orchestration**: coordinate multiple agents working on shared semantic state
- **Human feedback**: propagate corrections into the semantic layer
- **Self-extension**: propose new semantic structures when needed
- **Execution grounding**: tool failures become semantic constraints
- **Persistent state**: system state survives across sessions

---

## Components

| Component | Purpose |
|---|---|
| `self_extender.py` | Propose new primitives for unrecognized concepts |
| `propagator.py` | Propagate human edits and execution results into mumbleWRAP |
| `agents/` | Agent framework (planned) |
| `swarm/` | Multi-agent coordination (planned) |
| `orchestration/` | Task orchestration (planned) |

---

## The Operational Loop

```
Human / Agent Swarm
    ↕
SpecuLoop (orchestration + feedback)
    ↕
DRAG (reasoning + retrieval)
    ↕
mumbleWRAP (semantic inertia)
    ↕
Translations / Implementations / Tools
    ↕
Observed Reality
```

---

## Agent Infrastructure

The agent infrastructure may initially resemble OpenClaw-like systems. The agent framework is the operational infrastructure that allows SpecuLoop's semantic and reasoning systems to operate continuously. It is not the conceptual center.

---

## Status

Self-extension and feedback propagation implemented. Agent orchestration and swarm coordination planned.

**Related**: [mumbleWRAP](../mumblewrap/README.md), [DRAG](../drag/README.md), [ARCHITECTURE.md](../ARCHITECTURE.md)
