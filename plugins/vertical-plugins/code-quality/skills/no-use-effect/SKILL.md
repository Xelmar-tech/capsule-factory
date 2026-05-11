---
name: no-use-effect
version: 1.0.0
description: |
  Enforce the no-useEffect rule when writing or reviewing React code.
  Use when the user asks to "remove useEffect," "replace useEffect," or "review React code."
---

# No useEffect

Replace `useEffect` with derived state, event handlers, or server state.

## Rules

### When NOT to use useEffect

| Scenario | Better Pattern |
|----------|---------------|
| Deriving state from props | Compute in render or use `useMemo` |
| Syncing state between components | Lift state up, use context, or URL state |
| Fetching data | Server state library (TanStack Query, SWR, RTK Query) |
| Handling events | Event handler functions |
| Form submission | `onSubmit` handler |

### When useEffect IS okay

- Subscribing to external stores
- Setting up non-React event listeners (window resize, etc.)
- Integrating with imperative APIs (canvas, maps, etc.)
- Cleanup on unmount

## Refactoring Patterns

### Derive in render

Before:
```typescript
const [fullName, setFullName] = useState("")
useEffect(() => {
  setFullName(`${firstName} ${lastName}`)
}, [firstName, lastName])
```

After:
```typescript
const fullName = `${firstName} ${lastName}`
```

### Use server state library

Before:
```typescript
const [data, setData] = useState(null)
useEffect(() => {
  fetch("/api/users").then(r => r.json()).then(setData)
}, [])
```

After:
```typescript
const { data } = useQuery({ queryKey: ["users"], queryFn: fetchUsers })
```

## Verification

```bash
npm run lint  # no useEffect warnings
npm test      # behavior preserved
```
