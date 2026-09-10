"""Markdown Workspace demo — the milestone loop from the product brief.

Run: python3 demo_markdown.py

Copies the example workspace to a temp folder, ingests it into a semantic
graph, edits B.md, syncs incrementally, then answers:
  - What changed?
  - Why did it change?
  - Where did this relationship come from?
"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from speculoop.markdown_workspace import MarkdownWorkspace


def main():
    print("=" * 64)
    print("Markdown Workspace — Markdown → graph → edit → incremental update")
    print("=" * 64)

    src = Path(__file__).parent / "examples" / "markdown-workspace"
    ws = Path(tempfile.mkdtemp()) / "workspace"
    shutil.copytree(src, ws)

    mw = MarkdownWorkspace(ws)
    print(f"\nWorkspace: {ws}")
    print("Files: A.md (Speed), B.md (Quality), C.md (Testing)\n")

    print("▸ Step 1: Ingest Markdown → semantic graph")
    report = mw.ingest()
    print(report.render())
    print(mw.stats())

    print("\n▸ Step 2: Where does 'Good tooling → quality' come from?")
    for src_info in mw.relationship_source("Good tooling", "increases", "quality"):
        for prov in src_info["provenance"]:
            print(f"  {prov['file']}:{prov['line']} "
                  f"section='{prov['section']}' version={prov['version']}")

    print("\n▸ Step 3: Edit B.md — replace a claim, add a new one")
    b = ws / "B.md"
    b.write_text(
        "# Quality\n\n"
        "- Good tooling improves quality.\n"
        "- Good tooling decreases testing time.\n",
        encoding="utf-8",
    )
    print("  wrote B.md:")
    print("  " + "\n  ".join(b.read_text().splitlines()))

    print("\n▸ Step 4: Incremental sync — what changed and why?")
    report2 = mw.sync()
    print(report2.render())
    print(mw.stats())

    print("\n▸ Step 5: Why does 'quality' exist in the graph?")
    info = mw.explain_node("quality")
    print(f"  id={info['id']}")
    for prov in info["provenance"]:
        print(f"  from {prov['file']}:{prov['line']} "
              f"section='{prov['section']}' version={prov['version']}")
    rels = sorted({f"{e['relation']} → {e['other']}" for e in info["edges"]})
    for r in rels:
        print(f"  edge: {r}")

    print("\n" + "=" * 64)
    print("Complete: edit a .md file and the semantic model changes as a "
          "consequence,")
    print("with provenance back to file / section / line / version.")
    print("=" * 64)


if __name__ == "__main__":
    main()
