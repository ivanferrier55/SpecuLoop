"""Semantic compression, evidence, and self-refactoring primitives.

This module is intentionally model-agnostic.  It implements the recovered
invariant that a semantic representation should be judged by how much evidence
it can explain and, when a decoder is available, how well the decoder can
reconstruct that evidence.

The historical implementation is unknown.  This is a small replaceable kernel
for experimenting with the recovered ideas without hard-coding an LLM,
embedding provider, or guessed historical DRAG equation.
"""
from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Iterable

from .core.graph import Graph
from .core.node import Node

_TOKEN_RE = re.compile(r"[A-Za-z0-9_'-]+")


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in _TOKEN_RE.findall(text) if len(t) > 1}


def _overlap(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass
class Clue:
    """An observation retained for later semantic solving."""

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
    """Auditable evidence connecting a clue, hypothesis, test, and result."""

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
    created_at: float = field(default_factory=time.time)


@dataclass
class CompressionResult:
    """Evidence about how well the current graph compresses a clue."""

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
    notes: list[str] = field(default_factory=list)


@dataclass
class BasisScore:
    """Score for a candidate semantic basis."""

    primitive_ids: list[str]
    coverage: float
    reconstruction_error: float
    complexity: int
    score: float


@dataclass
class RefactorProposal:
    """A non-destructive proposal to replace several primitives with one."""

    old_primitive_ids: list[str]
    candidate: Node
    old_score: BasisScore
    candidate_score: BasisScore
    improvement: float


class SemanticLearner:
    """Self-updating semantic-compression loop.

    The learner separates observation from acceptance.  Unfamiliar statements
    become uncertainty and provisional hypotheses instead of silently becoming
    permanent primitives.  Evidence is also retained as graph nodes so a later
    agent can inspect why a basis changed.
    """

    def __init__(self, graph: Graph, compression_threshold: float = 0.35) -> None:
        self.graph = graph
        self.compression_threshold = compression_threshold
        self.clues: list[Clue] = []
        self.history: list[CompressionResult] = []
        self.evidence: list[Evidence] = []

    def observe(
        self,
        text: str,
        decoder: Callable[[str], str] | None = None,
        *,
        lens: str | None = None,
        task: str | None = None,
        decoder_name: str | None = None,
    ) -> CompressionResult:
        """Record a clue and evaluate it against the current semantic basis.

        ``lens`` and ``task`` make compression explicitly contextual.  A
        decoder can be backed by an LLM; the deterministic lexical baseline is
        retained so experiments remain reproducible without an external model.
        """
        clue = Clue(text=text, metadata={"lens": lens, "task": task})
        self.clues.append(clue)

        ranked: list[tuple[float, Node]] = []
        for node in self.graph.nodes.values():
            node_tokens = _tokens(f"{node.label} {node.content}")
            score = _overlap(clue.tokens, node_tokens)
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
            notes.append("Current basis cannot adequately compress this clue.")
            notes.append("Candidate primitive is provisional; it is not auto-accepted.")

        decoder_score = None
        if decoder is not None:
            generated = decoder(reconstruction)
            decoder_score = _overlap(clue.tokens, _tokens(generated))
            reconstruction_error = 1.0 - ((coverage + decoder_score) / 2.0)
            notes.append("Decoder reconstruction score was evaluated.")

        uncertainty = reconstruction_error
        evidence = Evidence(
            kind="compression",
            clue_id=clue.id,
            hypothesis=(candidate.content if candidate else "existing basis is sufficient"),
            prediction=reconstruction,
            observation=("candidate required" if candidate else "existing basis reused"),
            score=(decoder_score if decoder_score is not None else coverage),
            uncertainty=uncertainty,
            lens=lens,
            task=task,
            decoder=decoder_name,
        )
        self.evidence.append(evidence)
        evidence_node = Node(
            kind="evidence",
            label=f"evidence:{evidence.id}",
            content=f"{evidence.kind} for clue {clue.id}",
            metadata={
                "evidence": evidence.__dict__,
                "reused_node_ids": [node.id for node in reused],
            },
        )
        self.graph.add_node(evidence_node)

        result = CompressionResult(
            clue=clue,
            coverage=coverage,
            reconstruction_error=reconstruction_error,
            reused_node_ids=[node.id for node in reused],
            unresolved_tokens=unresolved,
            candidate=candidate,
            reconstruction=reconstruction,
            decoder_score=decoder_score,
            uncertainty=uncertainty,
            lens=lens,
            task=task,
            decoder=decoder_name,
            evidence_id=evidence.id,
            notes=notes,
        )
        self.history.append(result)
        return result

    def propose_primitive(self, text: str, unresolved_tokens: Iterable[str] = ()) -> Node:
        """Create a provisional primitive hypothesis without mutating the graph."""
        tokens = list(unresolved_tokens) or sorted(_tokens(text))
        label = " ".join(tokens[:8]) or text.strip()[:80]
        return Node(
            kind="primitive",
            label=label,
            content=text.strip(),
            metadata={
                "provisional": True,
                "proposal_reason": "insufficient compression by existing basis",
                "unresolved_tokens": tokens,
            },
        )

    def accept_candidate(self, candidate: Node) -> Node:
        """Accept a provisional primitive into the persistent graph."""
        candidate.metadata["provisional"] = False
        candidate.metadata["accepted_at"] = time.time()
        self.graph.add_node(candidate)
        return candidate

    def score_basis(
        self,
        primitive_ids: Iterable[str],
        clues: Iterable[Clue] | None = None,
        *,
        lens: str | None = None,
        task: str | None = None,
    ) -> BasisScore:
        """Score explanatory coverage plus a small complexity penalty."""
        basis = [self.graph.get_node(node_id) for node_id in primitive_ids]
        basis = [node for node in basis if node is not None]
        target_clues = list(clues or self.clues)
        if not target_clues:
            return BasisScore([], 0.0, 1.0, len(basis), float(len(basis)))

        coverages: list[float] = []
        for clue in target_clues:
            basis_tokens = set()
            for node in basis:
                basis_tokens |= _tokens(f"{node.label} {node.content}")
            coverages.append(_overlap(clue.tokens, basis_tokens))

        coverage = sum(coverages) / len(coverages)
        error = 1.0 - coverage
        complexity = len(basis)
        score = error + (0.01 * complexity)
        return BasisScore([node.id for node in basis], coverage, error, complexity, score)

    def propose_refactor(
        self,
        old_primitive_ids: Iterable[str],
        candidate: Node,
        clues: Iterable[Clue] | None = None,
    ) -> RefactorProposal | None:
        """Compare a candidate basis against existing primitives without mutating state."""
        old_ids = list(old_primitive_ids)
        old_score = self.score_basis(old_ids, clues)
        target_clues = list(clues or self.clues)
        if not target_clues:
            return None

        candidate_tokens = _tokens(f"{candidate.label} {candidate.content}")
        coverages = [_overlap(clue.tokens, candidate_tokens) for clue in target_clues]
        coverage = sum(coverages) / len(coverages)
        error = 1.0 - coverage
        candidate_score = BasisScore([], coverage, error, 1, error + 0.01)
        improvement = old_score.score - candidate_score.score
        return RefactorProposal(old_ids, candidate, old_score, candidate_score, improvement)

    def accept_refactor(self, proposal: RefactorProposal, minimum_improvement: float = 0.05) -> Node:
        """Accept a refactor only when the candidate materially improves the score.

        Old primitives are retained in the graph and marked superseded.  This
        preserves provenance and allows later evidence to revisit the decision.
        """
        if proposal.improvement < minimum_improvement:
            raise ValueError("refactor does not meet minimum improvement")

        candidate = self.accept_candidate(proposal.candidate)
        candidate.metadata.update({
            "refactor_of": proposal.old_primitive_ids,
            "refactor_improvement": proposal.improvement,
        })
        for node_id in proposal.old_primitive_ids:
            old = self.graph.get_node(node_id)
            if old is not None:
                old.metadata["superseded_by"] = candidate.id
                old.updated_at = time.time()
        return candidate

    @staticmethod
    def _reconstruct(nodes: Iterable[Node]) -> str:
        parts = []
        for node in nodes:
            if node.label:
                parts.append(node.label)
        return "; ".join(dict.fromkeys(parts))
