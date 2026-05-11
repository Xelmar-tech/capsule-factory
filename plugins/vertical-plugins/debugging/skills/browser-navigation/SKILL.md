---
name: browser-navigation
version: 1.0.0
description: |
  Automate browser interactions for web testing, form filling, screenshots, and data extraction.
  Use when the user asks to "test a web app," "take a screenshot," "fill a form," or "scrape data."
---

# Browser Navigation

Drive browsers for testing and debugging.

## Quick Start

```bash
# Open page
agent-browser open <url>

# Get interactive elements
agent-browser snapshot -i

# Click, fill, type
agent-browser click @e1
agent-browser fill @e2 "text"

# Screenshot
agent-browser screenshot

# Close
agent-browser close
```

## Workflow

1. **Open** target URL
2. **Snapshot** to get element refs (`@e1`, `@e2`)
3. **Interact** using refs
4. **Re-snapshot** after navigation or DOM changes
5. **Screenshot** for evidence
6. **Close** when done

## Tips

- Use `-i` for interactive elements only (faster)
- Re-snapshot after any navigation
- Screenshots are full-page by default
- Always close the browser when done

## Anti-patterns

- Guessing selectors: Always snapshot first
- Not re-snapshotting: Stale refs after navigation
- Forgetting to close: Leaves browser processes running
