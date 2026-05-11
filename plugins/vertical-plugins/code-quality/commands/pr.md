---
description: Create a pull request with proper conventions
argument-hint: '"<branch-name>" or "<feature description>"'
---

# PR Command

Create a pull request with Conventional Commits and proper body.

## Workflow

### Step 1: Prepare

Ensure branch is clean, commits follow Conventional Commits.

### Step 2: Create PR

Use `create-pr` skill to:
1. Write PR body from template
2. Link Linear issues
3. Create via GitHub MCP

### Step 3: Verify

- PR is accessible
- CI passes
- Reviewers assigned
