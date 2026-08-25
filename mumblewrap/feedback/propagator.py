
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

"""FeedbackPropagator: translates human edits back into WRAP updates.

This implements the "interlocked translation" feedback loop:
  edited Mumble → identify affected WRAP structures → update graph

Initial implementation: provenance-based tracking + heuristic updates.
Replaceable with: LLM-based semantic diff, embedding-based matching, etc.
"""
from __future__ import annotations
import re
import time
from dataclasses import dataclass, field

from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge


@dataclass
class EditResult:
    """Result of processing a human edit."""
    original_text: str = ""
    edited_text: str = ""
    affected_node_ids: list[str] = field(default_factory=list)
    affected_edge_ids: list[str] = field(default_factory=list)
    nodes_updated: list[Node] = field(default_factory=list)
    edges_updated: list[Edge] = field(default_factory=list)
    new_nodes: list[Node] = field(default_factory=list)
    new_edges: list[Edge] = field(default_factory=list)
    details: str = ""


class FeedbackPropagator:
    """Translates human edits back into WRAP updates.

    Initial implementation: provenance extraction + heuristic interpretation.
    Replaceable with: LLM-based semantic diff, embedding-based matching, etc.
    """

    def __init__(self, graph: Graph):
        self.graph = graph

    def process_edit(self, original_markdown: str, edited_markdown: str) -> EditResult:
        """Process a human edit to generated Markdown and propagate to WRAP."""
        result = EditResult(
            original_text=original_markdown,
            edited_text=edited_markdown,
        )

        # Extract provenance from both versions
        original_provs = self._extract_provenance(original_markdown)
        edited_provs = self._extract_provenance(edited_markdown)

        # Find which provenance groups were affected
        affected_ids = set()
        for s_id, prov in original_provs.items():
            if s_id in edited_provs:
                # Check if the text changed
                orig_text = self._extract_sentence_text(original_markdown, s_id)
                edit_text = self._extract_sentence_text(edited_markdown, s_id)
                if orig_text != edit_text:
                    affected_ids.update(prov["node_ids"])
                    affected_ids.update(prov["edge_ids"])
            else:
                # Sentence was removed
                affected_ids.update(prov["node_ids"])
                affected_ids.update(prov["edge_ids"])

        result.affected_node_ids = list(affected_ids & set(self.graph.nodes.keys()))
        result.affected_edge_ids = list(affected_ids & set(self.graph.edges.keys()))

        # For each affected node, try to interpret the semantic change
        for node_id in result.affected_node_ids:
            node = self.graph.get_node(node_id)
            if node:
                # Check if the edit contains the node's label
                if node.label.lower() in edited_markdown.lower():
                    # Node is still referenced — update usage
                    node.update_usage()
                    result.nodes_updated.append(node)
                else:
                    # Node may no longer be relevant — reduce weight
                    self._reduce_node_weight(node)

        # For each affected edge, try to interpret changes
        for edge_id in result.affected_edge_ids:
            edge = self.graph.get_edge(edge_id)
            if edge:
                source = self.graph.get_node(edge.source)
                target = self.graph.get_node(edge.target)
                if source and target:
                    # Check if the relationship is still expressed
                    if (source.label.lower() in edited_markdown.lower() and
                        target.label.lower() in edited_markdown.lower()):
                        # Relationship still present — check for qualifiers
                        qualifier = self._detect_qualifier(
                            source.label, target.label, edge.relation, edited_markdown
                        )
                        if qualifier == "strengthened":
                            edge.weight = min(edge.weight + 0.2, 5.0)
                        elif qualifier == "weakened":
                            edge.weight = max(edge.weight - 0.2, 0.1)
                        edge.updated_at = time.time()
                        result.edges_updated.append(edge)

        # Look for new concepts in the edit that aren't in the graph
        new_concepts = self._find_new_concepts(original_markdown, edited_markdown)
        for concept in new_concepts:
            node = Node(kind="concept", label=concept, content=concept,
                       metadata={"source": "human_edit", "timestamp": time.time()})
            self.graph.add_node(node)
            result.new_nodes.append(node)

        result.details = (
            f"Processed edit: {len(result.affected_node_ids)} affected nodes, "
            f"{len(result.nodes_updated)} updated, "
            f"{len(result.new_nodes)} new nodes"
        )
        return result

    def process_feedback(self, involved_structures: list[str],
                         success_score: float) -> None:
        """Process execution feedback (success/failure) for DRAG backprop.

        success_score: -1.0 (total failure) to 1.0 (perfect success)
        """
        for struct_id in involved_structures:
            # Update node
            node = self.graph.get_node(struct_id)
            if node:
                # Adjust relevance based on success
                relevance_delta = success_score * 0.1
                for lens_id, lens_data in node.lenses.items():
                    lens_data["relevance"] = lens_data.get("relevance", 1.0) + relevance_delta
                node.update_usage()

            # Update edges
            for edge in self.graph.get_edges(struct_id):
                relevance_delta = success_score * 0.05
                for lens_id, lens_data in edge.lenses.items():
                    lens_data["relevance"] = lens_data.get("relevance", 1.0) + relevance_delta

    def _extract_provenance(self, markdown: str) -> dict:
        """Extract provenance metadata from Markdown."""
        provs = {}
        pattern = re.compile(
            r'<!-- provenance: (\S+) nodes=\[([^\]]*)\](?:\s+edges=\[([^\]]*)\])?(?:\s+lens=(\S+))? -->',
            re.MULTILINE
        )
        for match in pattern.finditer(markdown):
            s_id = match.group(1)
            node_ids = [n.strip() for n in match.group(2).split(",") if n.strip()]
            edge_ids = [e.strip() for e in (match.group(3) or "").split(",") if e.strip()]
            lens = match.group(4) or "default"
            provs[s_id] = {"node_ids": node_ids, "edge_ids": edge_ids, "lens": lens}
        return provs

    def _extract_sentence_text(self, markdown: str, sentence_id: str) -> str:
        """Extract the text content of a provenance-marked sentence."""
        pattern = re.compile(
            rf'<!-- provenance: {re.escape(sentence_id)}.*?-->\n(.*?)\n<!-- /provenance -->',
            re.DOTALL
        )
        match = pattern.search(markdown)
        return match.group(1).strip() if match else ""

    def _detect_qualifier(self, source_label: str, target_label: str,
                          relation: str, text: str) -> str:
        """Detect if a relationship was strengthened or weakened in the edit."""
        # Simple heuristic: look for qualifying words
        weakening_words = {"perhaps", "maybe", "sometimes", "usually", "might", "could"}
        strengthening_words = {"always", "definitely", "certainly", "always", "must", "certainly"}

        text_lower = text.lower()
        for word in weakening_words:
            if word in text_lower:
                return "weakened"
        for word in strengthening_words:
            if word in text_lower:
                return "strengthened"
        return "unchanged"

    def _reduce_node_weight(self, node: Node) -> None:
        """Reduce a node's relevance when it appears less in edits."""
        for lens_id, lens_data in node.lenses.items():
            lens_data["relevance"] = max(lens_data.get("relevance", 1.0) * 0.9, 0.1)

    def _find_new_concepts(self, original: str, edited: str) -> list[str]:
        """Find concepts in the edit that weren't in the original."""
        # Simple: find capitalized words or quoted terms in the edit not in the original
        original_lower = original.lower()
        new_words = []

        # Look for quoted terms
        quoted = re.findall(r'"([^"]+)"', edited)
        for term in quoted:
            if term.lower() not in original_lower:
                new_words.append(term)

        # Look for capitalized phrases (simple heuristic)
        capitalized = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', edited)
        for phrase in capitalized:
            if phrase.lower() not in original_lower and len(phrase) > 2:
                # Check it's not a common word
                if phrase.lower() not in {"the", "and", "but", "for", "not", "you", "all", "can", "her", "was", "one", "our", "out"}:
                    new_words.append(phrase)

        # Deduplicate while preserving order
        seen = set()
        result = []
        for w in new_words:
            if w.lower() not in seen:
                seen.add(w.lower())
                result.append(w)
        return result
