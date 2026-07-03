# Fakeble

Make Claude Code on Opus/Sonnet behave more like Fable — the perceptive, anticipating, "somehow it just gets me" experience — using nothing but scaffolding: a CLAUDE.md fragment, two skills, an optional hook, and a state-file convention.

No API keys, no servers, no dependencies. Everything here is plain markdown and one optional settings snippet.

## The idea

What feels like "perceptiveness" in a frontier model decomposes into two parts:

1. **Aggressive information gathering** (~70%) — reading files you didn't ask it to read, recalling past context, noticing what's on disk. This is *entirely* reproducible with scaffolding: curated state files, memory conventions, and a catch-up procedure.
2. **Depth of judgment** (~30%) — knowing which thread to pull, holding multiple hypotheses without confusing their evidence. Partially reproducible: a procedural pre-response check converts "be perceptive" (interpretation) into "answer these 3 questions" (execution), and a conservative confidence rule converts wrong guesses into silence.

Fakeble packages the reproducible parts:

| Piece | What it does | Install target |
|---|---|---|
| `claude-md/fakeble.md` | Procedural pre-response check + silence rule + response shape | append to `~/.claude/CLAUDE.md` |
| `skills/companion-state` | Teaches the model to maintain a curated state file about you / your project | `~/.claude/skills/` |
| `skills/catchup` | Low-token session catch-up: state file first, primary sources only when needed | `~/.claude/skills/` |
| `hooks/reinjection` | Optional: re-inject the check every turn (for models that drift in long sessions) | `~/.claude/settings.json` |
| `templates/` | Starting points for the state file and a style few-shot file | your project |

## Install

```bash
./install.sh            # copies skills, appends the CLAUDE.md fragment (with your confirmation)
```

Or manually: copy `skills/*` into `~/.claude/skills/`, and append `claude-md/fakeble.md` to your `~/.claude/CLAUDE.md`.

## The three rules that matter most

If you take nothing else from this repo:

1. **Procedural beats declarative.** "Anticipate the user's intent" asks for interpretation. "Before replying, answer internally: (a) what's the unstated premise, (b) what past context is relevant, (c) what comes next" asks only for execution. The capability gap matters much less.
2. **Silence beats a wrong guess.** Weave in at most 2 anticipated points, and only those you're confident about. A wrong anticipation is worse than none — it reads as presumptuous, not perceptive.
3. **The better your state files, the less intelligence is needed at runtime.** Most of what feels like mind-reading is a well-maintained `companion-state.md` being read at the right moment. Curate it; have the model update it at the end of every session.

## Origin

Born from a side-by-side experiment: the same user ran Fable 5 and local/smaller models on identical daily-driver tasks, then distilled what actually produced the "it gets me" feeling into mechanisms. A sibling project implements the same ideas as an agent-loop plugin for local LLMs; this repo is the zero-dependency distillation for Claude Code + Opus/Sonnet.

See [docs/design.md](docs/design.md) for the full reasoning, including what does *not* transfer (deep multi-hypothesis bookkeeping) and the escalation convention for it.

## 日本語での概要

Fable 5 の「察してくれる」体験のうち、足場（スキャフォールディング）で再現できる部分を Claude Code (Opus/Sonnet) 向けに抽出したセットです。中身は CLAUDE.md 断片＋スキル2つ＋任意のフック＋状態ファイル運用の規約だけで、依存もサーバーも不要。核は3つ: 宣言ではなく手続きで指示する／外すくらいなら黙る／状態ファイルの手入れが実行時の知能を代替する。詳細は docs/design.md へ。

## License

MIT
