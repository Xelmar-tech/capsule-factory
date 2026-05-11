---
name: agent-orchestrator
version: 1.0.0
description: |
  Bootstrap an agent team to execute a Linear epic. Use when the user invokes
  "/orchestrate <epic-id>", says "run the team on epic X", "kick off this epic",
  or hands off a planned epic for execution. This skill spawns the epic-conductor
  agent via the Team tool with the appropriate teammates and lets the conductor
  take over.
---

# Agent orchestrator

The job: turn a planned Linear epic into a running team. This skill is **the entry point** invoked by `/orchestrate`. It does not itself coordinate the work — it stands up the team and hands control to epic-conductor.

This skill is also referenced internally by epic-conductor when it needs to (re)spawn a teammate that exited or was added mid-epic.

## 1. Resolve the epic

`$ARGUMENTS` should contain a Linear epic reference: bare ID (`CAP-42`), `#42`, or a full Linear URL. Resolve via the Linear MCP to fetch:

- Epic title and body
- Current child tickets (state, assignee, parent)
- Project / team
- Existing labels and metadata

If `$ARGUMENTS` is empty, list the user's recent epics from Linear and ask which one. Do not pick automatically.

## 2. Pre-flight: environment

Before spawning any teammate, ensure the working repo has its env materialized. Run the **manage-secrets** skill (from the `infra` plugin) with `capxul dev` (or whatever the repo's default is). If the user's Bitwarden MCP is not connected, point them at `/capsule-setup` and stop. Do not spawn agents into a half-configured environment — they'll waste a turn discovering env failures.

## 3. Decide the team composition

Read the epic body and child tickets to figure out which teammates the epic needs. Defaults:

| Always include | Conditional                                                                          |
|----------------|---------------------------------------------------------------------------------------|
| epic-conductor | implementer (any coding work)                                                         |
|                | analyst (if epic touches auth, secrets, payments, external surfaces)                  |
|                | qa-capture (if epic body mentions "demo", "verify", "evidence", or has user-facing UI) |
|                | debug-guru (if epic body mentions "investigation", "debug", or "intermittent")        |

Err on the side of including a teammate — the conductor can choose not to call them. Excluding a teammate is harder to undo than including one and ignoring them.

## 4. Spawn the team

Use the **Team tool** (`TeamCreate`). The conductor is the team owner; other teammates are members. Suggested call shape:

```
TeamCreate({
  name: "<epic-id>-<short-epic-slug>",
  owner: "epic-conductor",
  members: ["implementer", "analyst", "qa-capture", "debug-guru"],  // adjust per step 3
  context: {
    epic_id: "<linear-id>",
    epic_url: "<linear-url>",
    repo: "<absolute-path-to-current-repo>",
    config: "<contents of .capsule-factory.yml>",
  }
})
```

Pass the epic context in the team's shared context so every teammate starts informed.

## 5. Hand off to the conductor

After `TeamCreate` returns the team handle, send the initial message to epic-conductor:

> Epic <id> is live. Read the epic body and current ticket state, then plan the first wave of work and dispatch teammates via SendMessage. You own the team until every child ticket reaches a terminal status.

Print to the user:
- Team name and handle
- Members included (and why)
- A pointer: "Tail the team with `TaskOutput({name: '<team-name>'})` or wait for completion."

Then exit. The conductor takes it from here.

## What this skill does NOT do

- It does not create child tickets. The conductor does that as work surfaces.
- It does not modify code, push commits, or open PRs. Implementer does that.
- It does not write reports. pm-reporting + scribe do that.
- It does not loop / wait for completion. Spawning is a one-shot — the team runs autonomously after.
- It does not fan out via Task tool sub-agents. The Team tool is the orchestration primitive, not Task.
