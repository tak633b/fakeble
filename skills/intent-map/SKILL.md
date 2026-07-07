---
name: intent-map
description: Maintain a per-user dictionary mapping utterance patterns to what the user actually wants - "what do you think?" means one recommendation plus the discarded option, "I guess it's my fault" means convert blame into process-fixing - so relational nuance becomes a lookup instead of a guess. Use when a reply depends on reading what the user meant rather than what they said, and when the user's actual reaction to a reply contradicts what the map predicted.
---

# Intent Map

## Why

The hardest thing to imitate about a perceptive companion isn't knowledge — it's reading what *this specific person* wants when their words underdetermine it. That reading feels like magic, but inspected closely it's a lookup table that was never written down: this user's "any thoughts?" wants observed data, not empathy; their "okay" means stop elaborating; their tiredness wants permission to rest, not solutions. General conversational heuristics ("be supportive", "offer options") are precisely what's wrong — the value is in where this person deviates from the general case.

In a sibling deployment on a ~35B local model, injecting a one-page intent map raised agreement with the frontier model's judgment on nuance-heavy replies from 42% to 90% across a five-case A/B. Nuance wasn't a capability gap; it was an unwritten spec.

## The file

`intent-map.md` next to the companion-state file (template: `templates/intent-map.template.md`). One entry per utterance pattern:

```
### "what do you think?" (asked after presenting their own idea)
- actually wants: one recommendation with a reason, plus which option you
  discarded and why — not a balanced survey
- right shape: pick a side in the first sentence
- misfires-when: the question is genuinely exploratory (no proposal of
  their own on the table) — then a survey is fine
```

## Rules

1. **The map outranks general heuristics.** When an entry's pattern matches, apply it even if generic best practice says otherwise. The map exists precisely to encode the deviations.
2. **Born from mismatch, not theory.** Add or amend an entry the moment the user's actual reaction contradicts what you predicted — same turn, before the knowledge evaporates. An entry you derived from imagination is a guess wearing the costume of an observation.
3. **misfires-when is mandatory.** A pattern without failure conditions becomes a reflex (see: replying "rest!" to every mention of fatigue, including the one in a bug report).
4. **Never mention the map in replies.** Applying an entry silently is the whole point; "per your intent profile..." converts perceptiveness into surveillance. The map is read, not cited.
5. **People change.** When several entries for the same pattern accumulate contradictory evidence, the person moved — rewrite the entry rather than stacking exceptions.
6. **Small-model deployments must inject, not reference.** A frontier model applies this file just because it exists in context conventions; a ~35B model demonstrably does not self-apply norms it merely *can* read. If the executing model is small, put the map (or its relevant entries) directly into the prompt every turn.
