---
description: Generate a progress report with velocity metrics and status updates
argument-hint: '["weekly" | "sprint" | "epic"] [team or project name]'
---

# Report Command

Generate a progress report from Linear and GitHub data.

## Workflow

### Step 1: Gather Data

Fetch from Linear MCP:
- Issues completed this period
- Issues in progress
- Blocked issues
- Cycle time metrics

Fetch from GitHub MCP:
- PRs merged
- PRs open
- Review turnaround time
- CI failure rate

### Step 2: Calculate Metrics

- Velocity: issues completed per day
- Cycle time: started → completed
- Review latency: PR opened → first review
- WIP limits: issues in progress vs capacity

### Step 3: Generate Report

Structure:
- Executive summary (3-5 bullets)
- Completed work with links
- In-progress work with blockers
- Risks and escalations
- Next period forecast

### Step 4: Humanize

Use `human-writing` skill to remove AI patterns from the report text.
