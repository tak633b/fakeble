---
name: catchup
description: Catch up on the user's ongoing situation at minimum token cost - state file first, primary sources only for what the state file cannot answer. Use at the start of a session when the user references ongoing work ("where were we", "you probably know my situation", "continue from last time") or asks for advice that depends on context from previous sessions.
---

# Catch-up

## Procedure

1. **State file first.** Read `companion-state.md` (see companion-state skill). For most questions this is sufficient — answer from it and say so briefly.
2. **Identify the gap, not the archive.** If the question needs something the state file lacks, name precisely what's missing ("what happened after 7/2", "the exact wording of that email") and read only the primary source that answers it. The state file's "Purpose & sources" section says where primary sources live.
3. **Targeted extraction over bulk reading.** Prefer one filtered query (grep by date, SQL with a WHERE clause, last-N-messages extraction) over reading whole logs. When a source is large, extract to a scratch file and read the extract.
4. **Close the loop.** Whatever you learned from primary sources that the state file should have known — add it. The next catch-up should be cheaper than this one.

## Anti-patterns

- Re-reading raw transcripts when the state file already answers the question.
- Answering from a stale state file without checking dates on time-sensitive facts. If a snapshot entry is older than the events it predicts, verify against the primary source first.
- Silently guessing. If neither the state file nor a quick primary lookup resolves an ambiguity that changes your answer, ask the user — one precise question beats a wrong assumption.
