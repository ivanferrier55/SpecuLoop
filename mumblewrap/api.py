"""SpecuLoop: the complete self-updating reasoning environment.

Combines mumbleWRAP (semantic state), DRAG (dynamic retrieval/reasoning),
and semantic compression with human feedback and execution grounding.
"""
from __future__ import annotations
from pathlib import Path

from mumblewrap.core.graph import Graph
from mumblewrap.core.node import Node
from mumblewrap.core.edge import Edge
from mumblewrap.core.lens import Lens
from mumblewrap.translation.translator import Translator, TranslationResult
from mumblewrap.translation.decomposer import Decomposer
from mumblewrap.translation.composer import Composer, CompositionResult
from mumblewrap.semantic import CompressionResult, SemanticLearner
from drag.selector import DRAGSelector, Subgraph
from drag.scorer import Scorer
from speculoop.self_extender import SelfExtender, Proposal
from speculoop.propagator import FeedbackPropagator, EditResult
from mumblewrap.persistence.store import Store


class SpecuLoop:
    """The complete self-updating reasoning environment.

    The semantic learner adds a model-agnostic core loop:
    observe → compress → measure uncertainty → propose/test a new basis.
    New primitives remain provisional until explicitly accepted.
    """

    def __init__(self, graph_path: str | Path = "wrap_graph.json"):
        self.store = Store(graph_path)
        self.graph = self.store.load()
        self.translator = Translator(self.graph)
        self.scorer = Scorer()
        self.drag = DRAGSelector(self.graph, self.scorer)
        self.extender = SelfExtender()
        self.feedback = FeedbackPropagator(self.graph)
        self.semantic = SemanticLearner(self.graph)

    def ingest(self, text: str) -> TranslationResult:
        """Ingest human language into mumbleWRAP."""
        result = self.translator.ingest(text)
        self.store.save(self.graph)
        return result

    def learn(self, text: str, decoder=None) -> "SemanticSolveResult":
        """Run the recovered semantic compression loop.

        Compression is evaluated against the *pre-ingest* basis. This is
        important: a genuinely new clue must be allowed to register as
        uncertain before the ordinary translator adds its surface concepts.
        The resulting translation is then persisted, while the provisional
        candidate remains separate until accepted.
        """
        compression = self.semantic.observe(text, decoder=decoder)
        translation = self.ingest(text)
        return SemanticSolveResult(translation=translation, compression=compression)

    def accept_candidate(self, candidate: Node) -> Node:
        """Accept a provisional semantic primitive and persist it."""
        result = self.semantic.accept_candidate(candidate)
        self.store.save(self.graph)
        return result

    def emit(self, node_ids: list[str] | None = None,
             lens: Lens | None = None) -> CompositionResult:
        """Generate human-readable text from mumbleWRAP."""
        return self.translator.emit(node_ids=node_ids, lens=lens)

    def emit_full(self, lens: Lens | None = None) -> CompositionResult:
        """Generate human-readable text from the entire graph."""
        return self.translator.emit_full(lens=lens)

    def query(self, query_text: str, lens: Lens | None = None,
              max_nodes: int = 20) -> CompositionResult:
        """Query via DRAG: select relevant subgraph, then compose."""
        subgraph = self.drag.select(query_text, lens, max_nodes)
        return self.translator.emit(
            node_ids=list(subgraph.nodes.keys()),
            lens=lens,
        )

    def edit(self, original_markdown: str, edited_markdown: str) -> EditResult:
        """Process a human edit and propagate back into mumbleWRAP."""
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


class SemanticSolveResult:
    """Combined translation and semantic-compression result."""

    def __init__(self, translation: TranslationResult, compression: CompressionResult):
        self.translation = translation
        self.compression = compression

    @property
    def uncertainty(self) -> float:
        return self.compression.uncertainty

    @property
    def candidate(self) -> Node | None:
        return self.compression.candidate
