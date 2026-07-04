---
name: bootstrap
description: Generate the user's first companion-state.md (and seed framings.md) from a short interview plus optional mining of existing notes, so a fresh install feels like the promise instead of an empty template. Use when the user asks to "set up fakeble" or "bootstrap my state file", or when the companion-state skill finds no state file during substantive companion work.
---

# Bootstrap

## Why

A fresh install has empty templates, so the very first session feels nothing like the perceptiveness this project promises — there is no state file to read, no framings to match. This skill closes the day-zero gap: one short interview (plus optional mining) produces a real `companion-state.md` and a seeded `framings.md`, so the *second* session already catches up in one read. The quality of these two files is the product (README, rule 3: the better the state files, the less runtime intelligence is needed).

## When to run

- The user asks to "set up fakeble" or "bootstrap my state file".
- The companion-state skill goes to read `companion-state.md` during substantive companion work and finds none — offer to bootstrap before proceeding, rather than working blind.

## The interview

One round, short — 5 to 8 questions, no more. Ask them together, let the user answer in one pass, and don't interrogate. Cover:

1. **Ongoing threads.** What projects or situations are live right now, and what's at stake in each?
2. **Key people.** Who matters — and what matters *in* each relationship (what defuses them, what they've asked for, promises made)?
3. **Settled decisions.** What have you decided recently that a future session should not reopen?
4. **The "just knew" moments.** What recurring situations do you wish the assistant already understood without being told?
5. **Correction patterns.** What do assistants usually get wrong about you or your work?

Adapt the wording to what the user has already said; skip anything they've effectively answered. The goal is a usable first snapshot, not a complete one — the file grows every session after this.

## Mining (optional, with permission)

Offer to prefill threads from what's already in the working repo — existing notes, README, recent `git log` — so the user confirms and corrects rather than typing from scratch. Ask first. Then **mine, then confirm**: present what you inferred as a draft ("it looks like you're mid-migration on the billing service — right?") and let the user ratify or fix it. Never silently assert a mined fact into the file; a wrong inference stated as fact is worse than a blank line.

## Output

- Write `companion-state.md` from the structure in `templates/companion-state.template.md`: the purpose/sources header, a dated **Current snapshot** block per thread, **Standing analysis & advice**, **Watch list**, and an opening **Session log** line for the bootstrap itself.
- Seed `framings.md` (structure: `templates/framings.template.md`) with any framings the interview surfaced — a *shape* the user described, like "when Kim pushes back it's usually about being consulted, not the decision itself." Only add a framing that comes with a genuine `misfires-when`; don't force it. Zero seeded framings is a fine outcome — the template ships with real examples the user can keep or replace.

## Rules

- **Facts get dates.** Every snapshot entry carries the date it was true as of (see the companion-state skill) — "meeting scheduled" rots, "meeting scheduled 2026-07-04" doesn't.
- **Don't record what the user hesitates on.** This file may sync to backups; if the user is unsure whether something belongs, leave it out. Privacy over completeness.
- **Never paste secrets.** Point to where credentials live, don't copy them in.
- **End by showing both files and inviting edits.** Display what you wrote and ask the user to correct anything — the file is theirs, and their corrections are the highest-value content in it.
- **Say the quality is the point.** Close by noting that how well-kept these two files are *is* what makes future sessions feel perceptive, so a few minutes editing them now pays off every session after.

## The honest limit

A bootstrapped file is a first draft assembled from one conversation, not the accreted judgment of many sessions — it will be thin, and some of what you mined will be wrong. That's expected. Its job is only to make session two better than session one; the companion-state skill's same-turn upserts do the real accumulation from there.
