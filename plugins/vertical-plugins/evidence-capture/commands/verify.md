---
description: Test a claim about behavior and report whether the evidence supports or refutes it
argument-hint: '"<claim to test>" or "<PR-number> -- <specific claim>"'
---

# Verify Command

Test a claim as an investigator and report whether evidence confirms or refutes it.

## Workflow

### Step 1: Parse Arguments

Determine:
- Direct claim or PR reference + claim
- Evidence type: screenshot, text snapshot, byte capture
- Comparison: before/after or single-state
- Video proof: yes/no
- Showcase: yes/no

### Step 2: Understand What to Test

Determine the single specific behavior to observe.
What would a skeptic need to see?

### Step 3: Load Skills

Use routing from `capture`, `compose`, `verify`:
- Target route: determine driver
- Stage route: capture + verify (+ compose if video)
- Artifact route: showcase if committed

### Step 4: Capture

Record the behavior. If it doesn't match the claim, capture the actual state.

### Step 5: Compose (if committed)

Assemble into video if video proof was requested.

### Step 6: Verify

Check deliverable against commitments.

### Step 7: Report

```
## Verify: <claim>

**Environment:** <driver, terminal/browser, OS>
**Branch:** <branch name or commit>

### Evidence
<snapshots, screenshots, byte captures, or video path>

### Conclusion
**CONFIRMED** | **REFUTED** | **INCONCLUSIVE**

<explanation>
```

### When Refuted
1. State expected behavior
2. State observed behavior
3. Include evidence inline
4. Note environmental factors
