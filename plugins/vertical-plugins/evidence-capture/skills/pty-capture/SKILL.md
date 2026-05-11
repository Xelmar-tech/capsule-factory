---
name: pty-capture
version: 1.0.0
description: |
  Capture raw terminal byte sequences for low-level debugging.
  Use when investigating keyboard encoding, escape sequences, or terminal rendering issues.
---

# PTY Capture

Capture raw terminal bytes for debugging.

## When to Use

- Keyboard encoding issues
- Escape sequence problems
- Terminal rendering bugs
- Byte-level verification

## Workflow

### 1. Start Capture

```bash
script -q /tmp/terminal.log
```

### 2. Reproduce Issue

Perform the interaction that shows the problem.

### 3. Stop Capture

```bash
exit
```

### 4. Analyze

```bash
xxd /tmp/terminal.log | head -50
```

Look for:
- Escape sequences (`\x1b[`)
- UTF-8 encoding
- Control characters

## Platform Notes

### Linux
- Use `script` or `ttyrec`
- Wayland: may need `true-input` for real rendering

### macOS
- `script` available by default
- Terminal.app vs iTerm2 differences

### Windows
- Use Windows Terminal or WSL
- PowerShell: `Start-Transcript`

## Output

- Raw byte log
- Hex dump for analysis
- Timing information (if available)

## Anti-patterns

- **Not reproducing the issue**: Capture must include the problem
- **Analyzing without context**: Need to know what SHOULD happen
- **Ignoring timing**: Some issues are race conditions
