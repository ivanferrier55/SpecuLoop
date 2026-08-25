# Large Context Problem

**Search terms**: context window optimization, token-efficient AI agents, LLM context window pressure, reduce context size

## The Problem

AI agents working with large knowledge bases must read many files to understand the system. As the knowledge base grows:

- More files must be loaded into context
- Context windows fill up
- Token costs increase
- Agent reasoning degrades with irrelevant information

Loading a 1000-file knowledge base into a 128K-token context window is impractical. Even with larger windows, the agent wastes tokens on irrelevant information.

## Current Approaches

- **Load everything**: expensive, often impossible
- **Keyword search**: misses semantic relationships
- **Vector RAG**: retrieves by similarity, but may retrieve many documents for a single question

## SpecuLoop's Approach

Semantic zoom compresses the knowledge graph into a context-appropriate summary. The active lens determines what level of detail is relevant for the current question.

A 1000-node graph might compress to 5 nodes under a `high-level` lens, or 50 nodes under a `detailed` lens — without losing the semantic relationships that matter for the query.

**Related**: [Semantic Zoom](../concepts/semantic-zoom.md), [Dynamic RAG](../concepts/dynamic-rag.md)
