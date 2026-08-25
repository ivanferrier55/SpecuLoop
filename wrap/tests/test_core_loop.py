"""End-to-end test of the WRAP core loop.

This tests the full vertical slice:
  Mumble → WRAP → persistent graph → selected graph → Mumble Markdown → edit → WRAP update
"""
import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from wrap.core import Node, Edge, Graph, Lens
from wrap.translation import Translator, Decomposer, Composer
from wrap.drag import DRAGSelector, Subgraph
from wrap.drag.scorer import Scorer
from wrap.extension import SelfExtender, Proposal
from wrap.feedback import FeedbackPropagator, EditResult
from wrap.persistence import Store
from wrap.api import SpecuLoop


def test_node_creation():
    """Test basic node creation."""
    n = Node(kind="concept", label="speed", content="The rate of execution")
    assert n.id
    assert n.kind == "concept"
    assert n.label == "speed"
    print("✓ Node creation")


def test_edge_creation():
    """Test basic edge creation."""
    n1 = Node(kind="concept", label="speed")
    n2 = Node(kind="concept", label="quality")
    e = Edge(source=n1.id, target=n2.id, relation="decreases")
    assert e.source == n1.id
    assert e.target == n2.id
    force = e.force()
    assert force["magnitude"] < 0  # decreases is negative
    print("✓ Edge creation and force computation")


def test_graph_persistence():
    """Test graph save/load."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test_graph.json")
        
        # Create and save
        g = Graph()
        n1 = Node(kind="concept", label="A", content="Node A")
        n2 = Node(kind="concept", label="B", content="Node B")
        g.add_node(n1)
        g.add_node(n2)
        g.add_edge(Edge(source=n1.id, target=n2.id, relation="causes"))
        g.save(path)
        
        # Load
        g2 = Graph.load(path)
        assert len(g2.nodes) == 2
        assert len(g2.edges) == 1
        assert g2.get_node(n1.id).label == "A"
        print("✓ Graph persistence")


def test_ingest_simple():
    """Test ingesting a simple statement."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        
        result = loop.ingest("Increasing speed decreases quality.")
        
        assert result.confidence > 0
        assert len(result.new_nodes) >= 2  # speed, quality
        assert len(result.new_edges) >= 1  # decreases
        
        # Check graph has the structures
        assert len(loop.graph.nodes) >= 2
        assert len(loop.graph.edges) >= 1
        
        # Verify the edge
        edge = list(loop.graph.edges.values())[0]
        assert edge.relation == "decreases"
        
        print(f"✓ Ingest: {result.details}")
        print(f"  Nodes: {len(result.new_nodes)} new, {len(result.reused_nodes)} reused")
        print(f"  Edges: {len(result.new_edges)} new")


def test_emit_markdown():
    """Test generating Mumble Markdown from graph."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        
        # Build a small graph
        n1 = Node(kind="concept", label="speed", content="execution speed")
        n2 = Node(kind="concept", label="quality", content="output quality")
        loop.graph.add_node(n1)
        loop.graph.add_node(n2)
        loop.graph.add_edge(Edge(source=n1.id, target=n2.id, relation="decreases"))
        
        # Emit
        result = loop.emit()
        
        assert result.markdown
        assert "speed" in result.markdown.lower() or "quality" in result.markdown.lower()
        assert "provenance" in result.markdown
        
        print(f"✓ Emit: {result.token_estimate} tokens")
        print(f"  Output: {result.markdown[:200]}...")


def test_full_vertical_slice():
    """Test the complete Mumble → WRAP → Mumble → edit → WRAP loop."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        
        # Step 1: Ingest
        print("\n--- Step 1: Ingest ---")
        result1 = loop.ingest("Speed and quality are in tension.")
        print(f"  Ingested: {result1.details}")
        print(f"  Graph: {loop.stats()}")
        
        # Step 2: Emit (generate Markdown)
        print("\n--- Step 2: Emit ---")
        emit1 = loop.emit_full()
        print(f"  Markdown:\n{emit1.markdown}")
        
        # Step 3: Human edit
        print("\n--- Step 3: Human Edit ---")
        # The original markdown mentions "speed" and "quality"
        # Human adds a qualifier about tooling
        edited = emit1.markdown.replace(
            "Speed",
            "Speed, with good tooling,"
        ) if emit1.markdown else "Speed, with good tooling, decreases quality."
        
        # For this test, construct a realistic edit
        original_text = emit1.markdown
        # Simulate: original said "Speed decreases quality."
        # Human edits to: "Speed, with good tooling, can reduce quality loss."
        
        # Step 4: Process edit
        print("\n--- Step 4: Process Edit ---")
        # We'll create a direct edit scenario
        if emit1.provenance:
            # Construct edit based on what was generated
            edit_result = loop.edit(
                original_markdown=emit1.markdown,
                edited_markdown="Speed, with good tooling, can reduce quality loss."
            )
            print(f"  Edit result: {edit_result.details}")
            print(f"  Affected nodes: {edit_result.affected_node_ids}")
            print(f"  New nodes: {[n.label for n in edit_result.new_nodes]}")
        else:
            print("  (No provenance to test edit propagation)")
        
        # Step 5: Verify graph state
        print("\n--- Step 5: Verify Graph ---")
        print(f"  Final stats: {loop.stats()}")
        
        # Verify persistence
        loop2 = SpecuLoop(path)
        assert loop2.stats()["nodes"] == loop.stats()["nodes"]
        print(f"  ✓ Persistence verified")


def test_drag_query():
    """Test DRAG selection and query."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        
        # Build a graph with multiple concepts
        loop.ingest("Speed and quality are in tension.")
        loop.ingest("Good tooling improves quality.")
        loop.ingest("Time pressure increases speed.")
        
        # Query
        result = loop.query("What affects quality?")
        assert result.markdown
        assert "quality" in result.markdown.lower()
        
        print(f"✓ DRAG query: {result.token_estimate} tokens")
        print(f"  Result: {result.markdown[:300]}")


def test_self_extension():
    """Test self-extension proposals."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        
        # Propose a new primitive
        proposal = loop.propose("consciousness")
        assert proposal.kind == "primitive"
        assert proposal.proposed_node is not None
        assert proposal.proposed_node.label == "consciousness"
        
        print(f"✓ Proposal: {proposal.reason}")
        
        # Confirm it
        confirmed = loop.confirm_proposal(proposal)
        assert confirmed
        assert "consciousness" in [n.label for n in loop.graph.nodes.values()]
        
        print(f"  Confirmed and added to graph")


def test_lens():
    """Test lens filtering."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.json")
        loop = SpecuLoop(path)
        
        loop.ingest("Speed and quality are in tension.")
        loop.ingest("Good tooling improves quality.")
        
        # Create a lens that emphasizes quality
        lens = Lens(
            name="quality-focus",
            description="Emphasizes quality-related concepts",
            kind_weights={"concept": 1.5},
            relation_weights={"decreases": 2.0, "increases": 2.0},
        )
        loop.add_lens(lens)
        
        # Query with lens
        result = loop.query("quality", lens=lens)
        assert result.markdown
        
        print(f"✓ Lens filtering works")
        print(f"  Result: {result.markdown[:200]}")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("WRAP Core Loop — End-to-End Test")
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
