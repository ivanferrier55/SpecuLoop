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
        )
        assert result.compression.decoder_score is not None
        assert result.compression.decoder_score > 0.8


def run_all_tests():
    tests = [
        test_existing_basis_compresses_clue,
        test_uncompressible_clue_generates_provisional_candidate,
        test_candidate_can_be_accepted_and_reused,
        test_decoder_score_is_separate_from_structural_coverage,
    ]
    for test in tests:
        test()
        print(f"✓ {test.__name__}")
    print(f"{len(tests)}/{len(tests)} semantic tests passed")


if __name__ == "__main__":
    run_all_tests()
