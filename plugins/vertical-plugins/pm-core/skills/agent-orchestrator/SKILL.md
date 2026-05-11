---
name: agent-orchestrator
version: 1.0.0
description: |
  Route work to coding agents, track their completion, and coordinate handoffs between PM team members.
  Use when the user wants to "assign work," "delegate a task," or "coordinate agents."
---

# Agent Orchestrator

Route work to the right agent and track it to completion.

## Routing Table

| Work Type | Target Agent | Skills Needed |
|-----------|-------------|---------------|
| Epic planning | epic-conductor | linear-epic-planning, pm-reporting |
| PR creation/review | implementer | create-pr, follow-up-on-pr, simplify |
| TypeScript enforcement | implementer | ban-type-assertions, no-use-effect, fix-knip-unused-exports |
| Security scan | analyst | security-review, commit-security-scan |
| Threat modeling | analyst | threat-model-generation |
| Research/experiments | analyst | autoresearch |
| Progress reports | reporter | pm-reporting, wiki |
| Documentation | reporter | wiki, human-writing |
| Presentations | reporter | visual-design |
| Demo videos | qa-capture | capture, compose, showcase |
| QA testing | qa-capture | capture, verify |
| Proof verification | qa-capture | verify |
| Browser debugging | debug-guru | browser-navigation, agent-browser |
| Frontend review | debug-guru | frontend-design |
| API debugging | debug-guru | http-toolkit-intercept |

## Workflow

### 1. Classify Incoming Work

Determine:
- **What**: Description of the task
- **Who**: Which agent has the right skills
- **When**: Deadline or priority
- **How**: Acceptance criteria

### 2. Prepare Handoff Document

```
## Task: [Clear title]

**Agent**: [target agent name]
**Deadline**: [date or "none"]
**Priority**: urgent | high | normal | low

### Context
[Background the agent needs]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Links
- Linear issue: [URL]
- GitHub PR: [URL]
- Related docs: [URL]

### Notes
[Any special instructions]
```

### 3. Dispatch

Load the target agent's skills and invoke the appropriate workflow.

### 4. Track Progress

Monitor for:
- Acknowledgment
- Progress updates
- Blockers
- Completion

### 5. Verify Completion

Check deliverable against acceptance criteria.
Update Linear issue status.

## Handoff Patterns

**Synchronous**: Agent completes work in same session, immediate verification.
**Asynchronous**: Agent works in background, check back later. Use Linear comments for updates.
**Chained**: One agent's output is another's input. E.g., analyst finds security issue → implementer fixes it → qa-capture verifies the fix.

## Anti-patterns

- **Vague handoffs**: "Fix the bug" — which bug? What's the expected behavior?
- **Missing criteria**: Agent doesn't know when it's "done"
- **No deadline**: Work sits indefinitely
- **Wrong agent**: Sending a frontend task to the security analyst
