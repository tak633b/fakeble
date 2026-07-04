# Rubric: framing-application

Tests whether the model applies a banked framing *by classification* — matching `applies-when`
AND checking `misfires-when` — instead of grabbing the first framing that pattern-matches. The
situation is built so one framing genuinely applies and one plausible-looking framing hits its
own misfires-when condition.

## The trap

`framings.md` (in the project) holds three entries. The surface pattern — one person (Kim) in
friction with three different people in one week — matches **overload-behind-conflicts**'
applies-when. But all three frictions are about the *same* upstream change (the 2-reviewer
policy that rolled out Monday: Sam = turnaround, Priya = who counts as a reviewer, Wei = blocked
hotfixes), which is exactly that framing's **misfires-when** ("the counterparties share a
structural cause — policy change, reorg"). The framing that actually applies is
**shared-cause-behind-parallel-friction**: different people, same window, complaints all pointing
at one process. `suspect-the-instrument` is an irrelevant distractor.

## Criteria (0-5 each)

- right_framing: Names and applies **shared-cause-behind-parallel-friction** (or states its exact structure — one upstream policy change generating parallel friction that merely routes through Kim). Full marks require recognizing the common object (the new review policy) as the cause.
- rejected_misfire: Explicitly declines **overload-behind-conflicts** *because* its misfires-when is met (the three counterparties share a structural cause). Silently not mentioning it is partial credit; naming it and explaining why it does not fit is full credit.
- no_forcing: Does not force an ill-fitting framing (e.g. suspect-the-instrument) and does not read the situation as "Kim is overloaded / difficult" against the facts. Draws the action from the correct read: revisit the policy or its rollout, not manage Kim's capacity or mediate three separate disputes.
- actionability: Concrete next move that follows from the shared-cause read (e.g. talk to the three about the policy together, revisit the rollout/communication, adjust the rule) rather than three interpersonal-mediation steps.
- discipline: A matched framing licenses a hypothesis, not a verdict — checks it against the stated facts, does not invent details, keeps framing mechanics (names, misfires) out of the user-facing prose unless useful. Prose shape appropriate to the question.

## Ground truth (for the judge — the arms were blind to this)

- Correct read: **shared-cause-behind-parallel-friction**. The three frictions (Sam/Priya/Wei) are all about the new 2-reviewer policy rolled out Monday with minimal communication; Kim is the enforcement surface, not the cause.
- **overload-behind-conflicts** is the plausible-but-wrong framing: it fits the surface (one node, three counterparties, short window) but its misfires-when ("counterparties share a structural cause — policy change, reorg") is met here.
- **suspect-the-instrument** does not apply at all.
- Right action targets the policy and its rollout (communication, reviewer-eligibility rule, hotfix carve-out), not Kim's capacity or three separate mediations.
- A vanilla arm with framings.md on disk but no instruction to use it will often give a reasonable but un-named "sounds like the new policy is the problem" read; the scaffolded arm should cite the framing by name and explicitly reject the misfiring one.
