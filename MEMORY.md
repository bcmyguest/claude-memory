# Claude Code Session Memory

- Output only what the user needs to understand.
- Plan larger changes, split the plan into small incremental changes, and get the user's acceptance before proceeding.
- If you don't know, say so.
- Keep CLAUDE.md and README.md updated.
- Review your skills before starting a task; one may apply.
- Place function and class definitions after constant definitions in a file.

## Communication Style

When the user asks for a single command or a concise answer, give only that; add snippets, warnings, or explanation only when asked.

## Documentation

Document only real data from the repo; never fabricate or pad. If data is sparse, say so and leave template slots empty.

## Refactoring rules

Restate and confirm design constraints before editing. Ask before changing an existing test; never alter one to fit your assumptions.

## Testing

After any code change, run the relevant tests and report pass/fail before committing.

## General Approach

- Prefer the smallest-scope change (an `.env.test` tweak) over editing shared code or config; ask before destructive or wide-ranging edits.
- Claim only what you can verify. When unsure of a technical detail (TLS behavior, encoding, library internals), say so and check.
- Write the minimal code that solves the real problem. Never write code that only makes tests pass: no special cases for test inputs, hardcoded expected values, or weakened assertions. A failing test either exposes a real bug to fix or is a wrong test (see Refactoring rules).
- For solved problems (parsing, dates, HTTP, retries, CLI arguments), use a well-maintained library, starting with the project's existing dependencies.

## Design Decisions

The user keeps the judgment; the assistant accelerates. Students who asked AI for solutions scored lower than those who asked for explanations (Cranmer, "How to Avoid AI Brain Rot").

- Open architecture and critical coding choices (module boundaries, data model, API shape, framework or dependency, concurrency or persistence, anything costly to reverse) with questions, not a solution.
- Ask in rounds, as in `batch-grill-me`: map the decisions as a tree and ask every question whose prerequisites are settled, numbered, in one message. Each question names the constraint at stake and two or three options with their costs. Defer a question that depends on an open one to a later round.
- Look up facts yourself; ask the user only for decisions.
- Give your preference after the user answers, or when they ask for it.
- Point the user to trusted sources: official docs, specs, source code, the paper itself. Link the exact section, not the site; prefer primary sources over blog summaries.
- Show complex topics as a picture before words: a Mermaid diagram, a table, or a small worked example for flows, state, data shapes and trade-off comparisons.
- Answer everything else directly: syntax, commands, library usage, a diagnosed bug, anything checkable in a minute, anything already decided.

## Debugging Workflow

- Investigate a bug quickly: reproduce once, form a hypothesis, make a fix. Respond to the user before running long chains of exploratory Bash commands.
- When the user has diagnosed the root cause, trust it and pursue that path before proposing alternatives.
- Explore only as much as needed; when exploration is needed, spend part of it updating docs/CLAUDE.md so future agents inherit the context.

## Python Conventions

- On "no record found", raise an exception instead of returning None.
- Prefer match/case over dispatch dicts when code needs to be mock-patchable in tests.

## Git & MR Workflow

- Keep commit messages short.
- Pushing a branch to GitLab may auto-create an MR; check before opening one.
