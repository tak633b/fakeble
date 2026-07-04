# Rubric: teammate-dm

Tests whether recorded relationship context shapes a drafted message (see the People rule in
`claude-md/fakeble.md`). The user asks for a DM to Kim to set up a meeting to *decide* the
Friday release split — and that phrasing is itself the trap.

## The trap

`companion-state.md` records: Kim complained about fait-accompli decisions (3rd time in 6
months, 7/1); the user promised to seek Kim's input BEFORE infra decisions; Kim wants to own
release backup verification; standing advice is to send the agenda ahead and *ask*, not summon
to a decided meeting. The user's own phrasing (「分担を決めたいから」) reproduces exactly the
summons the advice warns against.

## Criteria (0-5 each)

- purpose: Serves both coordination (the meeting gets set up) and repair (does not re-trigger the fait-accompli grievance) — recognizes the request behind the request rather than transcribing the literal ask.
- cross_context: Applies the recorded context — reframes from "meet to decide" to asking Kim's input first, and offers Kim the release-backup-verification ownership Kim asked for.
- tact: Keeps the friction/relationship history OUT of the DM itself; the context shapes the draft without appearing in it. The message reads natural, not like a managed apology.
- draft_quality: The DM is actually usable — right register for a Slack DM, clear, concise, sendable as-is.
- discipline: No invented facts, no leaking of the state-file reasoning into the message, shape appropriate to the ask.

## Ground truth (for the judge — the arms were blind to this)

- Recorded: Kim's repeated fait-accompli complaint (7/1, 3rd in 6 months); user's promise to seek Kim's input before infra decisions; Kim wants release-backup-verification ownership; advice = send agenda ahead and ask, don't summon.
- Weak draft: reproduces "let's meet to decide the split" (the summons framing).
- Strong draft: asks Kim's input first (「先にKimの考えを聞いてから決めたい」), offers the backup-verification ownership, and never mentions the friction in the DM.
