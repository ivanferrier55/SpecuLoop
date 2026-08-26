# SpecuLoop Glossary

This glossary defines the terminology used by the current reconstruction. Some terms describe implemented behavior; others describe experimental hypotheses and should not be read as claims about the lost original system.

| Term | Meaning in SpecuLoop |
|---|---|
| **Semantic memory** | Persistent representation of reusable meaning rather than a collection of isolated retrieved documents. |
| **Semantic primitive** | A reusable unit in the semantic basis used to represent or reconstruct information. |
| **Semantic basis** | The current collection of primitives used to represent incoming clues and existing knowledge. |
| **Semantic compression** | Representing information compactly while preserving enough structure for useful reconstruction by an intended decoder, lens, and task. |
| **Reconstruction** | Testing whether a compact semantic representation can recover relevant information. |
| **Decoder** | A model or process used to reconstruct information from a semantic representation. |
| **Lens** | A task- or context-dependent projection that changes which relationships or information are relevant. |
| **Semantic zoom** | Lens-dependent compression or coarsening of semantic state; currently an experimental/reconstruction target rather than a completed general algorithm. |
| **Provenance** | Information recording where a semantic structure or change came from and what evidence supported it. |
| **Uncertainty** | A signal that the current semantic basis does not adequately explain or reconstruct incoming evidence. |
| **Refactoring** | Replacing or superseding existing semantic primitives with a better explanatory basis while preserving historical provenance. |
| **DRAG** | The Dynamic RAG / semantic reasoning layer responsible for retrieval, scoring, semantic zoom, and numerical reasoning experiments. |
| **mumbleWRAP** | The persistent semantic substrate containing the graph, relationships, provenance, and primitive basis. |
| **SpecuLoop** | The broader reasoning environment that combines semantic state, retrieval/reasoning, agents, tools, feedback, and execution constraints. |

## Implementation status

SpecuLoop is an experimental reconstruction. See [RECONSTRUCTION_STATUS.md](RECONSTRUCTION_STATUS.md) for the distinction between implemented behavior, strong recollections, and hypotheses.
