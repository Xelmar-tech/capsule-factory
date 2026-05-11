---
name: wiki
version: 1.0.0
description: |
  Generate comprehensive codebase documentation for a repository.
  Use when the user asks to "document the codebase," "create a wiki," or "generate docs."
---

# Wiki Generation

Read a repository and produce interconnected documentation.

## Workflow

### 1. Survey

Read:
- README.md, AGENTS.md, CONTRIBUTING.md
- package.json / Cargo.toml / go.mod
- docs/ directory
- Entry points
- CI/CD config
- Directory structure

### 2. Discover Topics

Find subsystems:
- Feature flags → capabilities
- API endpoints → domains
- Frontend routes → user features
- Service classes → background systems

### 3. Tier Topics

| Tier | Coverage |
|------|----------|
| Tier 1 | Core subsystems — full dedicated page |
| Tier 2 | Important but specialized — shorter page |
| Tier 3 | Niche — paragraph in "Other" page |

### 4. Write Pages

For each topic:
```
## Topic Name

### Purpose
[What this does and why]

### Key Files
- src/services/data.ts
- src/models/user.ts

### Data Flow
[How data moves through]

### API / Interface
[Public methods, types]

### Gotchas
[Non-obvious behaviors]
```

### 5. Link Pages

Cross-reference related topics:
```
See also: [Authentication](./auth.md), [Database](./db.md)
```

### 6. Output

Generate `wiki/` directory with:
- index.md (overview)
- One file per Tier 1/2 topic
- other.md (Tier 3 topics)

## Anti-patterns

- **Shallow coverage**: Only reading top-level files
- **Missing cross-references**: Pages in isolation
- **Outdated info**: Not reflecting actual code
- **Too much detail**: Focus on architecture, not every function
