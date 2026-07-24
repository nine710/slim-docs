# architecture-map

Read when: layout, modules, architecture, apps/, packages/, where to edit
Out of scope: deploy runbooks, product roadmap, archival history

## Invariants / hard rules

- Request → route handler → service → repository → DB. No SQL in route handlers.
- Web may call API only over HTTP; packages must not import from apps.
- Circular imports between packages are forbidden; shared types go in `packages/shared`.
- Prefer pure functions in `packages/shared` when logic is not I/O bound.
- Keep controllers thin; business rules live in services.

## Key paths

- `apps/web` — Next.js frontend (`apps/web/src/app`)
- `apps/api` — HTTP API (`apps/api/src/routes`, `services`, `workers`)
- `packages/shared` — shared types and pure helpers
- `packages/ui` — design system components
- `packages/db` — Prisma schema and client helpers
- `infra/` — Terraform and deploy scripts
- `scripts/` — one-off maintenance tools

## Do / Don't

- Do: put domain logic in services; put cross-cutting types in shared.
- Don't: import apps from packages or put SQL in handlers.

## Verify

- Smoke: health endpoint, login path, and one paid checkout path in staging when deploy-related.
