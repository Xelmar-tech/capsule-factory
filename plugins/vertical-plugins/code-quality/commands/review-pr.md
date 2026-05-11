---
description: Review and update an existing PR
argument-hint: '"<PR-number>" [--comments] [--ci]'
---

# Review PR Command

Follow up on an existing pull request.

## Workflow

### Step 1: Fetch PR

Get PR details via GitHub MCP.

### Step 2: Address Comments

Use `follow-up-on-pr` skill to:
1. Rebase if needed
2. Address each review comment
3. Fix CI failures

### Step 3: Push Updates

Push changes and re-request review.

### Step 4: Verify

- All comments resolved
- CI passes
- No conflicts
