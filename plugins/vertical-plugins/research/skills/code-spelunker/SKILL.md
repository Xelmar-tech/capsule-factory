---
name: code-spelunker
version: 1.0.0
description: |
  Explore and understand unfamiliar codebases quickly.
  Use when the user asks to "explore the codebase," "find where X is implemented," or "understand how Y works."
---

# Code Spelunker

Navigate and understand unfamiliar code efficiently.

## Workflow

### 1. Get Oriented

Read:
- README.md
- package.json / Cargo.toml / go.mod (dependencies and scripts)
- Directory structure
- Entry points (src/index.ts, main.go, app.py)

### 2. Find the Target

Use search to locate relevant code:
```bash
# Find function definitions
grep -r "function targetName" src/

# Find imports/usage
grep -r "targetName" src/ --include="*.ts"

# Find by pattern
grep -r "class.*Component" src/
```

### 3. Trace the Flow

Follow data flow:
1. Where is it defined?
2. Where is it called?
3. What does it depend on?
4. What depends on it?

### 4. Build a Map

Document your findings:
```
## Code Map: <Feature>

### Entry Point
- File: src/api/routes.ts
- Function: handleRequest()

### Key Files
1. src/services/data.ts — fetches from DB
2. src/models/user.ts — defines User type
3. src/utils/validation.ts — input sanitization

### Data Flow
Request → handleRequest() → validate() → fetchData() → Response

### Gotchas
- Validation happens AFTER auth check (not before)
- DB connection is lazy-initialized
```

## Techniques

### Grepping Effectively

```bash
# Find definitions
grep -rn "export.*function\|export.*class\|export.*const" src/ | grep target

# Find all references
grep -rn "targetName" src/ --include="*.ts"

# Find in specific file types
grep -rn "pattern" src/ --include="*.tsx" --exclude-dir=node_modules
```

### Reading Efficiently

- Start with types/interfaces (contracts)
- Read tests (show expected behavior)
- Skip boilerplate (focus on logic)
- Follow imports (trace dependencies)

## Anti-patterns

- **Reading everything**: Focus on the relevant subsystem
- **Guessing**: Use grep, don't assume
- **Not documenting**: You'll forget what you found
- **Ignoring tests**: Tests reveal intent better than code
