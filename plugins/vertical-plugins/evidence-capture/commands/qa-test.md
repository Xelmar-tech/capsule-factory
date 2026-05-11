---
description: Run an automated QA test flow against a terminal CLI or web/Electron app
argument-hint: '"<URL>" or "<app-name>" or "<PR-number> [-- focus area]" or "<description>"'
---

# QA Test Command

Drive a terminal, browser, or Electron flow and report step-level pass/fail evidence.

## Workflow

### Step 1: Parse Arguments

Determine target:
- URL → web app
- App name → Electron app
- CLI command → terminal TUI
- PR reference → infer from diff
- Free-text → infer target and flow

### Step 2: Define Test Steps

**Web/Electron:**
1. Open page
2. Wait for load
3. Screenshot
4. Interact with primary UI
5. Verify state changes
6. Screenshot
7. Close

**Terminal:**
1. Launch app
2. Wait for ready
3. Snapshot
4. Exercise primary features
5. Verify output
6. Snapshot
7. Close

### Step 3: Load Skills

Use routing from `capture`, `compose`, `verify`:
- Target route: determine driver
- Stage route: capture + verify
- Artifact route: showcase if polish needed

### Step 4: Capture

Execute test steps. Record evidence at every step.
If a step fails, record the failure and continue.

### Step 5: Compose (if committed)

Assemble into video if recording was requested.

### Step 6: Verify

Check deliverable and QA report completeness.

### Step 7: Report

```
## QA Test Report

**Target:** <URL or app>
**Driver:** <driver>

### Results
| Step | Status | Notes |
|------|--------|-------|
| ... | PASS/FAIL | ... |

### Issues Found
- <description with screenshot/snapshot reference>

### Evidence
<saved to ./qa-results/>
```
