---
name: evidence-pipeline
version: 1.0.0
description: |
  Orchestration glue over the evidence-capture vertical: capture → compose → verify →
  showcase as one continuous flow. Use when qa-capture is dispatched to verify a PR or
  produce a demo, vs invoking capture/compose/verify/showcase piecemeal. Handles the
  routing between target-type (CLI / web / Electron / TUI) and stage (capture / compose
  / verify / showcase).
---

# Evidence pipeline

The job: drive the QA flow end-to-end. The underlying skills (`capture`, `compose`, `verify`, `showcase`, plus the target-drivers `agent-browser`, `agent-control`, `agent-cli`, `pty-capture`, `tuistory`, `true-input`) each handle one stage or one target type. This skill composes them into a coherent run.

This skill exists because qa-capture invocations almost always need **all four stages** in order, and composing them ad-hoc per session means re-deriving the routing table every time.

## When to use

- qa-capture is dispatched to verify a PR — runs the full pipeline
- The user invokes `/demo` or `/verify` — those commands route in via this skill
- Explicit user request: "drive the full QA flow on this change"

For one-off stages ("just give me a screenshot of the login page"), call the underlying skills directly. This skill is the orchestrator, not the only way in.

## Pipeline stages

```
┌─────────┐    ┌─────────┐    ┌────────┐    ┌──────────┐
│ Capture │ -> │ Compose │ -> │ Verify │ -> │ Showcase │
└─────────┘    └─────────┘    └────────┘    └──────────┘
   raw            curated        claims         polished
   recording      timeline       checked        deliverable
```

Each stage produces input for the next.

### Stage 1 — Capture

Capture raw recordings of the target executing the test script. The right driver depends on the target:

| Target           | Driver skill              |
|------------------|----------------------------|
| Web app (Chrome) | `agent-browser`            |
| Native macOS app | `agent-control`            |
| CLI / TUI        | `agent-cli` + `pty-capture`|
| Mixed (CLI + UI) | `agent-control` (coordinates) |

For comparison demos (before / after, two branches), capture **both branches** with identical scripts. The compose stage assumes paired inputs.

### Stage 2 — Compose

Take raw captures and produce a curated timeline:

- Trim dead air (idle waits, page-load spinners > 2s)
- Apply effects (zoom on the interaction point, keystroke overlays if user input is critical, callouts on UI changes)
- Lay out side-by-side if comparison, single-track otherwise
- Render to MP4 via the `compose` skill (uses Remotion under the hood)

Effects tier (set during capture's `/demo` planning, default to **utilitarian** for verify, **full** for showcase):

| Tier         | Includes                                           |
|--------------|----------------------------------------------------|
| utilitarian  | Zoom for readability, keystroke overlay            |
| full         | Zoom + keystroke + spotlight + callout             |
| none         | Raw recording trimmed only                         |

Output: `reports/media/YYYY-MM-DD-pr<n>-<scene>.mp4`.

### Stage 3 — Verify

Walk the claims list from the qa-capture agent's Step 1 (claim extraction). For each:

- Run the captured method
- Observe the result against the expected / null hypothesis
- Assign `ok` / `warn` / `crit` verdict

This stage uses the `verify` skill. Its output is the structured verdict payload that scribe will turn into the verify-report HTML.

### Stage 4 — Showcase (conditional)

Only run this stage if the deliverable is **polished** — meant to be shared beyond the PR (a launch demo, a marketing-adjacent clip, a hero video for a landing page). For a normal PR-verification, **skip showcase**.

If running, the `showcase` skill applies the selected preset (`factory`, `factory-hero`, `hero`, `presentation`, `minimal`, `macos`) — wraps the composed MP4 in branded frames, adds intro/outro, etc.

Output: `reports/media/YYYY-MM-DD-pr<n>-showcase.mp4`.

## Routing rules

When this skill is invoked, decide:

1. **Targets** — what surfaces does the PR touch? (web, native, CLI, mixed)
2. **Stages** — which stages to run? (always 1+2+3 for verify; +4 for explicit showcase)
3. **Layout** — comparison (before/after) or single-track? (comparison when the PR is a fix or a perf change; single-track for new features)
4. **Effects tier** — utilitarian (default), full (showcase), none (explicit opt-out)

Load each target's driver skill before running its stage. Don't load all the target drivers upfront — they have heavy contexts.

## Output

Produce a payload for the qa-capture agent to hand to scribe:

```yaml
title: "Verify — PR #<n>: <pr-title>"
pr_url: <github-url>
claims:
  - claim: "<from agent's Step 1>"
    method: "<exact actions taken>"
    observed: "<what happened>"
    verdict: "ok | warn | crit"
    evidence:
      - kind: "video" | "screenshot" | "log" | "snippet"
        ref: "<relative path>"
        caption: "<one line>"
overall_verdict: "ok | warn | crit"
```

The qa-capture agent then calls scribe with this payload.

## What this skill does NOT do

- Does not extract claims from the PR. That's the qa-capture agent's job (Step 1 in its loop).
- Does not write the final HTML. That's scribe.
- Does not post the PR comment. That's the qa-capture agent.
- Does not push code, modify the working tree, or run unit tests. CI handles unit tests; you handle behavioral verification.

## Failure handling

- **Can't start the dev server** — stop the pipeline, report the blocker to qa-capture (which messages conductor).
- **A capture is corrupted** — re-run that one stage (capture) before re-running compose; don't redo the whole pipeline.
- **A verify verdict is `crit`** — still produce the report; the verdict goes into the payload as `crit` and the qa-capture agent decides whether to file a child ticket.
