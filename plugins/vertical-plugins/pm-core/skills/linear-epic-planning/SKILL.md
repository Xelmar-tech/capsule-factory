---
name: linear-epic-planning
version: 1.0.0
description: |
  Bootstrap a new epic in Linear from a one-line intent or expand an existing stub ticket.
  Use when the user says "/plan-epic", "plan an epic for X", "scope out the work to build X",
  or hands you a Linear ticket ID and asks you to turn it into an epic. This skill creates
  the epic container only — child tickets are added later by the coding agents themselves
  as work progresses.
---

# Linear epic planning

The job: read the user's intent, draft a short epic body, push it to Linear as a top-level epic, and hand control to the orchestrator. **You are not creating the child tickets.** Child tickets are the implementer/analyst/qa-capture agents' job — they file them as they discover the work. Your only output in Linear is the epic itself.

## 1. Resolve the Linear target

Read `.capsule-factory.yml` at the repo root. The schema is:

```yaml
linear:
  team: <team-key-or-id>      # e.g. CAP
  project: <project-key-or-id> # optional; if absent, epic lives at team root
github:
  default_base_branch: main
  draft_by_default: false
```

If the file is missing, prompt the user for `team` and `project`, then offer to write the file. Do not proceed without a resolved team — guessing creates tickets in the wrong place and is annoying to clean up.

## 2. Parse the input

`$ARGUMENTS` (or the user's free-form request) is one of:

- **A short intent string** ("build a KYC pack uploader", "migrate the legacy auth flow") — draft from scratch.
- **A Linear ticket reference** (`CAP-1234`, full Linear URL) — fetch the ticket via the Linear MCP, treat its body as the seed, and expand it into a full epic.
- **A path to a brief or design doc** — read the doc, summarize, then draft.

If the input is genuinely ambiguous (e.g., `/plan-epic "foo"`), ask one clarifying question. Do not file a vague epic.

## 3. Draft the epic body

Epic bodies should be short — under ~300 words. Long PRDs go elsewhere (a separate doc, a Notion page, a `docs/` file referenced by the epic). The epic body is the **mission statement** that every agent on the team reads at the start of every turn.

Sections (use exactly these headings, in this order):

```markdown
## Goal

One or two sentences: what is the outcome of this epic? Frame as a user-facing or business-facing result, not a technical task.

## Scope

What is in scope. Bullet points, 3–8 items. Each item is a capability or surface area, not a ticket.

## Out of scope

What is explicitly NOT in scope. Helps prevent agent drift. Bullet points.

## Acceptance

How the team knows the epic is done. Concrete, observable criteria — not vague "feature works." 2–5 items.

## Notes

Any constraints, deadlines, stakeholders, or related epics. Optional.
```

## 4. Present to user and confirm

Print the drafted body to the user. Ask "Push to Linear as <team>/<project> epic? (y/n/edit)". On `edit`, take revisions and re-print. On `y`, proceed. On `n`, save the draft to `epics/draft-<slug>.md` and stop.

## 5. Create the epic in Linear

Use the Linear MCP `save_issue` (or equivalent) with:

- `team_id`: from config
- `project_id`: from config (if set)
- `title`: short noun phrase matching the goal (not "Epic: ..." — Linear's epic flag handles that)
- `description`: the drafted body
- Mark as an epic (set the appropriate `parent_id` or epic flag per Linear's API)
- Initial status: `Backlog` or `Todo` per the team's default

Return the created epic's URL and ID. Print both to the user.

## 6. Hand off

After the epic exists, suggest the next step explicitly:

> Epic created: <URL>. Run `/orchestrate <epic-id>` to spawn the team and start work, or open the Linear ticket to review/edit before kicking off.

Do not auto-invoke `/orchestrate` from this skill. The user reviews the epic in Linear first.

## What this skill does NOT do

- It does not create child tickets. The implementer/analyst/qa-capture agents file their own as work surfaces.
- It does not write code, scaffold a repo, or create branches. Implementer does that after `/orchestrate`.
- It does not assign anyone to the epic. The orchestrator (epic-conductor agent) does that based on team membership when it spawns.
- It does not write a PRD. Long-form requirements live outside Linear; the epic body links to them if needed.
