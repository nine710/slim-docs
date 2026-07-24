# Tiers

| tier | entry max lines | topic files (excl. index) | use when |
|------|-----------------|---------------------------|----------|
| low | 80 | 2–3 | small repo, shallow layout |
| medium | 100 | 4–8 | multi-module, repeated footguns |
| high | 120 | 8–20 | monorepo / many domains |

Rules:
- Complexity goes into `agent-docs/`, not the entry file.
- Classification is **task/domain slots**, not human doc types (tutorial/ADR).
- high may use subfolders under `agent-docs/` for storage only; routing stays in top `index.md`.

Heuristic if user did not pick a tier:
1. entry lines > 150 or >3 top-level packages → suggest medium or high
2. entry lines ≤ 100 and simple tree → low
3. Always state the suggestion in one sentence and confirm before writing many files.
