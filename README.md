# Fakeble

Scaffolding that makes Claude Code feel more like Fable — the perceptive, anticipating, *"how did it know that's what I meant"* experience — using nothing but markdown: a CLAUDE.md fragment, five skills, an optional hook, and two state-file conventions.

No dependencies, no servers, no API keys. Everything here is plain text you can read in ten minutes.

## The story

This project started at 3 a.m.

I'd been running Fable 5 as a daily companion — not just for code, but for the whole mess of a working life. One night it caught up on my situation from my agents' logs, quietly fixed a broken mail pipeline while we talked, and then said the thing none of my tools had ever said: that the problem wasn't the six open problems, it was that every one of them lived in my head at once — and that it was 3 a.m., and I should go to sleep.

That's the experience this repo chases. And the immediate obstacle was mundane: rate limits and cost. You can't run a frontier model as your always-on companion. So the question became precise: **when Fable feels a class above, what exactly am I paying for — and how much of it can be rebuilt for free?**

I asked Fable itself. Its answer, compressed:

> What reads as "perceptiveness" splits apart under inspection. About 70% is aggressive information gathering — reading the files you didn't mention, recalling Tuesday's decision, noticing what's on disk. That part is not intelligence; it's logistics, and logistics can be scaffolded. Another chunk converts: "is this worth saying?" becomes a confidence threshold, "is this past thing related?" becomes a retrieval-then-verify classification. What genuinely resists conversion is two things: **knowing which fact matters most in a situation nobody wrote a rubric for**, and **knowing precisely where your own judgment ends**.
>
> Scaffolding is for reliably using what you already know. The real thing is for meeting what you don't.

So we built the scaffolding, ran blind A/B experiments (vanilla Claude Code vs. Claude Code + these files, judged by fresh model instances that didn't know which was which), kept what measurably worked, and wrote honest notes on what didn't. A sibling project implements the same theory as an agent-loop plugin for local LLMs; this repo is the zero-machinery distillation for Claude Code, where the host model is strong enough that conventions replace code.

One more line from that conversation, because it's the actual research program here:

> The most interesting finding is that the boundary isn't fixed — it moves as you get better at converting judgment into retrieval and classification. Fakeble is really a survey of that boundary.

## What's in the box

| Piece | What it does | Install target |
|---|---|---|
| `claude-md/fakeble.md` | The behavioral core: procedural pre-response check, silence rule, behind-the-request / decision-consistency / people rules, same-turn state upsert | append to `~/.claude/CLAUDE.md` |
| `skills/companion-state` | Maintain a curated state file so any future session catches up in one read | `~/.claude/skills/` |
| `skills/catchup` | Low-token catch-up: state file first, primary sources only for the named gap | `~/.claude/skills/` |
| `skills/hypothesis-ledger` | Keep evidence attributed to hypotheses during long investigations | `~/.claude/skills/` |
| `skills/framing-library` | Bank named structural insights; re-apply deep judgments by classification | `~/.claude/skills/` |
| `skills/self-calibration` | Counterfactual salience checks, variance probes, a mistake log | `~/.claude/skills/` |
| `hooks/reinjection` | Optional anti-drift reminder for very long sessions (off by default) | `~/.claude/settings.json` |
| `templates/` | Starting points: state file, framings library, style few-shot | your project |
| `experiments/` | Reproducible A/B scenarios, method, and blind-judged results | reference |
| `docs/design.md` | The full theory: what transfers, what converts, what doesn't, and why | reference |

## Install

```bash
git clone https://github.com/tak633b/fakeble && cd fakeble && ./install.sh
```

The installer copies the skills and asks before touching your `CLAUDE.md`. Manual install: copy `skills/*` into `~/.claude/skills/`, append `claude-md/fakeble.md` to your `~/.claude/CLAUDE.md`, and start a state file from `templates/companion-state.template.md`.

## The three rules that matter most

1. **Procedural beats declarative.** "Anticipate the user's intent" demands interpretation; "before replying, answer internally: (a) what's unstated, (b) what past context is relevant, (c) what comes next" demands only execution. The capability gap matters much less.
2. **Silence beats a wrong guess.** Volunteer at most two anticipated points, only when genuinely confident. An assistant that anticipates something every turn feels like a horoscope; "occasionally sharp" is what perceptiveness feels like from outside.
3. **The better your state files, the less intelligence is needed at runtime.** Most of what feels like mind-reading is a well-maintained `companion-state.md` being read at the right moment. Curate it; have the model update it the moment facts change.

## What we measured

Twelve headless runs (four scenarios × two arms × Opus/Sonnet), isolated from user config, blind-judged. Full details in [`experiments/RESULTS.md`](experiments/RESULTS.md). The shape of the result:

- **The scaffold's effect lands exactly where the theory predicts** — on *purpose* and *cross-context* in companion-style tasks. On the people-task with Opus the gap was decisive (24–14): the scaffolded arm asked the teammate's input before deciding and offered them the ownership they'd once asked for; the vanilla arm drafted the exact "summons to a decided meeting" the recorded advice warned against.
- **Short evidence-driven debugging gains ~nothing** (24–24). A ten-minute investigation fits in working memory; the ledger targets investigations long enough for bookkeeping to dissolve.
- **Scaffolding does not rescue a mid-tier model on judgment-heavy people tasks.** Recorded advice is only as good as the model's ability to apply it — which is why the People rule is procedural now.
- **"Update the state file at session end" never fires in real life.** Headless and interrupted sessions have no end; the polite model asks permission and dies waiting. Hence: same-turn upsert, no asking.

Treat all of it as mechanism demonstrations, not benchmarks — n=1 per cell, and the caveats section in RESULTS.md is honest about the flaws.

## What doesn't transfer — and what we do about it

Two capabilities survived every conversion attempt: **salience under novelty** (which of ten true facts matters right now, with no rubric anywhere) and **precise self-limit awareness** (a shallow read doesn't feel shallow from the inside). We don't pretend to scaffold them. We imitate their *function* with measurement: counterfactual sensitivity instead of asking "what matters", behavioral variance probes instead of self-reported confidence, a framing library so that a stronger model's past insights can be re-applied by classification, and an escalation convention so the questions that genuinely need depth get banked for the real thing.

The result is a different kind of intelligence than the one that inspired it — slower, institutional, accumulated rather than instantaneous. For an always-on companion, that trade turns out to be a good one. For the moment of first contact with a genuinely novel problem, there is still no substitute. Both of those sentences are in this repo's spirit: say what works, and say what doesn't.

## 日本語で

これは、Fable 5 を日常の相棒として使っていて何度も感動した「察する能力」——頼んでいないところまで先回りして把握し、質問の裏にある本当の質問に答えてくる体験——を、レート制限とコストの壁を越えて素の Claude Code (Opus/Sonnet) で再現しようとしたプロジェクトです。

出発点は Fable 本人との対話でした。「察し」を分解すると、7割は知能ではなく段取り（読みに行く・思い出す・手入れされた状態ファイル）で、さらに一部は変換で移植できる（「言うべきか」→確信度の閾値、「関係あるか」→検索+検証の分類）。どうしても残るのは2つ——**誰も基準を書いていない状況で何が重要かを見抜く力**と、**自分の判断の限界を精密に知る力**。この2つは移植せず、測定で機能だけ近似する（反事実感度・分散プローブ・フレーミングライブラリ・エスカレーション規約）。

中身は全部 markdown です。CLAUDE.md 断片1つ、スキル5つ、任意のフック1つ、状態ファイルの運用規約。ブラインドA/B実験の結果と限界も experiments/ に正直に書いてあります。核になる設計原則は3つ: **宣言ではなく手続きで指示する／外すくらいなら黙る／状態ファイルの手入れが実行時の知能を代替する**。

ローカルLLM向けの姉妹実装（エージェントループ・プラグイン版)も別途開発中です。

## License

MIT
