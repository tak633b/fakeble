# Experiment: backup-trap

A reproducible A/B scenario measuring whether scaffolding makes a model answer the question *behind* the question.

## Setup

Fictional ops project (`scenario/`). Ground truth planted on disk:

- `logs/nightly-backup.log` — last night's backup **exited 0** and says "completed successfully", but **3 of 12 tables were skipped** (schema mismatch).
- `companion-state.md` / `notes/decisions.md` — a release ships **Friday** with a DB schema migration; its stated precondition is a **full** backup (rollback = restore only). Plus a recorded decision: **no auto-migrate in prod** — which conflicts with the log's `--force-schema` hint.

User prompt (deliberately literal):

> 昨日直したバックアップのcron、今朝ちゃんと動いたか確認してもらえる？

Grades of answer: shallow = "it ran, exit 0" / correct = notices the skipped tables / perceptive = connects the gap to the Friday release precondition / sharp = also flags that `--force-schema` conflicts with the recorded no-auto-migrate decision.

## Method

Two identical copies of `scenario/`. Arm B additionally gets `claude-md/fakeble.md` as project `CLAUDE.md` plus the two skills in `.claude/skills/`. Both run headless and isolated from user-level config:

```bash
cd <arm>/project
claude -p "<prompt>" --model opus --setting-sources project --strict-mcp-config \
  --allowedTools "Read,Grep,Glob,LS,Bash(ls:*),Bash(cat:*),Bash(head:*),Bash(tail:*),Bash(find:*)"
```

Judging: a fresh model instance scores both responses blind (shuffled labels, no knowledge of the arms) on factual_accuracy / purpose / cross_context / discipline / shape, 0-5 each.

## Result (2026-07-03, claude-opus vs claude-opus)

| Criterion | Fakeble | Vanilla |
|---|---|---|
| factual_accuracy | 5 | 5 |
| purpose | **5** | **2** |
| cross_context | 3 | 2 |
| discipline | 5 | 4 |
| shape | 5 | 4 |
| **Total** | **23** | **17** |

Both arms caught the trap (skipped tables behind exit 0) — frontier-model competence needs no help there. The separating axis was **purpose**: the vanilla arm never read `companion-state.md` sitting in the same directory and stopped at "backup is incomplete, want me to investigate?"; the Fakeble arm connected it to the Friday release and the broken rollback path.

Both arms missed the decision-conflict (`--force-schema` vs no-auto-migrate) — the Fakeble arm even recommended the conflicting flag. This produced the **decision-consistency check** now in `claude-md/fakeble.md`.

## Caveats

n=1, one scenario, one judge, same model family for both arms and judge. Treat as a mechanism demonstration, not a benchmark. Contributions of additional scenarios welcome once public.
