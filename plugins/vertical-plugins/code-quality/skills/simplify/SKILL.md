---
name: simplify
version: 1.0.0
description: |
  Review changed code for reuse, quality, and efficiency, then fix any issues found.
  Use when the user asks to "simplify code," "review changes," or "improve quality."
---

# Simplify

Review code changes and improve them.

## Workflow

### 1. Read the Changes

Get the diff:
```bash
git diff HEAD~1
```

Or for a PR:
```bash
gh pr diff <number>
```

### 2. Look For

- **Duplication**: Same pattern repeated → extract function/component
- **Complexity**: Nested conditionals → early returns, guard clauses
- **Verbosity**: Unnecessary abstractions → inline if simpler
- **Performance**: Inefficient loops, unnecessary re-renders
- **Readability**: Unclear names, missing comments

### 3. Apply Fixes

Make changes:
- One concern per commit
- Keep tests passing
- Don't change behavior (refactor only)

### 4. Verify

```bash
npm test        # or equivalent
npm run lint    # no new warnings
npm run typecheck  # TypeScript passes
```

## Rules

- **Preserve behavior**: Simplification ≠ functionality change
- **Test coverage**: Don't drop tests unless code is truly gone
- **Incremental**: One simplification at a time, not a mega-refactor
- **Explain**: In commit message, explain WHY the change is simpler

## Example

Before:
```typescript
function getStatus(user) {
  if (user) {
    if (user.isActive) {
      if (user.subscription) {
        return "active"
      }
    }
  }
  return "inactive"
}
```

After:
```typescript
function getStatus(user) {
  if (!user?.isActive) return "inactive"
  return user.subscription ? "active" : "inactive"
}
```
