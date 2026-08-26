"""Semantic compression, grounding, evidence, and self-refactoring primitives."""
from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Iterable

from .core.graph import Graph
from .core.node import Node
from .grounding import Grounding

_TOKEN_RE = re.compile(r"[A-Za-z0-9_'-]+")


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in _TOKEN_RE.findall(text) if len(t) > 1}


def _overlap(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass
class Clue:
    """A semantic observation derived from a grounding."""
    text: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at: float = field(default_factory=time.time)
    tokens: set[str] = field(default_factory=set)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.tokens:
            self.tokens = _tokens(self.text)


@dataclass
class Evidence:
    """Auditable evidence connecting grounding, hypothesis, test and result."""
    kind: str
    clue_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    hypothesis: str = ""
    test: str = ""
    prediction: str = ""
    observation: str = ""
    score: float | None = None
    uncertainty: float | None = None
    lens: str | None = None
    task: str | None = None
    decoder: str | None = None
    grounding_id: str | None = None
    grounding_kind: str | None = None
    grounding_strength: float | None = None
    created_at: float = field(default_factory=time.time)


@dataclass
class CompressionResult:
    """Evidence about how well the current graph compresses a grounding."""
    clue: Clue
    coverage: float
    reconstruction_error: float
    reused_node_ids: list[str] = field(default_factory=list)
    unresolved_tokens: list[str] = field(default_factory=list)
    candidate: Node | None = None
    reconstruction: str = ""
    decoder_score: float | None = None
    uncertainty: float = 0.0
    lens: str | None = None
    task: str | None = None
    decoder: str | None = None
    evidence_id: str | None = None
    grounding_id: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass
class BasisScore:
    primitive_ids: list[str]
    coverage: float
    reconstruction_error: float
    complexity: int
    score: float


@dataclass
class RefactorProposal:
    old_primitive_ids: list[str]
    candidate: Node
    old_score: BasisScore
    candidate_score: BasisScore
    improvement: float


class SemanticLearner:
    """Self-updating semantic-compression loop with source-aware grounding."""

    def __init__(self, graph: Graph, compression_threshold: float = 0.35) -> None:
        self.graph = graph
        self.compression_threshold = compression_threshold
        self.groundings: list[Grounding] = []
        self.clues: list[Clue] = []
        self.history: list[CompressionResult] = []
        self.evidence: list[Evidence] = []

    def observe_grounding(
        self,
        grounding: Grounding,
        decoder: Callable[[str], str] | None = None,
        *,
        lens: str | None = None,
        task: str | None = None,
        decoder_name: str | None = None,
    ) -> CompressionResult:
        """Collect any grounding source and evaluate it against the current basis."""
        self.groundings.append(grounding)
        return self._observe_text(
            grounding.text, decoder, lens, task, decoder_name, grounding
        )

    def observe(
        self,
        text: str,
        decoder: Callable[[str], str] | None = None,
        *,
        lens: str | None = None,
        task: str | None = None,
        decoder_name: str | None = None,
    ) -> CompressionResult:
        """Backward-compatible human observation entry point."""
        return self.observe_grounding(
            Grounding(text=text, kind="human", strength=0.5),
            decoder=decoder, lens=lens, task=task, decoder_name=decoder_name,
        )

    def _observe_text(self, text, decoder, lens, task, decoder_name, grounding):
        clue = Clue(text=text, metadata={
            "lens": lens, "task": task,
            "grounding_id": grounding.id,
            "grounding_kind": grounding.kind,
            "grounding_strength": grounding.strength,
        })
        self.clues.append(clue)

        ranked: list[tuple[float, Node]] = []
        for node in self.graph.nodes.values():
            score = _overlap(clue.tokens, _tokens(f"{node.label} {node.content}"))
            if score > 0:
                ranked.append((score, node))
        ranked.sort(key=lambda item: (item[0], item[1].usage_count), reverse=True)
        selected = ranked[:8]
        reused = [node for score, node in selected if score > 0.0]

        covered: set[str] = set()
        for _, node in selected:
            covered |= clue.tokens & _tokens(f"{node.label} {node.content}")
            node.update_usage()

        coverage = len(covered) / len(clue.tokens) if clue.tokens else 1.0
        unresolved = sorted(clue.tokens - covered)
        reconstruction = self._reconstruct(reused)
        reconstruction_error = 1.0 - coverage
        candidate = None
        notes: list[str] = []
        if coverage < self.compression_threshold:
            candidate = self.propose_primitive(text, unresolved)
            notes.append("Current basis cannot adequately compress this grounding.")
            notes.append("Candidate primitive is provisional; it is not auto-accepted.")

        decoder_score = None
        if decoder is not None:
            generated = decoder(reconstruction)
            decoder_score = _overlap(clue.tokens, _tokens(generated))
            reconstruction_error = 1.0 - ((coverage + decoder_score) / 2.0)
            notes.append("Decoder reconstruction score was evaluated.")

        evidence = Evidence(
            kind="compression", clue_id=clue.id,
            hypothesis=(candidate.content if candidate else "existing basis is sufficient"),
            prediction=reconstruction,
            observation=("candidate required" if candidate else "existing basis reused"),
            score=(decoder_score if decoder_score is not None else coverage),
            uncertainty=reconstruction_error, lens=lens, task=task,
            decoder=decoder_name, grounding_id=grounding.id,
            grounding_kind=grounding.kind, grounding_strength=grounding.strength,
        )
        self.evidence.append(evidence)
        self.graph.add_node(Node(
            kind="evidence", label=f"evidence:{evidence.id}",
            content=f"{evidence.kind} for grounding {grounding.id}",
            metadata={"evidence": evidence.__dict__,
                      "grounding": grounding.as_dict(),
                      "reused_node_ids": [node.id for node in reused]},
        ))

        result = CompressionResult(
            clue=clue, coverage=coverage, reconstruction_error=reconstruction_error,
            reused_node_ids=[node.id for node in reused], unresolved_tokens=unresolved,
            candidate=candidate, reconstruction=reconstruction,
            decoder_score=decoder_score, uncertainty=reconstruction_error,
            lens=lens, task=task, decoder=decoder_name, evidence_id=evidence.id,
            grounding_id=grounding.id, notes=notes,
        )
        self.history.append(result)
        return result

    def propose_primitive(self, text: str, unresolved_tokens: Iterable[str] = ()) -> Node:
        tokens = list(unresolved_tokens) or sorted(_tokens(text))
        return Node(kind="primitive", label=" ".join(tokens[:8]) or text.strip()[:80],
                    content=text.strip(), metadata={
                        "provisional": True,
                        "proposal_reason": "insufficient compression by existing basis",
                        "unresolved_tokens": tokens,
                    })

    def accept_candidate(self, candidate: Node) -> Node:
        candidate.metadata["provisional"] = False
        candidate.metadata["accepted_at"] = time.time()
        self.graph.add_node(candidate)
        return candidate

    def score_basis(self, primitive_ids: Iterable[str], clues: Iterable[Clue] | None = None, *, lens: str | None = None, task: str | None = None) -> BasisScore:
        basis = [self.graph.get_node(node_id) for node_id in primitive_ids]
        basis = [node for node in basis if node is not None]
        target_clues = list(clues or self.clues)
        if not target_clues:
            return BasisScore([], 0.0, 1.0, len(basis), float(len(basis)))
        basis_tokens = set()
        for node in basis:
            basis_tokens |= _tokens(f"{node.label} {node.content}")
        coverages = [_overlap(clue.tokens, basis_tokens) for clue in target_clues]
        coverage = sum(coverages) / len(coverages)
        error = 1.0 - coverage
        complexity = len(basis)
        return BasisScore([node.id for node in basis], coverage, error, complexity, error + 0.01 * complexity)

    def propose_refactor(self, old_primitive_ids: Iterable[str], candidate: Node, clues: Iterable[Clue] | None = None) -> RefactorProposal | None:
        old_ids = list(old_primitive_ids)
        old_score = self.score_basis(old_ids, clues)
        target_clues = list(clues or self.clues)
        if not target_clues:
            return None
        candidate_tokens = _tokens(f"{candidate.label} {candidate.content}")
        coverage = sum(_overlap(clue.tokens, candidate_tokens) for clue in target_clues) / len(target_clues)
        candidate_score = BasisScore([], coverage, 1.0 - coverage, 1, 1.01 - coverage)
        return RefactorProposal(old_ids, candidate, old_score, candidate_score, old_score.score - candidate_score.score)

    def accept_refactor(self, proposal: RefactorProposal, minimum_improvement: float = 0.05) -> Node:
        if proposal.improvement < minimum_improvement:
            raise ValueError("refactor does not meet minimum improvement")
        candidate = self.accept_candidate(proposal.candidate)
        candidate.metadata.update({"refactor_of": proposal.old_primitive_ids, "refactor_improvement": proposal.improvement})
        for node_id in proposal.old_primitive_ids:
            old = self.graph.get_node(node_id)
            if old is not None:
                old.metadata["superseded_by"] = candidate.id
                old.updated_at = time.time()
        return candidate

    @staticmethod
    def _reconstruct(nodes: Iterable[Node]) -> str:
        return "; ".join(dict.fromkeys(node.label for node in nodes if node.label))
