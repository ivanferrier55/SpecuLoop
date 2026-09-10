"""Local HTTP server for the Markdown workspace UI.

Run via:  python3 -m speculoop serve --workspace ./knowledge-folder
Then open: http://localhost:8080

The server wraps MarkdownWorkspace and exposes a REST API consumed by
``static/index.html``.  No dependencies beyond the Python stdlib.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from .markdown_workspace import MarkdownWorkspace

_STATIC = Path(__file__).parent / "static"
_workspace: MarkdownWorkspace | None = None


class SpecuLoopHandler(BaseHTTPRequestHandler):

    def _json(self, code: int, data: dict | list | None = None,
              headers: dict | None = None) -> None:
        body = json.dumps(data).encode() if data is not None else b""
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    # --- routes --------------------------------------------------------

    def do_GET(self) -> None:
        path = urlparse(self.path)
        route = path.path.rstrip("/") or "/"
        qs = parse_qs(path.query)

        if route == "/":
            self._serve_static("index.html", "text/html")
        elif route == "/api/files":
            self._handle_files()
        elif route == "/api/file":
            self._handle_get_file(qs)
        elif route == "/api/graph":
            self._handle_graph()
        elif route == "/api/explain":
            self._handle_explain(qs)
        elif route == "/api/source":
            self._handle_source(qs)
        elif route == "/api/stats":
            self._handle_stats()
        elif route == "/api/workspace":
            self._handle_workspace()
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_PUT(self) -> None:
        path = urlparse(self.path)
        if path.path.rstrip("/") == "/api/file":
            self._handle_put_file(parse_qs(path.query))
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # --- static files --------------------------------------------------

    def _serve_static(self, name: str, content_type: str) -> None:
        target = _STATIC / name
        if not target.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # --- handlers ------------------------------------------------------

    def _handle_files(self) -> None:
        files = []
        for rel, version in _workspace._scan().items():
            prev = _workspace.state.get("files", {}).get(rel, {})
            files.append({
                "name": rel,
                "version": version,
                "unchanged": prev.get("version") == version,
            })
        self._json(200, files)

    def _handle_get_file(self, qs: dict) -> None:
        name = qs.get("name", [None])[0]
        if not name:
            self._json(400, {"error": "missing ?name="})
            return
        path = _workspace.dir / name
        if not path.exists():
            self._json(404, {"error": f"{name} not found"})
            return
        self._json(200, {
            "name": name,
            "content": path.read_text(encoding="utf-8"),
            "version": _workspace._scan().get(name, ""),
        })

    def _handle_put_file(self, qs: dict) -> None:
        name = qs.get("name", [None])[0]
        if not name:
            self._json(400, {"error": "missing ?name="})
            return
        body = json.loads(self._read_body())
        content = body.get("content", "")
        path = _workspace.dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        report = _workspace.sync()
        self._json(200, {
            "report": {
                "events": [
                    {
                        "kind": ev.kind,
                        "file": ev.file,
                        "line": ev.line,
                        "sentence": ev.sentence,
                        "triple": ev.triple,
                        "reason": ev.reason,
                        "edges_affected": ev.edges_affected,
                        "nodes_affected": ev.nodes_affected,
                    }
                    for ev in report.events
                ],
                "unresolved": report.unresolved,
                "files_scanned": report.files_scanned,
                "files_changed": report.files_changed,
            },
            "graph": _workspace.graph.stats(),
        })

    def _handle_graph(self) -> None:
        nodes = []
        for nid, node in _workspace.graph.nodes.items():
            nodes.append({
                "id": nid,
                "label": node.label,
                "kind": node.kind,
                "usage": node.usage_count,
                "provenance": node.metadata.get("provenance", []),
                "claims": node.metadata.get("claims", []),
            })
        edges = []
        for eid, edge in _workspace.graph.edges.items():
            src = _workspace.graph.get_node(edge.source)
            tgt = _workspace.graph.get_node(edge.target)
            edges.append({
                "id": eid,
                "source": edge.source,
                "target": edge.target,
                "relation": edge.relation,
                "weight": edge.weight,
                "source_label": src.label if src else "?",
                "target_label": tgt.label if tgt else "?",
                "provenance": edge.metadata.get("provenance", []),
                "claims": edge.metadata.get("claims", []),
            })
        self._json(200, {"nodes": nodes, "edges": edges})

    def _handle_explain(self, qs: dict) -> None:
        label = qs.get("label", [None])[0]
        if not label:
            self._json(400, {"error": "missing ?label="})
            return
        self._json(200, _workspace.explain_node(label))

    def _handle_source(self, qs: dict) -> None:
        subject = qs.get("subject", [None])[0]
        relation = qs.get("relation", [None])[0]
        target = qs.get("object", [None])[0]
        if not all([subject, relation, target]):
            self._json(400,
                       {"error": "missing ?subject=&relation=&object="})
            return
        self._json(200,
                   _workspace.relationship_source(subject, relation, target))

    def _handle_stats(self) -> None:
        self._json(200, _workspace.stats())

    def _handle_workspace(self) -> None:
        self._json(200, {
            "dir": str(_workspace.dir),
            "graph": str(_workspace.graph_path),
            "files": len(list(_workspace._markdown_files())),
            "graph_stats": _workspace.stats(),
        })

    def log_message(self, fmt, *args) -> None:
        pass  # suppress noisy request logs; errors still print


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SpecuLoop Markdown workspace server")
    parser.add_argument("--workspace", required=True,
                        help="path to the Markdown knowledge folder")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    global _workspace
    ws = Path(args.workspace).resolve()
    if not ws.is_dir():
        print(f"error: {ws} is not a directory", file=sys.stderr)
        return 1

    _workspace = MarkdownWorkspace(ws)
    report = _workspace.ingest()
    print(f"workspace: {ws}")
    print(f"files: {report.files_scanned}, "
          f"nodes: {_workspace.stats()['nodes']}, "
          f"edges: {_workspace.stats()['edges']}")
    print(f"  {report.render()}\n")

    server = HTTPServer((args.host, args.port), SpecuLoopHandler)
    print(f"serving at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
