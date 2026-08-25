# Related Work

Academic papers and open-source projects related to SpecuLoop's core concepts.

---

## GraphRAG

- **Microsoft GraphRAG** (2024) — builds knowledge graphs from documents, uses community detection for retrieval. [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)
- **nano-GraphRAG** — lightweight GraphRAG implementation. [github.com/gusye1234/nano-graphrag](https://github.com/gusye1234/nano-graphrag)

**Relation to SpecuLoop**: SpecuLoop shares graph-based retrieval but adds numeric forces, lenses, and persistent incremental updates rather than per-query graph construction.

---

## Agent Memory

- **MemGPT / Letta** — persistent memory for LLM agents using flat text tiers. [github.com/cpacker/MemGPT](https://github.com/cpacker/MemGPT)
- **Generative Agents** (Park et al., 2023) — agent memory streams with reflection and planning.
- **MemoryBank** (Zhong et al., 2024) — long-term memory for LLM agents.

**Relation to SpecuLoop**: SpecuLoop stores memory as a semantic graph with typed relationships and numeric forces, rather than flat text summaries.

---

## Knowledge Graphs

- **RDF / SPARQL** — standard knowledge graph query language.
- **Neo4j** — graph database with Cypher query language.
- **Wikidata** — collaborative knowledge graph.
- **ConceptNet** — common-sense knowledge graph.

**Relation to SpecuLoop**: SpecuLoop adds dynamic edge weights, lenses, and provenance to the knowledge graph model.

---

## Graph Embeddings

- **TransE** (Bordes et al., 2013) — embedding entities and relations.
- **Node2Vec** (Grover & Leskovec, 2016) — node embeddings via biased random walks.
- **Graph Neural Networks** (Kipf & Welling, 2017) — neural message passing on graphs.

**Relation to SpecuLoop**: SpecuLoop's scoring mechanism is designed to eventually incorporate graph embeddings but starts with simpler heuristics.

---

## Graph Coarsening / Multiscale Graphs

- **Graph coarsening** (Karypis & Kumar, 1998) — reducing graph size while preserving structure.
- **Multiscale graph neural networks** — processing graphs at multiple resolutions.
- **Hierarchical clustering** — grouping related nodes.

**Relation to SpecuLoop**: Semantic zoom is a form of lens-dependent graph coarsening, where compression depends on the query and active lens.

---

## Hierarchical Retrieval

- **Hierarchical Navigable Small World (HNSW)** — approximate nearest neighbor search.
- **RAPTOR** (Sarthi et al., 2024) — hierarchical retrieval with tree-based summarization.
- **REMEMBER** — hierarchical memory for LLM agents.

**Relation to SpecuLoop**: SpecuLoop achieves multi-level retrieval through semantic zoom rather than fixed document hierarchies.

---

## Causal Reasoning

- **Causal graphs** (Pearl, 2009) — structural causal models.
- **Causal inference** — do-calculus and counterfactuals.
- **Causal discovery** — learning causal structure from data.

**Relation to SpecuLoop**: Causal relationships are one of many edge types in WRAP. SpecuLoop does not implement full causal inference but represents causal structure as graph edges.

---

## Human-in-the-Loop Learning

- **Interactive machine learning** — incorporating human feedback.
- **Active learning** — selecting samples for human annotation.
- **RLHF** — reinforcement learning from human feedback.

**Relation to SpecuLoop**: SpecuLoop propagates human corrections as semantic updates to the graph, rather than fine-tuning a model.

---

## Bidirectional Programming / Program Synthesis

- **Bidirectional programming** (Foster et al., 2007) — lenses for bidirectional data transformation.
- **Program synthesis** — generating code from specifications.
- **Natural language to code** — converting English to executable code.

**Relation to SpecuLoop**: Interlocked translation is intended to eventually support bidirectional linking between natural-language specifications and executable code.

---

## Semantic Compression

- **Knowledge distillation** — compressing model knowledge.
- **Semantic hashing** — mapping text to compact codes.
- **Abstractive summarization** — generating compressed representations.

**Relation to SpecuLoop**: Semantic zoom compresses graph structures rather than text, preserving relationships while reducing detail.
