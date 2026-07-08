#!/usr/bin/env bash
# Sync personal CLAUDE.md instructions into ~/.claude and reference them from the
# global CLAUDE.md via the @include syntax — the same pattern rtk uses with @RTK.md.
# Idempotent: re-run any time to pull the latest instructions.
set -euo pipefail

SRC_URL="https://raw.githubusercontent.com/bcmyguest/personal-skills/main/CLAUDE.md"
DEST="$HOME/.claude/personal-memory.md"
GLOBAL="$HOME/.claude/CLAUDE.md"
REF="@personal-memory.md"

mkdir -p "$HOME/.claude"
curl -fsSL "$SRC_URL" -o "$DEST"

touch "$GLOBAL"
if ! grep -qxF "$REF" "$GLOBAL"; then
  printf '\n%s\n' "$REF" >>"$GLOBAL"
  echo "Added $REF to $GLOBAL"
fi
echo "Synced $DEST from bcmyguest/personal-skills"
