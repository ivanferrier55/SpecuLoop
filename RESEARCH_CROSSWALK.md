# Research Crosswalk

Maps project concepts to conventional research areas, algorithms, open-source projects, and papers.

---

## Semantic Zoom

**Project concept**: Semantic Zoom
→ **Research area**: Multiscale Graph Representation
→ **Algorithms**: Graph coarsening, hierarchical clustering, community detection
→ **Open source**: Graph-tool, NetworkX, SNAP
→ **Papers**:
- Karypis & Kumar, "A Fast and High Quality Multilevel Scheme for Partitioning Irregular Graphs" (1998)
- Leskovec et al., "Scalable Modeling of Real Graphs using Kronecker Multiplication" (2007)
- Fortunato, "Community Detection in Graphs" (2010)

**What this project adds**: Lens-dependent semantic compression. Different lenses produce different coarsened views.

**Open questions**:
- How should edge weights determine graph coarsening priority?
- What is the right compression ratio for different query types?
- How should coarsened nodes be labeled?

---

## Semantic Lenses

**Project concept**: Semantic Lenses
→ **Research area**: Multi-view Graph Representation
→ **Algorithms**: Multi-head attention, graph projections, topic modeling
→ **Open source**: DGL (Deep Graph Library), PyTorch Geometric
→ **Papers**:
- Velickovic et al., "Graph Attention Networks" (2018)
- Dong et al., "Metagraph Convolutional Networks" (2019)

**What this project adds**: Explicit, user-definable lens structures that modify edge and node weights globally.

**Open questions**:
- How many lenses are needed for typical use cases?
- Should lenses be learned from data or hand-defined?
- How should new lenses propagate through existing graphs?

---

## Semantic Forces

**Project concept**: Semantic Forces
→ **Research area**: Signed Graphs, Force-Directed Models
→ **Algorithms**: Force-directed layout, signed network analysis
→ **Open source**: Gephi, Cytoscape
→ **Papers**:
- Fruchterman & Reingold, "Graph Drawing by Force-Directed Placement" (1991)
- Cartwright & Harary, "Structural Balance: A Generalization of Heider's Theory" (1956)
- Kunegis et al., "Signed Graph Networks" (2019)

**What this project adds**: Forces represent semantic relationships (causes, opposes, supports), not just spatial layout. Forces are modified by lenses.

**Open questions**:
- What is the right force model for semantic relationships?
- How do forces propagate through multi-hop paths?
- Can forces be learned from data?

---

## Interlocked Translation

**Project concept**: Interlocked Translation
→ **Research area**: Bidirectional Programming, Program Synthesis
→ **Algorithms**: Bidirectional lenses, source-target synchronization
→ **Open source**: Boomerang, ML-like bidirectional transformations
→ **Papers**:
- Foster et al., "Combining Programming and Theorem Proving" (2007)
- Bohannon et al., "Boomerang: Beam me up, Scotty" (2008)
- Polikarpova et al., "Program Synthesis from Dependent Types" (2016)

**What this project adds**: Translation operates through a semantic graph intermediary. Changes propagate through graph structures, not direct text transformation.

**Open questions**:
- How should code translation be implemented?
- What is the right granularity for provenance tracking?
- How should conflicting edits be resolved?

---

## Dynamic RAG

**Project concept**: Dynamic RAG (DRAG)
→ **Research area**: Adaptive Retrieval, Incremental Learning
→ **Algorithms**: Online learning, incremental graph construction
→ **Open source**: LangChain, LlamaIndex, Haystack
→ **Papers**:
- Edge et al., "From Local to Global: A Graph RAG Approach" (2024)
- Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey" (2024)
- Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique" (2023)

**What this project adds**: Both retrieval scope and knowledge graph are dynamic. Graph updates improve retrieval quality over time.

**Open questions**:
- How should graph updates be weighted by recency?
- How should failed retrievals affect graph structure?
- What is the right balance between exploration and exploitation?

---

## Persistent Semantic Memory

**Project concept**: Persistent Semantic Memory
→ **Research area**: Agent Memory, Long-term LLM Memory
→ **Algorithms**: Memory streams, reflection, knowledge graphs
→ **Open source**: MemGPT/Letta, Generative Agents, MemoryBank
→ **Papers**:
- Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023)
- Packer et al., "MemGPT: Towards LLMs as Operating Systems" (2023)
- Zhong et al., "MemoryBank: Enhancing Large Language Models with Long-Term Memory" (2024)

**What this project adds**: Memory is a semantic graph with typed relationships and numeric forces, not flat text summaries.

**Open questions**:
- How should graph size be managed over long periods?
- When should old nodes be pruned?
- How should conflicting memories be resolved?

---

## Provenance Tracking

**Project concept**: Provenance
→ **Research area**: Explainable AI, Attribution
→ **Algorithms**: Citation tracking, attention visualization, chain-of-thought
→ **Open source**: Captum, InterpretML
→ **Papers**:
- Wiegreffe & Pinter, "Attention is not not Explanation" (2019)
- DeYoung et al., "ERASER: A Benchmark to Evaluate Rationalized NLP Models" (2020)

**What this project adds**: Provenance links generated text to specific graph nodes and edges, not just documents or attention weights.

**Open questions**:
- What is the right granularity for provenance?
- How should provenance survive graph updates?
- How should conflicting provenance be resolved?

---

## Causal Reasoning

**Project concept**: Causal Edges
→ **Research area**: Causal Inference, Causal Discovery
→ **Algorithms**: Structural causal models, do-calculus, causal discovery
→ **Open source**: DoWhy, CausalNex, Causal-learn
→ **Papers**:
- Pearl, "Causality: Models, Reasoning, and Inference" (2009)
- Spirtes et al., "Causation, Prediction, and Search" (2000)

**What this project adds**: Causal relationships are one of many edge types, alongside opposition, support, and dependency. Causal structure is represented as graph edges with numeric forces.

**Open questions**:
- Should causal edges have special propagation rules?
- Can causal structure be inferred from graph patterns?
- How should causal and non-causal relationships interact?

---

## Human-in-the-Loop Learning

**Project concept**: Semantic Feedback
→ **Research area**: Interactive Machine Learning, Active Learning
→ **Algorithms**: Active learning, preference learning, RLHF
→ **Open source**: ModAL, alipy
→ **Papers**:
- Settles, "Active Learning Literature Survey" (2009)
- Ouyang et al., "Training Language Models to Follow Instructions with Human Feedback" (2022)

**What this project adds**: Feedback modifies graph structure (nodes, edges, weights), not model parameters.

**Open questions**:
- How should conflicting human feedback be resolved?
- How should confidence in human corrections be weighted?
- When should the system ask for feedback vs. auto-update?
