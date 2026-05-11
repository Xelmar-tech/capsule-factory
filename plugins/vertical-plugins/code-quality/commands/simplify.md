---
description: Simplify and improve code quality
argument-hint: '"<file-path>" or "<PR-number>"'
---

# Simplify Command

Review code for quality and efficiency improvements.

## Workflow

### Step 1: Read Code

Get the diff or file content.

### Step 2: Analyze

Use `simplify` skill to find:
- Duplication
- Complexity
- Verbosity
- Performance issues

### Step 3: Apply Fixes

Make changes incrementally, one concern per commit.

### Step 4: Verify

```bash
npm test
npm run lint
npm run typecheck
```
