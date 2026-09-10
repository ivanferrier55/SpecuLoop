"""Markdown-native workspace: files as source of truth, graph as derived state.

Implements the smallest complete loop from the product brief:

    Markdown
      ↓ parse
    semantic extraction   (existing Decomposer, SVO patterns)
      ↓
    graph                 (existing mumbleWRAP Graph, persisted as JSON)
      ↓
    provenance            (file / section / line / version on nodes + edges)
      ↓
    change Markdown
      ↓
    incremental sync      (hash-based; only changed files re-processed)
      ↓
    report                (what changed, why, and where each claim came from)

The Markdown files are authoritative. The graph and workspace state live in a
derived ``.speculoop/`` folder inside the workspace, so the source tree stays
git-friendly and human-readable.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from mumblewrap.core.graph import Graph
from mumblewrap.core.node import Node
from mumblewrap.core.edge import Edge
from mumblewrap.translation.decomposer import Decomposer

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
_HEADING_RE = re.compile(r"^#{1,6}\s+(.*)")
_LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*)")
_BLOCKQUOTE_RE = re.compile(r"^\s*>\s?(.*)")
_EMPTY_ALT_RE = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
_URL_RE = re.compile(r"^\s*(?:https?://|www\.)\S+\s*$")


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _claim_id(sentence: str) -> str:
    return hashlib.sha1(_normalized(sentence).encode()).hexdigest()[:16]


def _file_version(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


@dataclass
class SourceRef:
    """Where a claim came from, down to file / section / line / version."""
    file: str
    line: int
    section: str
    version: str

    def to_dict(self) -> dict:
        return {"file": self.file, "line": self.line,
                "section": self.section, "version": self.version}

    @classmethod
    def from_dict(cls, d: dict) -> "SourceRef":
        return cls(file=d.get("file", ""), line=d.get("line", 0),
                   section=d.get("section", ""), version=d.get("version", ""))


@dataclass
class Claim:
    """A candidate semantic statement extracted from a Markdown line."""
    id: str
    sentence: str
    source: SourceRef

    def to_dict(self) -> dict:
        return {"id": self.id, "sentence": self.sentence,
                "source": self.source.to_dict()}

    @classmethod
    def from_dict(cls, d: dict) -> "Claim":
        return cls(id=d["id"], sentence=d["sentence"],
                   source=SourceRef.from_dict(d.get("source", {})))


@dataclass
class SyncEvent:
    """One observable change produced by a sync run, with a human reason."""
    kind: str              # claim_added | claim_removed | file_added | file_deleted
    file: str
    line: int | None = None
    sentence: str = ""
    triple: str = ""       # "Subject --[relation]--> Object"
    edges_affected: list[str] = field(default_factory=list)
    nodes_affected: list[str] = field(default_factory=list)
    reason: str = ""

    def render(self) -> str:
        loc = f"{self.file}:{self.line}" if self.line is not None else self.file
        if self.kind == "claim_added":
            return f"ADDED      {loc}  {self.sentence or self.triple!r}\n           → {self.reason}"
        if self.kind == "claim_removed":
            return f"REMOVED    {loc}  {self.sentence or self.triple!r}\n           → {self.reason}"
        if self.kind == "file_added":
            return f"FILE ADDED {loc}\n           → {self.reason}"
        if self.kind == "file_deleted":
            return f"FILE DELETED {loc}\n           → {self.reason}"
        return f"{self.kind:10s} {loc}  {self.reason}"


@dataclass
class SyncReport:
    """Output of a workspace ingest/sync: events + diagnostics."""
    events: list[SyncEvent] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    files_scanned: int = 0
    files_changed: int = 0
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None

    def render(self, with_unchanged: bool = False) -> str:
        lines = []
        for ev in self.events:
            if ev.kind == "claim_unchanged" and not with_unchanged:
                continue
            lines.append(ev.render())
        head = (f"scanned {self.files_scanned} file(s), "
                f"{self.files_changed} changed, "
                f"{len(self.events)} event(s)")
        if self.unresolved:
            head += f", {len(self.unresolved)} unresolved"
        body = "\n".join(lines) if lines else "(no changes)"
        return f"{head}\n{body}"


class MarkdownWorkspace:
    """A folder of Markdown files with a derived semantic graph.

    The workspace folder holds the source of truth (``*.md``). A hidden
    ``.speculoop/`` folder holds derived state: the graph JSON and a state
    file mapping files → versions → claims → graph objects, which makes
    subsequent syncs incremental.
    """

    def __init__(self, workspace_dir: str | Path,
                 graph_path: str | Path | None = None,
                 state_path: str | Path | None = None) -> None:
        self.dir = Path(workspace_dir)
        self.state_dir = self.dir / ".speculoop"
        self.graph_path = Path(graph_path) if graph_path else self.state_dir / "graph.json"
        self.state_path = Path(state_path) if state_path else self.state_dir / "state.json"
        self._decomposer = Decomposer()
        self.graph = self._load_graph()
        self.state: dict = self._load_state()

    # ---------- persistence ----------

    def _load_graph(self) -> Graph:
        if self.graph_path.exists():
            return Graph.load(self.graph_path)
        return Graph()

    def _load_state(self) -> dict:
        if self.state_path.exists():
            return json.loads(self.state_path.read_text())
        return {"files": {}}

    def _save_all(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.graph.save(self.graph_path)
        self.state_path.write_text(json.dumps(self.state, indent=2))

    # ---------- scanning + parsing ----------

    def _markdown_files(self) -> list[Path]:
        return sorted(p for p in self.dir.rglob("*.md")
                      if ".speculoop" not in p.parts)

    def _scan(self) -> dict[str, str]:
        """Relative path → content hash for every Markdown file."""
        versions: dict[str, str] = {}
        for path in self._markdown_files():
            rel = path.relative_to(self.dir).as_posix()
            versions[rel] = _file_version(path.read_text(encoding="utf-8"))
        return versions

    def _parse_file(self, path: Path, rel: str, version: str) -> list[Claim]:
        """Extract candidate claims from a file with line + section provenance."""
        claims: list[Claim] = []
        section = ""
        in_code = False
        for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.rstrip()
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            stripped = line.strip()
            if not stripped:
                continue
            m = _HEADING_RE.match(line)
            if m:
                section = m.group(1).strip()
                continue
            if _EMPTY_ALT_RE.match(stripped) or _URL_RE.match(stripped):
                continue
            m = _LIST_RE.match(line)
            if m:
                candidate = m.group(1)
            else:
                candidate = stripped.lstrip("> ").strip()
            for sentence in _SENTENCE_RE.split(candidate):
                sentence = sentence.strip()
                if len(sentence) < 5:
                    continue
                claims.append(Claim(
                    id=_claim_id(sentence),
                    sentence=sentence,
                    source=SourceRef(file=rel, line=lineno,
                                     section=section, version=version),
                ))
        return claims

    # ---------- ingest / sync ----------

    def ingest(self) -> SyncReport:
        """Full build: ingest every file. Equivalent to sync on an empty state."""
        return self.sync()

    def sync(self) -> SyncReport:
        """Incrementally reconcile the graph with the Markdown sources.

        Unchanged files (by content hash) are skipped. Changed files are
        re-parsed; added claims are extracted into the graph, removed claims
        are detached, and every change is reported with a reason.
        """
        report = SyncReport()
        versions = self._scan()
        report.files_scanned = len(versions)
        old_files = set(self.state.get("files", {}))
        new_files = set(versions)

        # Pre-parse changed files so claim removal can tell which claims stay
        # alive elsewhere in the workspace (shared nodes/edges must survive).
        parsed: dict[str, list[Claim]] = {}
        remaining_ids: set[str] = set()
        for rel, version in versions.items():
            prev = self.state["files"].get(rel)
            if prev and prev.get("version") == version:
                remaining_ids.update(prev.get("claims", {}))
            else:
                claims = self._parse_file(self.dir / rel, rel, version)
                parsed[rel] = claims
                remaining_ids.update(c.id for c in claims)
        remaining_ids = {cid for cid in remaining_ids if cid}  # drop empties

        for rel in sorted(new_files):
            version = versions[rel]
            prev = self.state["files"].get(rel)
            if prev and prev.get("version") == version:
                continue  # unchanged
            report.files_changed += 1
            claims = parsed[rel]
            old_claims = (prev or {}).get("claims", {})
            self._apply_file(rel, version, claims, old_claims, report,
                             remaining_ids, was_added=(rel not in old_files))

        for rel in sorted(old_files - new_files):
            report.files_changed += 1
            old_claims = self.state["files"].get(rel, {}).get("claims", {})
            self._remove_all_claims(rel, old_claims, report,
                                    remaining_ids, deleted_file=True)

        report.finished_at = time.time()
        self._save_all()
        return report

    def _apply_file(self, rel: str, version: str, claims: list[Claim],
                    old_claims: dict, report: SyncReport,
                    remaining_ids: set[str], *, was_added: bool) -> None:
        new_claims = {c.id: c for c in claims}
        old_ids = set(old_claims)
        new_ids = set(new_claims)
        storable: dict = {}

        if was_added and new_ids:
            added_count = len(new_ids - old_ids)
            report.events.append(SyncEvent(
                kind="file_added", file=rel,
                reason=f"new Markdown file; {added_count} claim(s) extracted",
            ))

        for cid in sorted(new_ids - old_ids):
            claim = new_claims[cid]
            ev = self._add_claim(claim, report)
            if ev is not None:
                storable[cid] = {
                    "sentence": claim.sentence,
                    "line": claim.source.line,
                    "edge_ids": ev.edges_affected,
                    "node_ids": ev.nodes_affected,
                }
                report.events.append(ev)

        for cid in sorted(old_ids - new_ids):
            stored = old_claims[cid]
            self._remove_claim(rel, cid, stored, report, remaining_ids)

        for cid in sorted(new_ids & old_ids):
            storable[cid] = old_claims[cid]
            storable[cid]["line"] = new_claims[cid].source.line

        self.state["files"][rel] = {"version": version, "claims": storable}

    def _add_claim(self, claim: Claim, report: SyncReport) -> SyncEvent | None:
        decomp = self._decomposer.decompose(claim.sentence, self.graph)
        if not (decomp.new_edges or decomp.reused_edges or decomp.new_nodes or decomp.reused_nodes):
            report.unresolved.append(
                f"{claim.source.file}:{claim.source.line} "
                f"'{claim.sentence}' (no SVO pattern matched)"
            )
            return None

        src = claim.source.to_dict()
        node_ids: list[str] = []
        edge_ids: list[str] = []

        for node in decomp.new_nodes:
            node.metadata.setdefault("provenance", []).append(src)
            node.metadata.setdefault("claims", []).append(claim.id)
            self.graph.add_node(node)
            node_ids.append(node.id)

        for node in decomp.reused_nodes:
            node.metadata.setdefault("provenance", []).append(src)
            node.metadata.setdefault("claims", []).append(claim.id)
            node_ids.append(node.id)

        for edge in decomp.new_edges:
            if edge.source in self.graph.nodes and edge.target in self.graph.nodes:
                edge.metadata.setdefault("provenance", []).append(src)
                edge.metadata.setdefault("claims", []).append(claim.id)
                self.graph.add_edge(edge)
                edge_ids.append(edge.id)

        for edge in decomp.reused_edges:
            existing = self.graph.edges.get(edge.id)
            if existing is None:
                continue
            existing.metadata.setdefault("provenance", []).append(src)
            if claim.id not in existing.metadata.setdefault("claims", []):
                existing.metadata["claims"].append(claim.id)
            edge_ids.append(existing.id)

        triple = decomp.details.split(": ", 1)[-1] if decomp.details else ""
        return SyncEvent(
            kind="claim_added",
            file=claim.source.file,
            line=claim.source.line,
            sentence=claim.sentence,
            triple=triple,
            edges_affected=edge_ids,
            nodes_affected=node_ids,
            reason=(f"extracted '{triple or claim.sentence}' from "
                    f"{claim.source.file}:{claim.source.line} "
                    f"(section '{claim.source.section or 'top-level'}', version {claim.source.version})"),
        )

    def _remove_all_claims(self, rel: str, old_claims: dict,
                           report: SyncReport, remaining_ids: set[str],
                           *, deleted_file: bool) -> None:
        for cid in sorted(old_claims):
            self._remove_claim(rel, cid, old_claims[cid], report, remaining_ids)
        self.state["files"].pop(rel, None)
        if deleted_file:
            report.events.append(SyncEvent(
                kind="file_deleted", file=rel,
                reason="Markdown file no longer present; all its claims detached",
            ))

    def _remove_claim(self, rel: str, cid: str, stored: dict,
                      report: SyncReport, remaining_ids: set[str]) -> None:
        edge_ids = stored.get("edge_ids", [])
        node_ids = stored.get("node_ids", [])
        removed_edge_ids: list[str] = []
        kept_nodes: list[str] = []
        removed_node_ids: list[str] = []

        for eid in edge_ids:
            edge = self.graph.get_edge(eid)
            if edge is None:
                continue
            if any(c in remaining_ids for c in edge.metadata.get("claims", [])):
                kept_nodes.append(edge.source)  # endpoints survive via this edge
                kept_nodes.append(edge.target)
                continue
            self.graph.remove_edge(eid)
            removed_edge_ids.append(eid)

        for nid in node_ids:
            node = self.graph.get_node(nid)
            if node is None:
                continue
            if nid in kept_nodes:
                continue
            if self.graph.get_edges(nid):
                kept_nodes.append(nid)
                continue
            if any(c in remaining_ids for c in node.metadata.get("claims", [])):
                kept_nodes.append(nid)
                continue
            self.graph.nodes.pop(nid, None)
            self.graph.adjacency.pop(nid, None)
            removed_node_ids.append(nid)

        report.events.append(SyncEvent(
            kind="claim_removed",
            file=rel,
            line=stored.get("line"),
            sentence=stored.get("sentence", ""),
            edges_affected=removed_edge_ids,
            nodes_affected=removed_node_ids + kept_nodes,
            reason=(f"source line no longer present; "
                    f"{len(removed_edge_ids)} edge(s) detached"
                    + (f"; node(s) removed: {', '.join(removed_node_ids)}"
                       if removed_node_ids else
                       "; shared nodes and edges kept")),
        ))

    @staticmethod
    def _has_other_claims(node: Node, removed_claim: str) -> bool:
        return any(c != removed_claim for c in node.metadata.get("claims", []))

    # ---------- inspection ----------

    def relationship_source(self, subject: str, relation: str,
                            target: str) -> list[dict]:
        """Where did this relationship come from? Returns provenance list."""
        src = self.graph.find_node_by_label(subject)
        tgt = self.graph.find_node_by_label(target)
        if not src or not tgt:
            return []
        results = []
        for edge in self.graph.find_edges_between(src.id, tgt.id):
            if edge.relation != relation:
                continue
            prov = edge.metadata.get("provenance", [])
            claims = edge.metadata.get("claims", [])
            results.append({
                "relation": relation,
                "weight": edge.weight,
                "claims": claims,
                "provenance": prov,
            })
        return results

    def explain_node(self, label: str) -> dict:
        """Why does this node exist? Provenance + connected edges."""
        node = self.graph.find_node_by_label(label)
        if node is None:
            return {"label": label, "found": False}
        return {
            "label": label,
            "id": node.id,
            "kind": node.kind,
            "found": True,
            "provenance": node.metadata.get("provenance", []),
            "claims": node.metadata.get("claims", []),
            "edges": [
                {
                    "id": e.id,
                    "relation": e.relation,
                    "weight": e.weight,
                    "other": (
                        self.graph.get_node(e.target).label
                        if e.target != node.id and self.graph.get_node(e.target)
                        else self.graph.get_node(e.source).label
                        if self.graph.get_node(e.source)
                        else None
                    ),
                    "provenance": e.metadata.get("provenance", []),
                }
                for e in self.graph.get_edges(node.id)
            ],
        }

    def stats(self) -> dict:
        return self.graph.stats()
