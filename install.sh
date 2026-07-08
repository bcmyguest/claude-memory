#!/usr/bin/env bash
# Install personal Claude Code instructions into ~/.claude and reference them from the
# global CLAUDE.md via the @include syntax — the same pattern rtk uses with @RTK.md.
# Idempotent: `git pull` this repo and re-run to pick up updates.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude/personal-memory.md"
GLOBAL="$HOME/.claude/CLAUDE.md"
REF="@personal-memory.md"

mkdir -p "$HOME/.claude"
cp "$SCRIPT_DIR/MEMORY.md" "$DEST"

touch "$GLOBAL"
if ! grep -qxF "$REF" "$GLOBAL"; then
  printf '\n%s\n' "$REF" >>"$GLOBAL"
  echo "Added $REF to $GLOBAL"
fi
echo "Installed MEMORY.md as $DEST"
