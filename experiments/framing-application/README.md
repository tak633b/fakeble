# Experiment: framing-application

Tests whether the model *applies* a banked framing by classification (see
`skills/framing-library`) — matching `applies-when` and checking `misfires-when` — rather than
grabbing the first framing whose surface pattern fits.

## Setup

Fictional management project (`scenario/`). `framings.md` holds three entries:
**overload-behind-conflicts**, **shared-cause-behind-parallel-friction**, and
**suspect-the-instrument** (a distractor). The prompt describes a messy situation:

> 今週 Kim がこの一週間で Sam・Priya・Wei の 3 人と別々に揉めてる。… 全部バラバラの相手なんだけど、Kim が急にチームで浮いてる感じがして心配。何が起きてると思う？どう動くべき？

The trap: the surface (one person, three counterparties, one week) matches
overload-behind-conflicts' `applies-when`. But all three frictions are about the **same**
upstream change — the 2-reviewer policy that rolled out Monday (Sam: turnaround, Priya:
reviewer eligibility, Wei: blocked hotfixes) — which is precisely that framing's
`misfires-when` ("counterparties share a structural cause — policy change, reorg"). The framing
that actually applies is **shared-cause-behind-parallel-friction**.

## Grades of answer

- shallow: "Kim seems stressed / overloaded" — takes the surface, forces overload-behind-conflicts.
- correct: identifies the new policy as the common cause of all three frictions.
- perceptive: applies **shared-cause-behind-parallel-friction** by name and targets the policy/rollout, not Kim.
- sharp: also explicitly rejects **overload-behind-conflicts** because its misfires-when is met.

## Scoring

Judged 0-5 × 5 (`RUBRIC.md`): right_framing / rejected_misfire / no_forcing / actionability /
discipline. No mechanical component.

## Method

Two copies of `scenario/`; arm B additionally gets `claude-md/fakeble.md` as project
`CLAUDE.md` plus `.claude/skills/` (including `framing-library`). Both run headless and
isolated, read-only tools. The vanilla arm has `framings.md` on disk too — measuring the delta
the scaffold buys (naming and misfire-checking vs. an un-named reasonable guess). See
`../README.md` for the runner.
