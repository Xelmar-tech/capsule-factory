# Capsule Factory — working notes

This repo is **Capxul's dual Claude Code + Codex plugin marketplace**. Claude consumes it with `/plugin marketplace add Xelmar-tech/capsule-factory` and then `/plugin install <name>@capsule-factory`. Codex consumes `.agents/plugins/marketplace.json` and the sibling `.codex-plugin/plugin.json` manifests.

The work here is mostly **authoring plugin content** (skills, commands, agents, Codex templates) and **keeping both catalogs spec-compliant**. It is not a runtime — there is nothing to build or deploy.

## Repository shape

```
.claude-plugin/marketplace.json    # Claude catalog. Spec-defined fields only.
.agents/
  plugins/marketplace.json         # Codex catalog.
  codex-migration-map.json         # Source-of-truth mapping for drift checks.
AGENTS.md                          # Dual-target maintainer notes.
scripts/
  validate-codex-migration.py      # Static drift validator.
plugins/
  vertical-plugins/                # Shared skills + slash commands per domain
    <name>/
      .claude-plugin/plugin.json   # { name, version, description }
      .codex-plugin/plugin.json    # Codex plugin manifest.
      skills/<skill-name>/SKILL.md # Auto-invoked from description match
      commands/<cmd>.md            # Claude /<cmd>, thin wrapper around a skill
  agent-plugins/                   # Specialized agents + their own skills
    <name>/
      .claude-plugin/plugin.json
      .codex-plugin/plugin.json
      agents/<name>.md             # Claude @<name> persona definition
      codex-agents/<name>.toml     # Codex custom-agent template
      skills/<skill>/SKILL.md
```

## Spec rules (drop, do not negotiate)

- `marketplace.json` must use `name` + `source` (not `id` + `path`). Sources are relative paths starting with `./`.
- Top-level `owner` is required (object with `name`, optionally `email`).
- Non-spec fields (`installCommand`, `mcpServers`, `verticalDependencies`, `mcpDependencies`, `binaries`, `scripts`, `remotion`, per-plugin `commands` / `skills` / `agent` arrays) are silently ignored by Claude Code at load time. **Do not add them back.** Commands, skills, and agents are discovered by walking the plugin tree.
- Each plugin needs a `.claude-plugin/plugin.json` with at least `name`, `version`, `description`. The `name` must match its catalog entry.

## Codex parity rules

- Each `.claude-plugin/plugin.json` must have a sibling `.codex-plugin/plugin.json`.
- Each `.claude-plugin/marketplace.json` entry must have a matching `.agents/plugins/marketplace.json` entry.
- Each `plugins/agent-plugins/*/agents/*.md` file must have a matching `codex-agents/*.toml` template.
- Codex marketplace plugins ship skills and tools. Runnable custom subagents are project/user config, so `$capsule-setup` installs templates into `.codex/agents/` in the consuming repo.
- Claude `commands/*.md` are still Claude-only. Codex equivalents are skills/default prompts. Record the mapping in `.agents/codex-migration-map.json`.
- When changing plugin behavior, bump the changed plugin's version in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Codex caches installed plugins by version.
- After changing plugin, command, skill, or agent surfaces, run `python3 scripts/validate-codex-migration.py`.

## Skill file conventions

Frontmatter:

```yaml
---
name: <slug>                 # must match the directory name
version: 1.0.0
description: |
  One or two sentences. Used by Claude Code for auto-invocation:
  if the user's request matches this description, the skill loads automatically.
  Be concrete about WHEN to use this skill, not just WHAT it does.
---
```

Body: command-style instructions written for the model. Sub-headings (`## 1. Survey`, `## 2. Plan`, …) are encouraged when the skill has phases. Keep it precise — every paragraph should change behavior.

Optional frontmatter knobs (use sparingly):

- `user-invocable: true` — exposes the skill to the user as a `/<slug>` handle (rare; usually a command wrapper is cleaner).
- `user-invocable: false` — internal helper skills referenced by other skills, not directly triggered.
- `disable-model-invocation: true` — opts the skill OUT of auto-invocation. Only set this if the skill is heavy and must be triggered by an explicit `/command`; pair it with a command wrapper.

## Command file conventions

```yaml
---
description: One line. Shown in the slash-command picker.
argument-hint: '<what to type after the slash>'
---
```

Body becomes the prompt when the user invokes `/<command>`. Typical shape:

> Load skill: **<skill-name>**.
>
> The user invoked `/<command>` on `$ARGUMENTS`. [1–3 sentences specifying any per-command framing the skill body doesn't already cover.]

Commands are thin. If the body grows past a screen, move the logic into the skill and keep the command focused on argument parsing and framing.

## Agent file conventions

```yaml
---
name: <agent-name>
description: When to invoke this agent. Auto-routing depends on this.
tools: [list]                # optional; omit to inherit all tools
---
```

Body: persona, when invoked, what it owns, hand-off rules, success criteria. Agents are heavier than skills — invoked via `@<name>` or spawned by another agent. Aim for 50–200 lines.

## Codex agent template conventions

Codex custom-agent templates live next to the matching Claude agent:

```toml
name = "<agent-name>"
description = "When to invoke this agent."
model = "gpt-5.4"
model_reasoning_effort = "medium"
sandbox_mode = "workspace-write"
developer_instructions = """
Role, ownership, handoff rules, success criteria.
"""
```

Keep these templates implementation-facing and Codex-native. Put exact Claude runtime terminology in `.agents/codex-migration-map.json`, not inside Codex agent instructions.

## When adding a new plugin

1. Create `plugins/<vertical|agent>-plugins/<name>/.claude-plugin/plugin.json`.
2. Create `plugins/<vertical|agent>-plugins/<name>/.codex-plugin/plugin.json`.
3. Add entries to `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`.
4. Add at least one skill, command, or agent under the plugin directory.
5. If this is an agent plugin, add both `agents/<name>.md` and `codex-agents/<name>.toml`.
6. Update `.agents/codex-migration-map.json`.
7. Bump the plugin version in both manifests when behavior changes.
8. Test Claude locally: `/plugin marketplace add ~/projects/capxul/capsule-factory` (or refresh if already added), then `/plugin install <name>@capsule-factory`.
9. Test Codex locally by installing from `.agents/plugins/marketplace.json`, then run `$capsule-setup` in a disposable repo if agent templates changed.
10. Run `python3 scripts/validate-codex-migration.py`.

## What NOT to do

- Do not stuff decorative metadata into `marketplace.json`. Catalog is for discovery, not documentation.
- Do not author a command wrapper for every skill. Most skills auto-invoke from their `description` and a wrapper just adds maintenance. Add a command only when explicit triggering is part of the UX (e.g., `/pr`, `/threat-model`).
- Do not pull content from `~/.factory` byte-for-byte without checking whether it references Factory-specific tooling (`droid wiki-upload`, `droid-evolved`, etc.). Adapt or fork.
- Do not assume plugin-bundled Codex agent templates are directly runnable. They must be copied into `.codex/agents/` or the user's Codex agent directory.

## References

- Marketplace schema: https://code.claude.com/docs/en/plugin-marketplaces
- Plugin manifest spec: https://code.claude.com/docs/en/plugins-reference
- Codex migration map: `.agents/codex-migration-map.json`
