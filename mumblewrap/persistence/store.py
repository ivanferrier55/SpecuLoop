"""Store: handles persistence of the WRAP graph.

Wraps Graph.save/load with convenience methods.
"""
from __future__ import annotations
from pathlib import Path

from ..core.graph import Graph


class Store:
    """Persistent storage for the WRAP graph."""

    def __init__(self, path: str | Path = "wrap_graph.json"):
        self.path = Path(path)

    def save(self, graph: Graph) -> None:
        graph.save(self.path)

    def load(self) -> Graph:
        if self.path.exists():
            return Graph.load(self.path)
        return Graph()

    def exists(self) -> bool:
        return self.path.exists()
