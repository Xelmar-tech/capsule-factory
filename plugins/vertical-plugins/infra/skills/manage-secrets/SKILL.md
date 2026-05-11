---
name: manage-secrets
version: 1.0.0
description: |
  Materialize project environment files from Bitwarden / Vaultwarden via the Bitwarden MCP.
  Use when configuring an agent worktree, before coding starts, when env vars are missing,
  or when the user asks to "materialize env", "set up secrets", "pull env from bitwarden",
  or "get the dev keys". Never prints secret values; writes mode 0600 files only to
  git-ignored paths.
---

# Manage secrets

The job: read project env files from a Bitwarden / Vaultwarden vault via the Bitwarden MCP and write them to disk so coding agents can run the repo's normal startup commands without missing-env-var failures. The skill is **MCP-first** — there is no bundled CLI helper. The MCP server handles auth, session, and decryption; this skill applies the safety rules on top.

## When to use this skill

Pre-flight before any coding work on a Capxul repo, OR on demand when env vars are missing. Implementer / debug-guru / qa-capture all call this before they spawn long sessions.

## Prerequisites

The Bitwarden MCP must be configured in the user's Claude Code settings:

```json
{
  "mcpServers": {
    "bitwarden": {
      "command": "npx",
      "args": ["-y", "@bitwarden/sdk-napi"],
      "env": ["BW_ACCESS_TOKEN"]
    }
  }
}
```

If the MCP is not connected, stop and tell the user to run `/capsule-setup` (which installs and configures it). Do not prompt for credentials in chat — the MCP handles unlock state via its own session.

## Vault layout (Capxul convention)

Secrets are organized by `organization` → `collection` → `manifest item` → `split items`:

```
organization: Agents
collection: hermes
manifest item: capxul/<env>/env-files   (e.g. capxul/dev/env-files)
split items:
  - capxul/<env>/env-root-and-apps
  - capxul/<env>/env-backend
  - capxul/<env>/env-packages
```

The manifest item is a Bitwarden secure note whose body is YAML describing each destination path and which split item contains its contents. Splits exist because individual Vaultwarden secure notes have a length cap — large monorepos need their env spread across multiple notes.

Only `capxul dev` is implemented today. Other envs (`staging`, `production`) require explicit user confirmation before any read — production reads must never auto-fire from an implementer pre-flight.

## Workflow

### 1. Resolve project + environment

`$ARGUMENTS` is usually `<project> <env>` (e.g. `capxul dev`). If missing, default to `capxul dev` in a Capxul repo, otherwise ask. Reject anything you don't recognize — do not guess at vault names.

### 2. Confirm the repo target

Operate on the current working directory unless an explicit `--repo <path>` is given. The destination must be a real git repo (`.git/` present). Reject paths outside any repo — refuse to write env files into a home directory or `/tmp`.

### 3. Fetch the manifest

Via the Bitwarden MCP:
- List items in `Agents/hermes` collection
- Find the item named `<project>/<env>/env-files`
- Read its notes field (YAML)

The manifest schema:

```yaml
files:
  - path: .env                           # destination, relative to repo root
    source: capxul/dev/env-root-and-apps # which split item contains this file's contents
    section: root                        # key inside the split item that holds this file's body
  - path: apps/web/.env.local
    source: capxul/dev/env-root-and-apps
    section: web
  - path: services/api/.env
    source: capxul/dev/env-backend
    section: api
  # ...
```

If the manifest fails to parse, stop. Do not write partial state.

### 4. Verify destinations are git-ignored

For every `path` in the manifest, check:

```bash
git -C "$REPO" check-ignore -q "$path"
```

If any path is NOT ignored, abort and tell the user which paths to add to `.gitignore`. Never write a secret to a tracked file.

### 5. Fetch each split item

Via the Bitwarden MCP, read each unique `source` item once and cache its decrypted body in memory. The body is a structured note where each `section` key maps to a file's contents.

### 6. Write the files

For each manifest entry:
- Open `<repo>/<path>` with mode `0600`
- Write the section's contents
- Close

Then print **only**:
- The destination paths written
- The list of env var keys set (names only, never values)
- Nothing else

### 7. Verify the repo can start

After materialization, check whether the repo has a known bootstrap command:
- `package.json` → run `npm run dev --dry-run` or equivalent if available
- `Makefile` with a `bootstrap` target → suggest running it
- Otherwise → tell the user "env files are in place; run your normal startup"

Do not actually start the dev server from this skill — that's the caller's job. Just confirm the env reads succeed.

## Safety rules (hard requirements)

- **Never print secret values.** Not in logs, not in tool output, not in summaries. If a debug situation requires showing a value, ask the user to read it from the file themselves.
- **Never ask the user to paste a vault password, BW_SESSION, recovery key, or any token into chat.** The MCP handles auth.
- **Never write to a path that is not git-ignored.** Hard stop, no override.
- **Always mode 0600.** No 0644, no 0666, no whatever the umask says.
- **Production requires explicit per-call confirmation.** An implementer pre-flight may call this for `dev`. It may never call it for `production` without an `--allow-production` flag *and* a user confirmation in the same turn.
- **The current working repo is the only valid target unless `--repo` is given.** Reject relative paths that escape the repo.

## Caching

The MCP server caches an unlocked session. This skill does not cache plaintext. Each invocation re-reads from the MCP — that round-trip is cheap and avoids accidental leakage if Claude's context is later compressed or exfiltrated.

## What this skill does NOT do

- It does not write or update vault items. Use the Bitwarden MCP directly (with explicit user authorization) for that.
- It does not manage MCP installation — `/capsule-setup` does that.
- It does not handle non-Capxul vault layouts. If a project uses a different org/collection/manifest convention, that is a separate skill.
- It does not log anything to a file. Output is to chat only, paths and key-names only.
