# Linear PM Team — Claude Code Guide

How to use this plugin ecosystem effectively.

## Commands

All commands are available in Claude Code after installing the plugin.

### Project Management

| Command | Description | Example |
|---------|-------------|---------|
| `/plan-epic` | Break an epic into Linear issues | `/plan-epic "Build auth system"` |
| `/report` | Generate progress report | `/report weekly backend-team` |
| `/orchestrate` | Route work to agents | `/orchestrate "Fix login bug" --agent debug-guru` |

### Code Quality

| Command | Description | Example |
|---------|-------------|---------|
| `/pr` | Create a pull request | `/pr feature/oauth` |
| `/review-pr` | Follow up on existing PR | `/review-pr 456` |
| `/simplify` | Review and improve code | `/simplify src/auth.ts` |

### Security

| Command | Description | Example |
|---------|-------------|---------|
| `/security-scan` | Scan code for vulnerabilities | `/security-scan pr 123` |
| `/threat-model` | Generate STRIDE threat model | `/threat-model "API Gateway"` |

### Evidence & QA

| Command | Description | Example |
|---------|-------------|---------|
| `/demo` | Record a demo video | `/demo "Show new feature"` |
| `/verify` | Test a claim with evidence | `/verify "Login works on mobile"` |
| `/qa-test` | Run automated QA flow | `/qa-test https://staging.app.com` |

### Research

| Command | Description | Example |
|---------|-------------|---------|
| `/experiment` | Run optimization experiment | `/experiment "Reduce build time"` |
| `/explore` | Explore codebase | `/explore "Find auth middleware"` |

### Documentation

| Command | Description | Example |
|---------|-------------|---------|
| `/wiki` | Generate codebase wiki | `/wiki` |
| `/humanize` | Remove AI patterns from text | `/humanize report.md` |
| `/design` | Create presentation | `/design "Q2 Review"` |

### Debugging

| Command | Description | Example |
|---------|-------------|---------|
| `/debug-api` | Intercept API calls | `/debug-api intercept curl https://api.example.com` |
| `/create-skill` | Create a new skill | `/create-skill "deploy-checklist"` |

## Agent Invocation

Agents are invoked automatically based on work type, or explicitly:

```bash
# Explicit agent invocation
@epic-conductor Plan the Q3 roadmap

@implementer Create a PR for the auth fix

@analyst Run security scan on PR 123

@reporter Generate weekly report

@qa-capture Record a demo of the new dashboard

@debug-guru Debug why the API returns 500
```

## MCP Configuration

Configure these MCP servers in Claude Code:

### Linear
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your-api-key"
      }
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
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

## Tips

- **Start with the conductor.** The epic-conductor agent can route work to the right team member.
- **Use commands for quick tasks.** Commands are faster than full agent invocation.
- **Chain agents.** One agent's output can be another's input. Example: analyst finds security issue → implementer fixes it → qa-capture verifies.
- **Evidence first.** Every claim needs proof. Use `/verify` and `/demo` to capture evidence.
- **Keep skills fresh.** Use `/create-skill` to codify new patterns as the team learns.
