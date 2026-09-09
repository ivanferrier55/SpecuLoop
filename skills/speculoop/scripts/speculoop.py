#!/usr/bin/env python3
"""SpecuLoop Agent CLI — persistent grounded semantic memory for agents.

Wraps the SpecuLoop library (mumblewrap / DRAG / speculoop layers) so an
agent can record facts, ground them against evidence, query them back, and
propagate corrections — across sessions.

The decomposer in the library is pattern-based and weak. This CLI's primary
path is `know`, which accepts an already-decomposed subject-relation-object
triple. The agent does the semantic decomposition; the graph stores it.

Usage:
  speculoop.py install --root <speculoop-repo>   # one-time setup
  speculoop.py know SUBJECT RELATION OBJECT [--status S] [--source SRC] [--note TEXT]
  speculoop.py ingest "a natural sentence"
  speculoop.py query "a question" [--lens NAME]
  speculoop.py emit [--node ID ...]
  speculoop.py graph
  speculoop.py stats
  speculoop.py learn "text" [--lens NAME] [--task TASK]
  speculoop.py propose "concept"
  speculoop.py confirm PROPOSAL_ID
  speculoop.py status --label LABEL --state observed|hypothesis|superseded [--source SRC]
  speculoop.py lens add NAME --description D --weights '{"increases": 2.0}'
  speculoop.py lens list
  speculoop.py edit --original TEXT --edited TEXT  (or --from-file F --to-file G)
  speculoop.py reset
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_DIR / "state" / "config.json"
DEFAULT_GRAPH = SKILL_DIR / "state" / "graph.json"

# Fallback roots to locate the SpecuLoop library, in priority order.
DEFAULT_ROOTS = [
    Path(os.environ.get("SPECULOOP_ROOT", "")),
    CONFIG_PATH.parent.parent.parent,  # repo/skills/speculoop -> repo
    Path(__file__).resolve().parent.parent.parent.parent,  # repo/skills/speculoop/scripts -> repo
    Path.cwd(),
]

RELATIONS = {
    "increases": "A raises B",
    "decreases": "A lowers B",
    "causes": "A makes B happen",
    "requires": "A needs B (backward)",
    "supports": "A backs B (bidirectional)",
    "opposes": "A conflicts with B (bidirectional)",
    "motivates": "A drives B",
    "solves": "A fixes B",
    "clarifies": "A explains B",
    "demonstrates": "A shows B",
    "contains": "A includes B",
    "part_of": "A belongs to B",
}


def _load_config() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def _save_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))


def _find_root() -> Path | None:
    """Locate the directory containing the mumblewrap package."""
    cfg = _load_config()
    if cfg.get("root"):
        p = Path(cfg["root"])
        if (p / "mumblewrap").is_dir():
            return p
    for root in DEFAULT_ROOTS:
        if root and (root / "mumblewrap").is_dir():
            return root
    return None


def _graph_path(args_root: str | None = None) -> Path:
    env = os.environ.get("SPECULOOP_GRAPH", "")
    if env:
        return Path(env)
    if args_root:
        return Path(args_root)
    cfg = _load_config()
    if cfg.get("graph"):
        return Path(cfg["graph"])
    return DEFAULT_GRAPH


def _loop(root: Path, graph_path: Path):
    sys.path.insert(0, str(root))
    from mumblewrap.api import SpecuLoop
    return SpecuLoop(graph_path)


def _get_lens(loop, name: str):
    if not name:
        return None
    for lens in loop.graph.lenses.values():
        if lens.name == name:
            return lens
    sys.exit(f"error: lens '{name}' not found. Use: lens list")


def _normalize_label(text: str) -> str:
    """Canonical node label: trimmed, single-spaced noun phrase."""
    return " ".join(text.strip().strip(".").split())


def _find_or_create_node(graph, label: str, kind: str, metadata: dict):
    node = graph.find_node_by_label(label)
    if node:
        for k, v in metadata.items():
            if k == "source" and v:
                node.metadata.setdefault("sources", []).append(v)
            else:
                node.metadata[k] = v
        node.update_usage()
        return node, False
    from mumblewrap.core.node import Node
    node = Node(kind=kind, label=label, content=label, metadata=metadata)
    graph.add_node(node)
    return node, True


def cmd_install(args) -> int:
    """Record the SpecuLoop repo root and verify the library imports."""
    root = Path(args.root).resolve()
    if not (root / "mumblewrap").is_dir():
        print(f"error: {root} does not contain the mumblewrap package", file=sys.stderr)
        return 1
    cfg = _load_config()
    cfg["root"] = str(root)
    if args.graph:
        cfg["graph"] = str(Path(args.graph).resolve())
    _save_config(cfg)
    try:
        loop = _loop(root, _graph_path())
        loop.stats()
    except Exception as e:  # noqa: BLE001
        print(f"error: library import failed: {e}", file=sys.stderr)
        return 1
    print(f"installed: root={root}")
    print(f"graph={_graph_path()}")
    print("speculoop.py is ready. Start with: know SUBJECT RELATION OBJECT")
    return 0


def cmd_know(args) -> int:
    """Primary path: ingest an agent-decomposed SVO triple directly."""
    root = _find_root()
    if not root:
        print("error: SpecuLoop library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    graph = loop.graph

    subject = _normalize_label(args.subject)
    obj = _normalize_label(args.object)
    relation = args.relation.lower().strip()
    if not subject or not obj:
        print("error: subject and object must be non-empty", file=sys.stderr)
        return 1
    if relation and relation not in RELATIONS:
        print(f"warning: relation '{relation}' is not in the known vocabulary "
              f"({', '.join(sorted(RELATIONS))}); force defaults to 0", file=sys.stderr)

    status = getattr(args, "status", None) or "observed"
    source = getattr(args, "source", None)
    note = getattr(args, "note", None)

    base_meta: dict = {"status": status}
    if source:
        base_meta["sources"] = [source]
    if note:
        base_meta["note"] = note

    subj_meta = {"status": status}
    subj_node, subj_created = _find_or_create_node(graph, subject, "concept", subj_meta)
    obj_meta = {"status": status}
    obj_node, obj_created = _find_or_create_node(graph, obj, "concept", obj_meta)

    from mumblewrap.core.edge import Edge
    existing = graph.find_edges_between(subj_node.id, obj_node.id)
    for edge in existing:
        if edge.relation == relation:
            edge.weight = min(edge.weight + 0.1, 5.0)
            edge.metadata.setdefault("sources", []).append(source) if source else None
            graph.save(_graph_path(args.graph))
            print(f"strengthened: {subject} --[{relation}]--> {obj} "
                  f"(weight={edge.weight:.2f}, status={status})")
            return 0
    edge = Edge(source=subj_node.id, target=obj_node.id, relation=relation,
                weight=1.0, metadata={"status": status})
    if source:
        edge.metadata["sources"] = [source]
    graph.add_edge(edge)
    loop.store.save(graph)
    flags = []
    if subj_created:
        flags.append("new subject")
    if obj_created:
        flags.append("new object")
    print(f"stored: {subject} --[{relation}]--> {obj} [{', '.join(flags) or 'reused'}] status={status}")
    return 0


def cmd_ingest(args) -> int:
    """Pattern-based text ingest; reports gaps for the agent to re-decompose."""
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    result = loop.ingest(args.text)
    print(f"details: {result.details}")
    if result.gaps:
        print("gaps (could not decompose). Re-decompose as triples with `know`:")
        for gap in result.gaps:
            print(f"  - {gap}")
    loop.store.save(loop.graph)
    return 0


def cmd_query(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    lens = _get_lens(loop, args.lens) if args.lens else None
    result = loop.query(args.text, lens=lens, max_nodes=args.max)
    print(result.markdown)
    if not result.markdown.strip():
        print("(no results)")
    return 0


def cmd_emit(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    lens = _get_lens(loop, args.lens) if args.lens else None
    if args.node:
        result = loop.emit(node_ids=args.node, lens=lens)
    else:
        result = loop.emit_full(lens=lens)
    print(result.markdown)
    return 0


def cmd_graph(args) -> int:
    """Dump all triples as readable rows with status."""
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    graph = loop.graph
    rows = []
    for edge in graph.edges.values():
        src = graph.get_node(edge.source)
        tgt = graph.get_node(edge.target)
        if not src or not tgt:
            continue
        status = edge.metadata.get("status", "?")
        rows.append(f"{src.label} --[{edge.relation}/{edge.weight:.2f}]--> {tgt.label}  [{status}]")
    if args.status:
        rows = [r for r in rows if f"[{args.status}]" in r]
    if args.relation:
        rows = [r for r in rows if f"--[{args.relation}/" in r]
    for r in sorted(rows):
        print(r)
    if not rows:
        print("(empty)")
    print(f"\n{graph.stats()}")
    return 0


def cmd_stats(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    print(json.dumps(loop.stats(), indent=2))
    return 0


def cmd_learn(args) -> int:
    """Run the grounding loop: score text against the current basis."""
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    solve = loop.learn(args.text, lens=args.lens, task=args.task, decoder_name="cli-lexical")
    c = solve.compression
    print(f"coverage:      {c.coverage:.3f}")
    print(f"uncertainty:   {c.uncertainty:.3f}")
    print(f"reconstruction_error: {c.reconstruction_error:.3f}")
    if c.unresolved_tokens:
        print(f"unresolved:    {', '.join(c.unresolved_tokens)}")
    if c.candidate:
        print(f"candidate:     '{c.candidate.label}' (provisional — accept via api.accept_candidate)")
    print(f"evidence_id:   {c.evidence_id}")
    loop.store.save(loop.graph)
    return 0


def cmd_propose(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    proposal = loop.propose(args.text)
    print(f"proposal_id:  {proposal.id}")
    print(f"kind:         {proposal.kind}")
    print(f"reason:       {proposal.reason}")
    if proposal.proposed_node:
        print(f"node:         '{proposal.proposed_node.label}'")
    print("confirm with: confirm PROPOSAL_ID")
    return 0


def cmd_confirm(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    proposal = None
    for p in getattr(loop.extender, "proposals", []) or []:
        if p.id == args.proposal_id:
            proposal = p
            break
    if proposal is None:
        print("error: proposal lookup is process-local; re-propose in this session", file=sys.stderr)
        return 1
    ok = loop.confirm_proposal(proposal)
    print("confirmed" if ok else "not confirmed")
    return 0


def cmd_status(args) -> int:
    """Grounding operation: mark a node as observed / hypothesis / superseded."""
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    graph = loop.graph
    node = None
    if args.label:
        node = graph.find_node_by_label(_normalize_label(args.label))
        if node is None:
            node = graph.find_nodes(args.label)[0] if graph.find_nodes(args.label) else None
    elif args.id:
        node = graph.get_node(args.id)
    if node is None:
        print(f"error: node not found (label={args.label!r}, id={args.id!r})", file=sys.stderr)
        return 1
    node.metadata["status"] = args.state
    if args.source:
        node.metadata.setdefault("sources", []).append(args.source)
    graph.save(_graph_path(args.graph))
    print(f"{node.label} → status={args.state}" + (f" source={args.source}" if args.source else ""))
    return 0


def cmd_lens_add(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    from mumblewrap.core.lens import Lens
    weights = json.loads(args.weights or "{}")
    lens = Lens(name=args.name, description=args.description, relation_weights=weights)
    loop.add_lens(lens)
    print(f"lens added: {args.name} (id={lens.id})")
    print("use with: query TEXT --lens NAME")
    return 0


def cmd_lens_list(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    for lens in loop.graph.lenses.values():
        print(f"{lens.name} (id={lens.id}) — {lens.description}")
    if not loop.graph.lenses:
        print("(no lenses)")
    return 0


def cmd_edit(args) -> int:
    root = _find_root()
    if not root:
        print("error: library not found. Run: speculoop.py install --root <repo>", file=sys.stderr)
        return 1
    if args.from_file or args.to_file:
        original = Path(args.from_file).read_text() if args.from_file else args.original
        edited = Path(args.to_file).read_text() if args.to_file else args.edited
    else:
        original, edited = args.original, args.edited
    if not original or not edited:
        print("error: provide --original/--edited or --from-file/--to-file", file=sys.stderr)
        return 1
    loop = _loop(root, _graph_path(args.graph))
    result = loop.edit(original, edited)
    print(f"details: {result.details}")
    print(f"affected nodes: {len(result.affected_node_ids)}")
    print(f"new nodes: {[n.label for n in result.new_nodes]}")
    print(f"new edges: {len(result.new_edges)}")
    return 0


def cmd_reset(args) -> int:
    graph_path = _graph_path(args.graph)
    if graph_path.exists():
        graph_path.unlink()
        print(f"removed: {graph_path}")
    else:
        print("nothing to reset")
    return 0


def cmd_relations(args) -> int:
    print("Relation vocabulary (edge --relation values):")
    for rel, meaning in sorted(RELATIONS.items()):
        print(f"  {rel:16s} {meaning}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="speculoop.py", description=__doc__)
    parser.add_argument("--graph", help="override graph path for this command")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("install", help="one-time setup: record library root")
    p.add_argument("--root", required=True, help="path to the SpecuLoop repo")
    p.add_argument("--graph", help="graph file path (default: skill state)")
    p.set_defaults(func=cmd_install)

    p = sub.add_parser("know", help="record an SVO triple directly (primary path)")
    p.add_argument("subject")
    p.add_argument("relation")
    p.add_argument("object")
    p.add_argument("--status", choices=["observed", "hypothesis", "superseded"], default="observed")
    p.add_argument("--source", help="provenance: observation, file, experiment, ...")
    p.add_argument("--note", help="short annotation")
    p.set_defaults(func=cmd_know)

    p = sub.add_parser("ingest", help="pattern-based natural-language ingest")
    p.add_argument("text")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("query", help="DRAG query returns a relevant subgraph")
    p.add_argument("text")
    p.add_argument("--lens")
    p.add_argument("--max", type=int, default=20)
    p.set_defaults(func=cmd_query)

    p = sub.add_parser("emit", help="print the graph (or selected nodes) as text")
    p.add_argument("--node", action="append", default=[])
    p.add_argument("--lens")
    p.set_defaults(func=cmd_emit)

    p = sub.add_parser("graph", help="list all triples with status")
    p.add_argument("--status")
    p.add_argument("--relation")
    p.set_defaults(func=cmd_graph)

    p = sub.add_parser("stats", help="graph statistics")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("learn", help="score text against the basis (grounding loop)")
    p.add_argument("text")
    p.add_argument("--lens")
    p.add_argument("--task")
    p.set_defaults(func=cmd_learn)

    p = sub.add_parser("propose", help="propose a primitive for an unknown concept")
    p.add_argument("text")
    p.set_defaults(func=cmd_propose)

    p = sub.add_parser("confirm", help="accept a proposal made this session")
    p.add_argument("proposal_id")
    p.set_defaults(func=cmd_confirm)

    p = sub.add_parser("status", help="mark a node observed/hypothesis/superseded")
    p.add_argument("--label")
    p.add_argument("--id")
    p.add_argument("--state", required=True, choices=["observed", "hypothesis", "superseded"])
    p.add_argument("--source")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("lens", help="lens management")
    lens_sub = p.add_subparsers(dest="lens_cmd", required=True)
    lp = lens_sub.add_parser("add")
    lp.add_argument("name")
    lp.add_argument("--description", default="")
    lp.add_argument("--weights", default="{}", help='JSON: {"increases": 2.0}')
    lp.set_defaults(func=cmd_lens_add)
    lp2 = lens_sub.add_parser("list")
    lp2.set_defaults(func=cmd_lens_list)

    p = sub.add_parser("edit", help="propagate a human edit back into the graph")
    p.add_argument("--original")
    p.add_argument("--edited")
    p.add_argument("--from-file")
    p.add_argument("--to-file")
    p.set_defaults(func=cmd_edit)

    p = sub.add_parser("reset", help="delete the graph (danger)")
    p.set_defaults(func=cmd_reset)

    p = sub.add_parser("relations", help="list the relation vocabulary")
    p.set_defaults(func=cmd_relations)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
