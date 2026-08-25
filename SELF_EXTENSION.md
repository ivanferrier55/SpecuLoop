# Self-Extension Specification

**Status**: Provisional — reconstructed from memory
**Date**: 2026-08-25
**Confidence**: See per-section labels

---

## 1. Overview

Self-extension is the system's ability to grow its own semantic vocabulary when existing structures are insufficient. This is essential for a system that must represent arbitrary human knowledge.

**Confidence**: FOUNDATIONAL

---

## 2. The Problem

When a new input arrives, the system attempts to decompose it into existing WRAP nodes and edges. Sometimes this fails:

- No existing node matches a concept in the input
- No existing edge captures the relationship expressed
- The input introduces a genuinely new type of structure

In these cases, the system must propose new structures rather than silently failing or losing information.

**Confidence**: FOUNDATIONAL

---

## 3. Extension Interface

```python
class SelfExtender:
    def attempt_decompose(self, text: str, graph: Graph) -> DecompositionResult:
        """
        Try to decompose text into existing structures.
        Returns DecompositionResult with:
          - success: bool
          - reused: list of (node_ids, edge_ids) used
          - gaps: list of unresolved spans (text that couldn't be decomposed)
          - confidence: float
        """
    
    def propose_primitive(self, text: str, context: list[str]) -> Primitive:
        """
        Propose a new primitive node for a concept that doesn't exist.
        Returns a proposed Primitive with suggested kind, label, and content.
        """
    
    def propose_relation(self, source_id: str, target_id: str, 
                         context: str) -> Edge:
        """
        Propose a new edge type for a relationship that doesn't exist.
        Returns a proposed Edge with suggested relation type.
        """
    
    def confirm(self, proposal_id: str, human_feedback: str):
        """
        Human confirms or modifies a proposal.
        Confirmed proposals are added to the graph.
        Modified proposals are adjusted and then added.
        Rejected proposals are recorded but not added.
        """
```

**Confidence**: HIGH_CONFIDENCE — the interface is clear; proposal mechanism is provisional.

---

## 4. Proposal Flow

```
input text
    ↓
attempt_decompose()
    ↓
success? → use existing structures
    ↓ (failure)
propose_primitive() for unrecognized concepts
    ↓
propose_relation() for unrecognized relationships
    ↓
present proposals to human (or auto-accept with low confidence)
    ↓
human confirms / modifies / rejects
    ↓
confirmed proposals become new WRAP structures
```

**Confidence**: HIGH_CONFIDENCE

---

## 5. Proposal Quality

Proposals should be:

- **Specific**: not too vague, not too narrow
- **Justified**: explain why this primitive/relation is needed
- **Testable**: can be validated against future inputs
- **Mergeable**: can be combined with existing nodes if a match is found later

### Proposal Metadata

```python
@dataclass
class Proposal:
    id: str
    kind: str                   # "primitive" or "relation"
    proposed_structure: Node | Edge
    reason: str                 # why this is needed
    alternatives: list[str]     # other ways this could be represented
    confidence: float           # system's confidence in this proposal
    source_text: str            # the input that triggered this
    created_at: float
    status: str = "pending"     # pending, confirmed, modified, rejected
```

**Confidence**: MEDIUM_CONFIDENCE

---

## 6. Learning from Proposals

Over time, the system should:

1. Track which proposals are confirmed → increase confidence for similar proposals
2. Track which proposals are rejected → decrease confidence for similar proposals
3. Identify patterns in rejections → refine the proposal algorithm
4. Eventually propose structures that humans consistently accept

This is the beginning of the self-improvement loop.

**Confidence**: HYPOTHESIS — the concept is clear; the mechanism is speculative.

---

## 7. Guardrails

- Never auto-create nodes without recording that they are provisional
- Always present human review for low-confidence proposals
- Limit the number of proposals per input (prevent explosion)
- If too many proposals are needed, suggest that the input may need decomposition at a higher level
- Track total graph growth rate to prevent unbounded expansion

**Confidence**: MEDIUM_CONFIDENCE

---

## 8. Open Questions

- How did the original system handle genuinely novel concepts?
- Was there automatic primitive creation or always human-in-the-loop?
- How were proposals validated?
- Was there a concept of "proven" vs. "unproven" primitives?
