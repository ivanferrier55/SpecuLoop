# WRAP: Persistent Semantic State

WRAP is the core semantic knowledge graph of SpecuLoop. It is the authoritative store of all semantic information.

## Structure

- **Nodes**: concepts, actions, entities, properties, states, constraints
- **Edges**: typed relationships with numeric forces
- **Lenses**: weight modifiers for different views
- **Metadata**: source text, confidence, human verification status

## Operations

- Add/remove nodes and edges
- Find by label, content, kind, or relation
- Traverse connections
- Persist to JSON
- Load from JSON

## Design Principles

1. Graph is authoritative — all other views are derived
2. Nodes are reusable — never create duplicates for equivalent meaning
3. Usage is tracked — frequency provides importance signals
4. Every component is replaceable

See [WRAP_CORE_SPEC.md](../../WRAP_CORE_SPEC.md) for the full specification.
