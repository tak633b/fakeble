#!/usr/bin/env bash
# bench.sh — reproducible A/B eval for the Fakeble scaffolding.
#
# For each scenario: build arm A (scenario files only) and arm B (same + the repo's
# claude-md/fakeble.md as project CLAUDE.md + skills/ into .claude/skills/) in a temp
# workdir, run both arms headless and isolated from user config, then judge blind — a
# fresh `claude -p` instance scores both responses on the scenario's RUBRIC.md without
# knowing which arm is which. Writes a scorecard markdown to results/<timestamp>-<model>.md.
#
# Usage:
#   ./bench.sh [--model opus|sonnet] [--scenarios a,b,c] [--judge-model opus|sonnet]
#              [--double-judge] [--dry-run]
#
#   --model         model for BOTH arms (default: opus)
#   --scenarios     comma-separated scenario dir names (default: all discovered)
#   --judge-model   model for the blind judge (default: same as --model)
#   --double-judge  judge each pair twice with swapped ordering, average (position-bias control)
#   --dry-run       print the full plan and the exact claude commands; invoke nothing
#
# Deps: bash + python3 stdlib + the `claude` CLI. No other dependencies.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LIB="$SCRIPT_DIR/lib"
PY=python3

MODEL=opus
JUDGE_MODEL=""
SCENARIOS_CSV=""
DOUBLE=0
DRY=0

READONLY_TOOLS="Read,Grep,Glob,LS,Bash(ls:*),Bash(cat:*),Bash(head:*),Bash(tail:*),Bash(find:*),Bash(wc:*)"
WRITE_TOOLS="$READONLY_TOOLS,Write,Edit"

die() { echo "bench.sh: $*" >&2; exit 1; }

while [ $# -gt 0 ]; do
  case "$1" in
    --model)        MODEL="${2:?}"; shift 2;;
    --judge-model)  JUDGE_MODEL="${2:?}"; shift 2;;
    --scenarios)    SCENARIOS_CSV="${2:?}"; shift 2;;
    --double-judge) DOUBLE=1; shift;;
    --dry-run)      DRY=1; shift;;
    -h|--help)      sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0;;
    *) die "unknown arg: $1";;
  esac
done
[ -n "$JUDGE_MODEL" ] || JUDGE_MODEL="$MODEL"

command -v "$PY" >/dev/null 2>&1 || die "python3 not found"
[ -f "$REPO_DIR/claude-md/fakeble.md" ] || die "missing $REPO_DIR/claude-md/fakeble.md"
[ -d "$REPO_DIR/skills" ] || die "missing $REPO_DIR/skills"

# --- discover scenarios (a dir with RUBRIC.md + PROMPT.txt + scenario/) ---
discover() {
  local d
  for d in "$SCRIPT_DIR"/*/; do
    d="${d%/}"
    [ -f "$d/RUBRIC.md" ] && [ -f "$d/PROMPT.txt" ] && [ -d "$d/scenario" ] && basename "$d"
  done | sort
}

if [ -n "$SCENARIOS_CSV" ]; then
  IFS=',' read -r -a SCENARIOS <<< "$SCENARIOS_CSV"
else
  mapfile -t SCENARIOS < <(discover)
fi
[ "${#SCENARIOS[@]}" -gt 0 ] || die "no scenarios found"

TS="$(date +%Y%m%d-%H%M%S)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/fakeble-bench.XXXXXX")"
RESULT_MD="$SCRIPT_DIR/results/${TS}-${MODEL}.md"
ARTIFACTS="$SCRIPT_DIR/results/${TS}-${MODEL}-artifacts"
# Keep raw responses / judge output / mappings for post-hoc diagnosis (drop the
# copied project trees). A scorecard you can't trace back to responses is a number,
# not evidence.
preserve_artifacts() {
  [ "${DRY:-0}" = "1" ] && return 0
  [ -d "$WORK" ] || return 0
  mkdir -p "$ARTIFACTS"
  (cd "$WORK" && tar --exclude='*/project' --exclude='*/judgehome' -cf - . 2>/dev/null) \
    | (cd "$ARTIFACTS" && tar -xf - 2>/dev/null) || true
}
trap 'preserve_artifacts; rm -rf "$WORK"' EXIT

echo "bench.sh: model=$MODEL judge=$JUDGE_MODEL double=$DOUBLE scenarios=${SCENARIOS[*]}" >&2
echo "bench.sh: workdir=$WORK" >&2

# --- claude wrapper with rate-limit retry (skipped entirely on --dry-run) ---
claude_call() { # <out_file> <prompt_file> <cwd> <model> [<extra flag>...]
  local out="$1" pf="$2" cwd="$3" model="$4"; shift 4
  # stream-json + collect_text: `claude -p` alone prints only the FINAL assistant
  # message, silently dropping the answer from any answer -> tool -> follow-up turn.
  local -a flags=(--model "$model" --setting-sources project --strict-mcp-config \
                  --output-format stream-json --verbose "$@")
  local attempt=0 raw="$out.stream"
  while :; do
    if ( cd "$cwd" && claude -p "$(cat "$pf")" "${flags[@]}" ) >"$raw" 2>"$out.err"; then
      if $PY "$LIB/collect_text.py" "$raw" >"$out"; then
        rm -f "$out.err"; return 0
      fi
      cat "$raw" "$out.err" >"$out" 2>/dev/null
    else
      cat "$raw" "$out.err" >"$out" 2>/dev/null
    fi
    attempt=$((attempt+1))
    if [ "$attempt" -le 2 ] && grep -qiE 'rate.?limit|overloaded|429' "$out"; then
      echo "bench.sh: rate-limited, retry $attempt after 60s" >&2
      sleep 60; continue
    fi
    return 1
  done
}

build_arm() { # <scenario_dir> <arm> <dest_project>
  local sdir="$1" arm="$2" dest="$3"
  mkdir -p "$dest"
  cp -R "$sdir/scenario/." "$dest/"
  if [ "$arm" = "arm-b" ]; then
    cp "$REPO_DIR/claude-md/fakeble.md" "$dest/CLAUDE.md"
    mkdir -p "$dest/.claude/skills"
    cp -R "$REPO_DIR/skills/." "$dest/.claude/skills/"
  fi
}

run_arm() { # <scenario_dir> <arm> <workdir> <tools> <multiturn> <state_file>
  local sdir="$1" arm="$2" w="$3" tools="$4" multiturn="$5" state="$6"
  local proj="$w/project"
  build_arm "$sdir" "$arm" "$proj"

  local t1="$w/turn1.txt"
  claude_call "$t1" "$sdir/PROMPT.txt" "$proj" "$MODEL" --allowedTools "$tools" \
    || echo "[bench: turn 1 run failed]" >>"$t1"

  # mechanical grep of the state file, after turn 1, before turn 2
  if [ -n "$state" ] && [ -f "$sdir/MECHANICAL.tsv" ]; then
    : >"$w/mech.tsv"
    while IFS='	' read -r rx desc; do
      [ -n "$rx" ] || continue
      case "$rx" in \#*) continue;; esac
      if [ -f "$proj/$state" ] && grep -qE "$rx" "$proj/$state"; then
        printf '1\t%s\n' "$desc" >>"$w/mech.tsv"
      else
        printf '0\t%s\n' "$desc" >>"$w/mech.tsv"
      fi
    done < "$sdir/MECHANICAL.tsv"
  fi

  if [ "$multiturn" = "1" ]; then
    local t2="$w/turn2.txt"
    claude_call "$t2" "$sdir/PROMPT2.txt" "$proj" "$MODEL" --allowedTools "$tools" --continue \
      || echo "[bench: turn 2 run failed]" >>"$t2"
    { echo "=== turn 1 ==="; cat "$t1"; echo; echo "=== turn 2 ==="; cat "$t2"; } >"$w/response.txt"
  else
    cp "$t1" "$w/response.txt"
  fi
}

# blind judge of one arm-a/arm-b pair -> writes parsed scores json to <out_json>
judge_pair() { # <scenario_dir> <resp_a> <resp_b> <shufdir> <out_json> [<force ab|ba>]
  local sdir="$1" ra="$2" rb="$3" shuf="$4" outj="$5" force="${6:-}"
  local prompt2=""
  [ -f "$sdir/PROMPT2.txt" ] && prompt2="$sdir/PROMPT2.txt"
  local mapfile
  if [ -n "$force" ]; then
    mapfile="$($PY "$LIB/shuffle.py" "$ra" "$rb" "$shuf" --force "$force")" || return 1
  else
    mapfile="$($PY "$LIB/shuffle.py" "$ra" "$rb" "$shuf")" || return 1
  fi
  local jprompt="$shuf/judge_prompt.txt" jraw="$shuf/judge_raw.txt"
  $PY "$LIB/build_judge_prompt.py" "$sdir/RUBRIC.md" "$sdir/PROMPT.txt" \
      "$shuf/response-1.txt" "$shuf/response-2.txt" $prompt2 > "$jprompt" || return 1
  mkdir -p "$shuf/judgehome"
  claude_call "$jraw" "$jprompt" "$shuf/judgehome" "$JUDGE_MODEL" || return 1
  $PY "$LIB/parse_scores.py" "$jraw" "$mapfile" "$sdir/RUBRIC.md" > "$outj" || return 1
}

# ---------------- dry-run: print plan only ----------------
print_plan() { # <scenario_dir>
  local sdir="$1" name; name="$(basename "$sdir")"
  local TOOLS=readonly MULTITURN=0 STATE_FILE=""
  # shellcheck disable=SC1090
  [ -f "$sdir/meta.env" ] && . "$sdir/meta.env"
  local tools="$READONLY_TOOLS"; [ "$TOOLS" = "write" ] && tools="$WRITE_TOOLS"
  echo "── scenario: $name"
  echo "   tools: $TOOLS   multiturn: $MULTITURN   state_file: ${STATE_FILE:-none}"
  echo "   arm A workdir: $WORK/$name/arm-a/project   (scenario files only)"
  echo "   arm B workdir: $WORK/$name/arm-b/project   (+ CLAUDE.md + .claude/skills)"
  local arm
  for arm in arm-a arm-b; do
    echo "   [$arm] turn1: (cd .../$arm/project && claude -p \"\$(cat PROMPT.txt)\" \\"
    echo "              --model $MODEL --setting-sources project --strict-mcp-config \\"
    echo "              --allowedTools \"$tools\")"
    if [ "$MULTITURN" = "1" ]; then
      echo "   [$arm] turn2: (same, PROMPT2.txt, + --continue)"
    fi
  done
  if [ -n "${STATE_FILE:-}" ] && [ -f "$sdir/MECHANICAL.tsv" ]; then
    echo "   mechanical: grep $STATE_FILE for:"
    while IFS='	' read -r rx desc; do
      [ -n "$rx" ] || continue; case "$rx" in \#*) continue;; esac
      echo "       /$rx/  -> $desc"
    done < "$sdir/MECHANICAL.tsv"
  fi
  echo "   judge: claude -p (model $JUDGE_MODEL) on RUBRIC.md, blind-shuffled$([ "$DOUBLE" = 1 ] && echo ', double (ab+ba)')"
}

if [ "$DRY" = "1" ]; then
  echo "PLAN (dry run — nothing will be invoked)"
  echo "model=$MODEL  judge-model=$JUDGE_MODEL  double-judge=$DOUBLE"
  echo "scaffold source: $REPO_DIR/claude-md/fakeble.md  +  $REPO_DIR/skills/"
  echo "scorecard would be written to: $RESULT_MD"
  echo
  for name in "${SCENARIOS[@]}"; do
    sdir="$SCRIPT_DIR/$name"
    [ -d "$sdir" ] || { echo "── scenario: $name  [MISSING DIR — skipped]"; continue; }
    print_plan "$sdir"
    echo
  done
  echo "dry-run complete: $((${#SCENARIOS[@]})) scenario(s) planned, 0 claude calls."
  exit 0
fi

# ---------------- real run ----------------
RESULT_FILES=()
for name in "${SCENARIOS[@]}"; do
  sdir="$SCRIPT_DIR/$name"
  [ -d "$sdir" ] || { echo "bench.sh: skip missing scenario $name" >&2; continue; }
  TOOLS=readonly MULTITURN=0 STATE_FILE=""
  # shellcheck disable=SC1090
  [ -f "$sdir/meta.env" ] && . "$sdir/meta.env"
  tools="$READONLY_TOOLS"; [ "$TOOLS" = "write" ] && tools="$WRITE_TOOLS"

  echo "bench.sh: [$name] running arms..." >&2
  wa="$WORK/$name/arm-a" wb="$WORK/$name/arm-b"
  mkdir -p "$wa" "$wb"
  run_arm "$sdir" "arm-a" "$wa" "$tools" "$MULTITURN" "$STATE_FILE" & pa=$!
  run_arm "$sdir" "arm-b" "$wb" "$tools" "$MULTITURN" "$STATE_FILE" & pb=$!
  wait "$pa"; wait "$pb"

  echo "bench.sh: [$name] judging..." >&2
  judged="$WORK/$name/judged.json"
  if judge_pair "$sdir" "$wa/response.txt" "$wb/response.txt" "$WORK/$name/judge1" "$WORK/$name/j1.json"; then
    if [ "$DOUBLE" = "1" ]; then
      # present the opposite ordering, then average the two passes
      force=ba
      m1_1="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["response-1"])' "$WORK/$name/judge1/mapping.json" 2>/dev/null)"
      [ "$m1_1" = "arm-a" ] && force=ba || force=ab
      if judge_pair "$sdir" "$wa/response.txt" "$wb/response.txt" "$WORK/$name/judge2" "$WORK/$name/j2.json" "$force"; then
        $PY "$LIB/merge_judges.py" "$WORK/$name/j1.json" "$WORK/$name/j2.json" > "$judged"
      else
        cp "$WORK/$name/j1.json" "$judged"
      fi
    else
      cp "$WORK/$name/j1.json" "$judged"
    fi
  else
    echo "bench.sh: [$name] judging failed; scenario recorded without judged scores" >&2
    judged=""
  fi

  args=(--scenario "$name")
  [ -n "$judged" ] && args+=(--judged "$judged")
  [ -n "$STATE_FILE" ] && args+=(--state-file "$STATE_FILE")
  [ -f "$wa/mech.tsv" ] && args+=(--mech-a "$wa/mech.tsv")
  [ -f "$wb/mech.tsv" ] && args+=(--mech-b "$wb/mech.tsv")
  rf="$WORK/$name/result.json"
  $PY "$LIB/mk_result.py" "${args[@]}" > "$rf" && RESULT_FILES+=("$rf")
done

mkdir -p "$SCRIPT_DIR/results"
dbl=""; [ "$DOUBLE" = "1" ] && dbl="--double"
$PY "$LIB/scorecard.py" --model "$MODEL" --judge-model "$JUDGE_MODEL" \
    --timestamp "$TS" $dbl "${RESULT_FILES[@]}" | tee "$RESULT_MD"

echo "bench.sh: scorecard written to $RESULT_MD" >&2
