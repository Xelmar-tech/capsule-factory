---
description: Create a pull request for the current branch
argument-hint: '[optional notes or scope hints]'
---

Load skill: **create-pr**.

The user invoked `/pr` on the current branch. Follow the `create-pr` skill end-to-end: audit the diff, draft a title and body that reflect what actually changed, push the branch if needed, and open the PR. If `$ARGUMENTS` is non-empty, treat it as additional context or scope hints from the user (e.g., "draft only", "target staging", "split into two PRs") and adjust accordingly.

Do not silently include unstaged or unrelated changes. If the branch is dirty in a way that looks unintentional, ask before proceeding.
