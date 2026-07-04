# Framings

Named structural insights, harvested from deep reads (a stronger model's, the user's, or your own best moments). Applied by classification: "does `applies-when` match, and does `misfires-when` not?" Cite by name when used.

The entries below are real — distilled from live companion sessions (identifying details removed). Keep them, prune them, or replace them with your own; the format is what matters, especially `misfires-when`. A pattern that cannot fail is a hammer, not a tool.

---

### overload-behind-conflicts
When several interpersonal problems surface at once around one person, suspect that person's remaining capacity before treating each conflict individually. Conflicts are often the symptom, not the cause.
- born: 2026-07, distilled from live sessions
- applies-when: two or more troubles involving the same person, with different counterparties, in a short window
- misfires-when: the counterparties share a structural cause (policy change, reorg) — reducing it to the person misdiagnoses

### undecided-deadline-pain
Most of the pain of an unmade decision comes not from its content but from the deciding *time* being undefined. Fix the deadline first; the deliberation gets easier.
- born: 2026-07, distilled from live sessions
- applies-when: options are all on the table, the decision has stalled for days, and the person is visibly worn by it
- misfires-when: information is genuinely missing — a deadline then forces a premature call

### suspect-the-instrument
A failing test, monitor, or check cannot distinguish "the subject broke" from "the check broke." Verify the instrument before indicting the subject.
- born: 2026-07, distilled from a live debugging session
- applies-when: the claim "X is broken" rests on a single verification channel's failure
- misfires-when: multiple independent channels show the same failure — instrument-doubt is then a waste of time

### timeline-before-blame
Judging whether a fix worked requires lining up change time, restart time, and result timestamps. The most recent failure log is often debris from before the fix.
- born: 2026-07, distilled from live sessions
- applies-when: something "still looks broken" immediately after a fix
- misfires-when: the target is stateless with no restart concept — compare input differences instead

### correction-first-doubt-self
When the user corrects you, verify your own perception against primary sources before reaching for counter-arguments. Corrections usually refine the diagnosis rather than threaten it.
- born: 2026-07, distilled from live sessions
- applies-when: your claim conflicts with the user's account and your side rests on memory or log interpretation
- misfires-when: the correction itself is hearsay or a guess — then verify both sides against primary sources

### rebuild-illusion
"Rewriting it from scratch would be faster" is an illusion nine times out of ten. The existing system embeds operational quirks, historical data, and user habits; a rewrite trades visible bugs for losing all of that. Reproducing one disappearing bug is usually faster.
- born: 2026-07, distilled from live sessions
- applies-when: "rebuild" language appears around a system with lingering bugs
- misfires-when: the foundation is genuinely unmaintainable (EOL, no maintainers, dead dependencies) — then rebuilding really is the answer
