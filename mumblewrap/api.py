"""SpecuLoop WRAP API — the main interface to the semantic engine.

Provides the high-level loop:
  Mumble → WRAP → DRAG → Mumble Markdown → edit → WRAP update
"""
from __future__ import annotations
from pathlib import Path

from .core.graph import Graph
from .core.node import Node
from .core.edge import Edge
from .core.lens import Lens
from .translation.translator import Translator, TranslationResult
from .translation.decomposer import Decomposer
from .translation.composer import Composer, CompositionResult
from .drag.selector import DRAGSelector, Subgraph
from .drag.scorer import Scorer
from .extension.self_extender import SelfExtender, Proposal
from .feedback.propagator import FeedbackPropagator, EditResult
from .persistence.store import Store



# SpecuLoop — Persistent Semantic State Engine (WRAP)
# Semantic graph memory for AI agents: nodes, edges, forces.
# Supports: DRAG (Dynamic RAG), semantic zoom, interlocked translation,
# provenance tracking, self-extension, edit feedback propagation.
# Core: Mumble <-> WRAP graph bidirectional translation.

class SpecuLoop:
    """The main semantic engine interface."""

    def __init__(self, graph_path: str | Path = "wrap_graph.json"):
        self.store = Store(graph_path)
        self.graph = self.store.load()
        self.translator = Translator(self.graph)
        self.scorer = Scorer()
        self.drag = DRAGSelector(self.graph, self.scorer)
        self.extender = SelfExtender()
        self.feedback = FeedbackPropagator(self.graph)

    def ingest(self, text: str) -> TranslationResult:
        """Ingest Mumble text into WRAP."""
        result = self.translator. ingest(text)
        self.store.save(self.graph)
        return result

    def emit(self, node_ids: list[str] | None = None,
             lens: Lens | None = None) -> CompositionResult:
        """Generate Mumble Markdown from WRAP."""
        return self.translator.emit(node_ids=node_ids, lens=lens)

    def emit_full(self, lens: Lens | None = None) -> CompositionResult:
        """Generate Mumble Markdown from the entire graph."""
        return self.translator.emit_full(lens=lens)

    def query(self, query_text: str, lens: Lens | None = None,
              max_nodes: int = 20) -> CompositionResult:
        """Query the graph: select relevant subgraph, then compose Markdown."""
        subgraph = self.drag.select(query_text, lens, max_nodes)
        return self.translator.emit(
            node_ids=list(subgraph.nodes.keys()),
            lens=lens,
        )

    def edit(self, original_markdown: str, edited_markdown: str) -> EditResult:
        """Process a human edit and propagate changes back to WRAP."""
        result = self.feedback.process_edit(original_markdown, edited_markdown)
        self.store.save(self.graph)
        return result

    def decompose(self, text: str) -> TranslationResult:
        """Attempt decomposition without committing to the graph."""
        return self.translator.ingest(text)

    def propose(self, text: str) -> Proposal:
        """Propose a new primitive for an unrecognized concept."""
        return self.extender.propose_primitive(text)

    def confirm_proposal(self, proposal: Proposal, feedback: str = "") -> bool:
        """Confirm or modify a proposal."""
        result = self.extender.confirm(proposal, self.graph, feedback)
        if result:
            self.store.save(self.graph)
        return result

    def stats(self) -> dict:
        """Get graph statistics."""
        return self.graph.stats()

    def add_lens(self, lens: Lens) -> Lens:
        """Add a lens to the graph."""
        self.graph.add_lens(lens)
        self.store.save(self.graph)
        return lens
