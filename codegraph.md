# CodeGraph vs Grep

- **codegraph = 1 round-trip**: finds cross-file relationships, gives blast radius, expands scope via symbol resolution. Misses are rare.
- **grep = exact text**: zero false positives, but cross-file questions take multiple calls and it misses scope you didn't name.

## Use codegraph when the query spans files, involves relationships, or scope is unknown

"how does X work", "who calls Y", "blast radius before editing X", "trace flow from A to B"

## Use grep for exact text and regex patterns on known paths

"find this TODO comment", "grep -rn pattern"

## Anti-patterns

- ❌ grep first, then explore — codegraph answers cross-file questions in one call
- ❌ Read multiple files to trace relationships — codegraph returns verbatim source + call paths in one call
- ✅ Reach for codegraph first unless you already know the exact file path
