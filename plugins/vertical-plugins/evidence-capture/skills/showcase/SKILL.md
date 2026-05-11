---
name: showcase
version: 1.0.0
description: |
  Visual polish for demo videos: window chrome, branded frames, cinematic backgrounds.
  Use when the deliverable needs to be presentation-ready.
user-invocable: false
---

# Showcase

Add visual polish to demo recordings.

## Presets

| Preset | Use Case |
|--------|----------|
| **macos** | Default, clean desktop look |
| **hero** | Marketing, landing pages |
| **presentation** | Slide decks, talks |
| **minimal** | Docs embeds, inline |
| **factory** | Branded, official |
| **factory-hero** | Branded marketing |

## Elements

### Window Chrome
- Rounded corners
- Title bar with traffic lights
- Subtle shadow

### Background
- Gradient or texture
- Floating particles (optional)
- Brand color accent

### Title Card
- Project name
- Feature title
- Date/version

### Outro
- Logo/wordmark
- Call to action
- Links

## Workflow

### 1. Choose Preset

Match preset to audience:
- Internal team → `macos` or `minimal`
- External stakeholders → `hero` or `presentation`
- Public/marketing → `factory-hero`

### 2. Apply Layers

```
Background + FloatingParticles
  → Window Chrome + Content
    → Title Card (opening)
    → Content clips
    → Keystroke overlays
    → Spotlight/Zoom effects
    → Outro
```

### 3. Render

Use ffmpeg or Remotion for final output.

## Output

- Polished `.mp4` ready for sharing
- Consistent branding across all demos
