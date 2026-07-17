#!/usr/bin/env bash
# Install personal Claude Code instructions into ~/.claude and reference them from the
# global CLAUDE.md via the @include syntax — the same pattern rtk uses with @RTK.md.
# Idempotent: `git pull` this repo and re-run to pick up updates.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL="$HOME/.claude/CLAUDE.md"

mkdir -p "$HOME/.claude"
touch "$GLOBAL"

# install_doc <repo file> <name under ~/.claude>
install_doc() {
  local src="$1" dest_name="$2" ref="@$2"
  cp "$SCRIPT_DIR/$src" "$HOME/.claude/$dest_name"
  if ! grep -qxF "$ref" "$GLOBAL"; then
    printf '\n%s\n' "$ref" >>"$GLOBAL"
    echo "Added $ref to $GLOBAL"
  fi
  echo "Installed $src as ~/.claude/$dest_name"
}

install_doc MEMORY.md personal-memory.md
install_doc codegraph.md codegraph.md
