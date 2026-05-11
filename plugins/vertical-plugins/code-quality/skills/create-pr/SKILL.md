---
name: create-pr
version: 1.0.0
description: |
  Create a pull request with Conventional Commits formatting, a templated body, and local verification.
  Use when the user asks to "create a PR," "open a PR," or "put code up for review."
---

# Create PR

Create a pull request with proper conventions and verification.

## Workflow

### 1. Prepare Branch

Ensure:
- Branch is up to date with base
- Commits follow Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`)
- Changes are focused and reviewable (< 500 lines ideal)

### 2. Write PR Body

Template:
```markdown
## What
[One-paragraph description of the change]

## Why
[Context: what problem this solves, why now]

## How
[Key implementation decisions, tradeoffs]

## Testing
[How this was tested, what to verify]

## Screenshots / Evidence
[If UI change, include screenshots or demo links]
```

### 3. Create PR

Use GitHub MCP:
```
mcp__github__createPullRequest
  title: "feat: add OAuth login flow"
  body: "..."
  head: "feature/oauth-login"
  base: "main"
  draft: false
```

### 4. Link Linear Issues

In PR body:
```
Closes LINEAR-123
Related to LINEAR-456
```

### 5. Verify

- PR is created and accessible
- CI checks pass (if enabled)
- Reviewers are assigned
- Linked to correct Linear issues

## Anti-patterns

- **Giant PRs**: >1000 lines — break into smaller PRs
- **Missing context**: "Fix bug" — which bug? How was it broken?
- **No testing notes**: Reviewer doesn't know how to verify
- **Unlinked issues**: PR exists in vacuum, no tracking
