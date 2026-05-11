---
name: pm-reporting
version: 1.0.0
description: |
  Generate an internal status report covering the current Linear cycle's epics, tickets,
  and progress. Use when the user says "/report", "give me a status update", "what's
  shipped this week", or asks for an internal team status. Writes an HTML report via the
  scribe skill (status-report schema) to reports/YYYY-MM-DD-status.html.
---

# PM reporting

The job: read Linear's current cycle state, summarize what's in flight, what closed, what's blocked, and emit an HTML status report committed to the repo. Audience is internal (you and the Capxul team) — terse, factual, no narrative padding.

## 1. Resolve time window

`$ARGUMENTS` may contain a window override:
- No args → current Linear cycle (default)
- `--since=YYYY-MM-DD` → explicit start date through now
- `--last=7d` / `--last=30d` → rolling window
- `--cycle=<id>` → specific cycle

Default: read the active cycle from Linear via MCP. If no cycle is active (Linear team doesn't use cycles), fall back to rolling 7 days and note this in the report.

## 2. Resolve Linear target

Read `.capsule-factory.yml` for `linear.team`. If the config is missing, ask which team. Do not generate a report against the wrong team.

## 3. Pull data from Linear

Via the Linear MCP, in this order:

- **Active cycle metadata** — name, start/end, current day-of-cycle
- **Epics in flight** — epics in the cycle (or touched within the window), with status and owner
- **Tickets touched in window** — list with: id, title, state, assignee, last update, parent epic
- **Tickets closed in window** — same shape, grouped by epic
- **Blocked tickets** — anything with a "blocked" label or in a `Blocked` status
- **Tickets without an owner** — surfaced as a coordination gap

Do not pull anything beyond Linear. GitHub data, commit data, Slack data, and similar are out of scope for this skill. If the user wants PR / commit data, that's a different report.

## 4. Compute summary metrics

- Tickets opened this window
- Tickets closed this window
- Tickets in progress (active, not closed)
- Net velocity (closed minus opened)
- Cycle health: % of cycle elapsed vs % of ticketed work closed (rough proxy)

Round numbers. Do not over-engineer the metrics — this is a status report, not a dashboard.

## 5. Hand off to scribe (status-report schema)

Call the `scribe` skill with kind `status-report`. Pass:

```yaml
title: "<team> — <cycle name or window>"
generated_at: <ISO timestamp>
window: <human-readable, e.g. "Cycle 14 (day 6 of 14)" or "last 7 days">
summary:
  opened: <N>
  closed: <N>
  in_progress: <N>
  net: <signed N>
sections:
  - heading: Epics in flight
    items: [...]
  - heading: Closed this window
    items: [...]
  - heading: In progress
    items: [...]
  - heading: Blocked
    items: [...]
  - heading: Owner-less tickets
    items: [...]
slack_summary: |
  3–5 bullet points of the most important deltas, paste-ready into Slack.
```

scribe emits the HTML. This skill does not template HTML directly.

## 6. Write to disk

Target path: `reports/YYYY-MM-DD-status.html` at the repo root. If `reports/` doesn't exist, create it. If a status report for today already exists, suffix with `-1`, `-2`, etc.

## 7. Surface the Slack-paste summary

After writing the file, print the `slack_summary` block to chat as plain markdown bullets. The user copies this into Slack without opening the HTML. The HTML is for archive / detail review.

## What this skill does NOT do

- Does not post to Slack. The user pastes.
- Does not include per-person stats. Velocity-per-engineer is a toxic comparison that does not belong in team reports.
- Does not write client-facing reports. This is internal only. If the user wants a client report, they ask reporter (oh wait — there is no reporter agent; this skill handles all reporting). If a client format is ever needed, add `--for=client` and pass a different schema to scribe.
- Does not pull data from GitHub, commits, or other sources. Linear only.
