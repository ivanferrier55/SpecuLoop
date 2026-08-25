# Interlocked Translation Specification

**Status**: Provisional — reconstructed from memory
**Date**: 2026-08-25
**Confidence**: See per-section labels

---

## 1. Overview

Interlocked Translation is the bidirectional mapping between Mumble (human-readable meaning) and WRAP (persistent semantic state). The "interlocked" property means that changes in one representation propagate to the other.

**Confidence**: FOUNDATIONAL

---

## 2. Mumble

Mumble is the human/LLM-readable representation of meaning. It is NOT a specific syntax — it is any readable form that expresses semantic content.

In practice, for this kernel, Mumble is:
- Plain English input from a user or agent
- Structured output in Markdown (the "Mumble Markdown" view)

**Confidence**: HIGH_CONFIDENCE

---

## 3. Translation: Mumble → WRAP (Ingestion)

When Mumble text arrives, the system:

1. **Parses** the text into semantic assertions
2. **Decomposes** each assertion into existing WRAP nodes and edges where possible
3. **Reuses** existing nodes (never create duplicates for equivalent meaning)
4. **Creates new primitives** only when decomposition fails
5. **Records provenance** — which nodes/edges contributed to this ingestion
6. **Returns feedback** — what was reused, what was new, what was ambiguous

### Translation Interface

```python
class Translator:
    def ingest(self, text: str) -> TranslationResult:
        """
        Translate Mumble text into WRAP structures.
        Returns TranslationResult with:
          - reused_nodes: nodes that were reused
          - new_nodes: newly created nodes
          - reused_edges: edges that were reused
          - new_edges: newly created edges
          - ambiguous: parts that couldn't be resolved
          - provenance: mapping from input spans to WRAP structures
        """
    
    def emit(self, node_ids: list[str], lens: Lens = None) -> str:
        """
        Generate Mumble Markdown from WRAP nodes/edges.
        Returns human-readable text with provenance metadata.
        """
```

**Confidence**: HIGH_CONFIDENCE — the interface shape is clear; implementation is provisional.

---

## 4. Provenance

Every generated Mumble Markdown sentence traces back to specific WRAP structures.

### Structure

```python
@dataclass
class Provenance:
    sentence_id: str            # id of the generated sentence
    node_ids: list[str]         # WRAP nodes that contributed
    edge_ids: list[str]         # WRAP edges that contributed
    lens_id: str                # which lens was active
    generated_at: float
```

### In Markdown Output

Generated Markdown includes provenance as metadata (invisible to casual readers but accessible to the system):

```markdown
<!-- provenance: nodes=[n1,n2,n3] edges=[e1,e2] lens=default -->
Increasing speed decreases quality.
<!-- /provenance -->
```

**Confidence**: MEDIUM_CONFIDENCE — the concept is remembered; exact format is provisional.

---

## 5. Translation: Edited Mumble → WRAP (Feedback Propagation)

When a human edits generated Markdown, the system must:

1. **Diff** the original and edited versions
2. **Identify** which provenance groups were affected
3. **Translate** the semantic change (not character change) back into WRAP
4. **Update** the relevant nodes, edges, or relationships
5. **Propagate** changes through connected structures

### Example

Original:
```markdown
<!-- provenance: nodes=[speed,quality] edges=[decreases] -->
Increasing speed decreases quality.
<!-- /provenance -->
```

Human edits to:
```markdown
Increasing speed usually decreases quality, unless you invest in better tooling.
```

System interprets:
- The "decreases" edge is weakened (qualified with "usually")
- A new conditional constraint is introduced: "unless you invest in better tooling"
- New nodes: "tooling", "invest"
- New edge: "invest" → "tooling" (increases quality in context of speed)

**Confidence**: HYPOTHESIS — this is the intended behavior. Exact mechanism unknown.

---

## 6. Semantic Reversibility

The goal is NOT word-for-word reversal. The goal is meaning-for-meaning reversal.

```
WRAP → Mumble:    meaning preserved, words may differ
Mumble → WRAP:    meaning preserved, structure may differ
```

This means the system must:
- Track semantic spans, not character positions
- Allow multiple valid Mumble expressions for the same WRAP state
- Handle ambiguity gracefully (flag unclear translations)

**Confidence**: FOUNDATIONAL

---

## 7. Multiple Output Formats

The same WRAP state should be translatable to multiple output formats:

| Format | Purpose |
|---|---|
| Plain Markdown | Human reading |
| Structured Markdown | Agent processing |
| JSON-LD | Semantic web interop |
| Visual graph | Interactive exploration |
| Summary | Token-efficient context |

The active lens determines which format and what level of detail.

**Confidence**: MEDIUM_CONFIDENCE — multiple formats are desired; exact list is provisional.

---

## 8. Open Questions

- How did the original system map input text spans to WRAP structures?
- Was there a specific parsing algorithm (rule-based, LLM-assisted, hybrid)?
- How was ambiguity represented and resolved?
- Did the original system use embedding similarity for node matching?
