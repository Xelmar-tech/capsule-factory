---
description: Generate an internal status report covering the current Linear cycle
argument-hint: '[--since=YYYY-MM-DD | --last=7d | --cycle=<id>]'
---

Load skill: **pm-reporting**.

The user invoked `/report` with `$ARGUMENTS`. Apply the `pm-reporting` skill: resolve the window (default = current Linear cycle), pull epics/tickets/blocks via the Linear MCP, hand off to `scribe` with the `status-report` schema, write `reports/YYYY-MM-DD-status.html`, and print the Slack-paste-ready summary to chat.

Internal audience only. No per-person stats.
