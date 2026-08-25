# Changelog

All notable changes to SpecuLoop.

---

## 2026-08-25 — Phase 1: Core Kernel

**Initial release.** Implemented the minimal WRAP kernel demonstrating the core semantic loop.

### Added
- Core graph model: Node, Edge, Graph, Lens
- Mumble ↔ WRAP translation (Decomposer, Composer, Translator)
- DRAG subgraph selection with replaceable scoring
- Self-extension proposals for new primitives
- Edit feedback propagation (interlocked translation)
- JSON persistence
- 9 end-to-end tests (all passing)
- Demo script showing full vertical slice

### Design Decisions
- Pattern-based decomposition (replaceable with LLM)
- Text overlap scoring (replaceable with embeddings)
- Template-based composition (replaceable with LLM)
- JSON persistence (replaceable with SQLite/graph DB)

### Related Concepts
- semantic knowledge graph
- persistent agent memory
- dynamic RAG
- semantic zoom
- interlocked translation
- provenance tracking
- self-extending knowledge graph
