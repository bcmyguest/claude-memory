# claude-memory

Personal Claude Code, Codex, and Cursor session memory. Claude follows the
[rtk](https://github.com/rtk-ai) pattern: copy instructions into `~/.claude/`
and reference them from the global `~/.claude/CLAUDE.md` with an `@` include.
Codex and Cursor receive the same instructions in managed blocks in
`~/.codex/AGENTS.md` and `~/.cursor/rules.md`.

[`MEMORY.md`](MEMORY.md) is the single source of truth for the general instructions;
[`codegraph.md`](codegraph.md) holds the codegraph-vs-grep guidance.
The repo also carries debugging skills in [`skills/`](skills).

## Install / update

```bash
git clone git@github.com:bcmyguest/claude-memory.git
./claude-memory/install.sh
```

`install.sh` is idempotent:

1. Copies `MEMORY.md` to `~/.claude/personal-memory.md` and `codegraph.md` to
   `~/.claude/codegraph.md` (overwrites — `git pull` and re-run to update).
2. Appends `@personal-memory.md` and `@codegraph.md` to `~/.claude/CLAUDE.md`, once each.
3. Appends `@bcmyguest/personal-skills/files/skills/writing-with-clarity` to `~/.claude/CLAUDE.md`.
4. Replaces the marked `claude-memory` block in `~/.codex/AGENTS.md`, preserving
   any instructions outside that block.
5. Replaces the marked `claude-memory` block in `~/.cursor/rules.md`, preserving
   any instructions outside that block.

## Skills

| Skill | What |
|-------|------|
| `fast-hypothesis` | Rapid bug diagnosis — one hypothesis and a fix before exploring further |
| `reproduce-bug` | Reproduce-verify debugging discipline for broken builds/environments |
| `writing-with-clarity` | Guidelines for clear, effective writing |

```bash
npx skills add bcmyguest/claude-memory
```

## Uninstall

Delete `~/.claude/personal-memory.md` and `~/.claude/codegraph.md`, remove the
`@personal-memory.md`, `@codegraph.md`, and `@bcmyguest/personal-skills/files/skills/writing-with-clarity` lines from `~/.claude/CLAUDE.md`, and
remove the blocks between `<!-- claude-memory:start -->` and
`<!-- claude-memory:end -->` from both `~/.codex/AGENTS.md` and `~/.cursor/rules.md`.

## License

See [LICENSE](LICENSE). All rights reserved; in particular, the contents may **not** be
used as training, fine-tuning, or evaluation data for machine-learning or AI systems.
