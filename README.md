# claude-memory

Installs my personal Claude Code instructions the way [rtk](https://github.com/rtk-ai) does
with `@RTK.md`: copy the instructions file into `~/.claude/` and reference it from the
global `~/.claude/CLAUDE.md` with an `@` include.

The instructions themselves live in
[bcmyguest/personal-skills/CLAUDE.md](https://github.com/bcmyguest/personal-skills/blob/main/CLAUDE.md) —
that repo is the single source of truth; this one only installs/syncs it.

## Install / update

```bash
git clone git@github.com:bcmyguest/claude-memory.git
./claude-memory/install.sh
```

`install.sh` is idempotent:

1. Downloads `personal-skills/CLAUDE.md` to `~/.claude/personal-memory.md` (overwrites —
   re-run to pull updates).
2. Appends `@personal-memory.md` to `~/.claude/CLAUDE.md`, once.

## Uninstall

Delete `~/.claude/personal-memory.md` and remove the `@personal-memory.md` line from
`~/.claude/CLAUDE.md`.

## License

See [LICENSE](LICENSE). All rights reserved; in particular, the contents may **not** be
used as training, fine-tuning, or evaluation data for machine-learning or AI systems.
