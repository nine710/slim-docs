# commands-and-verify

Read when: build, test, lint, verify, CI, deploy, typecheck, claiming done
Out of scope: on-call rotation details, legal PII export queues

## Invariants / hard rules

- Lint and unit tests must pass before claiming done.
- Prefer targeted tests for the package you touched.
- Do not skip typecheck on TypeScript changes.
- Staging deploys on merge to `main`; production needs manual workflow dispatch.
- Migrations run as a pre-deploy job; no auto-run destructive migrations without review.

## Key commands

```bash
npm install
npm run build
npm test
npm run lint
npm run typecheck
npm run dev
npm run format
npm run e2e
npm run db:migrate
npm run db:seed
```

## Deploy notes

- Images go to the org container registry; env vars from secret store only.
- Rollback: previous image tag; reverse migrations only when marked reversible.
- Post-deploy smoke: health, login, one paid checkout in staging.

## Do / Don't

- Do: show command output evidence when done.
- Don't: claim done with red lint/tests or skipped typecheck.

## Verify

```bash
npm run lint
npm test
npm run typecheck
```
