# CodeGraph vs Grep

- **codegraph = 1 round-trip**: finds cross-file relationships, gives blast radius, expands scope via symbol resolution. Misses are rare.
- **grep = better for exact text**: zero false positives, but multiple calls needed for cross-file and scope you didn't name is missed.

## Use codegraph when the query spans files, involves relationships, or scope is unknown

"how does X work", "who calls Y", "blast radius before editing X", "trace flow from A to B"

## Use grep for exact text and regex patterns on known paths

"find this TODO comment", "grep -rn pattern"

## Anti-patterns

- ❌ grep first, then explore — codegraph answers cross-file questions in one call
- ❌ Read multiple files to trace relationships — codegraph returns verbatim source + call paths in one call
- ✅ Always reach for codegraph first when you don't already know the exact file path
