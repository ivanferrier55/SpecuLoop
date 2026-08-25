"""Composer: generates Mumble Markdown from WRAP structures.

This is the INITIAL implementation using template-based generation.
It is explicitly replaceable with LLM-based or more sophisticated generation.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge
from ..core.lens import Lens


# Natural language templates for relations (HYPOTHESIS — replaceable)
RELATION_TEMPLATES = {
    "causes":       "{source} causes {target}",
    "increases":    "{source} increases {target}",
    "decreases":    "{source} decreases {target}",
    "supports":     "{source} supports {target}",
    "opposes":      "{source} opposes {target}",
    "requires":     "{source} requires {target}",
    "demonstrates": "{source} demonstrates {target}",
    "clarifies":    "{source} clarifies {target}",
    "motivates":    "{source} motivates {target}",
    "solves":       "{source} solves {target}",
    "contains":     "{source} contains {target}",
    "part_of":      "{target} is part of {source}",
}


@dataclass
class Provenance:
    """Tracks which WRAP structures produced a generated sentence."""
    sentence_id: str
    node_ids: list[str] = field(default_factory=list)
    edge_ids: list[str] = field(default_factory=list)
    lens_id: str = "default"
    generated_at: float = 0.0


@dataclass
class CompositionResult:
    markdown: str = ""
    provenance: list[Provenance] = field(default_factory=list)
    token_estimate: int = 0  # rough word count as proxy


class Composer:
    """Generates Mumble Markdown from WRAP structures.

    Initial implementation: template-based.
    Replaceable with: LLM generation, more sophisticated NLG, etc.
    """

    def compose(self, node_ids: list[str] | None = None,
                edge_ids: list[str] | None = None,
                graph: Graph | None = None,
                lens: Lens | None = None) -> CompositionResult:
        """Generate Mumble Markdown from selected WRAP structures."""
        if graph is None:
            return CompositionResult()

        result = CompositionResult()
        sentences = []
        sentence_counter = 0

        # If specific nodes/edges given, compose from those
        if node_ids or edge_ids:
            target_edges = []
            if edge_ids:
                target_edges = [graph.edges[eid] for eid in edge_ids if eid in graph.edges]
            elif node_ids:
                # Get all edges between the specified nodes
                for nid in node_ids:
                    for edge in graph.get_edges(nid):
                        if edge.source in node_ids and edge.target in node_ids:
                            target_edges.append(edge)

            for edge in target_edges:
                sentence = self._compose_edge(edge, graph, lens)
                if sentence:
                    sentence_counter += 1
                    prov = Provenance(
                        sentence_id=f"s{sentence_counter}",
                        node_ids=[edge.source, edge.target],
                        edge_ids=[edge.id],
                        lens_id=lens.id if lens else "default",
                    )
                    sentences.append(f"<!-- provenance: {prov.sentence_id} nodes={prov.node_ids} edges={prov.edge_ids} lens={prov.lens_id} -->\n"
                                    f"{sentence}\n"
                                    f"<!-- /provenance -->")
                    result.provenance.append(prov)

            # Add any standalone nodes
            if node_ids:
                for nid in node_ids:
                    node = graph.get_node(nid)
                    if node and not any(e.source == nid or e.target == nid for e in target_edges):
                        sentence_counter += 1
                        text = self._compose_node(node, lens)
                        prov = Provenance(
                            sentence_id=f"s{sentence_counter}",
                            node_ids=[nid],
                            lens_id=lens.id if lens else "default",
                        )
                        sentences.append(f"<!-- provenance: {prov.sentence_id} nodes=[{nid}] lens={prov.lens_id} -->\n"
                                        f"{text}\n"
                                        f"<!-- /provenance -->")
                        result.provenance.append(prov)
        else:
            # Compose from entire graph (or lens-filtered)
            composed_edges = set()
            for edge in graph.edges.values():
                if lens:
                    w = lens.edge_weight(edge.id, edge.relation)
                    if w < 0.1:
                        continue
                if edge.id not in composed_edges:
                    sentence = self._compose_edge(edge, graph, lens)
                    if sentence:
                        sentence_counter += 1
                        prov = Provenance(
                            sentence_id=f"s{sentence_counter}",
                            node_ids=[edge.source, edge.target],
                            edge_ids=[edge.id],
                            lens_id=lens.id if lens else "default",
                        )
                        sentences.append(f"<!-- provenance: {prov.sentence_id} nodes={prov.node_ids} edges={prov.edge_ids} lens={prov.lens_id} -->\n"
                                        f"{sentence}\n"
                                        f"<!-- /provenance -->")
                        result.provenance.append(prov)
                        composed_edges.add(edge.id)

        result.markdown = "\n\n".join(sentences)
        result.token_estimate = len(result.markdown.split())
        return result

    def _compose_edge(self, edge: Edge, graph: Graph, lens: Lens | None = None) -> str:
        source = graph.get_node(edge.source)
        target = graph.get_node(edge.target)
        if not source or not target:
            return ""

        template = RELATION_TEMPLATES.get(edge.relation, f"{source.label} --{edge.relation}--> {target.label}")
        text = template.format(source=source.label, target=target.label)

        # Add qualifier if weight is not default
        if edge.weight < 0.5:
            text = f"Perhaps, {text.lower()}"
        elif edge.weight > 2.0:
            text = f"Importantly, {text.lower()}"

        return text[0].upper() + text[1:] + "."

    def _compose_node(self, node: Node, lens: Lens | None = None) -> str:
        return f"{node.label}: {node.content}" if node.content else node.label
