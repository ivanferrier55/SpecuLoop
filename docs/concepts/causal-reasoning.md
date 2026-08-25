# Causal Reasoning in Semantic Graphs

Causal relationships are one of many edge types in the WRAP graph. They represent cause-effect structure alongside opposition, support, and dependency.

## How It Works

A causal edge:

```
A --[causes]--> B
```

has a force of +1.0 (positive, directed). Under a causal lens, this edge is emphasized. Under an architecture lens, it may be de-emphasized.

## Causal Chains

Multiple causal edges form chains:

```
time_pressure --[increases]--> speed
speed --[decreases]--> quality
quality --[decreases]--> user_satisfaction
```

These chains can be traversed to understand cascading effects.

## Opposition and Tradeoffs

Causal edges interact with oppositional edges:

```
speed --[decreases]--> quality
tooling --[decreases]--> (speed-opposes-quality tension)
```

The system represents tradeoffs as oppositional structures with mediating nodes.

## Related Technical Concepts

- causal graphs (Pearl, 2009)
- structural causal models
- causal inference
- causal discovery
- counterfactual reasoning

**Related to**: [Semantic Forces](semantic-forces.md), [Semantic Lenses](semantic-lenses.md)

**Status**: Causal edges are one of 12+ edge types. Full causal inference not implemented.

**Confidence**: MEDIUM — the representation is clear; inference is unimplemented.

## Questions This Project Addresses

- How can causal relationships be represented alongside other relationship types?
- How can causal chains be traversed for reasoning?
- How can tradeoffs be modeled as oppositional structures?
