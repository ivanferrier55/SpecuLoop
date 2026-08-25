"""Selector: selects a relevant subgraph for a query. EXPLICITLY REPLACEABLE.

Initial implementation: score nodes, propagate through edges, collect top-K.
Replaceable with: graph neural networks, attention mechanisms, etc.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import heapq

from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge
from ..core.lens import Lens
from .scorer import Scorer



# SpecuLoop — Persistent Semantic State Engine (WRAP)
# Semantic graph memory for AI agents: nodes, edges, forces.
# Supports: DRAG (Dynamic RAG), semantic zoom, interlocked translation,
# provenance tracking, self-extension, edit feedback propagation.
# Core: Mumble <-> WRAP graph bidirectional translation.

@dataclass
class Subgraph:
    """A selected subset of the WRAP graph."""
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: dict[str, Edge] = field(default_factory=dict)
    root_ids: list[str] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    lens_id: str = "default"
    token_estimate: int = 0


class DRAGSelector:
    """Selects relevant subgraphs from the WRAP graph.

    Initial implementation: score-based with propagation.
    Replaceable with more sophisticated algorithms.
    """

    def __init__(self, graph: Graph, scorer: Scorer | None = None):
        self.graph = graph
        self.scorer = scorer or Scorer()

    def select(self, query: str, lens: Lens | None = None,
               max_nodes: int = 50) -> Subgraph:
        """Select the most relevant subgraph for a query."""
        subgraph = Subgraph(lens_id=lens.id if lens else "default")

        # Score all nodes
        scored_nodes: list[tuple[float, str]] = []
        for node_id, node in self.graph.nodes.items():
            score = self.scorer.score_node(node, query, self.graph, lens)
            scored_nodes.append((score, node_id))
            subgraph.scores[node_id] = score

        # Get top-K seed nodes
        scored_nodes.sort(reverse=True, key=lambda x: x[0])
        seed_ids = [nid for _, nid in scored_nodes[:min(max_nodes, len(scored_nodes))]]

        # Propagate from seeds through edges
        visited_edges: set[str] = set()
        node_budget = max_nodes

        for seed_id in seed_ids:
            if node_budget <= 0:
                break
            if seed_id not in self.graph.nodes:
                continue

            # Add the seed node
            seed_node = self.graph.nodes[seed_id]
            if seed_id not in subgraph.nodes:
                subgraph.nodes[seed_id] = seed_node
                node_budget -= 1
                subgraph.root_ids.append(seed_id)

            # Propagate through connected edges
            connected = self.graph.connected_nodes(seed_id)
            connected.sort(key=lambda x: self.scorer.score_edge(
                x[1], query, self.graph, lens), reverse=True)

            for other_node, edge in connected:
                if node_budget <= 0:
                    break
                if edge.id in visited_edges:
                    continue

                # Add the edge
                subgraph.edges[edge.id] = edge
                visited_edges.add(edge.id)

                # Add the connected node if not already present
                if other_node.id not in subgraph.nodes:
                    subgraph.nodes[other_node.id] = other_node
                    node_budget -= 1

        # Add edges between selected nodes that weren't captured by propagation
        for edge in self.graph.edges.values():
            if edge.id in subgraph.edges:
                continue
            if edge.source in subgraph.nodes and edge.target in subgraph.nodes:
                subgraph.edges[edge.id] = edge

        # Estimate tokens (rough word count)
        subgraph.token_estimate = sum(
            len(n.label.split()) + len(n.content.split())
            for n in subgraph.nodes.values()
        )

        return subgraph

    def propagate(self, node_id: str, depth: int = 2) -> list[str]:
        """Propagate from a node through the graph. Returns ordered node IDs."""
        if node_id not in self.graph.nodes:
            return []

        visited: set[str] = set()
        queue: list[tuple[float, str]] = [(1.0, node_id)]
        result: list[str] = []

        for _ in range(depth + 1):
            if not queue:
                break
            next_queue: list[tuple[float, str]] = []
            for priority, current_id in queue:
                if current_id in visited:
                    continue
                visited.add(current_id)
                result.append(current_id)

                for other, edge in self.graph.connected_nodes(current_id):
                    if other.id not in visited:
                        next_queue.append((edge.weight * priority, other.id))
            queue = sorted(next_queue, reverse=True)

        return result

    def compress(self, subgraph: Subgraph, target_tokens: int) -> Subgraph:
        """Compress a subgraph to fit within a token budget.

        Strategy: remove lowest-scored nodes until under budget.
        """
        if subgraph.token_estimate <= target_tokens:
            return subgraph

        # Sort nodes by score (ascending — remove worst first)
        node_scores = sorted(subgraph.scores.items(), key=lambda x: x[1])

        compressed = Subgraph(
            nodes=dict(subgraph.nodes),
            edges=dict(subgraph.edges),
            root_ids=list(subgraph.root_ids),
            scores=dict(subgraph.scores),
            lens_id=subgraph.lens_id,
            token_estimate=subgraph.token_estimate,
        )

        for node_id, _ in node_scores:
            if compressed.token_estimate <= target_tokens:
                break
            if node_id in compressed.root_ids:
                continue  # Don't remove root nodes

            node = compressed.nodes.pop(node_id, None)
            if node:
                compressed.token_estimate -= len(node.label.split()) + len(node.content.split())
                # Remove edges connected to this node
                edge_ids_to_remove = [
                    eid for eid, edge in compressed.edges.items()
                    if edge.source == node_id or edge.target == node_id
                ]
                for eid in edge_ids_to_remove:
                    compressed.edges.pop(eid, None)

        return compressed
