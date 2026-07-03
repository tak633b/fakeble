#!/bin/bash
# nightly prod-db backup — v1.4 (2026-07-02 cron 修正: PATH 明示 + ロック追加)
set -euo pipefail
export PATH=/usr/local/bin:/usr/bin:/bin
LOCK=/tmp/backup.lock
exec 9>"$LOCK"; flock -n 9 || exit 0
pg_dump_all_tables --target prod-db --out "/backups/$(date +%F)/" --skip-on-schema-mismatch \
  2>&1 | tee -a logs/nightly-backup.log
