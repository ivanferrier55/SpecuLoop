from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Lens:
    """A semantic lens that modifies how the graph is viewed and scored."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    node_weights: dict[str, float] = field(default_factory=dict)   # node_id → weight multiplier
    edge_weights: dict[str, float] = field(default_factory=dict)   # edge_id → weight multiplier
    kind_weights: dict[str, float] = field(default_factory=dict)   # node_kind → weight multiplier
    relation_weights: dict[str, float] = field(default_factory=dict)  # relation_type → weight multiplier
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def node_weight(self, node_id: str, node_kind: str = "") -> float:
        """Get the weight for a node under this lens."""
        if node_id in self.node_weights:
            return self.node_weights[node_id]
        if node_kind and node_kind in self.kind_weights:
            return self.kind_weights[node_kind]
        return 1.0

    def edge_weight(self, edge_id: str, relation: str = "") -> float:
        """Get the weight for an edge under this lens."""
        if edge_id in self.edge_weights:
            return self.edge_weights[edge_id]
        if relation and relation in self.relation_weights:
            return self.relation_weights[relation]
        return 1.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "node_weights": self.node_weights,
            "edge_weights": self.edge_weights,
            "kind_weights": self.kind_weights,
            "relation_weights": self.relation_weights,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Lens:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
