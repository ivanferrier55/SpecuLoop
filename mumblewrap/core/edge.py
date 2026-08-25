from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


# Default semantic forces for relation types
# These are HYPOTHESIS values — replaceable

# SpecuLoop — Persistent Semantic State Engine (WRAP)
# Semantic graph memory for AI agents: nodes, edges, forces.
# Supports: DRAG (Dynamic RAG), semantic zoom, interlocked translation,
# provenance tracking, self-extension, edit feedback propagation.
# Core: Mumble <-> WRAP graph bidirectional translation.

RELATION_FORCES = {
    "causes":       {"direction": "forward", "sign": 1.0},
    "increases":    {"direction": "forward", "sign": 1.0},
    "decreases":    {"direction": "forward", "sign": -1.0},
    "supports":     {"direction": "bidirectional", "sign": 1.0},
    "opposes":      {"direction": "bidirectional", "sign": -1.0},
    "requires":     {"direction": "backward", "sign": 1.0},
    "demonstrates": {"direction": "forward", "sign": 0.5},
    "clarifies":    {"direction": "forward", "sign": 0.3},
    "motivates":    {"direction": "forward", "sign": 0.7},
    "solves":       {"direction": "forward", "sign": 0.8},
    "contains":     {"direction": "forward", "sign": 0.0},
    "part_of":      {"direction": "backward", "sign": 0.0},
}


@dataclass
class Edge:
    """A semantic relationship between two WRAP nodes."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    source: str = ""
    target: str = ""
    relation: str = "supports"
    weight: float = 1.0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)
    lenses: dict[str, dict[str, float]] = field(default_factory=dict)

    def force(self) -> dict:
        """Return the semantic force of this edge based on its relation type."""
        base = RELATION_FORCES.get(self.relation, {"direction": "forward", "sign": 0.0})
        return {
            "direction": base["direction"],
            "magnitude": base["sign"] * self.weight,
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "weight": self.weight,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "lenses": self.lenses,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Edge:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return self.id == other.id
