# Reality-Constrained Reasoning

Tool failures and environmental constraints become persistent semantic information rather than transient errors.

## How It Works

```
desired operation
    →
attempted execution
    →
success / failure
    →
semantic update
```

A failed tool call records:
- What was attempted
- What failed
- Why it failed
- What constraint was encountered

This information persists in the graph and informs future planning.

## Example

```
Agent tries to read a file → file not found
    →
Constraint recorded: "file X does not exist at path Y"
    →
Future planning avoids this path
```

## Related Technical Concepts

- grounded agent reasoning
- execution feedback
- tool-aware reasoning
- environment-aware AI
- constraint-aware planning
- failure-driven learning

**Related to**: [Semantic Feedback](semantic-feedback.md), [Semantic Forces](semantic-forces.md)

**Status**: Designed — `process_feedback()` exists but is not wired into the main loop.

**Confidence**: LOW — mechanism designed, untested.

## Questions This Project Addresses

- How can tool failures become persistent knowledge?
- How can constraints inform future planning?
- How can the system learn from what it cannot do?
