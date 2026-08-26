"""Grounding: evidence entering the semantic system."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field


@dataclass
class Grounding:
    """Evidence entering SpecuLoop from any source, not only humans."""

    text: str
    kind: str = "human"
    strength: float = 0.5
    id: str = field(default_factory=lambda: f"g-{uuid.uuid4().hex[:12]}")
    created_at: float = field(default_factory=time.time)
    provenance: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.strength = max(0.0, min(1.0, float(self.strength)))

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "kind": self.kind,
            "strength": self.strength,
            "created_at": self.created_at,
            "provenance": self.provenance,
            "metadata": self.metadata,
        }
