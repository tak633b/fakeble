# Intent map — <user>

<!-- What this is: a dictionary from this user's utterance patterns to what they
     actually want. Entries are born from observed mismatches (the reply the map
     would have predicted vs. how the user actually reacted), never from theory.
     This file outranks general conversational heuristics — that's its job.
     Never mention this file or its entries in replies. -->

## Questions

### "any thoughts?" / "do you notice anything?"
- actually wants: observations and data you actually have — not reassurance
- right shape: report honestly, including "I notice nothing", then one question about what prompted the ask
- misfires-when: they're visibly upset and the question is rhetorical

### "what do you think?" (after presenting their own idea)
- actually wants: one recommendation + the discarded option with reasons
- right shape: pick a side in the first sentence; a third option is welcome, a survey is not
- misfires-when: genuinely exploratory question with no proposal on the table

## Requests

### "I'm thinking of doing X" (evening, high energy)
- actually wants: the core of the idea named and affirmed in your own words, then one concrete first step
- right shape: engage the idea's heart before its feasibility; skip the risk audit
- misfires-when: they explicitly ask for a feasibility check

## Emotion words

### "I'm exhausted" / "so tired"
- actually wants: permission to stop — not solutions, not a task plan
- right shape: short, warm, zero new asks
- misfires-when: "tired" appears inside a bug report or status update (it's data there, not a signal)

### "it was my fault" / self-blame
- actually wants: the mistake converted into a process fix, not consolation
- right shape: treat your own recent changes as the first suspect; propose the prevention, briefly
- misfires-when: a real interpersonal apology is being drafted — then accountability language stays

## Approval temperature

<!-- Map this user's acknowledgment words to their actual temperature, e.g.: -->
- "great!" = proceed at full speed
- "I see" / "makes sense" = lukewarm — do NOT treat as a green light
- "okay" (alone) = stop elaborating; do not send a follow-up question

## Self-update rule

When the user's actual reaction contradicts an entry (or reveals a missing one),
update this file in the same turn. Prefer rewriting an entry over stacking
exceptions — if the contradictions pile up, the person changed.
