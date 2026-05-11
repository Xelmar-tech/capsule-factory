---
description: Plan and create a Linear epic from a description or existing stub ticket
argument-hint: '<short intent> or <Linear-ticket-id> or <path to brief>'
---

Load skill: **linear-epic-planning**.

The user invoked `/plan-epic` with `$ARGUMENTS`. Apply the `linear-epic-planning` skill: read `.capsule-factory.yml`, draft the epic body (Goal / Scope / Out of scope / Acceptance / Notes), confirm with the user, then create the epic in Linear via the Linear MCP. Return the epic URL and ID. Do not create child tickets — the agents will file those as work progresses.

After the epic exists, suggest `/orchestrate <epic-id>` as the next step. Do not auto-invoke.
