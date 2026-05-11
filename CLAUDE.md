# Capsule Factory — working notes

This repo is **Capxul's Claude Code plugin marketplace**. It is consumed by `/plugin marketplace add Xelmar-tech/capsule-factory` and then `/plugin install <name>@capsule-factory`.

The work here is mostly **authoring plugin content** (skills, commands, agents) and **keeping the catalog spec-compliant**. It is not a runtime — there is nothing to build or deploy.

## Repository shape

```
.claude-plugin/marketplace.json    # The catalog. Spec-defined fields only.
plugins/
  vertical-plugins/                # Shared skills + slash commands per domain
    <name>/
      .claude-plugin/plugin.json   # { name, version, description }
      skills/<skill-name>/SKILL.md # Auto-invoked from description match
      commands/<cmd>.md            # /<cmd>, thin wrapper around a skill
  agent-plugins/                   # Specialized agents + their own skills
    <name>/
      .claude-plugin/plugin.json
      agents/<name>.md             # @<name> persona definition
      skills/<skill>/SKILL.md
```

## Spec rules (drop, do not negotiate)

- `marketplace.json` must use `name` + `source` (not `id` + `path`). Sources are relative paths starting with `./`.
- Top-level `owner` is required (object with `name`, optionally `email`).
- Non-spec fields (`installCommand`, `mcpServers`, `verticalDependencies`, `mcpDependencies`, `binaries`, `scripts`, `remotion`, per-plugin `commands` / `skills` / `agent` arrays) are silently ignored by Claude Code at load time. **Do not add them back.** Commands, skills, and agents are discovered by walking the plugin tree.
- Each plugin needs a `.claude-plugin/plugin.json` with at least `name`, `version`, `description`. The `name` must match its catalog entry.

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

## When adding a new plugin

1. Create `plugins/<vertical|agent>-plugins/<name>/.claude-plugin/plugin.json`.
2. Add an entry to `.claude-plugin/marketplace.json` with `name` + `source: "./plugins/.../<name>"` + `description`.
3. Add at least one skill, command, or agent under the plugin directory.
4. Test locally: `/plugin marketplace add ~/projects/capxul/capsule-factory` (or refresh if already added), then `/plugin install <name>@capsule-factory`.

## What NOT to do

- Do not stuff decorative metadata into `marketplace.json`. Catalog is for discovery, not documentation.
- Do not author a command wrapper for every skill. Most skills auto-invoke from their `description` and a wrapper just adds maintenance. Add a command only when explicit triggering is part of the UX (e.g., `/pr`, `/threat-model`).
- Do not pull content from `~/.factory` byte-for-byte without checking whether it references Factory-specific tooling (`droid wiki-upload`, `droid-evolved`, etc.). Adapt or fork.

## References

- Marketplace schema: https://code.claude.com/docs/en/plugin-marketplaces
- Plugin manifest spec: https://code.claude.com/docs/en/plugins-reference
