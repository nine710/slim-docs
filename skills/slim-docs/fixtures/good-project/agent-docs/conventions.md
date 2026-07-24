# conventions

Read when: style, naming, conventions, code review bans
Out of scope: product copywriting guidelines

## Invariants / hard rules

- TypeScript strict; avoid `any` without a one-line justification.
- Named exports preferred in shared modules.

## Key paths

- Repo root ESLint/Prettier configs

## Do / Don't

- Do: match existing naming in the folder you edit.
- Don't: introduce a second formatting style.

## Verify

- `npm run lint` is clean for touched files.
