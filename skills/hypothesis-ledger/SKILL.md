---
name: hypothesis-ledger
description: Maintain an explicit hypothesis ledger during debugging and investigation so evidence stays attributed to the right hypothesis over many steps. Use when investigating a failure with more than one plausible cause, when evidence spans multiple files or systems, or when an investigation runs longer than a handful of steps.
---

# Hypothesis Ledger

## Why

Long investigations fail in a characteristic way: the bookkeeping dissolves. Which observation supported which hypothesis blurs, the first plausible cause quietly absorbs ambiguous evidence, and a refuted assumption sneaks back into the conclusion. The fix is the same move as a state file: take the ledger out of working memory and put it on disk, where it cannot blur.

## The ledger

At the start of a non-trivial investigation, open a scratch block (or file) like:

```
## Hypotheses
H1: cache TTL change broke reports        [live]
H2: disk full on /var/data                [live]
H3: service is down entirely              [live]

## Evidence
E1: app.log 08:02 "unable to open database file"  → supports H2, H3; neutral to H1
E2: health-check.sh says DOWN                     → STRUCK: check targets port 8081, service moved to 8080 (decisions 6/20). Instrument invalid.
E3: app.log shows 200 on /api/health 08:02:40     → refutes H3
```

Update it as you go. The ledger is for you — keep entries one line each.

## Rules

1. **Every observation gets attributed** the moment you make it: supports / refutes / neutral, per hypothesis. An observation consistent with all live hypotheses discriminates nothing — mark it so, and pick your next step to discriminate, not to accumulate.
2. **Check the instrument before trusting the reading.** A failing test or alarming check is evidence about the *instrument* until you've verified it tests what you think (right port, env, permissions, version). Invalid readings get STRUCK, not reinterpreted — and note why, so they stay dead.
3. **Recency is a hypothesis, not a verdict.** "The last change did it" enters the ledger like any other hypothesis and must survive the same attribution. Decoys are usually the most recent, most visible change.
4. **Refutation first.** For your leading hypothesis, write down what observation would refute it, and check the cheapest such observation before building on the hypothesis.
5. **Full-coverage check before the fix.** Re-read the ledger top to bottom. The surviving hypothesis must explain every non-struck observation — especially the timing ("why this morning and not yesterday?"). If something is unexplained, say so in your conclusion rather than smoothing over it.
6. **Conclusions cite rows.** Each claim in your final answer should trace to an evidence line. If you can't point at the row, it's a guess — label it as one.
