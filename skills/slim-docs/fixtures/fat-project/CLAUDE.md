# Fat Demo App agent instructions

This repository is a deliberately bloated CLAUDE.md fixture used to exercise
slim-docs migration. Agents should not need every section every turn.

## Commands

- Install: `npm install`
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`
- Typecheck: `npm run typecheck`
- Dev server: `npm run dev`
- Format: `npm run format`
- E2E: `npm run e2e`
- DB migrate: `npm run db:migrate`
- DB seed: `npm run db:seed`

Always run lint and unit tests before claiming done. Prefer targeted tests for
the package you touched. Do not skip the typecheck on TS changes.

## Architecture

The monorepo layout is roughly:

- `apps/web` — Next.js frontend for customers and operators
- `apps/api` — Express/Fastify HTTP API
- `packages/shared` — shared types and pure helpers
- `packages/ui` — design system components
- `packages/db` — Prisma schema and client helpers
- `infra/` — Terraform and deploy scripts
- `scripts/` — one-off maintenance tools

Entry points:

- Web: `apps/web/src/app`
- API routes: `apps/api/src/routes`
- Domain services: `apps/api/src/services`
- Background jobs: `apps/api/src/workers`

Data flow is request → route handler → service → repository → DB. Do not put
SQL in route handlers. Prefer pure functions in `packages/shared` when logic is
not I/O bound. Keep controllers thin; business rules live in services.

Module boundaries matter: web may call API only over HTTP; packages must not
import from apps. Circular imports between packages are forbidden. If you need
a type on both sides, put it in `packages/shared`.

## Auth

Auth uses session cookies for the web app and bearer tokens for the public API.
Password hashing uses bcrypt with cost factor 12. Never log tokens, cookies, or
password hashes. Session TTL is 14 days with sliding refresh on activity.

Roles: `user`, `operator`, `admin`. Admin routes live under `/admin/*` and must
check both authentication and authorization. Impersonation is admin-only and
must write an audit log entry.

OAuth providers: Google and GitHub for social login. Callback URLs are
environment-specific; never hardcode production callback hosts in code. MFA is
optional for users and required for operators.

When changing auth:

- Update tests under `apps/api/src/services/auth/`
- Verify cookie flags: HttpOnly, Secure in prod, SameSite=Lax
- Do not store JWT secrets in the repo; use env vars
- Rate-limit login and password reset endpoints

Common pitfalls: mixing session and bearer auth on the same handler, forgetting
to clear sessions on password change, and leaking stack traces on 401 paths.

## Billing

Billing integrates Stripe. Products and prices are defined in the Stripe
dashboard and mirrored in `packages/db` tables `plans` and `subscriptions`.
Webhooks land at `POST /webhooks/stripe` and must verify signatures.

Subscription states: `trialing`, `active`, `past_due`, `canceled`. Feature
gates read from the subscription service, never directly from Stripe at request
time after the initial sync.

Invoices and receipts are emailed via the notification worker. Do not block the
HTTP request on email. Proration rules follow Stripe defaults unless product
explicitly overrides them in the billing service.

Test cards only in non-production. Never commit live Stripe keys. When adding a
plan, update seed data and feature-flag docs. Refunds require admin role and an
audit trail.

## Style

TypeScript strict mode is on. Prefer named exports. Avoid default exports in
packages. Use `async/await` over raw promises. Prefer early returns over deep
nesting. No `any` without a one-line justification comment.

Naming: files kebab-case, React components PascalCase, hooks `useX`. API route
files mirror URL path segments. Tests sit next to source as `*.test.ts`.

Comments explain why, not what. Do not leave large commented-out blocks.
Format with Prettier; lint with ESLint config in the repo root. Prefer existing
UI kit components over one-off CSS.

## Deploy

Staging deploys on merge to `main` via GitHub Actions. Production requires a
manual workflow dispatch with approval. Images go to the org container registry.

Env vars are managed in the secret store; never put secrets in Terraform state
comments or README samples. Migrations run as a pre-deploy job; do not auto-run
destructive migrations without a review checklist.

Rollback: redeploy the previous image tag and reverse migrations only when the
migration is marked reversible. Post-deploy smoke: health endpoint, login, and
one paid checkout path in staging.

## History

2024-01: Monorepo bootstrap from separate web and api repos.
2024-03: Introduced packages/shared and packages/ui.
2024-06: Stripe billing v1 with webhooks and plan gates.
2024-09: Operator console and MFA for staff.
2025-01: Migrated sessions to Redis-backed store.
2025-04: Added GitHub OAuth and audit log export.
2025-08: Split workers out of the API process.
2026-01: Terraform modules for staging and prod parity.

These history notes are archival. Prefer current Architecture and domain
sections for day-to-day work. Do not invent new historical facts when editing.

## Misc long notes agents rarely need every session

Filler detail 01: the default log level is info in prod and debug in local dev.
Filler detail 02: metrics export to Prometheus on port 9090 in the API pod.
Filler detail 03: tracing uses OpenTelemetry with a 5% sample rate in prod.
Filler detail 04: feature flags live in LaunchDarkly; local fallback is JSON.
Filler detail 05: cache TTLs for public catalog pages are five minutes.
Filler detail 06: the support inbox alias is ops+support@example.com.
Filler detail 07: load tests run weekly against staging with k6 scripts.
Filler detail 08: incident severity definitions are in the ops runbook only.
Filler detail 09: on-call rotation is weekly and starts Monday 09:00 UTC.
Filler detail 10: database backups are nightly with 30-day retention.
Filler detail 11: PII export requests go through the legal ticketing queue.
Filler detail 12: the design token source of truth is packages/ui/tokens.json.
Filler detail 13: storybook publishes on PR for UI package changes only.
Filler detail 14: dependency updates are batched weekly via Dependabot.
Filler detail 15: the preferred branch prefix is feat/, fix/, chore/, docs/.
Filler detail 16: commit messages follow conventional commits loosely.
Filler detail 17: large binary assets must not enter git; use object storage.
Filler detail 18: the demo tenant seed password is only for local Docker.
Filler detail 19: API public rate limit is 120 req/min per IP by default.
Filler detail 20: websocket support is experimental and off in production.
