---
name: verify
version: 1.0.0
description: |
  Check deliverables against original commitments.
  Use as the final stage of demo, verify, or qa-test workflows.
user-invocable: false
---

# Verify

Check that deliverables match what was promised.

## Inputs

- **Original commitments**: What the command promised
- **Deliverable**: The actual output
- **Evidence**: Screenshots, recordings, logs

## Checklist

### Technical Quality
- [ ] Resolution correct (1920×1080 for videos)
- [ ] Duration reasonable (not too short/long)
- [ ] Audio sync (if applicable)
- [ ] No corruption or artifacts

### Content Completeness
- [ ] All promised features shown
- [ ] Before/after states visible (if comparison)
- [ ] Disambiguating evidence present
- [ ] No missing steps

### Commitments Met
- [ ] Layout matches promise (single/side-by-side)
- [ ] Showcase wrapping if committed
- [ ] Keystroke overlay if committed
- [ ] Effects tier matches commitment

## Report

```
## Verification: <deliverable name>

### Commitments
- [x] Layout: side-by-side
- [x] Showcase: yes
- [ ] Keystrokes: missing

### Technical
- Resolution: 1920×1080 ✓
- Duration: 2:34 ✓

### Content
- All features shown: ✓
- Disambiguating evidence: ✓

### Verdict: PASS (with note: keystroke overlay missing)
```

## Anti-patterns

- **Skipping verification**: Every deliverable gets checked
- **Soft failures**: "Good enough" — be precise
- **Missing evidence**: Claims without proof
