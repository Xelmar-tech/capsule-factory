---
name: ban-type-assertions
version: 1.0.0
description: |
  Ban `as` type assertions in a package via the `@typescript-eslint/consistent-type-assertions` lint rule, replacing every `as X` cast with patterns the compiler can verify.
  Use when the user asks to "remove type assertions," "ban as casts," or "make types safer."
---

# Ban Type Assertions

Remove `as` casts and replace them with type-safe patterns.

## Workflow

### 1. Find Assertions

```bash
npx eslint . --rule '@typescript-eslint/consistent-type-assertions: [error, { assertionStyle: never }]'
```

Or grep:
```bash
grep -r "as " src/ --include="*.ts" --include="*.tsx" | grep -v "as const"
```

### 2. Replace Patterns

| Unsafe | Safe |
|--------|------|
| `value as string` | `typeof value === "string" ? value : ""` |
| `value as User` | `isUser(value) ? value : null` (type guard) |
| `value as any` | `unknown` + proper narrowing |
| `value as string[]` | `Array.isArray(value) && value.every(isString)` |

### 3. Add Type Guards

```typescript
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null &&
    "id" in value && typeof value.id === "string"
}
```

### 4. Configure ESLint

```json
{
  "rules": {
    "@typescript-eslint/consistent-type-assertions": ["error", { "assertionStyle": "never" }]
  }
}
```

### 5. Verify

```bash
npm run lint
npm run typecheck
npm test
```

## Anti-patterns

- **Replacing with `any`**: `as any` → `any` is worse
- **Ignoring edge cases**: Type guard that doesn't check all fields
- **Breaking tests**: Changing types without updating test mocks
