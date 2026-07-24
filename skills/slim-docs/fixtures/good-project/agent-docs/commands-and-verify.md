# commands-and-verify

Read when: build, test, lint, verify, CI, claiming done
Out of scope: production deploy approvals

## Invariants / hard rules

- Lint and unit tests must pass before claiming done.
- Prefer targeted tests for the package you touched.

## Key paths

- `package.json` scripts: build, test, lint

## Do / Don't

- Do: show command output evidence when done.
- Don't: skip type/lint failures with “will fix later”.

## Verify

```bash
npm run lint
npm test
```
