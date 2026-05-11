---
name: compose
version: 1.0.0
description: |
  Assemble captured recordings into polished deliverables: videos, annotated screenshots, comparison images.
  Use as part of demo or verify workflows.
user-invocable: false
---

# Compose

Assemble raw captures into polished deliverables.

## Inputs

- **Clips**: `.cast`, `.mp4`, screenshots
- **Layout**: single | side-by-side
- **Labels**: ["BEFORE", "AFTER"] or ["Branch A", "Branch B"]
- **Speed**: 1x, 2x, 3x (default: 3x for demos)
- **Title**: Demo title
- **Subtitle**: Context
- **Effects**: utilitarian | full | none

## Workflow

### 1. Normalize Clips

Convert `.cast` to `.mp4`:
```bash
agg /tmp/demo.cast /tmp/demo.mp4 --theme asciinema
```

### 2. Assemble

**Single layout:**
- One clip, full frame
- Title card at start

**Side-by-side:**
- Two clips, 50/50 split
- Labels below each panel
- Synchronized playback

### 3. Add Polish

| Effect | When |
|--------|------|
| Zoom | Highlight specific area |
| Spotlight | Focus attention |
| Keystroke overlay | Show key presses |
| Title card | Opening context |

### 4. Render

```bash
ffmpeg -i input.mp4 -vf "..." output.mp4
```

## Output

- Video file: `/tmp/demo-<id>.mp4`
- Resolution: 1920×1080 default
- Duration: matches content

## Handoff

Pass to `verify` skill for quality check.
