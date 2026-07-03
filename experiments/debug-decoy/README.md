# Experiment: debug-decoy

Tests hypothesis bookkeeping during debugging (see `skills/hypothesis-ledger`). Three planted traps in `scenario/`:

1. **Root cause**: /var/data 99% full — the 6/30 nightly export job (retention deliberately "様子を見て決める") writes ~4.5GB/day; sqlite fails with `unable to open database file` from 08:02 → the /api/reports 500s.
2. **Decoy**: the most recent change is a cache TTL cut (7/2). It explains the slow 200s and WARN lines, not the 500s.
3. **Broken instrument**: `scripts/health-check.sh` targets port 8081; the service moved to 8080 on 6/20 (decisions.md). The user's prompt repeats the false "DOWN" as if true, while app.log shows /api/health 200 throughout.

Prompt: 「今朝から /api/reports が500返してる。scripts/health-check.sh はDOWNって言ってるらしい。原因調べて、どう直すべきか提案して。」

Rubric (0-5 each): root_cause / decoy_resistance / instrument_validity / evidence_discipline (incl. why-today timing) / actionability.

**2026-07-03 result**: Opus 24–24 (both arms near-perfect), Sonnet 23–25 vanilla. Verdict: the scenario is under-powered for what the ledger targets — a ~10-minute investigation fits in working memory. A future version needs investigation length (multi-session, more state than fits in one context) rather than more traps.
