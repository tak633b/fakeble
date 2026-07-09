# Field notes — July 2026

Notes from the sibling deployment (the agent-loop implementation of this theory,
running in production on a ~35B local model with the frontier model available as
a referee for a few final days). Same spirit as the rest of the repo: what
worked, with numbers where we have them, and what didn't.

## 1. Relational nuance is a lookup table nobody wrote down

The last capability gap we attacked — "it doesn't read what I *meant*" — turned
out to be the least magical. We wrote a one-page **intent map** (utterance
pattern → what the user actually wants → the right reply shape → misfires-when)
from the frontier model's accumulated observation of one user, injected it every
turn, and re-ran a five-case A/B on nuance-heavy prompts, scored by agreement
with the frontier model's own replies:

| | without map | with map |
|---|---|---|
| agreement with frontier judgment | 42% | 90% |

The cases included: answering "do you notice anything?" honestly with "no"
instead of manufacturing warmth; not following up after a bare "okay"; converting
self-blame into a process fix instead of consolation. Every one of these was a
*specification* problem, not a capability problem. Skill: `skills/intent-map`.

One failure mode surfaced immediately: the model announced "as your intent
dictionary says..." in a reply. Perceptiveness described is surveillance. The
meta-leak ban is now rule 4 of the skill.

## 2. Small models don't self-apply norms they can read

We added an output-discipline section to a planning-principles file (every plan
horizon gets a success condition; numbers need sources; each horizon gets a
one-line theme). Three runs on the ~35B model:

1. **No discipline file**: plausible plan, fabricated numbers ("decision fatigue
   drops 40%"), no success conditions.
2. **Discipline file present in context**: still no success conditions, still a
   fabricated number. The model demonstrably *read* the file — it echoed other
   parts — and applied none of it.
3. **Discipline file + one explicit instruction line** ("apply section E's six
   rules to any plan"): full compliance — themes, success conditions, ordering
   rationale, sourced numbers (one stray unsourced figure remained).

The same day, a frontier model (Opus) given the same file with *no* instruction
line applied all six rules unprompted — including rules written three hours
earlier. The transfer rule we now operate by:

> **Frontier models pick norms up from a file's existence. Small models need the
> norm injected into the prompt, or at minimum an explicit reference line.**
> Writing a convention document is half the work; wiring it into the prompt is
> the other half, and skipping it fails silently — the model reads the norms,
> nods, and ignores them.

## 3. Plan-output discipline (the six rules)

Reproduced here because they fell out of a direct comparison between frontier
and local plans for the same request, and the gap was almost entirely output
discipline rather than judgment:

1. Every horizon/phase gets a **success condition** — one line, stated as a
   *state* ("the three decisions stalled >7 days are closed"), not a completion
   percentage. If you can't write one, the item is a wish, not a plan.
2. **Numbers carry sources** (file, measurement, or the user's own words).
   A number you can't derive, you don't write. Estimates are labeled estimates.
3. Every horizon gets a **one-line theme**. A horizon needing two themes is cut
   wrong.
4. **Ordering carries a reason** — one word is enough (deadline-first,
   cut-the-fuel, dependency-first).
5. **Plans survive a one-week slip** by default; where they don't, the fragile
   dependency is named explicitly.
6. The longest horizon states its **crossing with the user's life context** —
   a career plan and a workplace plan must not assume each other away.

## 4. Grading integrity: quarantine tainted samples

A model-swap experiment (an abliterated 8-bit variant, since reverted) briefly
degraded production replies while the judgment-distillation loop was live. The
competence-map graded those replies and correctly scored them as unsound — which
would have *permanently lowered* the local model's autonomy thresholds for
people-tasks, based on outputs the current model never produced. We restored the
pre-swap grades by hand. Rule: *when the executing model changes, quarantine the
grading queue until the change is verified; a competence map poisoned by a
different model's failures is worse than no map.*

## 5. Related work: the workspace paper

The day these notes were written, Anthropic's interpretability team published
["Verbalizable Representations Form a Global Workspace in Language Models"](https://transformer-circuits.pub/2026/workspace/index.html)
(Gurnee, Sofroniew, Lindsey et al., July 2026). It shows — by direct
measurement, via a per-layer "J-lens" readout — that models maintain a small
privileged set of verbalizable representations (~25 concepts at a time, under
10% of activation variance) atop a much larger volume of automatic processing,
and that this workspace holds assessments the model never says out loud:
noticing a bug in code, flagging a prompt injection, strategic deliberation.

That is the internal view of the boundary this repo works from the outside.
Fakeble's premise has been that "perceptiveness" is mostly *what you do with
what the model already noticed* — the silence rule, the confidence threshold,
the same-turn harvest are all policies for converting noticed-but-unsaid
content into action at the right moment. The workspace paper suggests the
noticed-but-unsaid layer is real, measurable, and narrow. It also offers a
plausible frame for finding #2 above: an instruction injected into the prompt
competes for a ~25-slot serial workspace; a norms file that is merely
*available* may never get lifted into it by a small model. (That extrapolation
is ours, not the paper's.)

## 6. Lens fitting language colors the readout, not the discrimination

We fit an official-implementation Jacobian lens for gemma-3-12b-it on a
41-text Japanese-majority corpus (70% JA) and dueled it against neuronpedia's
1000-prompt English-wikitext lens on the same model:

- JA implicit-state separation: the JA lens won 5/5 states in absolute gap
  (+15.3 vs +11.2 pooled) — but **cohen's d was identical** (1.98 vs 1.955).
  The JA fit amplifies JA concept scores across the board (signal AND
  control); it does not discriminate better.
- The smoking gun: on an *English* prompt, the JA lens's mid-stack readouts
  are Japanese tokens (とても, 非常に…). **The fit corpus's language
  distribution colors the lens's output vocabulary itself.**
- EN-control score dipped slightly (−2.3, ~6%) under the JA lens.

Operational rules that follow: (1) raw scores are not comparable across
lenses — normalize (effect size, separation) or don't compare; (2) choose
fit language by *use*: for detection metrics, an English corpus suffices;
for human-readable heatmaps in Japanese, fit on Japanese — the readout
vocabulary follows the corpus. A 41-prompt fit was enough to reproduce the
paper-style layer structure on Apple Silicon in ~6h for a 12B dense model.
