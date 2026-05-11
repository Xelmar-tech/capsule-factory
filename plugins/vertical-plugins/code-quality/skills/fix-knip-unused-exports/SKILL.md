---
name: fix-knip-unused-exports
version: 1.0.0
description: |
  Fix knip "Unused exports" violations. Handles all violation categories: test-only exports, dead barrel re-exports, and internally-only usage.
  Use when knip reports unused exports or the user asks to "clean up exports."
---

# Fix Knip Unused Exports

Clean up unused exports reported by knip.

## Workflow

### 1. Run Knip

```bash
npx knip
```

### 2. Categorize Violations

| Category | Action |
|----------|--------|
| **Test-only exports** | Move to `__tests__/` or mark with `// @knipignore` |
| **Dead barrel re-exports** | Remove from barrel file |
| **Internally-only** | Remove `export` keyword |
| **Actually unused** | Delete the code |

### 3. Apply Fixes

For each violation:
- Check if it's truly unused (not imported anywhere)
- If used in tests only: consider if it should be exported
- If barrel re-export: remove from index.ts
- If internal: remove export keyword

### 4. Verify

```bash
npx knip        # should be clean
npm run build   # no broken imports
npm test        # tests pass
```

## Anti-patterns

- **Mass-deleting**: Check each export before removing
- **Ignoring warnings**: Knip reports are usually correct
- **Breaking public API**: Don't remove exports consumed by other packages
