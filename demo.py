"""mumbleWRAP Demo — demonstrates the core semantic loop.

Run: python3 demo.py
"""
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mumblewrap.api import SpecuLoop
from mumblewrap.core import Lens


def main():
    print("=" * 60)
    print("mumbleWRAP — Core Loop Demo")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "demo_graph.json")
        loop = SpecuLoop(path)

        print("\n▸ Phase 1: Ingesting knowledge into mumbleWRAP\n")
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

        print("\n▸ Phase 2: Generating human-readable text from mumbleWRAP\n")
        emit = loop.emit_full()
        print(emit.markdown)
        print(f"  ({emit.token_estimate} tokens)")

        print("\n▸ Phase 3: DRAG query — 'What affects quality?'\n")
        result = loop.query("What affects quality?")
        print(result.markdown)
        print(f"  ({result.token_estimate} tokens)")

        print("\n▸ Phase 4: Lens filtering — 'quality-focus'\n")
        lens = Lens(
            name="quality-focus",
            description="Emphasizes quality-related relationships",
            relation_weights={"increases": 2.0, "decreases": 1.5},
        )
        loop.add_lens(lens)
        result_lens = loop.query("quality", lens=lens)
        print(result_lens.markdown)

        print("\n▸ Phase 5: Human edits → mumbleWRAP update\n")
        original = emit.markdown
        edited = original.replace(
            "Speed opposes quality.",
            "Speed opposes quality, but good tooling reduces this tension."
        ) if "Speed opposes quality." in original else original + "\n\nGood tooling reduces the tension between speed and quality."

        edit_result = loop.edit(original, edited)
        print(f"  Edit propagation: {edit_result.details}")
        print(f"  New nodes: {[n.label for n in edit_result.new_nodes]}")

        print("\n▸ Phase 6: Self-extension\n")
        proposal = loop.propose("creativity")
        print(f"  Proposal: {proposal.reason}")
        loop.confirm_proposal(proposal)

        print("\n▸ Phase 7: Final graph state\n")
        print(f"  Stats: {loop.stats()}")
        print()
        for edge in loop.graph.edges.values():
            source = loop.graph.get_node(edge.source)
            target = loop.graph.get_node(edge.target)
            if source and target:
                print(f"    {source.label} --[{edge.relation}]--> {target.label}")

        print()
        print("=" * 60)
        print("Demo complete.")
        print("  mumbleWRAP → DRAG → human language → edit → mumbleWRAP")
        print("=" * 60)


if __name__ == "__main__":
    main()
