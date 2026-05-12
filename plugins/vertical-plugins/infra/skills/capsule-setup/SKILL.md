---
name: capsule-setup
version: 1.0.0
description: |
  Install or refresh Capsule Factory's Codex agent team in the current repository.
  Use when the user asks to set up Capsule Factory for Codex, install the agent team,
  copy agent TOML templates, verify required connectors, or migrate a repo from
  Claude-only Capsule Factory usage.
---

# Capsule Setup

Set up Capsule Factory for Codex in the current repository. This is the Codex counterpart to Claude's `/capsule-setup`, but the runtime model is different: Codex marketplace plugins install skills and tooling, while runnable custom subagents are discovered from `.codex/agents/` or `~/.codex/agents/`.

If the user is asking what Capsule Factory is, which plugins to install, or how marketplace updates work, use `$capsule-onboarding` first. Use this skill when the next action is actually installing or refreshing the repo's agent TOML files.

## Installer

Prefer the bundled installer script when it is available:

```bash
python3 <this-skill>/scripts/install_codex_agents.py --repo <target-repo>
```

The script supports both Capsule Factory source layouts and Codex installed-cache layouts:

```text
plugins/agent-plugins/<name>/codex-agents/<name>.toml
~/.codex/plugins/cache/capsule-factory/<name>/<version>/codex-agents/<name>.toml
```

Use `--dry-run` to preview actions. Use `--force` only after the user explicitly approves replacing differing destination TOML files.

## Workflow

1. Confirm the target repo root.
   - Default to the current working directory.
   - Require a real git repository.
   - Create or update `.codex/agents/` in that repository.

2. Locate Capsule Factory.
   - Prefer the installed plugin paths if Codex exposes them.
   - In an installed Codex plugin cache, templates live at `~/.codex/plugins/cache/capsule-factory/<name>/<version>/codex-agents/<name>.toml`.
   - In a source checkout, templates live at `plugins/agent-plugins/<name>/codex-agents/<name>.toml`.
   - If using the bundled installer from this skill, it detects both layouts automatically.

3. Install the Codex agents.
   - Copy these templates into `.codex/agents/`:
     - `epic-conductor.toml`
     - `implementer.toml`
     - `analyst.toml`
     - `qa-capture.toml`
     - `debug-guru.toml`
   - Preserve local edits by default. If a destination exists and differs, show the diff summary and ask before replacing it.
   - If using the bundled script, first run it without `--force`; it will skip differing files and report them.

4. Check required integrations.
   - Linear: needed by planning, reporting, and conductor workflows.
   - GitHub: needed by PR lifecycle, review, and CI workflows.
   - Bitwarden or Vaultwarden: needed only when using `manage-secrets`.
   - Prefer Codex app connectors or configured MCP servers. Do not write Claude settings files.

5. Check per-repo config.
   - If `.capsule-factory.yml` exists, read it and report the Linear team/project and GitHub defaults.
   - If it is missing, ask for the Linear team key before any Linear write workflow. Do not guess.

6. Report the result.
   - List agent template paths installed or skipped.
   - List integration status by name only.
   - Tell the user to run `$agent-orchestrator <epic-id>` after setup, or `$capsule-onboarding` if they need the full workflow explanation.
   - Print no secret values.

## Safety

- Never ask for tokens or passwords in chat.
- Never print secret values.
- Never overwrite existing `.codex/agents/*.toml` files without an explicit confirmation in the same turn.
- Never modify `.claude/` or user-level Claude settings; those are Claude-only surfaces.

## Success Criteria

After setup, the consuming repo has:

```text
.codex/agents/epic-conductor.toml
.codex/agents/implementer.toml
.codex/agents/analyst.toml
.codex/agents/qa-capture.toml
.codex/agents/debug-guru.toml
```

The user can then ask Codex to run the Capsule team on an epic, and the parent Codex session can spawn those custom agents.

## Updating Existing Installs

When Capsule Factory updates:

- Users on a Git marketplace should run `codex plugin marketplace upgrade capsule-factory`.
- Users on a local marketplace should pull the local checkout and refresh in the Codex app; if the cache does not refresh, remove and re-add the marketplace.
- After updating any agent plugin, rerun this skill in each target repo. Existing differing `.codex/agents/*.toml` files are not replaced unless the user explicitly approves replacement.
