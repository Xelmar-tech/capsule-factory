# Linear PM Team

A Claude Code plugin ecosystem for managing software projects with Linear. Plan epics, manage PRs, run security scans, capture evidence, and generate reports — all through a cohesive team of specialized agents.

## What this is

This is a **marketplace plugin** for Claude Code. It provides:

- **7 vertical plugins** — Shared skills and commands for project management, code quality, security, evidence capture, research, documentation, and debugging
- **6 agent plugins** — Specialized PM team members that orchestrate work, implement features, analyze security, report progress, capture evidence, and debug issues
- **User-facing commands** — `/plan-epic`, `/report`, `/pr`, `/security-scan`, `/demo`, `/verify`, `/wiki`, `/debug-api`, and more

## Installation

```bash
# In Claude Code, install from this repository
claude plugins add https://github.com/capxul-agent/linear-pm-team
```

## Quick Start

```bash
# Plan an epic
/plan-epic "Build user authentication system"

# Create a PR
/pr feature/auth-login

# Run security scan
/security-scan pr 123

# Record a demo
/demo "Show the new login flow"

# Generate report
/report weekly

# Debug API calls
/debug-api intercept curl https://api.example.com
```

## The PM Team

| Agent | Role | Key Skills |
|-------|------|-----------|
| **epic-conductor** | Plans epics, orchestrates team | linear-epic-planning, pm-reporting, agent-orchestrator |
| **implementer** | PR lifecycle, code quality | create-pr, follow-up-on-pr, ban-type-assertions, no-use-effect |
| **analyst** | Security scans, research | security-review, autoresearch, threat-model-generation |
| **reporter** | Reports, docs, presentations | pm-reporting, wiki, human-writing, visual-design |
| **qa-capture** | Evidence, demos, verification | capture, compose, verify, showcase |
| **debug-guru** | Browser, frontend, API debug | browser-navigation, frontend-design, http-toolkit-intercept |

## Plugin Structure

```
.claude-plugin/
  marketplace.json          # Marketplace manifest
plugins/
  vertical-plugins/
    pm-core/                # Epic planning, reporting, orchestration
    code-quality/           # PR lifecycle, TypeScript rules
    security/               # STRIDE scanning, threat modeling
    evidence-capture/       # Demos, QA, verification
    research/               # Experiments, code exploration
    documentation/           # Wikis, humanized writing, presentations
    debugging/              # Browser, frontend, API debugging
  agent-plugins/
    epic-conductor/         # Epic planning agent
    implementer/            # Code delivery agent
    analyst/                # Security & research agent
    reporter/               # Documentation agent
    qa-capture/             # Evidence & testing agent
    debug-guru/           # Debugging agent
```

## Requirements

- Claude Code (Claude 3.5 Sonnet or later)
- Linear MCP server configured
- GitHub MCP server configured
- Optional: HTTP Toolkit for API debugging

## License

MIT
