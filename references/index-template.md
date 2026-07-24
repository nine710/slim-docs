# index template

Save as agent-docs/index.md. Use this table shape:

# agent-docs index

Task/domain router for agents. Read matching rows only.

| triggers (keywords / globs) | path | read when / get |
|-----------------------------|------|-----------------|
| build, test, lint, verify, CI | commands-and-verify.md | how to build and prove done |
| layout, modules, where to edit | architecture-map.md | where to change code |

Rules:
- Every topic .md under agent-docs/ (except index.md) MUST appear in at least one row.
- path is relative to agent-docs/.
- Prefer retrieval-friendly filenames: auth.md, not 01-overview.md.
