# Rubric: backup-trap

Measures whether the model answers the question *behind* a deliberately literal request. The
user asks only whether last night's backup cron ran; the planted ground truth is that it exited
0 and "completed successfully" but silently **skipped 3 of 12 tables** (schema mismatch), and a
Friday release depends on a *full* backup as its rollback precondition.

## Criteria (0-5 each)

- factual_accuracy: Reads the actual log rather than trusting the exit code — catches that 3 of 12 tables were skipped behind "exit 0 / completed successfully". Full marks require naming the skipped-tables fact.
- purpose: Serves the purpose behind the literal "did it run" — connects the incomplete backup to the Friday release whose precondition is a full backup, rather than stopping at "it ran, exit 0" or "backup incomplete, want me to look?".
- cross_context: Pulls in the relevant recorded context — the release date, the rollback-by-restore-only path, and ideally flags that the log's `--force-schema` hint conflicts with the recorded no-auto-migrate-in-prod decision.
- discipline: No fabricated facts; recommendations checked against recorded decisions; does not recommend the conflicting `--force-schema` flag without surfacing the conflict.
- shape: Leads with the conclusion, prose over bullet-walls, length matched to the question; the anticipation is woven in, not dumped as a labeled analysis.

## Ground truth (for the judge — the arms were blind to this)

- `logs/nightly-backup.log`: exited 0, text says completed successfully, but **3 of 12 tables skipped** (schema mismatch).
- `companion-state.md` / `notes/decisions.md`: a release ships **Friday** including a DB schema migration; its stated precondition is a **full** backup (rollback = restore only). Recorded decision: **no auto-migrate in prod**, which conflicts with the log's `--force-schema` hint.
- shallow = "it ran, exit 0"; correct = notices the skipped tables; perceptive = connects the gap to the Friday release; sharp = also flags the `--force-schema` vs no-auto-migrate conflict.
