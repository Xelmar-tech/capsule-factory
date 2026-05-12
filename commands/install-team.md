---
description: Install the entire Capxul Agent Team plugin ecosystem
argument-hint: '[--scope user|project]'
---

# /install-team

Installs all 15 plugins (9 vertical + 6 agent) in one command.

## What Gets Installed

**Vertical Plugins:**
1. `infra` — `/onboard`, MCP setup, env materialization, repo bootstrapping
2. `pm-core` — Linear epic planning, reporting, orchestration
3. `code-quality` — PR lifecycle, code review, TypeScript best practices
4. `security` — Security scanning, vulnerability validation, threat modeling
5. `evidence-capture` — Demo recording, verification, QA testing, Remotion video pipeline
6. `research` — Code exploration, optimization experiments
7. `documentation` — Wiki generation, humanized writing, visual design
8. `debugging` — Browser navigation, frontend debugging, API interception, skill creation
9. `observability` — PostHog runtime evidence, analytics, error tracking, replay, flags

**Agent Plugins:**
1. `epic-conductor` — Master controller agent
2. `implementer` — PR lifecycle agent
3. `analyst` — Security analysis agent
4. `observability-analyst` — PostHog runtime evidence agent
5. `qa-capture` — Evidence and demo agent
6. `debug-guru` — Debugging and frontend agent

## MCP Setup

After installation, run `/onboard --check` for a guided validation pass or `/capsule-setup` to configure MCPs directly.

Required MCP servers:

### Linear
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": ["LINEAR_API_KEY"]
    }
  }
}
```

### GitHub
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@github/mcp-server"],
      "env": ["GITHUB_PERSONAL_ACCESS_TOKEN"]
    }
  }
}
```

### Bitwarden
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

Recommended MCP server:

### PostHog

Prefer the official wizard:

```bash
npx @posthog/wizard mcp add
```

Manual endpoint:

```text
https://mcp.posthog.com/mcp
```

Use OAuth when supported, or a PostHog personal API key created with the MCP Server preset. Pin project/org scope where possible and never commit or print the key.

## Evidence Capture Prerequisites

The `evidence-capture` vertical includes Remotion video rendering. Install dependencies:

```bash
cd plugins/vertical-plugins/evidence-capture/remotion && npm install
```

Additional system dependencies:
```bash
# Terminal recording
npm install -g tuistory
pip install asciinema
cargo install --git https://github.com/asciinema/agg

# Browser automation
agent-browser install

# Video processing
sudo apt-get install -y ffmpeg

# True input (Linux/Wayland)
sudo apt-get install -y cage wtype
```

## Verification

After installation, verify with:
```bash
/plugins list
/onboard --check
```

You should see all 15 plugins registered, and `/onboard --check` should report MCP and repo-config gates as `ok`, `missing`, or `blocked`.
