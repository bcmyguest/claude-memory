#!/usr/bin/env bash
# Install personal instructions for Claude Code, Codex, and Cursor. Claude uses @include
# references; Codex and Cursor get the same source documents in managed blocks.
# Idempotent: `git pull` this repo and re-run to pick up updates.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_GLOBAL="$HOME/.claude/CLAUDE.md"
CODEX_GLOBAL="$HOME/.codex/AGENTS.md"
CURSOR_GLOBAL="$HOME/.cursor/rules.md"
CODEX_START='<!-- claude-memory:start -->'
CODEX_END='<!-- claude-memory:end -->'
CURSOR_START='<!-- claude-memory:start -->'
CURSOR_END='<!-- claude-memory:end -->'

mkdir -p "$HOME/.claude" "$HOME/.codex" "$HOME/.cursor"
touch "$CLAUDE_GLOBAL" "$CODEX_GLOBAL" "$CURSOR_GLOBAL"

# install_doc <repo file> <name under ~/.claude>
install_doc() {
  local src="$1" dest_name="$2" ref="@$2"
  cp "$SCRIPT_DIR/$src" "$HOME/.claude/$dest_name"
  if ! grep -qxF "$ref" "$CLAUDE_GLOBAL"; then
    printf '\n%s\n' "$ref" >>"$CLAUDE_GLOBAL"
    echo "Added $ref to $CLAUDE_GLOBAL"
  fi
  echo "Installed $src as ~/.claude/$dest_name"
}

install_codex_docs() {
  local unmanaged managed
  unmanaged="$(mktemp)"
  managed="$(mktemp)"
  trap 'rm -f "$unmanaged" "$managed"' RETURN

  awk -v start="$CODEX_START" -v end="$CODEX_END" '
    $0 == start { managed = 1; next }
    $0 == end { managed = 0; next }
    !managed { lines[++count] = $0 }
    END {
      while (count && lines[count] ~ /^[[:space:]]*$/) count--
      for (line = 1; line <= count; line++) print lines[line]
    }
  ' "$CODEX_GLOBAL" >"$unmanaged"

  {
    printf '%s\n\n' "$CODEX_START"
    cat "$SCRIPT_DIR/MEMORY.md"
    printf '\n\n'
    cat "$SCRIPT_DIR/codegraph.md"
    printf '\n\n%s\n' "$CODEX_END"
  } >"$managed"

  {
    cat "$unmanaged"
    if [[ -s "$unmanaged" ]]; then printf '\n'; fi
    cat "$managed"
  } >"$CODEX_GLOBAL.tmp"
  mv "$CODEX_GLOBAL.tmp" "$CODEX_GLOBAL"
  echo "Installed MEMORY.md and codegraph.md in ~/.codex/AGENTS.md"
}

install_cursor_docs() {
  local unmanaged managed
  unmanaged="$(mktemp)"
  managed="$(mktemp)"
  trap 'rm -f "$unmanaged" "$managed"' RETURN

  awk -v start="$CURSOR_START" -v end="$CURSOR_END" '
    $0 == start { managed = 1; next }
    $0 == end { managed = 0; next }
    !managed { lines[++count] = $0 }
    END {
      while (count && lines[count] ~ /^[[:space:]]*$/) count--
      for (line = 1; line <= count; line++) print lines[line]
    }
  ' "$CURSOR_GLOBAL" >"$unmanaged"

  {
    printf '%s\n\n' "$CURSOR_START"
    cat "$SCRIPT_DIR/MEMORY.md"
    printf '\n\n'
    cat "$SCRIPT_DIR/codegraph.md"
    printf '\n\n%s\n' "$CURSOR_END"
  } >"$managed"

  {
    cat "$unmanaged"
    if [[ -s "$unmanaged" ]]; then printf '\n'; fi
    cat "$managed"
  } >"$CURSOR_GLOBAL.tmp"
  mv "$CURSOR_GLOBAL.tmp" "$CURSOR_GLOBAL"
  echo "Installed MEMORY.md and codegraph.md in ~/.cursor/rules.md"
}

install_doc MEMORY.md personal-memory.md
install_doc codegraph.md codegraph.md
if ! grep -qxF '@bcmyguest/personal-skills/files/skills/writing-with-clarity' "$CLAUDE_GLOBAL"; then
  printf '\n%s\n' '@bcmyguest/personal-skills/files/skills/writing-with-clarity' >>"$CLAUDE_GLOBAL"
  echo "Added @bcmyguest/personal-skills/files/skills/writing-with-clarity to $CLAUDE_GLOBAL"
fi
install_codex_docs
install_cursor_docs
