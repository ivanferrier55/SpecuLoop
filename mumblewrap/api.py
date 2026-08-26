"""SpecuLoop: the self-updating semantic reasoning environment."""
from __future__ import annotations
from pathlib import Path

from mumblewrap.core.node import Node
from mumblewrap.core.lens import Lens
from mumblewrap.translation.translator import Translator, TranslationResult
from mumblewrap.translation.composer import CompositionResult
from mumblewrap.semantic import CompressionResult, RefactorProposal, SemanticLearner
from mumblewrap.grounding import Grounding
from drag.selector import DRAGSelector
from drag.scorer import Scorer
from speculoop.self_extender import SelfExtender, Proposal
from speculoop.propagator import FeedbackPropagator, EditResult
from mumblewrap.persistence.store import Store


class SpecuLoop:
    """The complete self-updating reasoning environment.

    Groundings are the source-agnostic evidence layer.  Semantic learning
    evaluates them before ordinary translation commits new semantic nodes.
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

    def ground(
        self,
        text: str,
        *,
        kind: str = "human",
        strength: float = 0.5,
        provenance: dict | None = None,
        metadata: dict | None = None,
        decoder=None,
        lens: str | None = None,
        task: str | None = None,
        decoder_name: str | None = None,
    ) -> "SemanticSolveResult":
        """Collect source-aware grounding and evaluate it against the basis.

        This does not auto-accept a new primitive.  The grounding and its
        compression evidence are persisted through the WRAP graph.
        """
        grounding = Grounding(
            text=text,
            kind=kind,
            strength=strength,
            provenance=provenance or {},
            metadata=metadata or {},
        )
        compression = self.semantic.observe_grounding(
            grounding,
            decoder=decoder,
            lens=lens,
            task=task,
            decoder_name=decoder_name,
        )
        self.store.save(self.graph)
        translation = self.translator.ingest(text)
        self.store.save(self.graph)
        return SemanticSolveResult(translation=translation, compression=compression)

    def learn(self, text: str, decoder=None, *, lens: str | None = None,
              task: str | None = None, decoder_name: str | None = None) -> "SemanticSolveResult":
        """Backward-compatible alias for a human grounding."""
        return self.ground(text, kind="human", decoder=decoder, lens=lens,
                           task=task, decoder_name=decoder_name)

    def accept_candidate(self, candidate: Node) -> Node:
        result = self.semantic.accept_candidate(candidate)
        self.store.save(self.graph)
        return result

    def propose_refactor(self, old_primitive_ids: list[str], candidate: Node) -> RefactorProposal | None:
        return self.semantic.propose_refactor(old_primitive_ids, candidate)

    def accept_refactor(self, proposal: RefactorProposal, minimum_improvement: float = 0.05) -> Node:
        result = self.semantic.accept_refactor(proposal, minimum_improvement)
        self.store.save(self.graph)
        return result

    def emit(self, node_ids: list[str] | None = None, lens: Lens | None = None) -> CompositionResult:
        return self.translator.emit(node_ids=node_ids, lens=lens)

    def emit_full(self, lens: Lens | None = None) -> CompositionResult:
        return self.translator.emit_full(lens=lens)

    def query(self, query_text: str, lens: Lens | None = None, max_nodes: int = 20) -> CompositionResult:
        subgraph = self.drag.select(query_text, lens, max_nodes)
        return self.translator.emit(node_ids=list(subgraph.nodes.keys()), lens=lens)

    def edit(self, original_markdown: str, edited_markdown: str) -> EditResult:
        result = self.feedback.process_edit(original_markdown, edited_markdown)
        self.store.save(self.graph)
        return result

    def decompose(self, text: str) -> TranslationResult:
        return self.translator.ingest(text)

    def propose(self, text: str) -> Proposal:
        return self.extender.propose_primitive(text)

    def confirm_proposal(self, proposal: Proposal, feedback: str = "") -> bool:
        result = self.extender.confirm(proposal, self.graph, feedback)
        if result:
            self.store.save(self.graph)
        return result

    def stats(self) -> dict:
        return self.graph.stats()

    def add_lens(self, lens: Lens) -> Lens:
        self.graph.add_lens(lens)
        self.store.save(self.graph)
        return lens


class SemanticSolveResult:
    def __init__(self, translation: TranslationResult, compression: CompressionResult):
        self.translation = translation
        self.compression = compression

    @property
    def uncertainty(self) -> float:
        return self.compression.uncertainty

    @property
    def candidate(self) -> Node | None:
        return self.compression.candidate

    @property
    def evidence_id(self) -> str | None:
        return self.compression.evidence_id
