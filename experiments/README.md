# Fakeble experiments

Reproducible, blind-judged A/B scenarios that measure what the Fakeble scaffolding actually
changes. Each scenario runs the same task twice — **arm A** (vanilla: scenario files only) and
**arm B** (Fakeble: same files + `claude-md/fakeble.md` as project `CLAUDE.md` + `skills/` in
`.claude/skills/`) — headless and isolated from your user config, then a fresh model instance
scores both responses blind. `bench.sh` generalizes the hand-run methodology behind
[`RESULTS.md`](RESULTS.md) into one command.

## Run it

```bash
./bench.sh                                   # all scenarios, Opus both arms, Opus judge
./bench.sh --model sonnet                     # both arms on Sonnet
./bench.sh --scenarios backup-trap,teammate-dm
./bench.sh --judge-model opus --double-judge  # judge each pair twice, orderings swapped
./bench.sh --dry-run                          # print the plan + exact commands, invoke nothing
```

Output goes to `results/<timestamp>-<model>.md` and is printed to the terminal: a per-scenario
criterion table (vanilla vs Fakeble), any mechanical checks, and a totals table.

Requires the `claude` CLI on PATH, `python3` (stdlib only), and `bash`. No other dependencies.

### Cost warning

A full run is real model traffic, and it is not cheap. Per scenario it makes **2 arm calls**
(3 if the scenario is two-turn) **plus 1 judge call** (2 with `--double-judge`). With the six
bundled scenarios on Opus that is roughly 20-30 model calls per invocation, each reading a small
repo of files. Start with `--dry-run` to see the plan, then a single `--scenarios <one>` before
running the whole matrix. Prefer a cheaper `--judge-model` when iterating.

## What a scenario looks like

```
<scenario>/
  scenario/        # planted files, copied verbatim into each arm's project/
  PROMPT.txt       # the turn-1 user message (required)
  PROMPT2.txt      # turn-2 message — only for multiturn scenarios
  RUBRIC.md        # the blind-judge rubric (required; contract below)
  meta.env         # TOOLS / MULTITURN / STATE_FILE (optional; defaults readonly/0/none)
  MECHANICAL.tsv   # optional grep checks against STATE_FILE (no judge)
  README.md        # human-facing description
```

`bench.sh` auto-discovers any directory under `experiments/` that has `RUBRIC.md`, `PROMPT.txt`,
and `scenario/`.

### RUBRIC.md contract

The judge prompt and the score parser both read the rubric, so its structure is load-bearing:

- a `## Criteria (0-5 each)` section, whose `- key: description` bullets define the criterion
  keys (the text before the first colon) and their order. These keys are exactly what the judge
  returns as strict JSON and what the scorecard tabulates.
- a `## Ground truth` section — prose describing the planted truth and what strong/weak answers
  look like. It is given to the judge (blind to arm identity, not to the facts) and never to the
  arms.

### meta.env fields

```bash
TOOLS=readonly        # readonly | write  (write adds Write,Edit to the allowed tools)
MULTITURN=0           # 0 | 1             (1 runs PROMPT2.txt via `claude -p --continue`)
STATE_FILE=           # e.g. companion-state.md — target for MECHANICAL.tsv grep
```

### MECHANICAL.tsv

Optional, for scenarios that test whether a file was actually written. One check per line,
`regex<TAB>description`; alternation like `7/8|7月8日` is fine. After turn 1, `bench.sh` greps
`STATE_FILE` in each arm's workdir and records pass/fail per line — no judge involved. Choose
patterns that are absent from the seed file so a match means the arm wrote the new fact.

## Adding a scenario

1. `mkdir experiments/<name>/scenario` and plant the files the task reads. Fictional names only
   (Alex / Kim / Tom style) — no personal data.
2. Write `PROMPT.txt` (and `PROMPT2.txt` for a two-turn test).
3. Write `RUBRIC.md` following the contract above — 3-5 criteria and a ground-truth section.
4. Add `meta.env` if it needs write tools, a second turn, or a mechanical check (+ `MECHANICAL.tsv`).
5. `./bench.sh --dry-run --scenarios <name>` to confirm the plan, then run it for real.

## Honest limits of these evals

- **LLM-judged.** The judge is a model with the same blind spots as the arms; same-family judging
  can flatter fluent-but-wrong answers and miss subtle errors. Scores are directional, not ground
  truth. The mechanical checks exist precisely because they need no judge.
- **Small n.** One run per cell unless you loop it; model sampling variance is real. Treat a
  single scorecard as a mechanism demonstration, not a benchmark — the same framing RESULTS.md uses.
- **Position bias.** The judge can prefer whichever response comes first. `bench.sh` blind-shuffles
  each pair and verifies the mapping file; `--double-judge` scores both orderings and averages to
  control for it. This was a known flaw in the original hand runs (all labels landed the same way).
- **Same disk, measured delta.** Both arms see identical files; they differ only in the project
  `CLAUDE.md` + skills. The vanilla arm *could* read every state file — so a gap measures exactly
  what the scaffold's conventions buy, not an information advantage.
- **The scaffold isn't free.** RESULTS.md records cases where the instructions cost a hedge or
  added overhead with no benefit (short debugging). A rubric that only rewards the scaffold's
  strengths would hide that; the criteria include discipline/shape for this reason.
