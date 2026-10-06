# Contributing

## Commit convention

Format: `type: short description` (imperative, lowercase, no final period).

Types: `chore`, `docs`, `feat`, `fix`, `test`.
Optional scope: `feat(plc): add pump alternation`.

## Rules

- One commit per completed step.
- Every functional requirement has a test and a traceability entry.
- Simulated safety logic is named with the `Sim` suffix and documented as such.
- No credentials, tokens or private addresses in the repository.
- No version is tagged stable until the critical tests pass.

## Language

English is the primary language. French summaries live in `README.fr.md` and `docs/fr/`.