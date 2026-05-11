---
name: pm-reporting
version: 1.0.0
description: |
  Generate progress reports, velocity metrics, and status updates for stakeholders.
  Use when the user asks for "a report," "velocity metrics," or "status update."
---

# PM Reporting

Generate evidence-based progress reports from Linear and GitHub data.

## Workflow

### 1. Gather Data

**Linear (via MCP):**
- Issues: created, completed, in-progress, blocked
- Cycle time: started → completed
- Team velocity: issues/week
- Epic progress: % complete

**GitHub (via MCP):**
- PRs: opened, merged, closed without merge
- Review latency: opened → first review
- CI metrics: pass/fail rate
- Code churn: lines changed

### 2. Calculate Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Velocity | Issues completed / week | Baseline + trend |
| Cycle Time | Started date → Completed date | < 5 days |
| Review Latency | PR opened → First review | < 24 hours |
| WIP | Issues in progress | < team size × 2 |
| Throughput | PRs merged / week | Steady or growing |

### 3. Structure the Report

```
## Executive Summary (3-5 bullets)

## Completed This Period
- Issue #123 — Feature X (link)
- PR #456 — Refactor Y (link)

## In Progress
- Issue #789 — Feature Z (50% complete, no blockers)

## Blocked / At Risk
- Issue #101 — Waiting for API contract (escalated to backend team)

## Metrics
- Velocity: 8 issues/week (↑ from 6)
- Cycle time: 3.2 days (↓ from 4.1)
- Review latency: 18 hours (↓ from 28)

## Forecast
- Next sprint: 10 issues planned
- Risks: API dependency may delay 2 issues
```

### 4. Humanize Output

Use `human-writing` skill to remove AI patterns:
- "The team completed 8 issues this week" → "We shipped 8 issues this week"
- "Velocity has increased" → "We're moving faster"
- "There are blockers" → "Two issues are stuck"

## Output Formats

- **Markdown**: For GitHub, Linear comments
- **HTML**: For stakeholder dashboards
- **Slide deck**: For exec reviews (use `visual-design` skill)

## MCP Calls

```
mcp__linear__issues(filter: { state: { eq: "completed" }, updatedAt: { gt: "2026-01-01" } })
mcp__github__pullRequests(state: MERGED, since: "2026-01-01T00:00:00Z")
```
