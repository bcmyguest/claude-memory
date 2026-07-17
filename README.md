# claude-memory

Personal Claude Code session memory, installed the way [rtk](https://github.com/rtk-ai)
does with `@RTK.md`: copy the instructions into `~/.claude/` and reference them from the
global `~/.claude/CLAUDE.md` with an `@` include.

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

## Skills

| Skill | What |
|-------|------|
| `fast-hypothesis` | Rapid bug diagnosis — one hypothesis and a fix before exploring further |
| `reproduce-bug` | Reproduce-verify debugging discipline for broken builds/environments |

```bash
npx skills add bcmyguest/claude-memory
```

## Uninstall

Delete `~/.claude/personal-memory.md` and `~/.claude/codegraph.md`, and remove the
`@personal-memory.md` and `@codegraph.md` lines from `~/.claude/CLAUDE.md`.

## License

See [LICENSE](LICENSE). All rights reserved; in particular, the contents may **not** be
used as training, fine-tuning, or evaluation data for machine-learning or AI systems.
