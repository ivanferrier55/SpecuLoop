
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

"""WRAP Node — A semantic unit in the knowledge graph.

Nodes represent concepts, actions, entities, properties, states, constraints,
or primitives. Each node carries:
    - kind: what type of semantic unit this is
    - label: human-readable name
    - content: semantic content
    - usage_count: how often this node has been reused
    - lenses: per-lens weight and relevance modifiers
    - metadata: arbitrary extensible data

Nodes are the atomic units of meaning in WRAP.
"""
from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    """A semantic unit in the WRAP graph."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    kind: str = "concept"  # concept, action, entity, property, state, constraint, primitive
    label: str = ""
    content: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    usage_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    lenses: dict[str, dict[str, float]] = field(default_factory=dict)  # lens_id → {weight, relevance}

    def update_usage(self) -> None:
        self.usage_count += 1
        self.updated_at = time.time()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kind": self.kind,
            "label": self.label,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "usage_count": self.usage_count,
            "metadata": self.metadata,
            "lenses": self.lenses,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Node:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.id == other.id
