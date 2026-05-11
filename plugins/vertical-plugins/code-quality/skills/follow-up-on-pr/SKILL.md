---
name: follow-up-on-pr
version: 1.0.0
description: |
  Follow up on an existing PR by rebasing on the base branch, addressing reviewer comments, fixing CI issues, and pushing updates.
  Use when the user asks to "update a PR," "address review comments," or "fix CI."
---

# Follow Up on PR

Keep a PR moving through review to merge.

## Workflow

### 1. Sync with Base

```bash
git fetch origin
git rebase origin/main  # or merge if team prefers
```

Resolve conflicts if any.

### 2. Address Review Comments

For each comment:
- **Accepted**: Make the change, mark as resolved
- **Disagreed**: Reply with reasoning, don't ignore
- **Question**: Answer, don't leave hanging

### 3. Fix CI Issues

If CI fails:
- Read the failure logs
- Fix the root cause (don't just retry)
- Re-push

### 4. Update PR

Push changes:
```bash
git push --force-with-lease  # if rebased
git push  # if merged
```

### 5. Re-request Review

Ping reviewers when ready:
```
@maintainer-jane @reviewer-bob — addressed all comments, ready for another look
```

### 6. Verify

- All comments resolved or responded to
- CI passes
- No new conflicts with base
- Reviewers re-requested

## Anti-patterns

- **Ignoring comments**: Every comment needs a response
- **Force-push without lease**: Can overwrite others' work
- **Fixing symptoms**: Retry CI without fixing root cause
- **Not re-requesting**: PR sits idle after fixes
