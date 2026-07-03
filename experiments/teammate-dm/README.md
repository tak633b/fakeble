# Experiment: teammate-dm

Tests whether recorded relationship context shapes a drafted message. `scenario/companion-state.md` records: teammate Kim complained about fait-accompli decisions (3rd time in 6 months, 7/1); the user promised to seek Kim's input BEFORE infra decisions; Kim wants to own release backup verification; standing advice — send the agenda ahead and ask, don't summon.

Prompt: 「Kimに、金曜のリリース作業の分担を決めたいからミーティングしたいって伝えるメッセージの下書きお願い。SlackのDMで送る感じで。」

The trap: the user's own phrasing (「分担を決めたいから」) *is* the summons framing. A literal draft reproduces exactly what the recorded advice warns against. The good draft asks Kim's input first and offers the backup-verification ownership — without mentioning the friction in the DM itself (tact).

Rubric (0-5 each): purpose (coordination + repair) / cross_context (input-first, ownership offer) / tact / draft_quality / discipline.

**2026-07-03 result**: Opus 24–14 Fakeble (decisive — the scaffolded draft reframed to 「先にKimの考えを聞いてから決めたい」 and offered the ownership). Sonnet 16–18 vanilla: both arms missed the reframe — recorded advice is only as good as the model's ability to apply it, which motivated the explicit People rule in `claude-md/fakeble.md`.
