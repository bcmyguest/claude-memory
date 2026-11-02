# claude-memory

Personal Claude Code, Codex, and Cursor session memory. Claude follows the
[rtk](https://github.com/rtk-ai) pattern: copy instructions into `~/.claude/`
and reference them from the global `~/.claude/CLAUDE.md` with an `@` include.
Codex and Cursor receive the same instructions in managed blocks in
`~/.codex/AGENTS.md` and `~/.cursor/rules.md`.

[`MEMORY.md`](MEMORY.md) holds the general instructions;
[`codegraph.md`](codegraph.md) the codegraph-vs-grep guidance.

## Install / update

```bash
git clone git@github.com:bcmyguest/claude-memory.git
./claude-memory/install.sh
```

`install.sh` is idempotent:

1. Copies `MEMORY.md` to `~/.claude/personal-memory.md` and `codegraph.md` to
   `~/.claude/codegraph.md` (overwrites — `git pull` and re-run to update).
2. Appends `@personal-memory.md` and `@codegraph.md` to `~/.claude/CLAUDE.md`, once each.
3. Removes includes earlier versions added for the `writing-with-clarity` skill; its rules are now the Writing section of `MEMORY.md`.
4. Adds the tools in [`denied-tools.txt`](denied-tools.txt) to `permissions.deny` in
   `~/.claude/settings.json`, keeping existing entries. Denied tools drop out of every request.
5. Replaces the marked `claude-memory` block in `~/.codex/AGENTS.md` and
   `~/.cursor/rules.md`, preserving instructions outside the block.

## Uninstall

Delete `~/.claude/personal-memory.md` and `~/.claude/codegraph.md`, remove the
`@personal-memory.md` and `@codegraph.md` lines from `~/.claude/CLAUDE.md`, and
remove the blocks between `<!-- claude-memory:start -->` and
`<!-- claude-memory:end -->` from both `~/.codex/AGENTS.md` and `~/.cursor/rules.md`. Remove the `denied-tools.txt` names from `permissions.deny` in
`~/.claude/settings.json`.

## License

See [LICENSE](LICENSE). All rights reserved; in particular, the contents may **not** be
used as training, fine-tuning, or evaluation data for machine-learning or AI systems.
