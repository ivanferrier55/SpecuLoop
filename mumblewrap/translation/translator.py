
"""
WRAP — Persistent Semantic State Engine for AI Agents

This module implements part of the SpecuLoop semantic graph system.
WRAP is a graph-based semantic memory representing knowledge as nodes,
edges, and numeric forces. It supports bidirectional natural language
translation (Interlocked Translation), Dynamic RAG (DRAG) subgraph
selection, semantic zoom, lenses, self-extension, provenance tracking,
and edit feedback propagation.

Core loop: Mumble input -> semantic decomposition -> WRAP graph ->
DRAG selection -> Mumble Markdown -> human edit -> WRAP update
"""

"""Translator: orchestrates Mumble ↔ WRAP translation.

Ties together Decomposer (text → graph) and Composer (graph → text).
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field

from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge
from ..core.lens import Lens
from .decomposer import Decomposer, DecompositionResult
from .composer import Composer, CompositionResult, Provenance


@dataclass
class TranslationResult:
    """Result of translating Mumble text into WRAP structures."""
    input_text: str = ""
    reused_nodes: list[Node] = field(default_factory=list)
    new_nodes: list[Node] = field(default_factory=list)
    reused_edges: list[Edge] = field(default_factory=list)
    new_edges: list[Edge] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    confidence: float = 0.0
    details: str = ""
    timestamp: float = field(default_factory=time.time)


class Translator:
    """Orchestrates bidirectional Mumble ↔ WRAP translation."""

    def __init__(self, graph: Graph, decomposer: Decomposer | None = None,
                 composer: Composer | None = None):
        self.graph = graph
        self.decomposer = decomposer or Decomposer()
        self.composer = composer or Composer()

    def ingest(self, text: str) -> TranslationResult:
        """Translate Mumble text into WRAP structures. Returns TranslationResult."""
        result = TranslationResult(input_text=text)

        # Decompose the text
        decomp = self.decomposer.decompose(text, self.graph)

        # Collect what was reused
        result.reused_nodes = decomp.reused_nodes
        result.reused_edges = decomp.reused_edges
        result.gaps = decomp.gaps
        result.confidence = decomp.confidence
        result.details = decomp.details

        # Add new nodes to graph
        for node in decomp.new_nodes:
            self.graph.add_node(node)
            result.new_nodes.append(node)

        # Add new edges to graph (only if both source and target exist)
        for edge in decomp.new_edges:
            if edge.source in self.graph.nodes and edge.target in self.graph.nodes:
                self.graph.add_edge(edge)
                result.new_edges.append(edge)
            else:
                result.gaps.append(f"Edge {edge.source}→{edge.target} missing node(s)")

        # Record provenance for this ingestion
        all_node_ids = [n.id for n in result.reused_nodes + result.new_nodes]
        all_edge_ids = [e.id for e in result.reused_edges + result.new_edges]

        return result

    def emit(self, node_ids: list[str] | None = None,
             edge_ids: list[str] | None = None,
             lens: Lens | None = None) -> CompositionResult:
        """Generate Mumble Markdown from WRAP nodes/edges."""
        return self.composer.compose(
            node_ids=node_ids,
            edge_ids=edge_ids,
            graph=self.graph,
            lens=lens,
        )

    def emit_full(self, lens: Lens | None = None) -> CompositionResult:
        """Generate Mumble Markdown from the entire graph."""
        return self.composer.compose(graph=self.graph, lens=lens)
