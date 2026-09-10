"""End-to-end test of the Markdown workspace loop.

Markdown → semantic extraction → graph → provenance → edit Markdown
→ incremental update → explain what/why/where.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from speculoop.markdown_workspace import MarkdownWorkspace


def _write(ws: Path, name: str, content: str) -> Path:
    p = ws / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def _workspace() -> tuple[Path, "MarkdownWorkspace"]:
    tmp = Path(tempfile.mkdtemp())
    _write(tmp, "A.md", "# Speed\n\nSpeed and quality are in tension.\n")
    _write(tmp, "B.md", "# Quality\n\n- Good tooling improves quality.\n- Testing requires time.\n")
    _write(tmp, "C.md", "# Testing\n\nTesting improves quality.\n")
    return tmp, MarkdownWorkspace(tmp)


def test_ingest_builds_graph_with_provenance():
    ws, mw = _workspace()
    report = mw.ingest()
    assert report.files_scanned == 3
    assert report.files_changed == 3
    assert mw.stats()["nodes"] >= 5
    assert mw.stats()["edges"] >= 4
    # Edges carry provenance down to file/line/section/version
    sources = mw.relationship_source("Good tooling", "increases", "quality")
    assert sources, "expected relationship from B.md"
    prov = sources[0]["provenance"][0]
    assert prov["file"] == "B.md"
    assert prov["line"] == 3
    assert prov["section"] == "Quality"
    assert prov["version"]
    print("✓ ingest builds graph with file/line/section/version provenance")


def test_edit_file_incremental_add_and_remove():
    tmp, mw = _workspace()
    mw.ingest()
    edges_before = mw.stats()["edges"]

    # Edit B.md: remove one claim, add another
    _write(tmp, "B.md",
           "# Quality\n\n- Good tooling improves quality.\n"
           "- Good tooling decreases testing time.\n")
    report = mw.sync()
    assert report.files_changed == 1  # only B.md touched

    kinds = {e.kind for e in report.events}
    assert "claim_added" in kinds
    assert "claim_removed" in kinds

    # New relationship exists, detached one is gone
    assert mw.relationship_source("Good tooling", "decreases", "testing time")
    assert not mw.relationship_source("Testing", "requires", "time")

    # Shared concepts survive: quality still connected to Good tooling
    assert mw.relationship_source("Good tooling", "increases", "quality")
    assert mw.stats()["edges"] == edges_before
    print("✓ edit detected added + removed claims; shared edges kept")


def test_unchanged_files_are_skipped():
    tmp, mw = _workspace()
    mw.ingest()
    report = mw.sync()
    assert report.files_changed == 0
    assert report.events == []
    print("✓ second sync skips unchanged files (0 events)")


def test_shared_claim_across_files_survives_partial_removal():
    tmp = Path(tempfile.mkdtemp())
    _write(tmp, "A.md", "Good tooling improves quality.\n")
    _write(tmp, "B.md", "Good tooling improves quality.\n")
    mw = MarkdownWorkspace(tmp)
    mw.ingest()
    edges = mw.stats()["edges"]

    # Delete A.md: B.md still grounds the same edge
    (tmp / "A.md").unlink()
    report = mw.sync()
    assert mw.stats()["edges"] == edges
    assert mw.relationship_source("Good tooling", "increases", "quality")
    # Provenance still carries B.md
    prov = mw.relationship_source("Good tooling", "increases", "quality")[0]["provenance"]
    assert any(p["file"] == "B.md" for p in prov)
    print("✓ shared claim survives file deletion; provenance retained")


def test_removed_claims_detach_nodes_when_private():
    tmp = Path(tempfile.mkdtemp())
    _write(tmp, "Only.md",
           "# Isolated\n\nSpeed and quality are in tension.\n")
    mw = MarkdownWorkspace(tmp)
    mw.ingest()
    nodes_before = mw.stats()["nodes"]
    assert mw.explain_node("Speed")["found"]

    _write(tmp, "Only.md", "# Isolated\n\n(nothing left)\n")
    mw.sync()
    assert not mw.explain_node("Speed")["found"]
    assert mw.stats()["nodes"] < nodes_before
    print("✓ claim removal detaches private nodes when nothing else references them")


def test_explain_node_reports_provenance_and_edges():
    tmp, mw = _workspace()
    mw.ingest()
    info = mw.explain_node("quality")
    assert info["found"]
    assert info["provenance"], "quality should have provenance"
    assert info["edges"], "quality should have connected edges"
    files = {p["file"] for p in info["provenance"]}
    assert "A.md" in files and "B.md" in files and "C.md" in files
    print("✓ explain_node answers why + where for a concept")


def run_all_tests():
    print("=" * 60)
    print("Markdown Workspace — Ingest / Sync / Provenance Test")
    print("=" * 60)

    tests = [
        test_ingest_builds_graph_with_provenance,
        test_edit_file_incremental_add_and_remove,
        test_unchanged_files_are_skipped,
        test_shared_claim_across_files_survives_partial_removal,
        test_removed_claims_detach_nodes_when_private,
        test_explain_node_reports_provenance_and_edges,
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
    sys.exit(0 if run_all_tests() else 1)
