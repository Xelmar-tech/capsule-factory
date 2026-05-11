---
description: Spawn the agent team to execute a Linear epic
argument-hint: '<epic-id> (e.g. CAP-42 or full Linear URL)'
---

Load skill: **agent-orchestrator**.

The user invoked `/orchestrate` with `$ARGUMENTS`. Apply the `agent-orchestrator` skill: resolve the epic via the Linear MCP, run the env-materialization pre-flight (`manage-secrets`), decide team composition, spawn the team via `TeamCreate` with `epic-conductor` as owner, and hand control to the conductor. Then exit — the team runs autonomously.

If the Bitwarden MCP isn't configured, stop and point at `/capsule-setup`.
