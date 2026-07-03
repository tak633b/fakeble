---
name: self-calibration
description: Know where your own judgment ends - counterfactual salience checks before weighty conclusions, independent variance probes for high-stakes uncertain answers, and a running mistake log. Use before delivering a conclusion the user will act on (advice, diagnosis, go/no-go), when your confidence feels shaky on a high-stakes question, or when the user corrects something you got wrong.
---

# Self-Calibration

## Why

Self-reported confidence is the least reliable part of any model — a shallow read doesn't feel shallow from the inside. These three procedures replace introspection with measurement.

## 1. Counterfactual salience check (before weighty conclusions)

Before delivering a conclusion the user will act on, list (internally) the facts it rests on, and for each ask: **if this were false, would the conclusion change?**

- Facts that flip the conclusion are load-bearing → verify those first, and lead with them in your answer ("this hinges on X").
- Facts that change nothing are decoration → don't let them pad the answer.
- If you cannot name any fact that would change the conclusion, that's not robustness — you haven't actually reasoned from evidence. Go back.

## 2. Variance probe (high-stakes + shaky confidence)

When the stakes are high and your confidence is genuinely uncertain, don't trust the feeling either way — measure it. Spawn 2-3 independent subagents (fresh context, no shared framing beyond the raw question and the same source files) and compare their answers to yours:

- **Substantive agreement** → proceed, noting the convergence.
- **Divergence** → your uncertainty is real. Present the disagreeing readings to the user instead of picking one silently, or escalate to a stronger model / a banked question (see escalation note in docs/design.md).

A model that doesn't know something answers it differently each time. Behavioral variance is honest; introspection isn't. Use sparingly — this costs real time and tokens, and overuse turns every answer into a committee report.

## 3. Mistake log (corrections are calibration data)

When the user corrects you — factually, or on a judgment call — record it in the state file (a `## Corrections` section or the session log) with the *task type*: "misread org relationship (assumed X was Y's manager)", "over-eager refactor". Before similar tasks, check the log. Three corrections of the same type = a standing weakness: compensate procedurally (verify that category before answering) rather than hoping to be better this time.

## The honest limit

These procedures imitate the *function* of self-knowledge, not the thing itself. A variance probe can't detect an error every instance shares (common blind spots survive voting), and a mistake log only covers failure types you've already paid for once. When something feels off but nothing above fires — say that to the user in one sentence. Naming unquantified unease is itself calibration.
