---
name: tuistory
version: 1.0.0
description: |
  Terminal session recorder and player. Use for capturing terminal interactions as `.cast` files.
  Use when recording demos, tutorials, or terminal-based evidence.
---

# Tuistory

Record and replay terminal sessions.

## Recording

```bash
tuistory rec demo.cast
# ... do your work ...
exit
```

## Playback

```bash
tuistory play demo.cast
```

## Convert to Video

```bash
agg demo.cast demo.mp4 --theme asciinema
```

## Tips

- Set consistent terminal size: `stty cols 120 rows 36`
- Use `FORCE_COLOR=3` for color output
- Record in clean environment (no sensitive data)

## Anti-patterns

- **Recording secrets**: Scrub `.cast` files before sharing
- **Inconsistent sizing**: Different sizes break side-by-side layouts
- **No color**: Monochrome recordings are hard to follow
