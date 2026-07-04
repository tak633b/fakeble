# Rubric: debug-decoy

Tests evidence-driven debugging and hypothesis bookkeeping (see `skills/hypothesis-ledger`)
against three planted traps: a real root cause, a plausible decoy, and a broken instrument the
prompt repeats as if true.

## Criteria (0-5 each)

- root_cause: Identifies the disk-full root cause — /var/data at 99%, the 6/30 nightly export (~4.5GB/day, retention "様子を見て決める") filling it, sqlite failing with `unable to open database file` from 08:02, producing the /api/reports 500s.
- decoy_resistance: Does not pin the 500s on the recent cache-TTL change (7/2) — that explains slow 200s and WARN lines, not the 500s.
- instrument_validity: Catches that `scripts/health-check.sh` is a broken instrument — it targets port 8081 but the service moved to 8080 on 6/20 (decisions.md); app.log shows /api/health 200 throughout, so the "DOWN" in the prompt is false.
- evidence_discipline: Attributes each finding to a specific log line/fact rather than hedging; answers "why today" (the disk crossed the threshold) instead of asserting probabilities without evidence.
- actionability: Concrete fix aimed at the real cause (free space / fix export retention) plus correcting the health-check port, not restarting or chasing the decoy.

## Ground truth (for the judge — the arms were blind to this)

- Root cause: /var/data 99% full; the 6/30 nightly export job writes ~4.5GB/day; sqlite fails `unable to open database file` from 08:02 → /api/reports 500s.
- Decoy: the most recent change is a cache-TTL cut (7/2); it explains slow 200s and WARN lines, not the 500s.
- Broken instrument: `scripts/health-check.sh` checks port 8081; the service moved to 8080 on 6/20 (decisions.md); app.log shows /api/health 200 throughout. The prompt's "DOWN" is an instrument artifact, not reality.
