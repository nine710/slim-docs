# Entry template (CLAUDE.md / AGENTS.md)

Keep under the tier line limit. Same structure for both filenames.
Copy the body below into the project entry file (omit this header comment area).

--- BODY START ---
# <Project> agent instructions

One sentence: what this repo is.

## Commands

- Build: ...
- Test: ...
- Lint: ...

## Hard rules

- (short bullets only)

## Map

- src/... — ...

## agent-docs load protocol

- Before non-trivial code changes: open agent-docs/index.md, match the task keywords / path globs, then Read only the linked topic file(s).
- Do not load the entire agent-docs/ tree.
- Before claiming done: follow commands in the entry and/or commands-and-verify topic; show evidence.

## Do not

- Do not paste long subsystem docs back into this file; update agent-docs/ + index instead.
--- BODY END ---
