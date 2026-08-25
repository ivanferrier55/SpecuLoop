
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

"""SelfExtender: proposes new primitives when decomposition fails.

When existing WRAP structures can't represent an input, this component
proposes new nodes or edges for human confirmation.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field

from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge


@dataclass
class Proposal:
    """A proposed new WRAP structure."""
    id: str = field(default_factory=lambda: f"prop_{int(time.time()*1000)}")
    kind: str = "primitive"  # "primitive" or "relation"
    proposed_node: Node | None = None
    proposed_edge: Edge | None = None
    reason: str = ""
    alternatives: list[str] = field(default_factory=list)
    confidence: float = 0.0
    source_text: str = ""
    created_at: float = field(default_factory=time.time)
    status: str = "pending"  # pending, confirmed, modified, rejected


class SelfExtender:
    """Proposes new structures when decomposition fails.

    Initial implementation: simple heuristic proposals.
    Replaceable with: LLM-based proposal, embedding-based matching, etc.
    """

    def propose_primitive(self, text: str, context: list[str] | None = None) -> Proposal:
        """Propose a new primitive node for an unrecognized concept."""
        # Simple heuristic: use the text as label, infer kind from context
        kind = "concept"
        context_text = " ".join(context or []).lower()

        # Kind inference (HYPOTHESIS — very basic)
        action_words = {"make", "do", "run", "build", "fix", "implement", "increase", "decrease"}
        entity_words = {"system", "tool", "module", "file", "server", "database"}
        property_words = {"fast", "slow", "reliable", "secure", "efficient", "simple"}

        words = set(text.lower().split())
        if words & action_words:
            kind = "action"
        elif words & entity_words:
            kind = "entity"
        elif words & property_words:
            kind = "property"

        node = Node(
            kind=kind,
            label=text.strip(),
            content=text.strip(),
            metadata={"proposed": True, "context": context or []},
        )

        return Proposal(
            kind="primitive",
            proposed_node=node,
            reason=f"No existing primitive matches '{text}'. Proposing new {kind}.",
            alternatives=[],
            confidence=0.3,
            source_text=text,
        )

    def propose_relation(self, source_id: str, target_id: str,
                         context: str, graph: Graph) -> Proposal:
        """Propose a new edge for an unrecognized relationship."""
        source = graph.get_node(source_id)
        target = graph.get_node(target_id)

        # Default to "supports" — most generic relation
        relation = "supports"

        edge = Edge(
            source=source_id,
            target=target_id,
            relation=relation,
            metadata={"proposed": True, "context": context},
        )

        source_label = source.label if source else source_id
        target_label = target.label if target else target_id

        return Proposal(
            kind="relation",
            proposed_edge=edge,
            reason=f"Proposing '{relation}' between '{source_label}' and '{target_label}'",
            alternatives=["causes", "motivates", "clarifies"],
            confidence=0.2,
            source_text=context,
        )

    def confirm(self, proposal: Proposal, graph: Graph,
                feedback: str = "") -> bool:
        """Confirm or modify a proposal. Returns True if added to graph."""
        if proposal.status != "pending":
            return False

        if feedback:
            proposal.status = "modified"
            # Simple modification: if feedback suggests a different label, use it
            if proposal.proposed_node and feedback.strip():
                proposal.proposed_node.label = feedback.strip()
                proposal.proposed_node.content = feedback.strip()
            if proposal.proposed_edge and feedback.strip():
                # Try to match feedback to a known relation
                known_relations = {"causes", "increases", "decreases", "supports",
                                   "opposes", "requires", "motivates", "solves",
                                   "clarifies", "demonstrates"}
                for rel in known_relations:
                    if rel in feedback.lower():
                        proposal.proposed_edge.relation = rel
                        break
        else:
            proposal.status = "confirmed"

        # Add to graph
        if proposal.proposed_node:
            proposal.proposed_node.metadata["proposed"] = False
            proposal.proposed_node.metadata["confirmed_at"] = time.time()
            graph.add_node(proposal.proposed_node)

        if proposal.proposed_edge:
            proposal.proposed_edge.metadata["proposed"] = False
            proposal.proposed_edge.metadata["confirmed_at"] = time.time()
            if (proposal.proposed_edge.source in graph.nodes and
                proposal.proposed_edge.target in graph.nodes):
                graph.add_edge(proposal.proposed_edge)

        return True
