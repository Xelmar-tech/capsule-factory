---
name: true-input
version: 1.0.0
description: |
  Real terminal input injection for authentic keyboard behavior capture.
  Use when you need genuine key events, not simulated typing.
---

# True Input

Inject real keyboard events for authentic terminal behavior.

## When to Use

- Testing keyboard shortcuts
- Verifying key combo behavior
- Capturing genuine escape sequences
- Real terminal rendering proof

## Workflow

### 1. Setup

Ensure terminal is ready:
```bash
# Check terminal capabilities
echo $TERM
tput colors
```

### 2. Inject Input

```bash
# Single key
echo -e '\x01' > /dev/tty  # Ctrl+A

# Sequence
printf '\x1b[H' > /dev/tty  # Home key
```

### 3. Capture Result

```bash
# Screenshot or recording
agent-browser screenshot
# or
tuistory rec session.cast
```

## Platform Notes

### Linux
- Direct `/dev/tty` access
- Wayland: use `ydotool` or `wtype`

### macOS
- `osascript` for key events
- `cliclick` for mouse/keyboard

### Windows
- `SendKeys` in PowerShell
- AutoHotkey scripts

## Anti-patterns

- **Simulating vs injecting**: Simulated typing may not trigger the same behavior
- **Wrong terminal**: Input goes to wrong TTY
- **Timing issues**: Too fast/slow injection misses race conditions
