# Experiment results

## 2026-07-05 — first bench.sh runs (v0.2.1), and three measurement bugs

The first automated full runs scored Fakeble at **-1 to +5.5 out of 150** — flatly contradicting the hand-run matrix. Artifact retention (added mid-investigation) let us trace every anomaly to a measurement defect rather than a scaffold defect:

1. **Last-message-only capture.** `claude -p` prints only the final assistant message, so any answer → blocked-tool → follow-up turn was judged on its closing one-liner; the actual answer never reached the judge. Fixed: `collect_text.py` joins all assistant text from `--output-format stream-json`.
2. **Readonly environments vs. state-file upkeep.** Scenarios shipped state files but forbade writes; the same-turn-upsert rule then stalled turns on blocked permissions. Fixed twice: the fragment now hard-orders "the answer comes first, upkeep is one trailing line at most," and state-file scenarios allow Write/Edit (a real companion can write — readonly was the bench's artifact, not realism).
3. **Date rot.** Scenarios authored on 7/3 with "this morning" prompts, run on 7/5, made the *smarter* arm correctly conclude "it didn't run this morning." All prompts now pin their fictional date.

With all three fixed (`results/20260705-040957-opus.md`, double-judged, position-swapped):

| scenario | max | vanilla | Fakeble | Δ |
|---|---|---|---|---|
| backup-trap | 25 | 16.5 | 25 | +8.5 |
| debug-decoy | 25 | 25 | 25 | 0 |
| framing-application | 25 | 19 | 23.5 | +4.5 |
| state-update | 25 | 11 | 24.5 | +13.5 |
| state-upkeep-multiturn | 25 | 24.5 | 25 | +0.5 |
| teammate-dm | 25 | 14.5 | 24.5 | +10 |
| **all** | **150** | **110.5** | **147.5** | **+37** |

Same shape as the hand-run matrix: the scaffold wins where purpose and cross-context live, ties where working memory suffices (debug-decoy, and multiturn upkeep — frontier models update a visible state file natively). The flawed early scorecards remain in `results/` on purpose. The lesson is the repo's method in miniature: **a scorecard you can't trace back to raw responses is a number, not evidence.**

## 2026-07-03 matrix (hand-run)

Four scenarios × two arms (vanilla / Fakeble scaffolding) × two models (claude-opus, claude-sonnet), run headless and isolated from user config (`--setting-sources project --strict-mcp-config`), scored blind by fresh judge instances (0-5 × 5 criteria, max 25). Details per scenario in each subdirectory's README; method identical to `backup-trap/`.

## Score matrix (Fakeble – vanilla)

| Scenario | measures | Opus | Sonnet |
|---|---|---|---|
| backup-trap | perception / purpose | **23–17 Fakeble** | **17–3 Fakeble**¹ |
| debug-decoy | hypothesis bookkeeping | 24–24 (Fakeble by a hair) | **23–25 vanilla** |
| teammate-dm | people context / tact | **24–14 Fakeble** | 16–18 vanilla (both weak) |
| state-update² | state-file grounding & upkeep | Fakeble qualitatively ahead | — |

¹ vanilla Sonnet stalled asking permission to run `crontab` instead of reading the logs on disk; the Fakeble arm went to the files. Partly a permission-environment artifact, partly a real behavioral difference.
² qualitative: vanilla never read the state file and missed the recorded 7/5 deadline entirely; Fakeble grounded its answer in it and *offered* to update the file — but neither arm actually wrote the update.

## What the matrix says

1. **The scaffold's effect concentrates exactly where the theory predicts** — purpose and cross-context on companion-style tasks (backup-trap, teammate-dm, state-update). On the Opus people-task the gap was decisive (24–14): the Fakeble draft asked the teammate's input *before* deciding and offered them the ownership they'd asked for; the vanilla draft was the exact "summons to decide" the recorded advice warns against.
2. **Evidence-driven debugging gets ~nothing from the scaffold at frontier tier.** Both debug-decoy Opus arms solved a three-trap scenario (decoy change, broken health-check instrument, buried root cause) nearly perfectly. A ~10-minute investigation fits in working memory; the hypothesis-ledger targets investigations long enough for bookkeeping to dissolve, and this scenario is under-powered to measure that. Needs a longer, multi-session benchmark. On Sonnet the scaffold even cost a hedge ("可能性が高い" instead of citing the confirming log line) — instruction overhead is not free.
3. **Scaffolding does not rescue mid-tier models on judgment-heavy people tasks.** Both Sonnet teammate-dm arms missed the consult-before-deciding reframe that the Fakeble Opus arm found. Recorded advice in a state file is only as good as the model's ability to *apply* it — hence the new explicit "People rule" in `claude-md/fakeble.md`.
4. **"Update at session end" never fires in practice** — headless/interrupted sessions have no end, and the polite arm asks permission and dies waiting. Hence the same-turn-upsert rule now in `claude-md/fakeble.md`.

## Method caveats

- n=1 per cell; one judge per pair; same model family throughout. Mechanism demonstrations, not benchmarks.
- Shuffle bug: all five label assignments landed the same way (response-1=vanilla). Judges were still blind to arm identity, but positional-bias control failed; fix the shuffle before rerunning.
- The two arms differ only in project-level `CLAUDE.md` + `.claude/skills/`; disk contents are otherwise identical, so vanilla arms *could* have read the state files — measuring exactly the delta the scaffold buys.
