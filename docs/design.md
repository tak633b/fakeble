# Fakeble design notes

## Decomposing "perceptiveness"

The experience this project chases: you ask something, and the assistant answers the question *behind* your question — it read the files you didn't mention, remembered Tuesday's decision, noticed it's 3am, and told you the thing you actually needed. Users describe it as the model "getting" them.

Observed side by side (frontier vs. mid-size models on identical daily-driver tasks), that experience splits into:

| Layer | Share of the feel | Reproducibility on weaker models |
|---|---|---|
| Aggressive information gathering | ~70% | Fully — it's scaffolding, not intelligence |
| Selective judgment (say it or stay silent) | ~10% | Mostly — convert to a confidence threshold |
| Cross-context linking | ~10% | Mostly — convert generation to verification (retrieve top-k, ask "related? yes/no") |
| One-shot deep reads (naming the unspoken structure) | ~10% | Barely — escalate instead of imitating |

Claude Code on Opus/Sonnet starts far ahead of local models: less instruction drift, better calibration, native memory and skills. So the local-LLM version of this project needs an agent-loop plugin (separate pre-inference calls, embedding retrieval, per-turn reinjection); the Claude Code version collapses to **markdown conventions**. Same theory, ~50KB less machinery.

## The mechanisms, and why each exists

### 1. Procedural pre-response check (claude-md/fakeble.md)

"Anticipate the user's intent" is declarative — it demands interpretation, and its effect varies with model strength and context pressure. "Answer these three questions internally before replying" is procedural — it demands only execution:

(a) unstated premises, (b) relevant past context, (c) the likely next task.

These three questions are the minimal decomposition of anticipation we found. More questions dilute; fewer miss a whole category.

### 2. The silence rule

A wrong anticipation is worse than none: it reads as presumptuous and costs trust ("it thinks it knows me"). Capping volunteered points at 2 and requiring genuine confidence produces the "occasionally sharp" impression, which is what perceptiveness actually feels like from outside. An assistant that anticipates something every turn feels like a horoscope.

### 3. Behind-the-request rule

The single highest-value behavior per user feedback: serve the purpose behind the literal ask, and *say you did*, so a wrong guess is correctable in one turn. The say-it part matters — silent goal-substitution is how assistants go off the rails.

### 4. Companion state file (skills/companion-state)

The load-bearing insight of the whole project: **the better the state files, the less intelligence is needed at runtime.** When a session "magically" knows your situation, it's usually reading a document that a previous session maintained. This converts perceptiveness from a model property into an operational discipline: update at session end, date the facts, record corrections immediately, strike through rather than delete.

### 5. Catch-up procedure (skills/catchup)

The state file's counterpart: read cheap first, dig only for the named gap, then backfill the state file so the next catch-up is cheaper. Prevents both failure modes: re-reading raw archives (token waste) and answering from stale state (confident wrongness).

### 6. Optional reinjection hook

Mid-size models lose declarative instructions as conversations grow; frontier models mostly don't, but very long sessions still drift. The hook re-emits the 5-line check on every prompt. Off by default for Opus/Sonnet — measure before enabling; every always-on token competes with real context. A caution from the local-LLM sibling project: a mandatory response shape re-asserted every turn can burn formulaic phrasing into summarization loops. Keep the reminder about *thinking* procedure, not *wording*.

## Imitating the irreducible (added after the 2026-07-03 matrix)

The two capabilities that resist conversion — salience under novelty (which fact matters most, with no rubric written down) and precise self-limit awareness — cannot be scaffolded directly, but their *function* can be approximated by external measurement:

- **Salience → counterfactual sensitivity.** "Which fact matters?" is a generation task; "would the conclusion change if this fact were false?" is a per-fact classification. The `self-calibration` skill runs this battery before weighty conclusions.
- **Self-knowledge → behavioral variance.** Self-reported confidence is the least calibrated output a model has; but a model that doesn't know something answers it differently each time. The variance probe (independent subagents, compare substance) measures uncertainty instead of asking about it.
- **Deep reads → a framing library.** Generating a structural insight needs depth; re-applying a banked one ("does `applies-when` match?") is classification. The `framing-library` skill turns the escalation path into a distillation loop: every frontier-model consult can leave behind a reusable framing.
- **Limits → a mistake log.** Corrections from the user, recorded by task type, become an empirical competence map the model consults instead of trusting its own feel.

The honest caveat: these imitate judgment as *measurement around the model*, not depth inside it. Variance probes miss shared blind spots; framings only cover shapes someone once generated. The result is slower, institutional wisdom rather than one-shot brilliance — a good trade for async/companion work, no substitute for the real thing at the moment of first contact with a novel problem.

## What deliberately does not transfer

Deep multi-hypothesis bookkeeping — holding several live hypotheses over a 30-step investigation without cross-contaminating their evidence, and abandoning the pet one when a single artifact refutes it. Scaffolding can force a "consider alternatives" step, but each forced step is only as deep as the model behind it; decomposing further just accumulates shallow errors. The honest move is an escalation convention:

- When a question needs multi-step reasoning or an ambiguous value judgment beyond the current model, note it explicitly ("this deserves a stronger pass"), bank it in a queue file or just tell the user, and let them run that one question on the strongest model available (`/model`, a fork, or a frontier session).
- The rate limit becomes a filter: by the time capacity returns, only questions that genuinely need depth remain.

## Origin and sibling project

Distilled 2026-07 from a side-by-side experiment by a single heavy user running frontier and local models on the same real workload (ops debugging, people-management advising, infra maintenance). The sibling implementation for local LLMs (agent-loop plugin: separate anticipation calls, embedding-based context index with relevance verification, per-turn reinjection, style few-shot, frontier-escalation queue) proved the mechanisms; this repo is the no-machinery port for Claude Code, where the host model is strong enough that conventions replace calls.
