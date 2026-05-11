---
description: Configure the MCPs required by the capsule-factory marketplace
argument-hint: '[--check] (verify-only mode)'
---

The user invoked `/capsule-setup`. Configure the MCP servers the marketplace plugins depend on, in the user's Claude Code settings.

## Required MCPs

| MCP        | Purpose                                  | Plugins that need it          |
|------------|------------------------------------------|--------------------------------|
| linear     | Read/write Linear issues and epics       | pm-core, epic-conductor       |
| github     | PR/issue operations                      | code-quality, implementer, analyst |
| bitwarden  | Decrypt vault items for env materialization | infra (manage-secrets)     |

## Workflow

1. Read the user's current `~/.claude/settings.json` (or project-local `.claude/settings.local.json` if the user prefers). Check which of the three MCPs are already declared.

2. For each missing MCP, propose the configuration block and ask the user to confirm before writing:

   ```jsonc
   "mcpServers": {
     "linear":    { "command": "npx", "args": ["-y", "@linear/mcp-server"],   "env": ["LINEAR_API_KEY"] },
     "github":    { "command": "npx", "args": ["-y", "@github/mcp-server"],   "env": ["GITHUB_PERSONAL_ACCESS_TOKEN"] },
     "bitwarden": { "command": "npx", "args": ["-y", "@bitwarden/sdk-napi"],  "env": ["BW_ACCESS_TOKEN"] }
   }
   ```

3. For each MCP, the corresponding env var must be set in the user's shell or settings. Do **not** prompt for the secret value in chat. Instead, tell the user:

   - **LINEAR_API_KEY** — generate at https://linear.app/settings/api → personal API keys. Set in `~/.zshrc` or your secret manager.
   - **GITHUB_PERSONAL_ACCESS_TOKEN** — generate at https://github.com/settings/tokens (classic) or fine-grained PAT. Needs `repo` + `pull_request` scopes.
   - **BW_ACCESS_TOKEN** — generate from a Bitwarden / Vaultwarden machine account. Pair with the dedicated agent CLI profile (see `infra/manage-secrets`).

4. After writing settings, ask the user to restart Claude Code so the MCP servers boot.

5. Verify with `/capsule-setup --check`:
   - Confirm each MCP appears in settings
   - Optionally probe each MCP server (e.g. linear `list_teams`, github `gh api user`, bitwarden `list-orgs`) to confirm auth works

## Safety

- Never write secret values into `settings.json`. The `env` array names the env-var keys; the values come from the shell environment at runtime.
- Never commit `settings.json` if it contains secrets. Verify the file is in `.gitignore` if it's the project-local one.
- If the user already has one of these MCPs configured with different args, do not overwrite — surface the difference and ask which version to keep.

## What this command does NOT do

- It does not install the underlying CLIs (`@linear/mcp-server`, etc.) — `npx -y` fetches them at invocation. If the user is offline, that's a separate problem.
- It does not configure the per-repo `.capsule-factory.yml` — that's `/plan-epic`'s job on first use.
- It does not materialize env files — `/materialize-env` does that after the bitwarden MCP is configured.
