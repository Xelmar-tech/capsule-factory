---
name: capture
version: 1.0.0
description: |
  Recording lifecycle for terminal and browser sessions.
  Use as part of demo, verify, or qa-test workflows.
user-invocable: false
---

# Capture

Record terminal sessions, browser interactions, and screenshots.

## Workflow

### 1. Pre-flight

Before recording:
- Terminal size: `--cols 120 --rows 36`
- Browser viewport matches layout (see below)
- Branch/worktree paths correct
- Color env vars set: `FORCE_COLOR=3`, `COLORTERM=truecolor`

### Browser Viewport Sizing

| Layout | Panel Aspect | Recommended Viewport |
|--------|-------------|---------------------|
| single | ~16:9 | 1280×720 or 1440×810 |
| side-by-side | ~8:9 | 960×1000 or 1024×1080 |

### 2. Launch and Record

**Terminal:**
```bash
asciinema rec /tmp/demo.cast --cols 120 --rows 36
```

**Browser:**
```bash
agent-browser open <url>
agent-browser snapshot -i
```

### 3. Execute Script

Follow the interaction script step by step.
Capture evidence at each step.

### 4. Save Outputs

- `.cast` files for terminal
- `.mp4` or screenshots for browser
- Keystroke logs if needed

## Isolation

Use `RUN_ID` for every session:
```bash
RUN_ID="$(date +%s)-$$"
RUN_DIR="$(mktemp -d /tmp/capture-${RUN_ID}-XXXXXX)"
```
