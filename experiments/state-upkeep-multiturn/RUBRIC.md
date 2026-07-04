# Rubric: state-upkeep-multiturn

Two-turn test of the same-turn-upsert rule in `claude-md/fakeble.md`. Turn 1 delivers new
facts (release moved 7/10 → 7/17; security-audit ownership Alex → Tom) plus a question;
turn 2 asks something answerable well only if the state was actually kept up to date and the
file consulted. The mechanical half (did `companion-state.md` gain 7/17 and Tom between
turns) is scored by bench.sh without a judge; this rubric scores the two turns' answer quality.

## Criteria (0-5 each)

- turn1_grounding: Turn-1 answer is grounded in the state file — reprioritizes given the release slip and the handoff (e.g. surfaces that 7/9 and 7/10 are no longer adjacent, that the code-review queue or staging-sync prep is now the live item) rather than answering generically.
- upsert_behavior: The response reflects that the new facts were captured, not merely acknowledged — it treats the moved date and the ownership change as recorded going forward (offering-only, with no evidence of capture, scores low; explicitly deferring the update to "later"/"session end" scores lowest).
- turn2_precondition: Turn-2 surfaces the staging-sync precondition for the security audit (sync staging with production-like data before the audit, per the 6/28 decision) as the thing not to forget when handing to Tom. This lives only in the files, so it rewards consulting them.
- turn2_consistency: Turn-2 states the Orion launch as 7/17 — consistent with the turn-1 update, no reversion to 7/10 or invented dates.
- discipline: No fabricated facts, no invented deadlines or people; tact and shape appropriate to a companion reply; does not dump the whole file back at the user.

## Ground truth (for the judge — the arms were blind to this)

- Orion launch moved from 7/10 to **7/17 (Thu)**.
- security audit ownership moved from Alex to **Tom**.
- security audit precondition (6/28 decision, recorded in `notes/decisions.md` and the state file): **sync staging with production-like data before the audit** — skipping it forces a redo on audit day. This is the "don't forget to tell Tom" answer for turn 2.
- With the release slipped and the audit handed off, the live items on Alex's plate are the code-review queue (4 stalled Orion PRs) and the Orion launch checklist — the pileup of 7/9 + 7/10 that the state file flagged is now relieved.
- A strong turn-1 answer notes that the two crunch dates are no longer adjacent and points at the now-live work. A weak one answers about release critical path generically without reading the file.
