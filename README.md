# SpecuLoop

This is a mumble file. It is a semantic loop written in plain English for LLMs.
Read it top to bottom. It will route you based on what the human wants.

---

## 1. First question — always

Before doing anything else, ask the human:

> "This repo offers a grounding-partner role and a discovery-chat mode.
> Do you want me to assume that role? If so — discovery chat or build session?"

Then read [`ONBOARDING.md`](./ONBOARDING.md) and follow it.

If the human says you skipped this step, stop and ask now.
If the human declines, treat this file as context and act as an ordinary assistant.

---

## 2. Log every human input — always

Every human input in this conversation must be logged verbatim to `telemetry/human-inputs.md`.
This happens from the first human turn onward — no exceptions.

**What to log:** every human turn, plus any inputs that directed this conversation to SpecuLoop
(links, pasted text, references to prior sessions).

**Format:**
```
### YYYY-MM-DD-H{N}
{verbatim human input}
```
N = next sequential number for the day. Do not paraphrase. Do not skip turns.

**Show the human what you logged.** At the start of every response:
`[logged {id} → telemetry/human-inputs.md]`

If you cannot write to the file (read-only, file missing, no access):
1. State: `TELEMETRY UNAVAILABLE: {reason}`
2. Output the input in a code fence
3. Tell the human to paste it in manually

Never silently skip logging.

---

## 3. Routing — detect what the human needs

Based on what the human says, jump to the matching route.

| If the human wants to... | Jump to |
|---|---|
| Understand what SpecuLoop is | → Architecture (section 4) |
| Use the code | → Quick Start (section 5) |
| Work on the system with you | → Discovery or Build (section 6) |
| Install the agent skill | → Agent Skill (section 7) |
| Edit the workspace UI | → Workspace UI (section 8) |
| Know the research context | → Research (section 9) |
| Know what exists in the codebase | → Map (section 10) |

---

## 4. Architecture — what SpecuLoop is

SpecuLoop is a semantic reasoning environment. It has three layers:

**mumbleWRAP** — the semantic substrate. Stores meaning as nodes, edges, and primitives.
It is the persistent knowledge store. Think of it as "Words Reconstructed As Primitives."
It decomposes input into reusable semantic building blocks.

**DRAG** — Dynamic RAG. Selects and compresses knowledge from the graph for a given query.
It scores relevance under different lenses and returns a subgraph.

**SpecuLoop** — the orchestration layer. Agents, tests, tools, feedback, and execution.
It runs the grounding loop: observe → test → measure → update the basis.

The core idea: AI can generate knowledge faster than it can be grounded.
Generation explores. Grounding constrains. The semantic basis records what currently survives.

```text
SpecuLoop
    ├── mumbleWRAP: persistent semantic state / primitive basis
    ├── DRAG: lens-dependent retrieval, forces, and semantic zoom
    └── SpecuLoop: agents, tests, tools, feedback, and execution
```

---

## 5. Quick Start

```bash
git clone https://github.com/ivanferrier55/SpecuLoop.git
cd SpecuLoop
python3 demo.py
python3 mumblewrap/tests/test_core_loop.py
python3 mumblewrap/tests/test_semantic_reconstruction.py
```

### Example

```python
from mumblewrap.api import SpecuLoop

loop = SpecuLoop("knowledge.json")

loop.ingest("Speed and quality are in tension.")
result = loop.query("What affects quality?")

solve = loop.learn(
    "Semantic zoom should compress related information.",
    lens="onboarding",
    task="understand_system",
    decoder_name="my-model",
)
print(solve.compression.coverage)
print(solve.compression.uncertainty)
print(solve.evidence_id)
```

---

## 6. Discovery or Build

If the human confirmed the grounding-partner role:

**Discovery chat** — recovering intended semantics.
- Human statements are primary source. Record verbatim, not paraphrased.
- Your inferences are provisional until the human confirms.
- Gaps between what the repo says and what the human means: name the gap, don't resolve it silently.
- Keep a running primary-source log.

**Build session** — changing the code.
- Read `map/CLAUDE.md` to orient.
- Find the object in `map/objects/`.
- Check `map/effects/CONTEXT.md` for side effects.
- Run `python3 tests/test_core_loop.py` to verify.

---

## 7. Agent Skill

[`skills/speculoop/`](skills/speculoop/) is an installable Codex skill.
It turns SpecuLoop into persistent, grounded semantic memory for an agent.

```bash
python3 skills/speculoop/scripts/speculoop.py install --root .
python3 skills/speculoop/scripts/speculoop.py know "Experiments" supports "Evidence" --status observed --source "GROUNDING.md"
python3 skills/speculoop/scripts/speculoop.py query "What decreases Semantic inertia?"
```

The agent decomposes observations into subject-relation-object triples,
stores them with provenance and evidence status, queries them through DRAG,
and updates status as claims get grounded.

---

## 8. Workspace UI

```bash
python3 -m speculoop --workspace examples/markdown-workspace --port 8080
```
Left: file list + Markdown editor. Right: interactive graph. Bottom: sync report + provenance inspector.

---

## 9. Research context

- [`GROUNDING.md`](GROUNDING.md) — grounded semantic reasoning
- [`SEMANTIC_SOLVE.md`](SEMANTIC_SOLVE.md) — the semantic solve loop
- [`RECONSTRUCTION_STATUS.md`](RECONSTRUCTION_STATUS.md) — evidence and implementation status
- [`GLOSSARY.md`](GLOSSARY.md) — terminology

---

## 10. Map — what exists

The codebase map is in `map/CLAUDE.md`. It routes to every object and process.

| Layer | Entry |
|---|---|
| mumbleWRAP | `mumblewrap/api.py` |
| DRAG | `drag/selector.py`, `drag/scorer.py` |
| SpecuLoop | `speculoop/self_extender.py`, `speculoop/propagator.py` |

---

## License

MIT
