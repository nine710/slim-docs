# conventions

Read when: style, naming, conventions, auth, billing, code review bans
Out of scope: archival release history filler, on-call schedules

## Invariants / hard rules

### Style

- TypeScript strict; no `any` without a one-line justification.
- Prefer named exports; avoid default exports in packages.
- Use `async/await`; prefer early returns over deep nesting.
- Files kebab-case; React components PascalCase; hooks `useX`.
- Tests sit next to source as `*.test.ts`. Format with Prettier; lint with root ESLint.
- Prefer existing UI kit components over one-off CSS.

### Auth

- Session cookies for web; bearer tokens for public API.
- Password hashing: bcrypt cost 12. Never log tokens, cookies, or password hashes.
- Roles: `user`, `operator`, `admin`. Admin routes under `/admin/*` need both auth and authz.
- Impersonation is admin-only and must audit-log.
- Cookie flags: HttpOnly, Secure in prod, SameSite=Lax.
- Rate-limit login and password reset. Clear sessions on password change.

### Billing

- Stripe webhooks at `POST /webhooks/stripe` must verify signatures.
- Feature gates read subscription service, not live Stripe per request after sync.
- Never commit live Stripe keys. Refunds need admin role + audit trail.
- Do not block HTTP on email; notifications go through workers.

## Do / Don't

- Do: update auth tests under `apps/api/src/services/auth/` when changing auth.
- Don't: mix session and bearer auth on the same handler or leak stack traces on 401.

## Verify

- `npm run lint` clean for touched files; auth/billing changes include unit tests.
