# slim-docs

[English](README.md) | [中文](README.zh-CN.md)

**Agent Skill** that migrates bloated project agent entry files (`CLAUDE.md`, `AGENTS.md`, …) into a **thin entry** plus a local **`agent-docs/`** task-slot library with index routing.

Compatible with the [Agent Skills](https://agentskills.io) format (`SKILL.md` + optional `references/` + `scripts/`).

## Problem

Long `CLAUDE.md` / `AGENTS.md` files are often injected every session. That burns context, dilutes hard rules, and still fails when you over-trim and the agent misses project facts.

## Approach

| Layer | Role |
|-------|------|
| **Thin entry** | Commands, hard rules, short map, **load protocol** only |
| **`agent-docs/index.md`** | Router: triggers → topic path → when to read |
| **Topic files** | Task/domain slots (e.g. `auth.md`, `commands-and-verify.md`) — not human “tutorial/ADR” taxonomy |
| **Tiers** | `low` / `medium` / `high` control entry line budget and topic count |

**Success criteria this skill optimizes for:**

- **A — Less permanent context:** entry stays under the tier line limit  
- **B — Routable loading:** healthy index + load protocol so agents open the right topic on demand  

## When to use

- Entry files are long or keep growing  
- You want `agent-docs/` for coding agents (not a human docs site / RAG store)  
- You need both Claude Code (`CLAUDE.md`) and Codex-style (`AGENTS.md`) thin entries over **one** library  

## When not to use

- Implementing product features unrelated to agent instruction structure  
- Building vector/RAG knowledge bases  
- Expecting a runtime supervisor that forces the agent to read docs every turn (v1 is **migration / setup**, not a live watchdog)

## Install

### Claude Code (personal skills)

```bash
git clone https://github.com/nine710/slim-docs.git ~/.claude/skills/slim-docs
```

Windows (Git Bash):

```bash
git clone https://github.com/nine710/slim-docs.git "$USERPROFILE/.claude/skills/slim-docs"
```

The folder name must remain `slim-docs` (matches skill `name`).

### Project-local skill

```bash
git clone https://github.com/nine710/slim-docs.git .claude/skills/slim-docs
```

### Update

```bash
cd ~/.claude/skills/slim-docs && git pull
```

Restart or open a new Claude Code session so the skill is rediscovered.

## Use

In a project with a fat entry file, ask the agent things like:

- “Our `CLAUDE.md` is too long — slim it with agent-docs (tier medium).”  
- “Create `agent-docs/` and thin both `CLAUDE.md` and `AGENTS.md`.”  
- “Migrate project agent instructions to progressive docs, tier low.”  

The skill walks explore → tier → plan split → write library → thin entries → **script hard gate**.

### Before / after (shape)

**Before (every session pays full tax):**

```text
CLAUDE.md   (300+ lines: architecture essays, auth, billing, style, …)
```

**After:**

```text
CLAUDE.md                 # thin: commands + hard rules + load protocol
AGENTS.md                 # optional; same protocol, same library
agent-docs/
  index.md                # trigger → path router
  architecture-map.md
  commands-and-verify.md
  auth.md                 # task/domain slots…
```

## Tiers

| Tier | Entry max lines | Topic files (excl. index) |
|------|-----------------|---------------------------|
| low | 80 | 2–3 |
| medium | 100 | 4–8 |
| high | 120 | 8–20 |

Details: [`references/tiers.md`](references/tiers.md).

## Verify scripts (hard gate)

From the **target project root** (not this skill repo), after migration:

```bash
python /path/to/slim-docs/scripts/measure_entry.py --root . --tier low|medium|high
python /path/to/slim-docs/scripts/check_agent_docs.py --root . --tier low|medium|high
```

Both must exit `0` before claiming migration is done.

| Script | Checks |
|--------|--------|
| `measure_entry.py` | `CLAUDE.md` / `AGENTS.md` line counts vs tier |
| `check_agent_docs.py` | `agent-docs/index.md` table, links, orphans, topic count in range |

Stdlib Python 3 only; no pip install required.

## Package layout

```text
slim-docs/                 # this repository root = skill package
├── SKILL.md               # agent instructions (runtime)
├── README.md              # humans (English)
├── README.zh-CN.md        # humans (Chinese)
├── LICENSE
├── references/            # templates loaded on demand by the skill
└── scripts/               # validation CLIs
```

## Security

- Review `scripts/` before install (they run on your machine).  
- Scripts are intended to **read** project files for structure/line counts; they should not modify your project.  
- Prefer install from this GitHub repo or a tag you trust.  
- Third-party skill forks can be a supply-chain risk — treat them like code.

## Compatibility

- **Claude Code:** `CLAUDE.md`  
- **Codex / AGENTS-style tools:** `AGENTS.md`  
- Same `agent-docs/` library for both; do not duplicate topic bodies  

Format reference: [agentskills.io](https://agentskills.io) · examples: [anthropics/skills](https://github.com/anthropics/skills)

## License

[MIT](LICENSE) © 2026 ninelie710
