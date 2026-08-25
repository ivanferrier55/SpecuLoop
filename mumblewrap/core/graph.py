
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

"""WRAP Graph — Persistent semantic knowledge store.

The graph is the authoritative store of all WRAP state. It contains:
    - nodes: semantic units (concepts, actions, entities, etc.)
    - edges: typed relationships with numeric forces
    - lenses: filters that modify how the graph is viewed
    - adjacency: fast lookup of connections per node

The graph is designed to be inspectable and human-readable in JSON format.
"""
from __future__ import annotations
import time
import json
from pathlib import Path
from typing import Any

from .node import Node
from .edge import Edge
from .lens import Lens


class Graph:
    """The persistent WRAP semantic graph."""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, Edge] = {}
        self.adjacency: dict[str, list[str]] = {}  # node_id → [edge_ids]
        self.lenses: dict[str, Lens] = {}
        self.created_at = time.time()
        self.updated_at = time.time()

    # --- Node operations ---

    def add_node(self, node: Node) -> Node:
        self.nodes[node.id] = node
        self.adjacency.setdefault(node.id, [])
        self.updated_at = time.time()
        return node

    def get_node(self, node_id: str) -> Node | None:
        return self.nodes.get(node_id)

    def find_nodes(self, query: str, kind: str = "") -> list[Node]:
        """Find nodes matching a query string in label or content."""
        query_lower = query.lower()
        results = []
        for node in self.nodes.values():
            if kind and node.kind != kind:
                continue
            if (query_lower in node.label.lower() or 
                query_lower in node.content.lower()):
                results.append(node)
        return results

    def find_node_by_label(self, label: str) -> Node | None:
        """Find a node by exact label match (case-insensitive)."""
        label_lower = label.lower()
        for node in self.nodes.values():
            if node.label.lower() == label_lower:
                return node
        return None

    def remove_node(self, node_id: str) -> None:
        """Remove a node and all connected edges."""
        edge_ids = list(self.adjacency.get(node_id, []))
        for eid in edge_ids:
            self._remove_edge_by_id(eid)
        self.nodes.pop(node_id, None)
        self.adjacency.pop(node_id, None)
        self.updated_at = time.time()

    # --- Edge operations ---

    def add_edge(self, edge: Edge) -> Edge:
        if edge.source not in self.nodes or edge.target not in self.nodes:
            raise ValueError(f"Edge references unknown node: {edge.source} → {edge.target}")
        self.edges[edge.id] = edge
        self.adjacency.setdefault(edge.source, []).append(edge.id)
        if edge.source != edge.target:
            self.adjacency.setdefault(edge.target, []).append(edge.id)
        self.updated_at = time.time()
        return edge

    def get_edge(self, edge_id: str) -> Edge | None:
        return self.edges.get(edge_id)

    def get_edges(self, node_id: str, direction: str = "both") -> list[Edge]:
        """Get edges connected to a node. direction: 'out', 'in', 'both'."""
        edge_ids = self.adjacency.get(node_id, [])
        results = []
        for eid in edge_ids:
            edge = self.edges.get(eid)
            if edge is None:
                continue
            if direction == "out" and edge.source == node_id:
                results.append(edge)
            elif direction == "in" and edge.target == node_id:
                results.append(edge)
            elif direction == "both":
                results.append(edge)
        return results

    def find_edges(self, relation: str = "", source: str = "", target: str = "") -> list[Edge]:
        """Find edges matching criteria."""
        results = []
        for edge in self.edges.values():
            if relation and edge.relation != relation:
                continue
            if source and edge.source != source:
                continue
            if target and edge.target != target:
                continue
            results.append(edge)
        return results

    def _remove_edge_by_id(self, edge_id: str) -> None:
        edge = self.edges.pop(edge_id, None)
        if edge:
            for nid in (edge.source, edge.target):
                if nid in self.adjacency:
                    self.adjacency[nid] = [eid for eid in self.adjacency[nid] if eid != edge_id]

    def remove_edge(self, edge_id: str) -> None:
        self._remove_edge_by_id(edge_id)
        self.updated_at = time.time()

    # --- Lens operations ---

    def add_lens(self, lens: Lens) -> Lens:
        self.lenses[lens.id] = lens
        return lens

    def get_lens(self, lens_id: str) -> Lens | None:
        return self.lenses.get(lens_id)

    # --- Search ---

    def find_edges_between(self, node_a: str, node_b: str) -> list[Edge]:
        """Find all edges between two nodes (either direction)."""
        results = []
        for edge in self.edges.values():
            if (edge.source == node_a and edge.target == node_b) or \
               (edge.source == node_b and edge.target == node_a):
                results.append(edge)
        return results

    def connected_nodes(self, node_id: str) -> list[tuple[Node, Edge]]:
        """Get all nodes connected to a given node, with the connecting edge."""
        results = []
        for edge in self.get_edges(node_id):
            other_id = edge.target if edge.source == node_id else edge.source
            other_node = self.nodes.get(other_id)
            if other_node:
                results.append((other_node, edge))
        return results

    # --- Stats ---

    def stats(self) -> dict:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "lenses": len(self.lenses),
            "node_kinds": self._count_kinds(),
            "relation_types": self._count_relations(),
        }

    def _count_kinds(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for node in self.nodes.values():
            counts[node.kind] = counts.get(node.kind, 0) + 1
        return counts

    def _count_relations(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for edge in self.edges.values():
            counts[edge.relation] = counts.get(edge.relation, 0) + 1
        return counts

    # --- Persistence ---

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges.values()],
            "lenses": [l.to_dict() for l in self.lenses.values()],
        }
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: str | Path) -> Graph:
        path = Path(path)
        data = json.loads(path.read_text())
        graph = cls()
        graph.created_at = data.get("created_at", time.time())
        graph.updated_at = data.get("updated_at", time.time())
        for nd in data.get("nodes", []):
            graph.add_node(Node.from_dict(nd))
        for ed in data.get("edges", []):
            graph.add_edge(Edge.from_dict(ed))
        for ld in data.get("lenses", []):
            graph.add_lens(Lens.from_dict(ld))
        return graph
