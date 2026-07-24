---
name: slim-docs
description: >
  Migrates bloated project agent entry files (CLAUDE.md, AGENTS.md) into a thin
  entry plus a local agent-docs/ task-slot library with index routing. Use when
  CLAUDE.md or AGENTS.md is too long, agent context is crowded by project
  instructions, the user asks to split or slim agent docs, create agent-docs,
  or set up progressive project docs for coding agents. Do NOT use for
  implementing product features, general writing, or RAG/vector knowledge bases.
---

# slim-docs

Turn fat agent entry files into a **thin entry** + **`agent-docs/`** library so sessions pay less permanent context tax while agents can still load the right topic on demand.

**Core principle:** Entry = commands + hard rules + load protocol. Topics = task/domain slots. Index = router.

## When to use

- Entry file(s) long / growing; user wants slim CLAUDE.md or AGENTS.md
- Need `agent-docs/` with per-task docs for agents (not a human docs site)

## When not to use

- Implementing app features unrelated to agent instruction structure
- Building vector/RAG search

## Required reading (from this skill)

Read before writing many files:

1. [references/tiers.md](references/tiers.md)
2. [references/load-protocol.md](references/load-protocol.md)
3. [references/entry-template.md](references/entry-template.md)
4. [references/index-template.md](references/index-template.md)

As needed: [topic-outlines.md](references/topic-outlines.md), [migration-checklist.md](references/migration-checklist.md).

## Procedure

Follow [migration-checklist.md](references/migration-checklist.md). Summary:

1. **Explore** — Find `CLAUDE.md` / `AGENTS.md`; note existing `agent-docs/`; skim layout.
2. **Pick tier** — User override wins; else suggest low|medium|high in one sentence and confirm.
3. **Plan split** — List keep-in-entry vs topics (triggers + path + purpose). **high: confirm plan before writing.**
4. **Write library** — `agent-docs/index.md` + topic files (task/domain slots). Unknown → `TODO`. Never invent business rules.
5. **Thin entries** — Every existing entry file; paste load protocol; stay under tier line limit.
6. **Verify (hard gate)** — From the **target project root**:

```bash
python <path-to-this-skill>/scripts/measure_entry.py --root . --tier <tier>
python <path-to-this-skill>/scripts/check_agent_docs.py --root . --tier <tier>
```

Both must exit 0. If not, fix until green. **Do not claim migration complete while red.**

7. **Report** — Files changed, tier, script summaries.

## Classification rule

Topics are **task/domain slots** (`auth.md`, `commands-and-verify.md`), not human genres (tutorial/ADR). Index rows must include triggers agents would match.

## Dual entries

Same `agent-docs/` for CLAUDE.md and AGENTS.md. Thin both if both exist. Do not duplicate topic bodies.

## Scripts

Treat scripts as black boxes; run them, read stdout. Only open source if debugging.

## Done definition

Checklist complete **and** both scripts exit 0 for the chosen tier.
