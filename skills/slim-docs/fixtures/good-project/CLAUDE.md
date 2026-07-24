# Good Demo App agent instructions

Small fixture repo with a thin entry and agent-docs library (tier low).

## Commands

- Install: `npm install`
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Hard rules

- Do not invent business rules; put unknown items as TODO in agent-docs topics.
- Prefer targeted tests for the package you touched.
- Never commit secrets or live API keys.

## Map

- `src/app` — UI entry
- `src/api` — HTTP handlers
- `src/lib` — shared helpers
- `agent-docs/` — task/domain topics (load via index)

## agent-docs load protocol

- Before non-trivial code changes: open `agent-docs/index.md`, match the task keywords / path globs, then Read **only** the linked topic file(s).
- Do **not** load the entire `agent-docs/` tree.
- Before claiming done: follow commands in the entry and/or `commands-and-verify` topic; show evidence.

## Do not

- Do not paste long subsystem docs back into this file; update agent-docs/ + index instead.
- Do not skip lint/tests when claiming done.
