---
name: debug-pipeline
version: 1.1.0
description: |
  Orchestration glue over the debugging vertical: browser-navigation, http-toolkit-intercept,
  frontend-design, and PostHog runtime evidence (plus evidence-capture target drivers when
  reproduction needs them). Use when debug-guru is dispatched on a multi-layer bug that
  touches browser + network + frontend state, or when production/staging telemetry can
  narrow the investigation. For single-layer bugs, call the underlying skill directly.
---

# Debug pipeline

The job: orchestrate the layered tooling debug-guru needs to chase down bugs that span the browser, the network, and the frontend's internal state. Each underlying skill handles one layer; this skill composes them so you can instrument all three at once when needed.

## When to use

- Bug spans 2+ layers (e.g., a UI behavior that depends on a specific network response shape)
- Reproduction needs simultaneous instrumentation (e.g., capture DOM state at the moment a request is sent)
- The bug is intermittent and you need to capture context across multiple attempts
- Long-running debug session that will reset between hypotheses

For single-layer bugs, call the layer's skill directly:
- DOM/UI state → `frontend-design`
- Network only → `http-toolkit-intercept`
- Browser navigation only → `browser-navigation`
- Runtime telemetry → `posthog-investigate` / `observability-analyst`

## The layer model

```
        ┌─────────────────────────────┐
        │  Browser (navigation,       │  browser-navigation
        │  page lifecycle, console)   │  agent-browser (evidence-capture)
        ├─────────────────────────────┤
        │  Frontend (React state,     │  frontend-design
        │  component tree, hooks)     │
        ├─────────────────────────────┤
        │  Network (requests,         │  http-toolkit-intercept
        │  responses, latency)        │
        ├─────────────────────────────┤
        │  Backend (logs, traces)     │  Bash + tailing logs
        ├─────────────────────────────┤
        │  Runtime observability      │  posthog-investigate /
        │  (errors, logs, replays,    │  observability-analyst
        │  flags, analytics, SDK)     │
        └─────────────────────────────┘
```

Most hard bugs live at the seams between layers — the network responded with X but the frontend showed Y; the click handler fired but the page didn't navigate. Identify the seam first, then instrument **both sides of the seam** at once.

## Workflow

### 1. Identify the seam

From the symptom, figure out which two adjacent layers are disagreeing. Don't instrument all four — narrow to the pair where the disagreement happens.

| Symptom                                    | Likely seam               |
|--------------------------------------------|----------------------------|
| "Click does nothing"                       | Browser ↔ Frontend         |
| "API returned 200 but UI shows error"      | Frontend ↔ Network         |
| "Request never sent"                       | Frontend ↔ Network         |
| "Response is wrong"                        | Network ↔ Backend          |
| "Works in dev, not in prod"                | Network (env/CORS) or Backend (config) |
| "Intermittent — sometimes works"           | Race across two layers; need timestamps |
| "Users saw errors in prod"                 | Runtime observability ↔ Code/Backend |
| "Event/flag/replay proves X"               | Runtime observability ↔ Frontend/Backend |

### 2. Set up the instrumentation

For the identified seam, load the relevant pair of skills and set up the captures **before** reproducing:

- Browser ↔ Frontend: `browser-navigation` to drive, `frontend-design` to read React state at known points (use the `useDebugValue` / DevTools hook trick, or temporary `console.log` injections)
- Frontend ↔ Network: `frontend-design` to read state, `http-toolkit-intercept` to capture the requests and responses with timestamps
- Network ↔ Backend: `http-toolkit-intercept` plus Bash-tailing the backend logs
- Runtime observability ↔ Code/Backend: `posthog-investigate` or `observability-analyst` to identify error groups, events, logs, traces, sessions, SDK health, and flag state; then map those identifiers to code paths before local reproduction or instrumentation

Use the `evidence-capture` target drivers (`agent-browser`, `agent-cli`) to **drive** the reproduction reliably. Manual clicking is fine for one-off; for an intermittent bug you need scripted repro across many runs.

### 3. Reproduce with capture

Run the reproduction. Save the trace. For intermittent bugs, run 5–20 times — the variation between runs is the signal.

### 4. Cross-reference timestamps

The trace from each layer has its own clock. Align them on a known event (the first request, the first paint, etc.) so you can see "at T+340ms, the frontend dispatched action X; at T+345ms, the network sent request Y; at T+520ms, the response came back; at T+540ms, the frontend updated state — but the component didn't re-render until T+1800ms."

Cross-referencing is where the bug usually reveals itself.

### 5. Form the next hypothesis or conclude

If the trace shows the root cause, write it up via debug-guru's Step 5. If it narrows the seam to a different layer, repeat with new instrumentation. **Change one variable per iteration** — adding multiple changes at once means you can't tell what mattered.

### 6. Clean up

Before exiting, **remove any instrumentation you added to the working tree**:
- Temporary `console.log` injections
- Test fixtures created just for this debug session
- HTTP toolkit configurations that shouldn't persist

Either clean them up directly or hand a list to debug-guru's cleanup step.

## Routing reference

| Layer        | Primary skill              | Target driver (for reproduction)         |
|--------------|----------------------------|-------------------------------------------|
| Browser      | `browser-navigation`       | `agent-browser` (Chrome MCP / Playwright)|
| Frontend     | `frontend-design`          | (driven via browser)                      |
| Network      | `http-toolkit-intercept`   | (proxy)                                   |
| Runtime observability | `posthog-investigate` / `observability-analyst` | PostHog MCP |
| TUI / CLI    | (not in debugging vertical)| `agent-cli` + `pty-capture` (evidence-capture) |

For CLI/TUI debugging, the evidence-capture drivers replace browser-level tools. The seam model still applies — CLI ↔ Network is the most common cross-layer CLI bug.

## What this skill does NOT do

- Does not propose fixes. Debug-guru's Step 5 writeup proposes the fix.
- Does not write production-ready code. Patches in the writeup are illustrative; implementer rewrites them.
- Does not run unit tests. CI handles unit tests; this pipeline handles runtime debugging.
- Does not capture polished demos. Use `evidence-pipeline` (qa-capture) for that.
