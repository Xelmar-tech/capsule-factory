---
description: Route work to coding agents and coordinate handoffs between PM team members
argument-hint: '"<work description>" [--agent <agent-name>]'
---

# Orchestrate Command

Route work to the appropriate PM team agent and track completion.

## Workflow

### Step 1: Classify Work

Determine the work type:
- **Code implementation** → implementer
- **Security review** → analyst
- **Documentation** → reporter
- **Demo/QA** → qa-capture
- **Debug/investigation** → debug-guru
- **Epic planning** → epic-conductor (self)

### Step 2: Prepare Handoff

For the target agent:
- Clear description of WHAT needs to be done
- Acceptance criteria
- Relevant links (Linear issue, GitHub PR, etc.)
- Deadline if applicable

### Step 3: Track Progress

Monitor:
- Agent acknowledgment
- Progress updates
- Blockers
- Completion evidence

### Step 4: Verify Completion

Check deliverable against acceptance criteria.
Update Linear issue status.
Report to epic-conductor if part of larger epic.
