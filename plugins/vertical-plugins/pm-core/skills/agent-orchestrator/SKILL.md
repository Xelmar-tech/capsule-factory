---
name: agent-orchestrator
version: 1.0.0
description: |
  Bootstrap an agent team to execute a Linear epic. Use when the user invokes
  "/orchestrate <epic-id>", says "run the team on epic X", "kick off this epic",
  or hands off a planned epic for execution. In Claude, this skill uses the Team
  tool. In Codex, it uses installed custom subagents from `.codex/agents/`.
---

# Agent orchestrator

The job: turn a planned Linear epic into a running team. This skill is **the entry point** invoked by `/orchestrate` in Claude or `$agent-orchestrator` in Codex. It does not itself coordinate the work — it stands up the team and hands control to epic-conductor.

This skill is also referenced internally by epic-conductor when it needs to (re)spawn a teammate that exited or was added mid-epic.

## Runtime mapping

Capsule Factory supports both Claude and Codex runtimes:

| Concept | Claude | Codex |
|---|---|---|
| Team bootstrap | Claude `TeamCreate` | Parent Codex session spawning custom subagents |
| Teammate dispatch | Claude `SendMessage` | Parent Codex session sends scoped prompts to subagents |
| Completion collection | Claude `TaskOutput` | Parent Codex session waits for subagent results |
| Agent definitions | `agents/*.md` inside plugins | `.codex/agents/*.toml` in the consuming repo |

Do not use Claude runtime tool names as Codex instructions. In Codex, first ensure `$capsule-setup` has installed the custom agent templates into `.codex/agents/`.

## 1. Resolve the epic

`$ARGUMENTS` should contain a Linear epic reference: bare ID (`CAP-42`), `#42`, or a full Linear URL. Resolve via the Linear MCP to fetch:

- Epic title and body
- Current child tickets (state, assignee, parent)
- Project / team
- Existing labels and metadata

If `$ARGUMENTS` is empty, list the user's recent epics from Linear and ask which one. Do not pick automatically.

## 2. Pre-flight: environment

Before spawning any teammate, ensure the working repo has its env materialized. Run the **manage-secrets** skill (from the `infra` plugin) with `capxul dev` (or whatever the repo's default is). If the user's Bitwarden or Vaultwarden integration is not connected, point them at `/capsule-setup` in Claude or `$capsule-setup` in Codex and stop. Do not spawn agents into a half-configured environment — they'll waste a turn discovering env failures.

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

### Claude

Use the Claude Team tool. The conductor is the team owner; other teammates are members. Suggested call shape:

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

### Codex

Use Codex custom subagents. The parent Codex session should spawn `epic-conductor` first, then spawn teammates only when the conductor requests them. Suggested parent prompt to the conductor:

```text
Epic <id> is live.
Repo: <absolute-path-to-current-repo>
Config: <contents of .capsule-factory.yml>
Read the epic body and current ticket state, then plan the first wave of work.
For each teammate needed, return an exact spawn request with agent name, task scope, expected deliverable, and handback condition.
```

The conductor should request these Codex custom agents by name:

- `implementer`
- `analyst`
- `qa-capture`
- `debug-guru`

## 5. Hand off to the conductor

After the team bootstrap succeeds, hand off to epic-conductor with runtime-specific wording.

Claude:

> Epic <id> is live. Read the epic body and current ticket state, then plan the first wave of work and dispatch teammates via SendMessage. You own the team until every child ticket reaches a terminal status.

Codex:

> Epic <id> is live. Read the epic body and current ticket state, then plan the first wave of work. Return exact spawn requests for any teammate you need, including agent name, scope, expected deliverable, and handback condition. You own orchestration until every child ticket reaches a terminal status.

Print to the user:
- Team name and handle in Claude, or conductor/subagent names in Codex
- Members included (and why)
- A runtime-appropriate pointer for waiting on teammate output.

Then exit. The conductor takes it from here.

## What this skill does NOT do

- It does not create child tickets. The conductor does that as work surfaces.
- It does not modify code, push commits, or open PRs. Implementer does that.
- It does not write reports. pm-reporting + scribe do that.
- It does not loop / wait for completion. Spawning is a one-shot — the team runs autonomously after.
- It does not treat Claude's Team tool as portable. Codex uses custom subagents installed by `$capsule-setup`.
