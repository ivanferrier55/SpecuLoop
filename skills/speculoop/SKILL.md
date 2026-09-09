---
name: speculoop
description: "Use SpecuLoop as persistent, grounded semantic memory for an agent. Use when you need to (1) remember facts, decisions, or observations across sessions instead of relying on conversation memory, (2) record knowledge as subject-relation-object triples with provenance and evidence status, (3) distinguish observed facts from hypotheses and track which claims are grounded, (4) query a growing knowledge graph for relevant information and see the provenance trail, (5) detect contradictions or semantic drift in stored knowledge, or (6) actually run the SpecuLoop grounding loop (learn, status, refactor). Triggers: remember this for next time, store that as a fact/hypothesis, persistent memory, knowledge graph, semantic memory, grounding claims, SpecuLoop"
---

# SpecuLoop Agent Memory

Use the SpecuLoop semantic graph as grounded, persistent memory. The agent is the decomposer: break observations into subject-relation-object triples, store them with provenance and evidence status, query them back, and update status as claims get grounded.

## Setup (one time)

```bash
scripts/speculoop.py install --root <path-to-speculoop-repo>
```

Verify: `scripts/speculoop.py stats`. Graph persists in `state/graph.json` by default. Per-project memory: set the `SPECULOOP_GRAPH` env var before running commands.

## Core workflow

1. **Decompose** each observation into SVO triples yourself. Never paste prose into `ingest` — the library decomposer is pattern-based and will drop it.
2. **Store** with `know SUBJECT RELATION OBJECT --status observed|hypothesis --source SRC`.
   - `observed` = grounded claim (you verified it, or it came from evidence).
   - `hypothesis` = proposed/uncertain claim awaiting grounding.
3. **Query** with `query "question"` when reasoning; read the returned subgraph, not the whole graph.
4. **Ground** with `status --label X --state observed --source SRC` when a hypothesis gets verified, or `--state superseded` when it is refuted. Do not delete refuted claims — mark them.
5. **Review** with `graph` to see every triple and its status; `stats` for scale.

## Commands

| Command | Purpose |
|---|---|
| `know "Subject" relation "Object" [--status observed\|hypothesis\|superseded] [--source SRC] [--note TEXT]` | Store an agent-decomposed triple. Primary path. |
| `query "question" [--lens NAME] [--max N]` | DRAG: retrieve relevant subgraph, emit markdown with provenance. |
| `graph [--status S] [--relation R]` | List all triples with weight and status. |
| `stats` | Node/edge/lens counts. |
| `learn "text" [--lens NAME] [--task TASK]` | Score text against the basis: coverage, uncertainty, candidate primitive. |
| `status --label X --state observed\|hypothesis\|superseded [--source SRC]` | Change a node's grounding status. |
| `ingest "simple sentence"` | Pattern-based ingest. Reports gaps; re-decompose gaps with `know`. |
| `emit [--node ID ...] [--lens NAME]` | Print graph (or nodes) as markdown. Useful as an edit surface. |
| `propose "concept"` / `confirm PROPOSAL_ID` | Propose/accept a new primitive. Proposals are process-local. |
| `lens add NAME --description D --weights '{"increases": 2.0}'` / `lens list` | Create/view lenses for viewpoint-specific queries. |
| `edit --from-file F --to-file G` | Propagate a human edit via the library propagator. Often weak; prefer `know` for corrections. |
| `relations` | Show the edge relation vocabulary. |
| `reset` | Delete the graph (dangerous). |

## Rules

- **Labels are noun phrases**: short, stable, singular. `"Good tooling"`, `"inertia"`, not sentences.
- **Relations come from the vocabulary**: `increases`, `decreases`, `supports`, `opposes`, `requires`, `causes`, `motivates`, `solves`, `clarifies`, `demonstrates`, `contains`, `part_of`.
- **Store distilled facts, not artifacts.** Never store file contents, chat transcripts, or code — store the semantic conclusion with `--source` pointing at the artifact.
- **Status must reflect reality**: `observed` only when grounded; `hypothesis` otherwise; `superseded` for refuted claims (keep the node).
- **Reuse concepts**: repeat a `know` with the same subject/object/relation to strengthen the edge (weight increases), not duplicate it.
- **Set `SPECULOOP_GRAPH` for workspace-scoped memory** so different projects do not pollute each other.
- **Re-run `learn` after ingesting** to detect unresolved tokens — high uncertainty means the basis cannot explain the claim yet.

## Limitations

- `edit` propagation is heuristic and often records 0 changes. Correct knowledge explicitly with `know` + `status` instead.
- `propose`/`confirm` do not persist proposals across processes; re-propose in the same session.
- The `ingest` decomposer matches only simple subject-verb-object patterns. Always prefer `know`.
