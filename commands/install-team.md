---
description: Install the entire Capxul Agent Team plugin ecosystem
argument-hint: '[--scope user|project]'
---

# /install-team

Installs all 13 plugins (7 vertical + 6 agent) in one command.

## What Gets Installed

**Vertical Plugins:**
1. `pm-core` — Linear epic planning, reporting, orchestration
2. `code-quality` — PR lifecycle, code review, TypeScript best practices
3. `security` — Security scanning, vulnerability validation, threat modeling
4. `evidence-capture` — Demo recording, verification, QA testing, Remotion video pipeline
5. `research` — Code exploration, optimization experiments
6. `documentation` — Wiki generation, humanized writing, visual design
7. `debugging` — Browser navigation, frontend debugging, API interception, skill creation

**Agent Plugins:**
1. `epic-conductor` — Master controller agent
2. `implementer` — PR lifecycle agent
3. `analyst` — Security analysis agent
4. `reporter` — Documentation and reporting agent
5. `qa-capture` — Evidence and demo agent
6. `debug-guru` — Debugging and frontend agent

## MCP Setup

After installation, configure these MCP servers:

### Linear
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": { "LINEAR_API_KEY": "your-api-key" }
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
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token" }
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
      "env": { "BW_ACCESS_TOKEN": "your-token" }
    }
  }
}
```

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
```

You should see all 13 plugins registered.
