# Migration checklist

Copy into the agent reply and check off:

- [ ] Explored entry files (CLAUDE.md / AGENTS.md) and repo layout
- [ ] Tier chosen: low | medium | high
- [ ] Read references: tiers, entry-template, index-template, load-protocol
- [ ] Split plan listed (keep vs move); high: user confirmed plan
- [ ] Wrote `agent-docs/index.md` with trigger rows
- [ ] Wrote topic files (task slots); TODOs only where unknown — no invented rules
- [ ] Thinned every existing entry file; pasted load protocol
- [ ] `python scripts/measure_entry.py --root <project> --tier <tier>` exit 0
- [ ] `python scripts/check_agent_docs.py --root <project> --tier <tier>` exit 0
- [ ] Reported file list + script output summary to user
