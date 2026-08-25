"""Semantic compression and self-update primitives.

This module is intentionally model-agnostic. It implements the reconstruction
invariant that a semantic representation should be judged by how much evidence
it can explain and, when a decoder is available, how well the decoder can
reconstruct that evidence.

The historical implementation is unknown. This is a small, replaceable kernel
for experimenting with the recovered ideas without hard-coding a guessed LLM
or embedding provider.
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
    """An observed statement retained for later semantic solving."""

    text: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    created_at: float = field(default_factory=time.time)
    tokens: set[str] = field(default_factory=set)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.tokens:
            self.tokens = _tokens(self.text)


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
    notes: list[str] = field(default_factory=list)


@dataclass
class BasisScore:
    """Score for a candidate semantic basis."""

    primitive_ids: list[str]
    coverage: float
    reconstruction_error: float
    complexity: int
    score: float


class SemanticLearner:
    """Small self-updating semantic-compression loop.

    The learner deliberately separates *observation* from *acceptance* of new
    primitives. It can therefore preserve uncertainty instead of silently
    converting every unfamiliar sentence into a permanent primitive.
    """

    def __init__(self, graph: Graph, compression_threshold: float = 0.35) -> None:
        self.graph = graph
        self.compression_threshold = compression_threshold
        self.clues: list[Clue] = []
        self.history: list[CompressionResult] = []

    def observe(
        self,
        text: str,
        decoder: Callable[[str], str] | None = None,
    ) -> CompressionResult:
        """Record a clue and evaluate it against the current semantic basis.

        ``decoder`` is optional. When supplied, it receives the compact
        reconstruction and may be backed by an LLM. Its output is compared to
        the original clue using a deterministic lexical score. This keeps the
        core independent of a particular model while enabling decoder-aware
        experiments.
        """
        clue = Clue(text=text)
        self.clues.append(clue)

        ranked: list[tuple[float, Node]] = []
        for node in self.graph.nodes.values():
            node_tokens = _tokens(f"{node.label} {node.content}")
            score = _overlap(clue.tokens, node_tokens)
            if score > 0:
                ranked.append((score, node))

        ranked.sort(key=lambda item: (item[0], item[1].usage_count), reverse=True)
        selected = ranked[:8]
        reused = [node for _, node in selected if _ > 0.0]

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

    def score_basis(self, primitive_ids: Iterable[str], clues: Iterable[Clue] | None = None) -> BasisScore:
        """Score a basis using compression plus a simple complexity penalty."""
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

    @staticmethod
    def _reconstruct(nodes: Iterable[Node]) -> str:
        parts = []
        for node in nodes:
            if node.label:
                parts.append(node.label)
        return "; ".join(dict.fromkeys(parts))
