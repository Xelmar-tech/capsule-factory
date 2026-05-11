# Capsule Factory

Capxul's Claude Code plugin marketplace. A cohesive set of plugins for managing Capxul's AI agent workforce: 8 vertical plugins that ship shared skills + slash commands, and 5 agent plugins with specialized agents.

## What's inside

**8 vertical plugins** (shared skills + slash commands):

- **infra** — `/capsule-setup`, `/materialize-env` (Bitwarden MCP, env materialization, repo bootstrapping)
- **pm-core** — `/plan-epic`, `/report`, `/orchestrate` (Linear epic planning, status reports, team orchestration)
- **code-quality** — `/pr`, `/review-pr`, `/simplify` (PR lifecycle, code review, TypeScript best practices)
- **security** — `/security-scan`, `/threat-model` (security scanning, threat modeling)
- **evidence-capture** — `/demo`, `/verify`, `/qa-test` (demo recording, verification, Remotion video pipeline)
- **research** — autoresearch skill (auto-invoked)
- **documentation** — `/humanize`, wiki skill (auto-invoked for wiki generation)
- **debugging** — browser navigation, frontend design, HTTP intercept, skill creation (auto-invoked)

**5 agent plugins** (specialized agents with their own sub-skills):

- **epic-conductor** — Team owner; orchestrates the workforce per epic, owns Linear writes, runs the decision log via `scribe`
- **implementer** — End-to-end coding: ticket → PR → address review feedback
- **analyst** — Security and architecture review; posts PR comments, produces threat models via `scribe`
- **qa-capture** — Verification and demos; produces MP4 + HTML verify reports via `scribe`
- **debug-guru** — Multi-layer debugging (browser + frontend + API); produces root-cause writeups

## Quick start

```bash
# Add this marketplace
/plugin marketplace add Xelmar-tech/capsule-factory

# Install in order:
/plugin install infra@capsule-factory       # first — has /capsule-setup
/plugin install pm-core@capsule-factory     # second — coordination commands
# then everything else as needed:
/plugin install code-quality@capsule-factory
/plugin install security@capsule-factory
/plugin install evidence-capture@capsule-factory
/plugin install documentation@capsule-factory
/plugin install debugging@capsule-factory
/plugin install research@capsule-factory
/plugin install epic-conductor@capsule-factory
/plugin install implementer@capsule-factory
/plugin install analyst@capsule-factory
/plugin install qa-capture@capsule-factory
/plugin install debug-guru@capsule-factory

# Then configure the MCPs the marketplace depends on
/capsule-setup
```

## Configuration

### Required MCPs

Configured by `/capsule-setup`:

| MCP        | Purpose                                       | Required env var              |
|------------|-----------------------------------------------|-------------------------------|
| linear     | Read/write Linear issues + epics              | `LINEAR_API_KEY`              |
| github     | PR/issue operations                           | `GITHUB_PERSONAL_ACCESS_TOKEN`|
| bitwarden  | Decrypt vault items for env materialization   | `BW_ACCESS_TOKEN`             |

### Per-repo config: `.capsule-factory.yml`

Drop this at the root of any repo where you'll run `/plan-epic` or spawn the team:

```yaml
linear:
  team: CAP              # Linear team key or ID
  project: <id-optional> # Linear project ID (optional; epic lives at team root if absent)
github:
  default_base_branch: main
  draft_by_default: false
```

`/plan-epic` reads this to know where to create the epic. If the file is missing, the skill prompts and offers to write it.

## Typical workflow

```bash
# 1. New initiative
/plan-epic "build a KYC pack uploader for B.V. companies"
#   → drafts epic body, confirms with you, creates epic in Linear
#   → returns: CAP-123 (https://linear.app/...)

# 2. Kick off the team
/orchestrate CAP-123
#   → pre-flights env (manage-secrets via Bitwarden MCP)
#   → spawns the team via TeamCreate with epic-conductor as owner
#   → conductor dispatches implementer, analyst, qa-capture as work surfaces

# 3. Weekly check-in
/report
#   → reads current Linear cycle
#   → writes reports/YYYY-MM-DD-status.html (via scribe)
#   → prints Slack-paste-ready summary
```

## Architecture

```
capsule-factory/
├── .claude-plugin/marketplace.json    # Spec-compliant catalog (name + owner + plugins[])
├── CLAUDE.md                          # Working notes for anyone editing this repo
├── plugins/
│   ├── vertical-plugins/              # Shared skills + slash commands
│   │   ├── infra/                     # /capsule-setup, /materialize-env, manage-secrets
│   │   ├── pm-core/                   # /plan-epic, /report, /orchestrate + 3 skills
│   │   ├── code-quality/              # /pr, /review-pr, /simplify + 6 skills
│   │   ├── security/                  # /security-scan, /threat-model + 4 skills
│   │   ├── evidence-capture/          # /demo, /verify, /qa-test + 10 skills + Remotion
│   │   ├── research/                  # autoresearch skill
│   │   ├── documentation/             # /humanize, wiki, human-writing, visual-design
│   │   └── debugging/                 # 4 debugging skills
│   └── agent-plugins/                 # Agents + agent-specific sub-skills
│       ├── epic-conductor/            # @epic-conductor + scribe (shared HTML primitive)
│       ├── implementer/               # @implementer + pr-lifecycle
│       ├── analyst/                   # @analyst + security-deep-dive
│       ├── qa-capture/                # @qa-capture + evidence-pipeline
│       └── debug-guru/                # @debug-guru + debug-pipeline
└── README.md
```

## Reports

All reporting agents emit HTML via the shared `scribe` skill (lives in `epic-conductor`). Reports land in `reports/` at the consuming repo's root, dated, type-suffixed:

- `reports/YYYY-MM-DD-status.html` — pm-reporting / `/report`
- `reports/YYYY-MM-DD-pr<n>-scan.html` — analyst security scan
- `reports/YYYY-MM-DD-<system>-threat-model.html` — analyst threat model
- `reports/YYYY-MM-DD-pr<n>-verify.html` — qa-capture verify report
- `reports/YYYY-MM-DD-epic-<id>.html` — epic-conductor's living overview
- `reports/YYYY-MM-DD-debug-<topic>.html` — debug-guru root-cause writeup

Scribe defines the schema for each kind and emits self-contained HTML (inline CSS, no JS, no external assets).

## Commands by agent type

Slash commands invoked directly:

| Command           | Plugin            | What it does                                          |
|-------------------|-------------------|--------------------------------------------------------|
| `/capsule-setup`  | infra             | Configure required MCPs                                |
| `/materialize-env`| infra             | Pull env files from Bitwarden                          |
| `/plan-epic`      | pm-core           | Draft + create a Linear epic                           |
| `/report`         | pm-core           | Internal status report (current Linear cycle)          |
| `/orchestrate`    | pm-core           | Spawn the team via TeamCreate                          |
| `/pr`             | code-quality      | Create a PR for the current branch                     |
| `/review-pr`      | code-quality      | Review a PR by number/URL                              |
| `/simplify`       | code-quality      | Review changed code, fix issues                        |
| `/security-scan`  | security          | Scan current diff / commit                             |
| `/threat-model`   | security          | Generate a threat model                                |
| `/humanize`       | documentation     | Rewrite AI-flavored prose                              |
| `/demo`           | evidence-capture  | Plan + record a demo video                             |
| `/verify`         | evidence-capture  | Verify a PR against its claims                         |
| `/qa-test`        | evidence-capture  | Run QA flows + capture evidence                        |

## Agents are invoked via `@`:

- `@epic-conductor` — usually spawned by `/orchestrate`, not invoked directly
- `@implementer` — for ticket-to-PR work
- `@analyst` — for security or architecture review
- `@qa-capture` — for verification / demos
- `@debug-guru` — for hard, multi-layer bugs

## License

MIT
