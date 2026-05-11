# Capsule Factory

A cohesive plugin ecosystem for managing Capxul's AI agent workforce. Built for Claude Code.

## What You Get

**7 Vertical Plugins** (shared skills + user-facing commands):
- **PM Core** — `/plan-epic`, `/report`, `/orchestrate`
- **Code Quality** — `/pr`, `/review-pr`, `/simplify`
- **Security** — `/security-scan`, `/threat-model`
- **Evidence Capture** — `/demo`, `/verify`, `/qa-test` (with Remotion video pipeline)
- **Research** — `/experiment`, `/explore`
- **Documentation** — `/wiki`, `/humanize`, `/design`
- **Debugging** — `/debug-api`, `/create-skill`

**6 Agent Plugins** (specialized agents with their own skills):
- **Epic Conductor** — Master controller, orchestrates the team
- **Implementer** — PR lifecycle, code quality
- **Analyst** — Security scanning, deep-dive analysis
- **Reporter** — Reports, docs, presentations
- **QA Capture** — Demos, verification, evidence
- **Debug Guru** — Browser, frontend, API debugging

## Quick Start

```bash
# Add this marketplace
/plugin marketplace add Xelmar-tech/capsule-factory

# Then install individual plugins
/plugin install pm-core@capsule-factory
/plugin install epic-conductor@capsule-factory
```

## Architecture

```
capsule-factory/
├── .claude-plugin/marketplace.json    # Plugin registry
├── plugins/
│   ├── vertical-plugins/              # Shared skills + commands
│   │   ├── pm-core/
│   │   ├── code-quality/
│   │   ├── security/
│   │   ├── evidence-capture/          # + bin/tctl + scripts/ + remotion/
│   │   ├── research/
│   │   ├── documentation/
│   │   └── debugging/
│   └── agent-plugins/                 # Agent definitions + specific skills
│       ├── epic-conductor/
│       ├── implementer/
│       ├── analyst/
│       ├── reporter/
│       ├── qa-capture/
│       └── debug-guru/
└── README.md
```

## Commands

All commands are available after installing the plugin. See [CLAUDE.md](CLAUDE.md) for full reference.

## Agents

Agents are invoked with `@agent-name` or automatically routed by the epic conductor.

## MCP Setup

Configure these MCP servers in Claude Code:
- **Linear** — `@linear/mcp-server`
- **GitHub** — `@github/mcp-server`
- **Bitwarden** — `@bitwarden/sdk-napi`

## License

MIT
