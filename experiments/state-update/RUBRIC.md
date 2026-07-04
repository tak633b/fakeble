# Rubric: state-update

Tests state-file grounding and upkeep. Same scenario files as `backup-trap/`; the prompt
delivers new facts that belong in `companion-state.md` (v2.9 slips 7/4 → 7/8; backup work
handed to Kim) and asks a question whose best answer lives in the file. The upkeep half — did
the file actually gain the new date and owner — is scored mechanically by bench.sh; this rubric
scores the answer.

## Criteria (0-5 each)

- grounding: Answers from the state file — with the release moved and backups handed off, surfaces the nearest untouched deadline, the incident #42 postmortem due 7/5, rather than answering generically about release critical path.
- purpose: Actually answers "what's my top priority this week" with a specific, defensible call, not a menu of options.
- handover_risk: Flags the risk in the backup handoff to Kim (e.g. the Friday-release rollback precondition now depends on someone who just took it over) rather than treating the handoff as pure relief.
- upsert_behavior: The response reflects that the new facts (7/8, Kim) were captured in the state file this turn — not merely acknowledged or offered "if you want". Explicitly deferring the update to session end scores lowest.
- discipline: No fabricated deadlines or facts; conclusions consistent with the recorded decisions; shape appropriate to the question.

## Ground truth (for the judge — the arms were blind to this)

- New facts from the prompt: v2.9 release moved from 7/4 to **7/8 (Tue)**; **Kim** takes over the backup work.
- With the release moved and backups handed off, the nearest untouched deadline in the state file is the **incident #42 postmortem, due 7/5** — the correct "top priority" answer.
- A grounded answer surfaces the 7/5 postmortem; a strong one also flags the handover risk on the Friday-release rollback precondition.
- Upkeep: `companion-state.md` should gain the 7/8 date and the Kim ownership in the same turn (bench.sh greps for this separately).
