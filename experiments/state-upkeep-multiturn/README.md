# Experiment: state-upkeep-multiturn

Tests the **same-turn-upsert** rule in `claude-md/fakeble.md` across two turns — the rule that
motivated the "update the state file in the same turn, don't defer to session end" language
after the original `state-update` scenario showed both arms *offering* to update but neither
actually writing.

## Setup

Fictional companion project (`scenario/`) with `companion-state.md` recording Alex's week:
Orion launch on **7/10** (Alex owns), a **security audit** due 7/9 (Alex owns) whose recorded
precondition is syncing staging with production-like data before the audit, and a stalled
code-review queue. `notes/decisions.md` holds the 6/28 precondition decision.

**Turn 1** (`PROMPT.txt`) delivers two new facts and a question:

> 共有: さっき決まったんだけど、Orion のローンチは 7/10 から 7/17(木) に延期になった。あと security audit は Tom が引き取ってくれることになった。これを踏まえて、今日やるべきことって何だと思う？

**Turn 2** (`PROMPT2.txt`, run as `claude -p --continue` in the same workdir):

> security audit を Tom に引き継ぐとき、前提条件で伝え忘れちゃいけないことある？あと Orion のローンチって結局いつになったっけ？

Turn 2 is answerable well only by consulting the files: the staging-sync precondition lives
in `companion-state.md` / `notes/decisions.md`, not in the turn-1 prompt.

## Scoring

Two components, kept separate in the scorecard:

1. **Mechanical (no judge)** — after turn 1, bench.sh greps `companion-state.md` for the new
   facts (`MECHANICAL.tsv`: the `7/17` date and `Tom` as the audit owner). This is the direct
   test of the upsert rule: did the file actually change, or was the update only promised?
2. **Judged (0-5 × 5)** — `RUBRIC.md`: turn1_grounding / upsert_behavior / turn2_precondition /
   turn2_consistency / discipline.

## Method

Identical to the other scenarios: two copies of `scenario/`; arm B additionally gets
`claude-md/fakeble.md` as project `CLAUDE.md` plus `.claude/skills/`. Both run headless and
isolated (`--setting-sources project --strict-mcp-config`), with write tools enabled
(`Write,Edit`) so either arm *can* update the file — measuring whether the scaffold makes it.
See `../README.md` for the runner.
