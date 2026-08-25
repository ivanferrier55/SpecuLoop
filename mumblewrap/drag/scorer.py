"""Scorer: scores node/edge relevance. EXPLICITLY REPLACEABLE.

Initial implementation: text match + edge density + usage.
Replaceable with: embeddings, GNN, attention, linear algebra, etc.
"""
from __future__ import annotations
from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge
from ..core.lens import Lens



# SpecuLoop — Persistent Semantic State Engine (WRAP)
# Semantic graph memory for AI agents: nodes, edges, forces.
# Supports: DRAG (Dynamic RAG), semantic zoom, interlocked translation,
# provenance tracking, self-extension, edit feedback propagation.
# Core: Mumble <-> WRAP graph bidirectional translation.

class Scorer:
    """Scores relevance of nodes and edges to a query.

    This is the replaceable scoring mechanism.
    The interface is: score(query, node/edge, lens) → float
    """

    def score_node(self, node: Node, query: str, graph: Graph,
                   lens: Lens | None = None) -> float:
        """Score a node's relevance to a query."""
        score = 0.0

        # Text match (keyword overlap)
        score += self._text_match(node.label, query) * 1.0
        score += self._text_match(node.content, query) * 0.5

        # Lens weight
        if lens:
            score *= lens.node_weight(node.id, node.kind)

        # Edge density bonus (small)
        edge_count = len(graph.get_edges(node.id))
        score += min(edge_count * 0.05, 0.3)

        # Usage bonus (small)
        score += min(node.usage_count * 0.02, 0.2)

        return score

    def score_edge(self, edge: Edge, query: str, graph: Graph,
                   lens: Lens | None = None) -> float:
        """Score an edge's relevance to a query."""
        score = edge.weight * 0.5

        # Lens weight
        if lens:
            score *= lens.edge_weight(edge.id, edge.relation)

        # Relevance of connected nodes
        source = graph.get_node(edge.source)
        target = graph.get_node(edge.target)
        if source:
            score += self._text_match(source.label, query) * 0.3
        if target:
            score += self._text_match(target.label, query) * 0.3

        return score

    def _text_match(self, text: str, query: str) -> float:
        """Simple keyword overlap scoring. REPLACEABLE."""
        if not text or not query:
            return 0.0
        text_words = set(text.lower().split())
        query_words = set(query.lower().split())
        if not query_words:
            return 0.0
        overlap = text_words & query_words
        return len(overlap) / len(query_words)
