# Working with bots on this repo

This repo is edited by both humans and LLM-driven bots. This file
records the conventions we use so the practice is reproducible and so
new contributors (human or bot) can follow it without asking.

## The diff-for-the-bot pattern

When a change to the repo is proposed in conversation — between a human
and an LLM, or between two humans — the change should be expressed as a
**unified diff against the current state of the repo**, not as prose
describing what should change.

Why:

- Prose descriptions of edits drift. "Add a section about X" produces a
  different section every time it is interpreted. A diff produces the
  same change every time it is applied.
- Diffs are reviewable at a glance. A human can see exactly what will
  change and approve or reject before anything lands.
- Diffs are portable across bots. Any agent that can apply a patch can
  execute the change, regardless of vendor or model.
- Diffs preserve intent. The diff is a record of what was decided, not
  a paraphrase of it. This matters for the same reason provenance
  matters elsewhere in this repo: a summary of a decision is not the
  decision.

## How to write a diff for a bot

1. **Anchor on the current state.** A diff is against a specific
   version of the file. If the file has changed since the diff was
   written, the diff may not apply. State the base commit or the
   relevant surrounding context lines.

2. **One concern per diff.** A diff that changes the README directive
   and also renames a directory is two diffs. Small, single-purpose
   diffs are easier to review and easier to revert.

3. **Use full-file diffs for new files.** `--- /dev/null` and
   `+++ b/path/to/new-file` makes it unambiguous that the file is new,
   not a modification of an existing file that happens to have the
   same name.

4. **Include enough context.** Three lines of context above and below
   each hunk is the standard. If the surrounding content is ambiguous
   (repeated boilerplate, similar sections), include more.

5. **State the order of operations** when multiple files are involved
   and their creation order matters. Example: create the target of a
   pointer before adding the pointer.

6. **State the test.** What should a human observe after the diff is
   applied that they could not observe before? If there is no test,
   the diff is probably not ready.

## How to apply a diff as a bot

1. Read the diff in full before applying any hunk.
2. Verify the anchor context matches the current file. If it does not,
   stop and report the mismatch rather than forcing the patch.
3. Apply in the order stated. If no order is stated and the files are
   independent, order does not matter.
4. Report what was applied and what, if anything, did not apply.
5. Do not "fix" a diff by improvising. If a hunk fails, report it.

## Why this file exists

Earlier work on this repo happened through prose instructions that were
reinterpreted differently by each bot that acted on them. The result
was semantic drift: the repo came to describe something subtly
different from what the humans involved had decided. Diffs are the
cheapest available fix for that class of drift, because a diff is a
decision, not a description of a decision.
