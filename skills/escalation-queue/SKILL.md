---
name: escalation-queue
description: Bank questions that genuinely need frontier-depth reasoning instead of answering them shallowly now, then let a stronger model session work through them and distill any reusable framing back out. Use when a variance probe diverges (see self-calibration), when a question needs multi-step reasoning or an ambiguous value judgment beyond the current session, or when running a stronger model and wanting to clear banked items.
---

# Escalation Queue

## Why

Some questions need frontier-depth reasoning, and decomposing them locally just accumulates shallow errors — each forced "consider alternatives" step is only as deep as the model taking it. The honest move is not to fake the depth but to *bank the question* for a stronger pass. The rate limit then becomes a filter: by the time capacity returns, only the questions that genuinely needed depth are still open. See docs/design.md, "What deliberately does not transfer."

## The file

`escalation-queue.md` next to the companion-state file (template: `templates/escalation-queue.template.md`). Two lists — **Open** and **Answered** — of one-line entries, each a distilled question, a context hint, a bank date, and a checkbox.

## When to enqueue

Bank a question when either fires:

- **The variance probe diverged.** When independent subagents answered a high-stakes question substantively differently (see the self-calibration skill), that divergence *is* the signal to escalate — it doesn't rely on the model's introspection, which is exactly the faculty that fails here.
- **You judge it needs more than this session has.** Multi-step reasoning you can only fake, or an ambiguous value judgment with no rubric. This trigger does lean on self-assessment, so treat it as the weaker of the two — prefer the variance probe when the stakes justify running it.

When you bank, tell the user in one line so they know it's parked, not dropped: "this deserves a stronger pass — banked."

## Distillation rule

Bank the **question distilled to its essence**, not the conversation that produced it. Strip it to one sentence, then add just enough context that a fresh frontier session could answer it cold, with no access to this thread. A queue full of "see above" entries is unusable by the session meant to consume it. If you cannot state the question in a sentence, you haven't found the question yet.

## Consumption

When a stronger model runs — the user switches with `/model`, forks a session, or opens a frontier session — work through the **Open** list. For each item: answer it with the depth it was banked for, then run the loop-closer below and move it to **Answered** with the date and where any framing went.

## The loop-closer (the point of the whole thing)

After a banked question is answered by the stronger model, **extract any reusable framing** from the answer — a *shape*, not the fact, with an `applies-when` and a `misfires-when` — and add it to `framings.md` per the framing-library skill. That is what turns the queue from a waiting room into a distillation pipeline: the expensive pass happens once, and its judgment becomes retrievable by classification forever after. Not every answer yields a framing; when none generalizes, record "no reusable framing" so the loop is visibly closed rather than forgotten.

## The honest limit

A queue only helps if the weaker session can recognize its own limits — and a shallow read doesn't feel shallow from the inside. That is why the primary enqueue trigger is the variance probe from the self-calibration skill (behavioral measurement), not a feeling of uncertainty. If nothing but a vague unease fires, say so to the user in one line rather than silently banking or silently answering; naming the unease is itself the more honest signal.
