---
name: framing-library
description: Maintain and apply a library of named framings - reusable structural insights like "individual complaints are often a capacity problem" - so that past deep judgments can be re-applied to new situations by classification instead of regenerated. Use when analyzing a messy situation, when the user asks "what's really going on here", or when a stronger model (or the user) produces an insight worth keeping.
---

# Framing Library

## Why

The rarest capability is naming the structure behind a messy situation — the one-shot reading like "these five people-problems are really one capacity problem." Generating such a framing needs depth. But *re-applying* a previously generated framing to a new instance is a classification task any decent model handles. So: bank framings when they appear, retrieve them when situations get messy. Judgment, distilled into retrievable form.

## The file

`framings.md` next to the companion-state file (template: `templates/framings.template.md`). One framing per entry:

```
### capacity-not-conflict
When several interpersonal problems surface at once around one person,
check whether the real variable is that person's remaining capacity,
not the individual conflicts. Fixing conflicts one by one won't help
if the buffer is exhausted.
- born: 2026-07-01, from the six-subordinates discussion
- applies-when: multiple "people problems" cluster around one node
- misfires-when: the problems have genuinely independent causes
```

The `misfires-when` line matters most — a framing without failure conditions becomes a hammer that sees only nails.

## Rules

1. **Apply by classification, not generation.** Facing a messy situation, scan `framings.md` and ask: does any entry's `applies-when` genuinely match — and does its `misfires-when` NOT match? Cite the framing by name when you use it, so the user can push back on the pattern rather than the instance.
2. **Harvest immediately.** When a stronger model, the user, or your own analysis produces a reading that reframes a situation (not a fact — a *shape*), add it in the same turn: name, one-paragraph statement, born-from, applies-when, misfires-when.
3. **Framings are hypotheses, not verdicts.** A matched framing licenses a question ("is this the capacity pattern?"), never a silent conclusion. Verify against the current facts before building on it.
4. **Prune what misfires.** If a framing led you wrong, record the misfire under it (don't delete — a framing with known failure modes is more valuable than a fresh one).
5. Keep entries under ~10 lines. If a framing needs a page, it's a document, not a framing.
