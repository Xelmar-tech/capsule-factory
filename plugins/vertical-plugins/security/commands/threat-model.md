---
description: Generate a STRIDE threat model for the repository
argument-hint: '["full" | "quick"] [component or epic name]'
---

# Threat Model Command

Create a security threat model for a codebase or component.

## Workflow

### Step 1: Understand Scope

Determine what to model:
- Full repository
- Specific component
- New feature/epic

### Step 2: Generate

Use `threat-model-generation` skill to:
1. Identify assets
2. Apply STRIDE to each component
3. Score risks

### Step 3: Output

Generate threat model document with:
- Assets list
- Threats table
- Mitigations
- Risk scores

### Step 4: Review

Ensure all critical/high risks have mitigations with owners and deadlines.
