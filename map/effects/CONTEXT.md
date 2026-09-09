---
type: process
name: effects-index
---

# Effects Index — what moves if you change X

Each line names a mutation point. If you change an object's implementation, follow its downstream hits.

## graph (mumblewrap/core/graph.py)

- `graph → node (write)` — adding/removing nodes changes graph state
- `graph → edge (write)` — adding/removing edges changes graph state
- `graph → store (write)` — every mutation triggers save
- **Hits:** ingest, edit, accept_candidate, accept_refactor, store
- **Does not hit:** scorer, composer (read-only)

## node (mumblewrap/core/node.py)

- `node → graph (write)` — new nodes change graph shape
- `node → scorer (read)` — scorer scores nodes
- `node → translator (read)` — decomposer matches against nodes
- **Hits:** ingest, edit, accept_candidate, accept_refactor, decomposer, scorer
- **Does not hit:** store (stores graph, not nodes directly)

## edge (mumblewrap/core/edge.py)

- `edge → graph (write)` — new edges change graph shape
- `edge → scorer (read)` — scorer uses edge forces
- `edge → translator (read)` — composer follows edges for output
- **Hits:** ingest, edit, accept_refactor, scorer, composer
- **Does not hit:** store

## lens (mumblewrap/core/lens.py)

- `lens → drag-selector (read)` — lens reweights scoring
- `lens → semantic-learner (read)` — lens-aware compression
- **Hits:** add_lens, query, learn
- **Does not hit:** ingest, edit, store

## translator (mumblewrap/translation/translator.py)

- `translator → decomposer (delegate)` — ingest path
- `translator → composer (delegate)` — emit path
- **Hits:** ingest, emit, query, learn
- **Does not hit:** edit, propose, refactor

## decomposer (mumblewrap/translation/decomposer.py)

- `decomposer → graph (write)` — creates nodes/edges
- `decomposer → node (read)` — reuses existing nodes
- **Hits:** ingest, learn
- **Does not hit:** emit, query (read path), edit

## composer (mumblewrap/translation/composer.py)

- `composer → node (read)` — generates text from nodes
- `composer → edge (read)` — follows edges for output
- `composer → lens (read)` — respects lens weights
- **Hits:** emit, query
- **Does not hit:** ingest, edit, propose

## scorer (drag/scorer.py)

- `scorer → node (read)` — scores nodes
- `scorer → edge (read)` — uses edge forces
- `scorer → lens (read)` — respects lens reweighting
- **Hits:** query (DRAGSelector uses scorer)
- **Does not hit:** ingest, emit, edit

## drag-selector (drag/selector.py)

- `drag-selector → scorer (read)` — scores all nodes
- `drag-selector → graph (read)` — traverses graph
- **Hits:** query
- **Does not hit:** ingest, emit, edit, learn

## self-extender (speculoop/self_extender.py)

- `self-extender → node (write)` — creates candidate
- **Hits:** propose, confirm_proposal
- **Does not hit:** ingest, emit, query, edit

## propagator (speculoop/propagator.py)

- `propagator → graph (write)` — adds nodes/edges from diff
- **Hits:** edit
- **Does not hit:** ingest, emit, query, learn

## store (mumblewrap/persistence/store.py)

- `store → graph (read/write)` — serializes entire graph
- **Hits:** all mutation paths (ingest, edit, accept_candidate, accept_refactor, learn, propose)
- **Does not hit:** read-only paths (emit, query, decompose)
