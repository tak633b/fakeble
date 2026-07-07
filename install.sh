#!/bin/bash
# Fakeble installer — copies skills and (with confirmation) appends the CLAUDE.md fragment.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SKILLS_DIR="$CLAUDE_DIR/skills"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"

echo "Fakeble installer"
echo "  target: $CLAUDE_DIR"
echo

# 1. Skills
mkdir -p "$SKILLS_DIR"
for skill in bootstrap companion-state catchup hypothesis-ledger framing-library self-calibration escalation-queue intent-map; do
  if [ -e "$SKILLS_DIR/$skill" ]; then
    echo "  skip skill '$skill' (already exists at $SKILLS_DIR/$skill)"
  else
    cp -r "$REPO_DIR/skills/$skill" "$SKILLS_DIR/$skill"
    echo "  installed skill '$skill'"
  fi
done

# 2. CLAUDE.md fragment
if [ -f "$CLAUDE_MD" ] && grep -q "Fakeble — perceptive-companion behavior" "$CLAUDE_MD"; then
  echo "  skip CLAUDE.md fragment (already present)"
else
  echo
  printf "  Append the Fakeble fragment to %s? [y/N] " "$CLAUDE_MD"
  read -r ans
  if [ "${ans:-n}" = "y" ] || [ "${ans:-n}" = "Y" ]; then
    mkdir -p "$CLAUDE_DIR"
    [ -f "$CLAUDE_MD" ] && cp "$CLAUDE_MD" "$CLAUDE_MD.bak-fakeble"
    { echo; cat "$REPO_DIR/claude-md/fakeble.md"; } >> "$CLAUDE_MD"
    echo "  appended (backup at $CLAUDE_MD.bak-fakeble)"
  else
    echo "  skipped — append claude-md/fakeble.md manually when ready"
  fi
fi

echo
echo "Optional: hooks/reinjection/ has an anti-drift hook for very long sessions (off by default; see its settings-snippet.json)."
echo "Templates: templates/companion-state.template.md is the starting point for your state file."
echo "Done."
