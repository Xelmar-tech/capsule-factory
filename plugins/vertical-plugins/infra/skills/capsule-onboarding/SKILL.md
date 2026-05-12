---
name: capsule-onboarding
version: 1.0.0
description: |
  Explain how to install, update, and use Capsule Factory in Codex. Use when the user
  asks what to install next, how the agent team works, how Codex differs from Claude,
  or how to keep the Capsule Factory marketplace and installed plugins up to date.
---

# Capsule Onboarding

Use this skill to orient a Codex user before or after installing Capsule Factory.

## Install Order

1. Install `infra` first.
   - It provides `$capsule-onboarding`, `$capsule-setup`, and `$manage-secrets`.
2. Install `pm-core`.
   - It provides `$linear-epic-planning`, `$agent-orchestrator`, and `$pm-reporting`.
3. Install agent plugins as needed.
   - `epic-conductor`
   - `implementer`
   - `analyst`
   - `qa-capture`
   - `debug-guru`
4. Install supporting vertical plugins when the workflow needs them.
   - `code-quality`, `security`, `evidence-capture`, `research`, `documentation`, `debugging`.

## Agent Model

Codex marketplace plugins can install skills and tools. Runnable custom subagents are discovered from `.codex/agents/` in the target repo or from the user's Codex agent directory.

The Capsule agent plugins ship TOML templates in the installed plugin cache:

```text
~/.codex/plugins/cache/capsule-factory/<agent-plugin>/<version>/codex-agents/<agent>.toml
```

Run `$capsule-setup` in each target repo to copy those templates into:

```text
.codex/agents/epic-conductor.toml
.codex/agents/implementer.toml
.codex/agents/analyst.toml
.codex/agents/qa-capture.toml
.codex/agents/debug-guru.toml
```

Installing the agent plugin alone is not enough to make a runnable custom subagent. The TOML file must exist in `.codex/agents/` or the user's Codex agent directory.

## First Run

1. Run `$capsule-setup` in the repo where the team will work.
2. Confirm Linear and GitHub connector or MCP availability.
3. Confirm Bitwarden or Vaultwarden only if env materialization is needed.
4. Add `.capsule-factory.yml` before Linear write workflows:

```yaml
linear:
  team: CAP
  project: <optional-project-id>
github:
  default_base_branch: main
  draft_by_default: false
```

## Typical Workflow

```text
$linear-epic-planning "build the thing"
$capsule-setup
$agent-orchestrator CAP-123
$pm-reporting
```

In Codex, orchestration means the parent Codex session starts `epic-conductor`, then starts `implementer`, `analyst`, `qa-capture`, or `debug-guru` when the conductor asks for them.

## Keeping It Up To Date

For users:

- If Capsule Factory was added as a Git marketplace, update it with:

```bash
codex plugin marketplace upgrade capsule-factory
```

- If it was added from a local checkout, pull the checkout and refresh from the Codex app. If the local cache does not refresh, remove and re-add the marketplace:

```bash
codex plugin marketplace remove capsule-factory
codex plugin marketplace add /path/to/capsule-factory
```

- After updating any agent plugin, rerun `$capsule-setup` in each target repo. It preserves differing local `.codex/agents/*.toml` files unless the user explicitly asks to replace them.

For maintainers:

- Bump the changed plugin's version in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.
- Update `.agents/codex-migration-map.json` when a command, skill, plugin, or agent surface changes.
- Run `python3 scripts/validate-codex-migration.py` before publishing.
- Push the repo; users on the Git marketplace can then run `codex plugin marketplace upgrade capsule-factory`.

## What To Say When Asked "What Next?"

Answer with the smallest next step:

- No marketplace installed: tell them to add Capsule Factory in Codex.
- Marketplace installed but no plugins: install `infra`, then run `$capsule-onboarding`.
- Agent plugins installed but no `.codex/agents/`: run `$capsule-setup`.
- `.codex/agents/` present: run `$agent-orchestrator <epic-id>` or `$linear-epic-planning`.
- Existing agents differ from templates: summarize the difference and ask before replacing.
