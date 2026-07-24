# architecture-map

Read when: layout, modules, where to edit, architecture questions
Out of scope: deploy runbooks, product roadmap

## Invariants / hard rules

- UI lives under `src/app`; HTTP under `src/api`; pure helpers under `src/lib`.
- Do not import app layers from lib packages circularly.

## Key paths

- `src/app` — pages and UI
- `src/api` — route handlers
- `src/lib` — shared pure helpers

## Do / Don't

- Do: put domain logic near the feature folder that owns it.
- Don't: dump one-off scripts into `src/lib`.

## Verify

- Smoke: app boots and health route responds.
