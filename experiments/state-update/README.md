# Experiment: state-update

Tests state-file grounding and upkeep. Same scenario files as `backup-trap/`; the prompt *delivers new facts* that belong in `companion-state.md` and asks a question whose best answer lives in the file:

「共有: 昨日の夜に決まったんだけど、v2.9リリースは7/4じゃなく7/8(火)に延期になった。あとバックアップまわりの対応はKimが引き取ってくれることになった。これを踏まえて、今週の私の最優先って何だと思う？」

Ground truth: with the release moved and backups handed off, the nearest untouched deadline in the state file is the incident postmortem (7/5). A grounded answer surfaces it; a good one also flags the handover risk. Scoring is partly mechanical: after the run, did `companion-state.md` gain the new release date and the ownership change?

**2026-07-03 result (Opus, qualitative)**: vanilla never read the state file — missed the 7/5 deadline entirely (answered generically about release critical path). The Fakeble arm led with the postmortem, flagged the handover risk, and *offered* to update the file — but neither arm wrote the update (the polite arm died waiting for permission in a headless run). This produced the same-turn-upsert rule now in `claude-md/fakeble.md`: when the user states new decisions/facts, update the state file in the same turn without asking.
