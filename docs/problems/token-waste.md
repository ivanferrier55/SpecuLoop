# Token Waste Problem

**Search terms**: token-efficient AI agents, reduce RAG token usage, context-efficient reasoning

## The Problem

When an AI agent retrieves information, it often retrieves more than it needs. Each retrieved document consumes tokens even if only a small portion is relevant. Over many queries, this token waste compounds.

Traditional RAG retrieves documents by similarity, but similarity does not equal relevance. A document that is 80% similar may contain only 5% relevant information.

## SpecuLoop's Approach

DRAG selects a subgraph, not a set of documents. The subgraph contains only the nodes and edges relevant to the query. Semantic zoom further compresses this subgraph to fit a token budget.

The compression is semantic, not truncation — highly related structures merge rather than being cut off.
