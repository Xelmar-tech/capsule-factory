---
description: Run a security scan over the current commit or working tree
argument-hint: '[optional scope: "staged", "branch", or a path]'
---

Load skill: **commit-security-scan**.

The user invoked `/security-scan`. Apply the `commit-security-scan` skill to the scope hinted by `$ARGUMENTS` (default: the diff since the branch point against `main`). Report findings grouped by severity, each with a file:line and a one-line rationale. If a finding is exploitable in the current configuration, mark it explicitly and propose a concrete fix; if it depends on context the scan can't see (e.g., auth boundary, deployment environment), surface the assumption.
