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
6. Installs every `bcmyguest` repo tagged with the GitHub topic `claude-memory`
   ([`install_repos.py`](install_repos.py)), into whichever agents are on `PATH`:
   - a Claude Code marketplace (`.claude-plugin/marketplace.json`): `claude plugin marketplace add` and `claude plugin install` for each plugin;
   - a Copilot marketplace (`.github/plugin/marketplace.json`): the same with `copilot`;
   - a Codex marketplace (`.agents/plugins/marketplace.json`): `codex plugin marketplace add`, then install from `/plugins`;
   - skills with no Claude marketplace: `npx skills add <repo> -g --all`, which links every skill into every detected agent.

   Add a repo with `gh repo edit bcmyguest/<repo> --add-topic claude-memory`; remove it with
   `--remove-topic`. Preview with `python3 install_repos.py --dry-run`. Override with
   `CLAUDE_MEMORY_OWNER` / `CLAUDE_MEMORY_TOPIC`, or skip with `CLAUDE_MEMORY_SKIP_REPOS=1`.
   Cursor imports marketplaces only from its dashboard, and opencode only from npm, so
   neither is covered; for oncebitten on opencode run `oncebitten hooks install --host opencode --scope user`.

Tests: `python3 test_install_repos.py`.

## Uninstall

Delete `~/.claude/personal-memory.md` and `~/.claude/codegraph.md`, remove the
`@personal-memory.md` and `@codegraph.md` lines from `~/.claude/CLAUDE.md`, and
remove the blocks between `<!-- claude-memory:start -->` and
`<!-- claude-memory:end -->` from both `~/.codex/AGENTS.md` and `~/.cursor/rules.md`. Remove the `denied-tools.txt` names from `permissions.deny` in
`~/.claude/settings.json`.

## License

See [LICENSE](LICENSE). All rights reserved; in particular, the contents may **not** be
used as training, fine-tuning, or evaluation data for machine-learning or AI systems.
