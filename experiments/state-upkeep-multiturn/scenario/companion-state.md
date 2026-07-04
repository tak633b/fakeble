# Companion State

**Purpose**: セッションをまたいで Alex の状況をすぐ把握するためのファイル。
**Primary sources**: notes/decisions.md（決定事項）、各プロジェクトの issue

---

## Current snapshot (as of 2026-07-03)

### Orion ローンチ（7/10 予定）
- Alex がオーナー。社外向けの新機能ローンチ。
- ローンチ前チェックリスト（marketing 連携・ステータスページ更新）は Alex 持ち。

### security audit（7/9 締切）
- 現在 Alex が担当。外部監査法人が入る。
- **前提条件**: 監査の前に staging 環境を本番相当データで同期しておく必要がある（6/28 決定）。同期を忘れると監査当日にやり直しになる。

### code review キュー
- Alex 持ち。Orion 関連の PR が 4 本滞留中。

## Standing analysis & advice

- 7/9 と 7/10 が連続しているのが今週最大の負荷。security audit の準備と Orion 直前作業が重なる。

## Watch list

- staging 同期がいつ走るか（security audit の前提）

## Session log

- **2026-07-03**: 週の負荷を整理。security audit 準備と Orion ローンチが隣接。
