"""Decomposer: breaks input text into existing WRAP structures.

This is the INITIAL implementation using keyword/pattern matching.
It is explicitly replaceable with LLM-based or embedding-based decomposition.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field

from ..core.graph import Graph
from ..core.node import Node
from ..core.edge import Edge


# Verb→relation mapping (HYPOTHESIS — replaceable)
VERB_RELATION_MAP = {
    "increase": "increases",
    "increases": "increases",
    "boost": "increases",
    "improve": "increases",
    "improves": "increases",
    "enhance": "increases",
    "decrease": "decreases",
    "decreases": "decreases",
    "reduce": "decreases",
    "harm": "decreases",
    "lower": "decreases",
    "cause": "causes",
    "causes": "causes",
    "lead": "causes",
    "leads": "causes",
    "require": "requires",
    "requires": "requires",
    "need": "requires",
    "support": "supports",
    "supports": "supports",
    "help": "supports",
    "oppose": "opposes",
    "opposes": "opposes",
    "conflict": "opposes",
    "limit": "opposes",
    "motivate": "motivates",
    "motivates": "motivates",
    "inspire": "motivates",
    "solve": "solves",
    "solves": "solves",
    "fix": "solves",
    "clarify": "clarifies",
    "clarifies": "clarifies",
    "explain": "clarifies",
    "demonstrate": "demonstrates",
    "demonstrates": "demonstrates",
    "show": "demonstrates",
    "contain": "contains",
    "contains": "contains",
    "include": "contains",
    "include": "contains",
}

# Phrase→relation mapping (for multi-word expressions)
PHRASE_RELATION_MAP = {
    "are in tension": "opposes",
    "is in tension": "opposes",
    "in tension": "opposes",
    "trade off": "opposes",
    "trade-off": "opposes",
    "conflicts with": "opposes",
    "comes from": "causes",
    "results from": "causes",
    "leads to": "causes",
    "depends on": "requires",
    "depends upon": "requires",
    "is needed for": "requires",
    "is required for": "requires",
    "improves": "increases",
    "makes better": "increases",
    "makes worse": "decreases",
    "reduces": "decreases",
}

# Simple subject-verb-object pattern
SVO_PATTERN = re.compile(
    r"(.+?)\s+(?:increases?|decreases?|causes?|requires?|supports?|opposes?|"
    r"motivates?|solves?|clarifies?|demonstrates?|contains?|includes?)\s+(.+)",
    re.IGNORECASE,
)

# Phrase pattern (X and Y are in tension / X conflicts with Y)
PHRASE_PATTERNS = [
    (re.compile(r"(.+?)\s+and\s+(.+?)\s+are\s+in\s+tension", re.IGNORECASE), "opposes"),
    (re.compile(r"(.+?)\s+and\s+(.+?)\s+conflict", re.IGNORECASE), "opposes"),
    (re.compile(r"(.+?)\s+and\s+(.+?)\s+trade[- ]off", re.IGNORECASE), "opposes"),
    (re.compile(r"(.+?)\s+conflicts?\s+with\s+(.+)", re.IGNORECASE), "opposes"),
    (re.compile(r"(.+?)\s+depends?\s+on\s+(.+)", re.IGNORECASE), "requires"),
    (re.compile(r"(.+?)\s+leads?\s+to\s+(.+)", re.IGNORECASE), "causes"),
    (re.compile(r"(.+?)\s+results?\s+in\s+(.+)", re.IGNORECASE), "causes"),
    (re.compile(r"(.+?)\s+improves?\s+(.+)", re.IGNORECASE), "increases"),
    (re.compile(r"(.+?)\s+reduces?\s+(.+)", re.IGNORECASE), "decreases"),
]


@dataclass
class DecompositionResult:
    success: bool = False
    reused_nodes: list[Node] = field(default_factory=list)
    reused_edges: list[Edge] = field(default_factory=list)
    new_nodes: list[Node] = field(default_factory=list)
    new_edges: list[Edge] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    confidence: float = 0.0
    details: str = ""


class Decomposer:
    """Breaks input text into existing WRAP structures.

    Initial implementation: keyword/pattern matching.
    Replaceable with: LLM decomposition, embedding similarity, etc.
    """

    def decompose(self, text: str, graph: Graph) -> DecompositionResult:
        """Attempt to decompose text into graph structures."""
        result = DecompositionResult()

        # Try phrase patterns first (e.g., "X and Y are in tension")
        for pattern, relation in PHRASE_PATTERNS:
            match = pattern.search(text)
            if match:
                return self._decompose_pair(match.group(1).strip(), 
                                            match.group(2).strip(),
                                            relation, text, graph)

        # Try SVO pattern
        match = SVO_PATTERN.search(text)
        if match:
            subject_text = match.group(1).strip().strip(".")
            # Find the verb
            verb = ""
            rest = text[match.start():match.end()]
            for v in VERB_RELATION_MAP:
                if re.search(rf'\b{v}\b', rest, re.IGNORECASE):
                    verb = VERB_RELATION_MAP[v]
                    break
            object_text = match.group(2).strip().strip(".")

            if verb:
                return self._decompose_pair(subject_text, object_text, verb, text, graph)

        # Fallback: try to find any existing node that matches the text
        matches = graph.find_nodes(text)
        if matches:
            for m in matches:
                m.update_usage()
                result.reused_nodes.append(m)
            result.success = True
            result.confidence = 0.3
            result.details = f"Partial match: found {len(matches)} existing node(s)"
            return result

        # No decomposition possible
        result.gaps.append(text)
        result.confidence = 0.0
        result.details = "Could not decompose into existing structures"
        return result

    def _decompose_pair(self, subject_text: str, object_text: str,
                        relation: str, full_text: str, graph: Graph) -> DecompositionResult:
        """Decompose a subject-relation-object triple."""
        result = DecompositionResult()

        # Clean up labels
        subject_text = subject_text.strip().strip(".").strip('"')
        object_text = object_text.strip().strip(".").strip('"')

        # Find or create source node
        source = graph.find_node_by_label(subject_text)
        if source:
            source.update_usage()
            result.reused_nodes.append(source)
        else:
            source = Node(kind="concept", label=subject_text, content=subject_text)
            result.new_nodes.append(source)

        # Find or create target node
        target = graph.find_node_by_label(object_text)
        if target:
            target.update_usage()
            result.reused_nodes.append(target)
        else:
            target = Node(kind="concept", label=object_text, content=object_text)
            result.new_nodes.append(target)

        # Check if this edge already exists
        if source.id in graph.nodes and target.id in graph.nodes:
            existing_edges = graph.find_edges_between(source.id, target.id)
            for ee in existing_edges:
                if ee.relation == relation:
                    ee.weight = min(ee.weight + 0.1, 5.0)
                    result.reused_edges.append(ee)
                    result.success = True
                    result.confidence = 0.7
                    result.details = f"Strengthened existing: {subject_text} --{relation}--> {object_text}"
                    return result

        # Create new edge
        edge = Edge(source=source.id, target=target.id, relation=relation)
        result.new_edges.append(edge)

        result.success = True
        result.confidence = 0.6
        result.details = f"Decomposed as: {subject_text} --{relation}--> {object_text}"
        return result
