# Capsule Factory

Capxul's dual Claude Code + Codex plugin marketplace. A cohesive set of plugins for managing Capxul's AI agent workforce: 8 vertical plugins that ship shared skills, Claude slash commands, Codex skills/default prompts, and 5 agent plugins with specialized Claude agents plus Codex custom-agent templates.

## What's inside

**8 vertical plugins** (shared skills + Claude slash commands + Codex skill UX):

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

### Claude Code

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

### Codex

Install the Codex marketplace from `.agents/plugins/marketplace.json`, then install plugins from the same plugin directories. Start with:

- `infra` for `$capsule-onboarding`, `$capsule-setup`, and `$manage-secrets`
- `pm-core` for `$plan-epic`, `$report`, and `$agent-orchestrator`
- one or more agent plugins for Codex custom-agent templates

If you are not sure what to install next, run `$capsule-onboarding` after installing `infra`.

After installing the plugins, run `$capsule-setup` in the consuming repo. The setup skill writes or updates:

```text
.codex/agents/epic-conductor.toml
.codex/agents/implementer.toml
.codex/agents/analyst.toml
.codex/agents/qa-capture.toml
.codex/agents/debug-guru.toml
```

Codex limitation to remember: marketplace plugins can ship skills and tools, but runnable custom subagents are discovered from `.codex/agents/` or `~/.codex/agents/`. Capsule Factory therefore ships agent templates under each agent plugin and uses `$capsule-setup` to install them into the consuming repo.

In an installed Codex cache, those templates live under:

```text
~/.codex/plugins/cache/capsule-factory/<agent-plugin>/<version>/codex-agents/<agent>.toml
```

## Configuration

### Required MCPs

Configured by `/capsule-setup` in Claude or `$capsule-setup` in Codex:

| Integration | Purpose                                     | Required material             |
|-------------|---------------------------------------------|-------------------------------|
| Linear      | Read/write Linear issues + epics            | Connector/MCP/API token       |
| GitHub      | PR/issue operations                         | Connector/CLI/API token       |
| Bitwarden or Vaultwarden | Decrypt vault items for env materialization | Existing local capability |

### Per-repo config: `.capsule-factory.yml`

Drop this at the root of any repo where you'll run `/plan-epic`, `$plan-epic`, or spawn the team:

```yaml
linear:
  team: CAP              # Linear team key or ID
  project: <id-optional> # Linear project ID (optional; epic lives at team root if absent)
github:
  default_base_branch: main
  draft_by_default: false
```

`/plan-epic` and `$plan-epic` read this to know where to create the epic. If the file is missing, the skill prompts and offers to write it.

## Typical workflow

### Claude

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

### Codex

```text
# 1. New initiative
$plan-epic "build a KYC pack uploader for B.V. companies"

# 2. Ask for install/order guidance if needed
$capsule-onboarding

# 3. Install agent templates in this repo, if not already present
$capsule-setup

# 4. Kick off orchestration
$agent-orchestrator CAP-123
#   -> preflights environment and integrations
#   -> starts epic-conductor as a Codex custom subagent
#   -> conductor selects implementer, analyst, qa-capture, or debug-guru roles

# 5. Weekly check-in
$pm-reporting
```

## Architecture

```
capsule-factory/
├── .claude-plugin/marketplace.json    # Claude catalog
├── .agents/
│   ├── plugins/marketplace.json       # Codex marketplace catalog
│   └── codex-migration-map.json       # Drift-control map between Claude and Codex surfaces
├── CLAUDE.md                          # Claude-oriented working notes
├── AGENTS.md                          # Dual-target maintainer notes
├── scripts/
│   └── validate-codex-migration.py    # Static drift validator
├── plugins/
│   ├── vertical-plugins/              # Shared skills + slash commands
│   │   ├── infra/                     # /capsule-setup, $capsule-setup, manage-secrets
│   │   ├── pm-core/                   # /plan-epic, /report, /orchestrate + 3 skills
│   │   ├── code-quality/              # /pr, /review-pr, /simplify + 6 skills
│   │   ├── security/                  # /security-scan, /threat-model + 4 skills
│   │   ├── evidence-capture/          # /demo, /verify, /qa-test + 10 skills + Remotion
│   │   ├── research/                  # autoresearch skill
│   │   ├── documentation/             # /humanize, wiki, human-writing, visual-design
│   │   └── debugging/                 # 4 debugging skills
│   └── agent-plugins/                 # Claude agents + Codex TOML templates + skills
│       ├── epic-conductor/            # @epic-conductor, codex-agents template, scribe
│       ├── implementer/               # @implementer, codex-agents template, pr-lifecycle
│       ├── analyst/                   # @analyst, codex-agents template, security-deep-dive
│       ├── qa-capture/                # @qa-capture, codex-agents template, evidence-pipeline
│       └── debug-guru/                # @debug-guru, codex-agents template, debug-pipeline
└── README.md
```

Each plugin directory has both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Keep those siblings aligned when adding or changing plugins.

## Reports

All reporting agents emit HTML via the shared `scribe` skill (lives in `epic-conductor`). Reports land in `reports/` at the consuming repo's root, dated, type-suffixed:

- `reports/YYYY-MM-DD-status.html` — pm-reporting / `/report`
- `reports/YYYY-MM-DD-pr<n>-scan.html` — analyst security scan
- `reports/YYYY-MM-DD-<system>-threat-model.html` — analyst threat model
- `reports/YYYY-MM-DD-pr<n>-verify.html` — qa-capture verify report
- `reports/YYYY-MM-DD-epic-<id>.html` — epic-conductor's living overview
- `reports/YYYY-MM-DD-debug-<topic>.html` — debug-guru root-cause writeup

Scribe defines the schema for each kind and emits self-contained HTML (inline CSS, no JS, no external assets).

## Commands and skills

Claude slash commands remain Claude-only. Codex uses skills/default prompts instead.

| Claude command    | Codex counterpart        | Plugin            | What it does                                  |
|-------------------|--------------------------|-------------------|-----------------------------------------------|
| `/capsule-setup`  | `$capsule-setup`         | infra             | Configure integrations and install agents     |
| Claude-only setup docs | `$capsule-onboarding` | infra             | Explain install order, agent model, and updates |
| `/materialize-env`| `$manage-secrets`        | infra             | Pull env files from vault tooling             |
| `/plan-epic`      | `$linear-epic-planning`  | pm-core           | Draft + create a Linear epic                  |
| `/report`         | `$pm-reporting`          | pm-core           | Internal status report                        |
| `/orchestrate`    | `$agent-orchestrator`    | pm-core           | Coordinate conductor + teammates              |
| `/pr`             | `$create-pr`             | code-quality      | Create a PR for the current branch            |
| `/review-pr`      | `$follow-up-on-pr`       | code-quality      | Review or address PR feedback                 |
| `/simplify`       | `$simplify`              | code-quality      | Review changed code, fix issues               |
| `/security-scan`  | `$commit-security-scan`  | security          | Scan current diff / commit                    |
| `/threat-model`   | `$threat-model-generation` | security        | Generate a threat model                       |
| `/humanize`       | `$human-writing`         | documentation     | Rewrite AI-flavored prose                     |
| `/demo`           | `$agent-control`         | evidence-capture  | Plan + record a demo video                    |
| `/verify`         | `$verify`                | evidence-capture  | Verify a PR against its claims                |
| `/qa-test`        | `$agent-control`         | evidence-capture  | Run QA flows + capture evidence               |

## Agents

Claude agents are invoked via `@`. Codex agents are installed as `.codex/agents/*.toml` and spawned as custom subagents.

| Role | Claude source | Codex template |
|------|---------------|----------------|
| epic-conductor | `plugins/agent-plugins/epic-conductor/agents/epic-conductor.md` | `plugins/agent-plugins/epic-conductor/codex-agents/epic-conductor.toml` |
| implementer | `plugins/agent-plugins/implementer/agents/implementer.md` | `plugins/agent-plugins/implementer/codex-agents/implementer.toml` |
| analyst | `plugins/agent-plugins/analyst/agents/analyst.md` | `plugins/agent-plugins/analyst/codex-agents/analyst.toml` |
| qa-capture | `plugins/agent-plugins/qa-capture/agents/qa-capture.md` | `plugins/agent-plugins/qa-capture/codex-agents/qa-capture.toml` |
| debug-guru | `plugins/agent-plugins/debug-guru/agents/debug-guru.md` | `plugins/agent-plugins/debug-guru/codex-agents/debug-guru.toml` |

## Maintenance

Run the drift validator after changing plugin, command, skill, or agent surfaces:

```bash
python3 scripts/validate-codex-migration.py
```

The validator checks manifest parity, marketplace parity, Codex agent templates, skill frontmatter, migration-map references, and obvious Claude-only terms in Codex-facing files.

## Updating Codex Installs

When this repo publishes a new plugin version, maintainers bump the changed plugin's version in both the Claude and Codex manifests. Codex installs are cached by marketplace, plugin, and version, for example:

```text
~/.codex/plugins/cache/capsule-factory/infra/1.0.1/
```

For a Git-backed marketplace, users update the marketplace with:

```bash
codex plugin marketplace upgrade capsule-factory
```

For a local checkout marketplace, pull the checkout and refresh/reinstall from the Codex app. If the local cache does not refresh, remove and re-add the marketplace:

```bash
codex plugin marketplace remove capsule-factory
codex plugin marketplace add /path/to/capsule-factory
```

After updating agent plugins, rerun `$capsule-setup` in each target repo. It will skip differing `.codex/agents/*.toml` files unless replacement is explicitly approved.

## License

MIT
