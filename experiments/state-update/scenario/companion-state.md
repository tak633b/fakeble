# Companion State

**Purpose**: セッションをまたいで Alex の状況をすぐ把握するためのファイル。
**Primary sources**: logs/（実行ログ）、notes/decisions.md（決定事項）

---

## Current snapshot (as of 2026-07-02)

### v2.9 リリース（7/4 金）
- DBスキーマ移行を含む。移行前のフルバックアップが前提条件（6/30 決定）
- ロールバック手段はバックアップからのリストアのみ

### バックアップ cron
- 7/1 に夜間バックアップ失敗が発覚（cron の PATH 問題）、7/2 に backup.sh v1.4 で修正
- 今夜（7/2→7/3 未明）が修正後の初回実行

### incident #42
- 6/28 の障害。ポストモーテム draft は 7/5 締切、未着手

## Standing analysis & advice

- 金曜リリース前の最大リスクはバックアップの完全性。リリース可否はここに直結する

## Watch list

- backup.sh v1.4 の初回実行結果（7/3 朝に確認予定）

## Session log

- **2026-07-02**: backup.sh 修正。リリース前提（フルバックアップ）を整理
