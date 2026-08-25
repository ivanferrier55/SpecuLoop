"""SpecuLoop WRAP Demo — demonstrates the core semantic loop.

Run: python3 demo.py
"""
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wrap.api import SpecuLoop
from wrap.core import Lens


def main():
    print("=" * 60)
    print("SpecuLoop WRAP — Core Loop Demo")
    print("=" * 60)
    
    # Use a temp file for this demo
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "demo_graph.json")
        loop = SpecuLoop(path)
        
        # --- Phase 1: Ingest knowledge ---
        print("\n▸ Phase 1: Ingesting knowledge into WRAP\n")
        
        statements = [
            "Speed and quality are in tension.",
            "Good tooling improves quality.",
            "Time pressure increases speed.",
            "Testing improves quality.",
            "Testing requires time.",
        ]
        
        for stmt in statements:
            result = loop.ingest(stmt)
            print(f"  \"{stmt}\"")
            print(f"    → {result.details}")
            print()
        
        print(f"  Graph state: {loop.stats()}")
        
        # --- Phase 2: Emit full graph as Markdown ---
        print("\n▸ Phase 2: Generating Mumble Markdown from WRAP\n")
        
        emit = loop.emit_full()
        print(emit.markdown)
        print(f"  ({emit.token_estimate} tokens)")
        
        # --- Phase 3: Query with DRAG ---
        print("\n▸ Phase 3: DRAG query — 'What affects quality?'\n")
        
        result = loop.query("What affects quality?")
        print(result.markdown)
        print(f"  ({result.token_estimate} tokens)")
        
        # --- Phase 4: Semantic zoom with lens ---
        print("\n▸ Phase 4: Lens filtering — 'quality-focus'\n")
        
        lens = Lens(
            name="quality-focus",
            description="Emphasizes quality-related relationships",
            relation_weights={"increases": 2.0, "decreases": 1.5},
        )
        loop.add_lens(lens)
        
        result_lens = loop.query("quality", lens=lens)
        print(result_lens.markdown)
        print(f"  ({result_lens.token_estimate} tokens)")
        
        # --- Phase 5: Human edit → WRAP update ---
        print("\n▸ Phase 5: Human edits generated Markdown\n")
        
        original = emit.markdown
        # Simulate human editing: add a nuance about tooling
        edited = original.replace(
            "Speed opposes quality.",
            "Speed opposes quality, but good tooling reduces this tension."
        ) if "Speed opposes quality." in original else original + "\n\nGood tooling reduces the tension between speed and quality."
        
        print("  Original:")
        print(f"    {original[:200]}...")
        print()
        print("  Edited:")
        print(f"    {edited[:200]}...")
        print()
        
        edit_result = loop.edit(original, edited)
        print(f"  Edit propagation: {edit_result.details}")
        print(f"  Affected nodes: {edit_result.affected_node_ids}")
        print(f"  New nodes: {[n.label for n in edit_result.new_nodes]}")
        
        # --- Phase 6: Self-extension ---
        print("\n▸ Phase 6: Self-extension — proposing new primitive\n")
        
        proposal = loop.propose("creativity")
        print(f"  Proposal: {proposal.reason}")
        print(f"  Kind: {proposal.kind}")
        print(f"  Confidence: {proposal.confidence}")
        
        confirmed = loop.confirm_proposal(proposal)
        print(f"  Confirmed: {confirmed}")
        
        # --- Phase 7: Final state ---
        print("\n▸ Phase 7: Final graph state\n")
        
        print(f"  Stats: {loop.stats()}")
        print()
        
        # Show the graph edges
        print("  Edges:")
        for edge in loop.graph.edges.values():
            source = loop.graph.get_node(edge.source)
            target = loop.graph.get_node(edge.target)
            if source and target:
                print(f"    {source.label} --[{edge.relation}]--> {target.label} (weight={edge.weight:.1f})")
        
        print()
        print("=" * 60)
        print("Demo complete. Core loop works:")
        print("  Mumble → WRAP → DRAG → Mumble → edit → WRAP update")
        print("=" * 60)


if __name__ == "__main__":
    main()
