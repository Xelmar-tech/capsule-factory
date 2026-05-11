---
description: Create a new skill for the PM team
argument-hint: '"<skill name>" [--from-session] [--plugin <plugin-name>]'
---

# Create Skill Command

Create a new skill following team conventions.

## Workflow

### Step 1: Define Skill

Determine:
- Name (kebab-case)
- Description (when to use it)
- Plugin to host it in
- Scope (one thing well)

### Step 2: Create Structure

```
plugins/vertical-plugins/<plugin>/skills/<skill-name>/
└── SKILL.md
```

### Step 3: Write Skill

Use `skill-creation` skill to:
1. Write YAML frontmatter
2. Document workflow
3. Include verification steps
4. Document anti-patterns

### Step 4: Verify

- Skill loads correctly
- Description is clear
- Instructions are complete
- Examples work

### Step 5: Register

Add to plugin manifest if needed.
