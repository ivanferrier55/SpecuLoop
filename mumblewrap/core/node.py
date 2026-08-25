from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any



# SpecuLoop — Persistent Semantic State Engine (WRAP)
# Semantic graph memory for AI agents: nodes, edges, forces.
# Supports: DRAG (Dynamic RAG), semantic zoom, interlocked translation,
# provenance tracking, self-extension, edit feedback propagation.
# Core: Mumble <-> WRAP graph bidirectional translation.

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
