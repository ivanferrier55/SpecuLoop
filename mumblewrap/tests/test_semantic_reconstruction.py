"""Tests for the semantic compression/self-update loop."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mumblewrap.api import SpecuLoop
from mumblewrap.core import Node


def test_existing_basis_compresses_clue():
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = SpecuLoop(Path(tmpdir) / "graph.json")
        loop.graph.add_node(Node(kind="primitive", label="semantic zoom", content="compress information at different granularities"))
        result = loop.learn("semantic zoom compresses information at different granularities")
        assert result.compression.coverage > 0.35
        assert result.compression.uncertainty < 0.65


def test_uncompressible_clue_generates_provisional_candidate():
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = SpecuLoop(Path(tmpdir) / "graph.json")
        result = loop.learn("a decoder needs a model-specific semantic scaffold")
        assert result.compression.candidate is not None
        assert result.compression.candidate.kind == "primitive"
        assert result.compression.candidate.metadata["provisional"] is True
        assert result.compression.uncertainty > 0
        assert result.evidence_id is not None
        assert any(node.kind == "evidence" for node in loop.graph.nodes.values())


def test_candidate_can_be_accepted_and_reused():
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = SpecuLoop(Path(tmpdir) / "graph.json")
        first = loop.learn("decoder scaffold")
        candidate = first.compression.candidate
        assert candidate is not None
        loop.accept_candidate(candidate)
        second = loop.learn("decoder scaffold")
        assert candidate.id in second.compression.reused_node_ids
        assert candidate.usage_count > 0


def test_decoder_score_is_separate_from_structural_coverage():
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = SpecuLoop(Path(tmpdir) / "graph.json")
        loop.graph.add_node(Node(kind="primitive", label="semantic zoom", content="lens dependent compression"))
        result = loop.learn(
            "semantic zoom is lens dependent compression",
            decoder=lambda compact: "semantic zoom is lens dependent compression",
            lens="overview",
            task="onboarding",
            decoder_name="test-decoder",
        )
        assert result.compression.decoder_score is not None
        assert result.compression.decoder_score > 0.8
        assert result.compression.lens == "overview"
        assert result.compression.task == "onboarding"
        assert result.compression.decoder == "test-decoder"


def test_refactor_proposal_is_non_destructive_until_accepted():
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = SpecuLoop(Path(tmpdir) / "graph.json")
        first = Node(kind="primitive", label="semantic", content="semantic representation")
        second = Node(kind="primitive", label="compression", content="compress information")
        loop.graph.add_node(first)
        loop.graph.add_node(second)
        loop.learn("semantic compression preserves semantic representation and compresses information")

        candidate = Node(
            kind="primitive",
            label="semantic compression",
            content="semantic compression preserves semantic representation and compresses information",
        )
        proposal = loop.propose_refactor([first.id, second.id], candidate)
        assert proposal is not None
        assert proposal.improvement > 0
        assert loop.graph.get_node(candidate.id) is None

        accepted = loop.accept_refactor(proposal, minimum_improvement=0.0)
        assert loop.graph.get_node(accepted.id) is not None
        assert loop.graph.get_node(first.id).metadata["superseded_by"] == accepted.id
        assert loop.graph.get_node(second.id).metadata["superseded_by"] == accepted.id


def run_all_tests():
    tests = [
        test_existing_basis_compresses_clue,
        test_uncompressible_clue_generates_provisional_candidate,
        test_candidate_can_be_accepted_and_reused,
        test_decoder_score_is_separate_from_structural_coverage,
        test_refactor_proposal_is_non_destructive_until_accepted,
    ]
    for test in tests:
        test()
        print(f"✓ {test.__name__}")
    print(f"{len(tests)}/{len(tests)} semantic tests passed")


if __name__ == "__main__":
    run_all_tests()
