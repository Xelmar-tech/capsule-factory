---
description: Review a pull request and post follow-up comments
argument-hint: '<PR-number> or <PR-URL>'
---

Load skill: **follow-up-on-pr**.

The user invoked `/review-pr` on `$ARGUMENTS`. Resolve the argument to a GitHub PR (accept bare numbers, `#123`, or full URLs) via `gh pr view`, then follow the `follow-up-on-pr` skill: read the diff, surface real issues (correctness, security, simplification opportunities), and post review comments via `gh pr review` / `gh api`. Skip nitpicks. If the PR is yours, default to checking whether requested changes have been addressed instead of authoring a new review.
