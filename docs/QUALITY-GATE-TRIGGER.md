# Quality Gate Trigger

This file exists solely to create observable pull-request runs of `.github/workflows/quality-gate.yml`.

- Branch: `verify/quality-gate`
- Purpose: verify install, typecheck, lint, build, and `dist/index.html` output
- Trigger attempts: PR opened; branch synchronized on 2026-07-22
- Safe rollback: close the verification PR and delete this branch/file after recording the workflow receipt
