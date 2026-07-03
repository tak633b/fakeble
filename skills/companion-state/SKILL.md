---
name: companion-state
description: Create and maintain a curated state file (companion-state.md) that lets any future session catch up on the user's ongoing situation in a few hundred tokens. Use when starting long-running advisory/companion work with a user, when the user asks to "remember my situation across sessions", or at the end of a substantial session to record what changed.
---

# Companion State

## Why

Most of what feels like a model "just knowing you" is a well-maintained state file being read at the right moment. This skill defines that file: one curated document holding the user's current situation, your standing analysis, and a log — so a fresh session reaches full context for a few hundred tokens instead of re-reading raw history.

## The file

Default location: `companion-state.md` in the project root (or the user's preferred notes directory). Use the template at `templates/companion-state.template.md` if starting fresh. Structure:

1. **Purpose & sources** — what this file is for, where the primary sources live (logs, transcripts, databases) for the rare cases you must dig deeper.
2. **Current snapshot** — the user's live situation, one short block per thread. Facts with dates. Strike through resolved items rather than deleting them immediately (`~~sent 7/3~~ → resolved`) so trajectory stays visible.
3. **Standing analysis & advice** — your current read of the deeper problem, and advice already given. This prevents re-litigating settled discussions.
4. **Watch list** — what to keep a light eye on across sessions.
5. **Session log** — one line per substantial session: date, what changed, what was decided.

## Rules

- **Update at the end of every substantial session.** An out-of-date state file is worse than none — it makes you confidently wrong. Move resolved items, add new threads, append the log line.
- **One level of abstraction up.** Record "what the user is wrestling with", not transcripts of what was said. The snapshot answers "what would a colleague need to know to cover for me today?"
- **Facts get dates.** "Meeting scheduled" rots; "meeting scheduled 2026-07-03, expected within 2 weeks" stays useful.
- **Corrections are gold.** When the user corrects your understanding, the corrected version goes in immediately — that is exactly the knowledge the next session cannot re-derive.
- **Never paste secrets** (credentials, tokens) into the file. Point to where they live instead.
- **Read before advising.** In any session touching the user's ongoing situation, read this file before your first substantive reply. If your conclusions change during the session, the file is stale — fix it.
