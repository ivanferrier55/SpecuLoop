# Semantic Drift Problem

**Search terms**: semantic drift, knowledge graph ambiguity, AI reasoning errors

## The Problem

When knowledge is stored as flat text or vector embeddings, the meaning of concepts can drift over time. The same word may refer to different concepts in different contexts, or different words may refer to the same concept.

Without explicit relationships, the system cannot distinguish between:

- "speed" as a software metric
- "speed" as a physical property
- "speed" as a business goal

## SpecuLoop's Approach

Nodes are explicit, labeled, and connected through typed edges. The same word in different contexts maps to different nodes. Relationships are explicitly typed (`causes`, `opposes`, `supports`), preventing implicit drift.

## Questions This Project Addresses

- [Add natural technical questions that this problem page answers]

- How can a knowledge graph distinguish between different meanings of the same word?
- How can explicit relationships prevent implicit semantic drift?
- How can semantic nodes be disambiguated through context?
