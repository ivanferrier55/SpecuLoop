"""End-to-end test of the mumbleWRAP core loop.

Tests the full vertical slice:
  Mumble → mumbleWRAP → DRAG → Mumble Markdown → edit → mumbleWRAP update
"""
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mumblewrap.core import Node, Edge, Graph, Lens
from mumblewrap.translation import Translator, Decomposer, Composer
from drag import DRAGSelector, Subgraph
from drag.scorer import Scorer
from speculoop import SelfExtender, Proposal, FeedbackPropagator, EditResult
from mumblewrap.persistence import Store
from mumblewrap.api import SpecuLoop


def test_node_creation():
    n = Node(kind="concept", label="speed", content="The rate of execution")
    assert n.id
    assert n.kind == "concept"
    assert n.label == "speed"
    print("✓ Node creation")


def test_edge_creation():
    n1 = Node(kind="concept", label="speed")
    n2 = Node(kind="concept", label="quality")
    e = Edge(source=n1.id, target=n2.id, relation="decreases")
    assert e.source == n1.id
    assert e.target == n2.id
    force = e.force()
    assert force["magnitude"] < 0
    print("✓ Edge creation and force computation")


def test_graph_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test_graph.json")
        g = Graph()
        n1 = Node(kind="concept", label="A", content="Node A")
        n2 = Node(kind="concept", label="B", content="Node B")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(source=n1.id, target=n2.id, relation="causes"))
        g.save(path)
        g2 = Graph.load(path)
        assert len(g2.nodes) == 2
        assert len(g2.edges) == 1
        assert g2.get_node(n1.id).label == "A"
        print("✓ Graph persistence")


def test_ingest_simple():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        result = loop.ingest("Increasing speed decreases quality.")
        assert result.confidence > 0
        assert len(result.new_nodes) >= 2
        assert len(result.new_edges) >= 1
        edge = list(loop.graph.edges.values())[0]
        assert edge.relation == "decreases"
        print(f"✓ Ingest: {result.details}")


def test_emit_markdown():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        n1 = Node(kind="concept", label="speed", content="execution speed")
        n2 = Node(kind="concept", label="quality", content="output quality")
        loop.graph.add_node(n1)
        loop.graph.add_node(n2)
        loop.graph.add_edge(Edge(source=n1.id, target=n2.id, relation="decreases"))
        result = loop.emit()
        assert result.markdown
        assert "speed" in result.markdown.lower() or "quality" in result.markdown.lower()
        assert "provenance" in result.markdown
        print(f"✓ Emit: {result.token_estimate} tokens")


def test_full_vertical_slice():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)

        print("\n--- Step 1: Ingest ---")
        result1 = loop.ingest("Speed and quality are in tension.")
        print(f"  Ingested: {result1.details}")

        print("\n--- Step 2: Emit ---")
        emit1 = loop.emit_full()
        print(f"  Markdown:\n{emit1.markdown}")

        print("\n--- Step 3: Human Edit ---")
        print("\n--- Step 4: Process Edit ---")
        if emit1.provenance:
            edit_result = loop.edit(
                original_markdown=emit1.markdown,
                edited_markdown="Speed, with good tooling, can reduce quality loss."
            )
            print(f"  Edit result: {edit_result.details}")

        print("\n--- Step 5: Verify ---")
        print(f"  Final stats: {loop.stats()}")

        loop2 = SpecuLoop(path)
        assert loop2.stats()["nodes"] == loop.stats()["nodes"]
        print(f"  ✓ Persistence verified")


def test_drag_query():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        loop.ingest("Speed and quality are in tension.")
        loop.ingest("Good tooling improves quality.")
        loop.ingest("Time pressure increases speed.")
        result = loop.query("What affects quality?")
        assert result.markdown
        assert "quality" in result.markdown.lower()
        print(f"✓ DRAG query: {result.token_estimate} tokens")


def test_self_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        proposal = loop.propose("creativity")
        assert proposal.kind == "primitive"
        assert proposal.proposed_node is not None
        assert proposal.proposed_node.label == "creativity"
        confirmed = loop.confirm_proposal(proposal)
        assert confirmed
        assert "creativity" in [n.label for n in loop.graph.nodes.values()]
        print(f"✓ Proposal confirmed and added")


def test_lens():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        loop.ingest("Speed and quality are in tension.")
        loop.ingest("Good tooling improves quality.")
        lens = Lens(
            name="quality-focus",
            description="Emphasizes quality-related relationships",
            kind_weights={"concept": 1.5},
            relation_weights={"decreases": 2.0, "increases": 2.0},
        )
        loop.add_lens(lens)
        result = loop.query("quality", lens=lens)
        assert result.markdown
        print(f"✓ Lens filtering works")


def run_all_tests():
    print("=" * 60)
    print("mumbleWRAP Core Loop — End-to-End Test")
    print("=" * 60)

    tests = [
        test_node_creation,
        test_edge_creation,
        test_graph_persistence,
        test_ingest_simple,
        test_emit_markdown,
        test_full_vertical_slice,
        test_drag_query,
        test_self_extension,
        test_lens,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            print(f"\n--- {test.__name__} ---")
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)}")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
