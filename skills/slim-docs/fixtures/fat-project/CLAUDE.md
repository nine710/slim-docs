# Fat Demo App agent instructions

Deliberately fat CLAUDE.md fixture after slim-docs migration (tier low).

## Commands

- Install: `npm install`
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Typecheck: `npm run typecheck`
- Dev: `npm run dev`

Always run lint and unit tests before claiming done. Prefer targeted tests.

## Hard rules

- Do not invent business rules; put unknowns as TODO in agent-docs topics.
- Web may call API only over HTTP; packages must not import from apps.
- Never log tokens, cookies, or password hashes; never commit live secrets.

## Map

- `apps/web` — Next.js frontend
- `apps/api` — HTTP API
- `packages/shared` — shared types/helpers
- `packages/ui` — design system
- `packages/db` — Prisma schema/client
- `agent-docs/` — task topics (load via index)

## agent-docs load protocol

- Before non-trivial code changes: open `agent-docs/index.md`, match the task keywords / path globs, then Read **only** the linked topic file(s).
- Do **not** load the entire `agent-docs/` tree.
- Before claiming done: follow commands in the entry and/or `commands-and-verify` topic; show evidence.

## Do not

- Do not paste long subsystem docs back into this file; update agent-docs/ + index instead.
- Do not skip lint/tests when claiming done.
