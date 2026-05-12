# Capsule Factory Agent Guidance

This repo is dual-target: keep Claude Code support and Codex support aligned.

## Surfaces

- Claude marketplace catalog: `.claude-plugin/marketplace.json`
- Codex marketplace catalog: `.agents/plugins/marketplace.json`
- Claude plugin manifest: `.claude-plugin/plugin.json`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Claude agent definition: `plugins/agent-plugins/<name>/agents/<name>.md`
- Codex custom-agent template: `plugins/agent-plugins/<name>/codex-agents/<name>.toml`
- Migration map: `.agents/codex-migration-map.json`

## Rules

- When adding or renaming a plugin, update both Claude and Codex manifests and the migration map.
- When changing plugin behavior, bump the changed plugin version in both manifests so Codex can cache a new version.
- When adding or renaming a Claude agent, add the matching Codex TOML template.
- Do not assume Codex marketplace plugins directly register runnable custom agents. Use `$capsule-setup` to copy templates into `.codex/agents/` in the consuming repo.
- Keep Claude-specific team API names out of Codex-facing instructions unless explicitly documented as Claude-only mappings.
- Run `python3 scripts/validate-codex-migration.py` after changing manifests, commands, skills, agents, or README setup docs.
