---
name: agent-browser
version: 1.0.0
description: |
  Automate browser interactions for web testing, form filling, screenshots, and data extraction.
  Use when the user asks to "test a web app," "take a screenshot," "fill a form," or "scrape data."
---

# Browser Automation

Drive browsers for testing and data extraction.

## Quick Start

```bash
# Navigate
agent-browser open <url>

# Get interactive elements
agent-browser snapshot -i

# Interact using refs
agent-browser click @e1
agent-browser fill @e2 "text"

# Close
agent-browser close
```

## Commands

### Navigation
```bash
agent-browser open <url>     # Navigate
agent-browser back             # Go back
agent-browser forward          # Go forward
agent-browser reload           # Reload
agent-browser close            # Close
```

### Snapshot
```bash
agent-browser snapshot         # Full accessibility tree
agent-browser snapshot -i      # Interactive elements only
agent-browser snapshot -c      # Compact output
agent-browser snapshot -d 3    # Limit depth
agent-browser snapshot -s "#main"  # Scope to selector
```

### Interactions
```bash
agent-browser click @e1        # Click
agent-browser dblclick @e1     # Double-click
agent-browser hover @e1        # Hover
agent-browser fill @e2 "text"  # Fill input
agent-browser type @e2 "text"  # Type (with key events)
agent-browser press Enter      # Press key
```

### Screenshots
```bash
agent-browser screenshot        # Full page
agent-browser screenshot -s     # Current viewport
```

## Workflow

1. **Open** the target URL
2. **Snapshot** to get element refs
3. **Interact** using refs from snapshot
4. **Re-snapshot** after navigation or DOM changes
5. **Screenshot** for evidence
6. **Close** when done

## Tips

- Use `-i` flag for interactive elements only (faster, less noise)
- Re-snapshot after any navigation or significant DOM change
- Screenshots are full-page by default; use `-s` for viewport-only
- Always close the browser when done

## Anti-patterns

- **Guessing selectors**: Always snapshot first
- **Not re-snapshotting**: Stale refs after navigation
- **Forgetting to close**: Leaves browser processes running
